#
# GeomProc: geometry processing library in python + numpy
#
# Copyright (c) 2008-2024 Oliver van Kaick <ovankaic@gmail.com>
# under the MIT License.
#
# See file LICENSE.txt for details on copyright licenses.
#
"""This module contains functions for loading geometric datasets of the
GeomProc geometry processing library.
"""


import numpy as np
import copy
import math
import random

from .mesh import *
from .pcloud import *
from .read_options import *


#### Functions for loading geometric datasets

# Create a model by loading its data from a file
def load(filename, ro = read_options()):
    """Load a geometric dataset from a file

    Parameters
    ----------
    filename : string
        Name of the input filename
    ro : read_options object, optional
        Object with flags that indicate how to handle the input file

    Returns
    -------
    dataset : object
        Loaded dataset, either a mesh or point cloud

    Notes
    -----
    The method reads all the information from the file and
    determines the type of dataset to be created, either a mesh with
    vertices and faces or a point cloud with only points.

    This is a list of features supported by the different formats and
    the implementation:

    - obj: supports triangles or quads and split_polygons, normals,
      texture coordinates, vertex colors, texture_name
    - off: supports triangles or quads and split_polygons, no other
      attributes
    - ply: supports triangles or quads and split_polygons, vertex/point
      normals, vertex/point colors, face colors

    See Also
    --------
    geomproc.mesh
    geomproc.pcloud
    geomproc.read_options

    Examples
    --------
    >>> import geomproc
    >>> tm = geomproc.load('sphere.obj')
    """

    # Check the file extension and call the relevant method to load
    # the file
    part = filename.split('.')
    if part[-1].lower() == 'obj':
        return load_obj(filename, ro)
    elif part[-1].lower() == 'off':
        return load_off(filename, ro)
    elif part[-1].lower() == 'ply':
        return load_ply(filename, ro)
    else:
        raise RuntimeError('file format "'+part[-1]+'" not supported')


# Load a mesh or point cloud from a file in obj format
def load_obj(filename, ro = read_options()):

    # Parse a vertex description of the form <vid>/<tid>/<nid>
    def get_parts(st):
        # Split vertex description into parts
        arr = st.split('/')
        # Initialize all parts with default values
        vid = None
        tid = None
        nid = None
        # Parse vertex description based on number of parts
        if len(arr) == 3:
            vid = arr[0]
            tid = arr[1]
            nid = arr[2]
        elif len(arr) == 2:
            vid = arr[0]
            tid = arr[1]
        elif len(arr) == 1:
            vid = arr[0]
        # Convert data into numbers
        vid = int(vid)-1
        if tid == '':
            tid = None
        if tid != None:
            tid = int(tid)-1
        if nid == '':
            nid = None
        if nid != None:
            nid = int(nid)-1
        return vid, tid, nid

    # Temporary lists to store the mesh data
    # Basic mesh: faces and vertices
    vertex = []
    face = []
    # Vertex colors
    vcolor = []
    # Normals and texture coordinates that can be reused
    normal = []
    uv = []
    # Corner descriptions: references to normals and texture coordinates
    cnormal = []
    cuv = []
    # Open the file
    with open(filename, 'r') as f: 
        # Process each line of the file
        for line in f:
            # Remove extra whitespace at the beginning or end of line
            line = line.strip()
            # Ignore empty lines
            if len(line) < 1:
                continue
            # Ignore comments
            if line[0] == '#':
                continue
            # Parse line
            part = line.split(' ')
            # Vertex command
            if part[0] == 'v':
                if (len(part) != 4) and (len(part) != 7):
                    raise RuntimeError('v command should have 3 or 6 numbers')
                vertex.append([float(part[1]), float(part[2]), float(part[3])])
                if len(part) == 7:
                    vcolor.append([float(part[4]), float(part[5]), float(part[6])])
            # Vertex normal command
            if part[0] == 'vn':
                if len(part) < 4:
                    raise RuntimeError('vn command has less than 3 numbers')
                normal.append([float(part[1]), float(part[2]), float(part[3])])
            # Vertex texture coordinates command
            if part[0] == 'vt':
                if len(part) < 3:
                    raise RuntimeError('vn command has less than 2 numbers')
                uv.append([float(part[1]), float(part[2])])
            # Vertex color command
            if part[0] == 'vc':
                if len(part) < 3:
                    raise RuntimeError('vc command has less than 2 numbers')
                vcolor.append([float(part[1]), float(part[2]), float(part[3])])
            # Face command
            if part[0] == 'f':
                # Check consistency of command
                if (len(part) < 4) or (len(part) > 5):
                    raise RuntimeError('f command should have 3 or 4 groups of numbers. Polygons of arbitrary size not supported by loading function')
                # Check if we have a triangle
                if len(part) == 4:
                    # Get first three ids of face
                    [vid1, tid1, nid1] = get_parts(part[1])
                    [vid2, tid2, nid2] = get_parts(part[2])
                    [vid3, tid3, nid3] = get_parts(part[3])
                    # Add face
                    face.append([vid1, vid2, vid3])
                    if nid1 != None:
                        cnormal.append([nid1, nid2, nid3])
                    if tid1 != None:
                        cuv.append([tid1, tid2, tid3])
                else:
                    # We have a quad
                    # Check if we should split polygons 
                    if ro.split_polygons:
                        # Split quad into two triangles
                        # Get first three ids of face
                        [vid1, tid1, nid1] = get_parts(part[1])
                        [vid2, tid2, nid2] = get_parts(part[2])
                        [vid3, tid3, nid3] = get_parts(part[3])
                        # Add face
                        face.append([vid1, vid2, vid3])
                        if nid1 != None:
                            cnormal.append([nid1, nid2, nid3])
                        if tid1 != None:
                            cuv.append([tid1, tid2, tid3])
                        # Parse last entry
                        [vid4, tid4, nid4] = get_parts(part[4])
                        # Add second face
                        face.append([vid1, vid3, vid4])
                        if nid1 != None:
                            cnormal.append([nid1, nid3, nid4])
                        if tid1 != None:
                            cuv.append([tid1, tid3, tid4])
                    else:
                        # Add entire polygon
                        # Get all the ids of the face
                        [vid1, tid1, nid1] = get_parts(part[1])
                        [vid2, tid2, nid2] = get_parts(part[2])
                        [vid3, tid3, nid3] = get_parts(part[3])
                        [vid4, tid4, nid4] = get_parts(part[4])
                        # Add face
                        face.append([vid1, vid2, vid3, vid4])
                        if nid1 != None:
                            cnormal.append([nid1, nid2, nid3, nid4])
                        if tid1 != None:
                            cuv.append([tid1, tid2, tid3, tid4])

    # Compose output object
    if len(face) > 0:
        # Create a mesh object
        output = mesh()
        # Vertices and faces
        output.vertex = np.array(vertex)
        output.face = np.array(face, dtype=np.int_)
        output.vcolor = np.array(vcolor)
        # Corner normals
        if len(cnormal) > 0:
            temp = []
            for ne in cnormal:
                temp_normal = [[normal[ne[0]][0], normal[ne[0]][1], normal[ne[0]][2]],
                               [normal[ne[1]][0], normal[ne[1]][1], normal[ne[1]][2]],
                               [normal[ne[2]][0], normal[ne[2]][1], normal[ne[2]][2]]]
                temp.append(temp_normal)
            output.cnormal = np.array(temp)
        # Corner texture coordinates
        if len(cuv) > 0:
            temp = []
            for te in cuv:
                temp_uv = [[uv[te[0]][0], uv[te[0]][1]],
                           [uv[te[1]][0], uv[te[1]][1]],
                           [uv[te[2]][0], uv[te[2]][1]]]
                temp.append(temp_uv)
            output.cuv = np.array(temp)
    else:
        # Create a point cloud object
        output = pcloud()
        # Points and colors
        output.point = np.array(vertex)
        output.color = np.array(vcolor)
        # Other properties
        if len(normal) > 0:
            if len(normal) == len(vertex):
                output.normal = np.array(normal)

    # Return output object
    return output


# Load a mesh or point cloud from a file in off format
def load_off(filename, ro = read_options()):
    # Temporary lists to store the mesh data
    # Basic mesh: faces and vertices
    vertex = []
    face = []
    # Open the file
    with open(filename, 'r') as f: 
        # Read header
        # Read file identifier
        line = f.readline()
        line = line.strip()
        if line[0:3] != 'OFF':
            raise RuntimeError("file does not have the 'OFF' identifier")
        # Read number of vertices and faces from header
        part = line.split()
        # Check if info is on the same line as the file identifier
        if len(part) == 4:
            # Discard file information from the parsed list
            part = [part[1], part[2], part[3]]
        else:
            # If info is not on the same line, try to read it from the
            # next line
            line = f.readline()
            line = line.strip()
            part = line.split()
            if len(part) != 3:
                raise RuntimeError('missing file information in the file header')
        # Get number of vertices and faces
        num_vertices = int(part[0])
        num_faces = int(part[1])
        # Read data
        # Read vertices
        for i in range(num_vertices):
            # Read line
            line = f.readline()
            line = line.strip()
            # Parse line
            part = line.split()
            if len(part) != 3:
                raise RuntimeError('vertex entry should have exactly 3 numbers')
            # Transform entries into numbers
            v1 = float(part[0])
            v2 = float(part[1])
            v3 = float(part[2])
            # Append data
            vertex.append([v1, v2, v3])
        # Read faces
        for i in range(num_faces):
            # Read line
            line = f.readline()
            line = line.strip()
            # Parse line
            part = line.split()
            if (len(part) != 4) and (len(part) != 5):
                raise RuntimeError('face entry should have 4 or 5 numbers. Polygons of arbitrary size not supported by loading function')
            # Transform entries into numbers
            id1 = int(part[1])
            id2 = int(part[2])
            id3 = int(part[3])
            # Check if it is a quad face
            if len(part) == 5:
                # Get remaining number
                id4 = int(part[4])
                if ro.split_polygons:
                    # Add two triangles
                    face.append([id1, id2, id3])
                    face.append([id1, id3, id4])
                else:
                    # Add quad
                    face.append([id1, id2, id3, id4])
            else:
                # Append single triangle
                face.append([id1, id2, id3])

    # Compose output object
    if len(face) > 0:
        # Create mesh structure
        output = mesh()
        # Vertices and faces
        output.vertex = np.array(vertex)
        output.face = np.array(face, dtype=np.int_)
    else:
        # Create a point cloud object
        output = pcloud()
        # Points and colors
        output.point = np.array(vertex)

    # Return output object
    return output


# Load a mesh or point cloud from a file in ply format
def load_ply(filename, ro = read_options()):

    # Temporary lists to store the mesh data
    # Basic mesh: faces and vertices
    vertex = []
    face = []
    # Vertex colors
    vcolor = []
    # Face colors
    fcolor = []
    # Normals and texture coordinates that can be reused
    normal = []
    uv = []

    # Open the file
    with open(filename, 'r') as f: 

        #### Read header
        header = []

        # Check if file starts with the string 'ply'
        line = f.readline().strip()
        if line != 'ply':
            raise RuntimeError('file does not have a valid ply magic number in the header')
        # Check if the file format and version is supported
        line = f.readline().strip()
        part = line.split()
        if part[0] != 'format':
            raise RuntimeError('file should specify ply format before any other commands')
        if part[1] != 'ascii':
            raise RuntimeError('only ply ascii format 1.0 is currently supported')
        if part[2] != '1.0':
            raise RuntimeError('only ply ascii format 1.0 is currently supported')
        # Read rest of header entries
        line = f.readline().strip()
        while line != 'end_header':
            part = line.split()
            
            if part[0] == 'element':
                # Append element name, count, and empty list of properties
                header.append([part[1], int(part[2]), []])
            elif part[0] == 'property':
                if part[1] == 'list':
                    # Append name, list, and types to the current element
                    header[-1][2].append([part[4], part[1], part[2], part[3]])
                else:
                    # Append name and type to the current element
                    header[-1][2].append([part[2], part[1]])
            elif part[0] == 'comment':
                [] # Ignore comment
            else:
                # Report error for unsupported command
                raise RuntimeError('unrecognized command"' + part[0] + '"')

            # Read next line and go back to while loop
            line = f.readline().strip()

        #### Read data
        #print(header) # For debug

        # For each element in the header
        for i in range(len(header)):
            # For each entry in the current element
            for j in range(header[i][1]):
                # Read data in the file
                line = f.readline().strip()
                part = line.split()
                index = 0
                # For each property in the current entry
                for k in range(len(header[i][2])):
                    # Parse property and copy data to corresponding array
                    if header[i][0] == 'vertex':
                        if header[i][2][k][0] == 'x':
                            if j == len(vertex):
                                vertex.append([0.0, 0.0, 0.0])
                            vertex[-1][0] = float(part[index])
                        if header[i][2][k][0] == 'y':
                            if j == len(vertex):
                                vertex.append([0.0, 0.0, 0.0])
                            vertex[-1][1] = float(part[index])
                        if header[i][2][k][0] == 'z':
                            if j == len(vertex):
                                vertex.append([0.0, 0.0, 0.0])
                            vertex[-1][2] = float(part[index])
                        if header[i][2][k][0] == 'nx':
                            if j == len(normal):
                                normal.append([0.0, 0.0, 0.0])
                            normal[-1][0] = float(part[index])
                        if header[i][2][k][0] == 'ny':
                            if j == len(normal):
                                normal.append([0.0, 0.0, 0.0])
                            normal[-1][1] = float(part[index])
                        if header[i][2][k][0] == 'nz':
                            if j == len(normal):
                                normal.append([0.0, 0.0, 0.0])
                            normal[-1][2] = float(part[index])
                        if header[i][2][k][0] == 'red':
                            if j == len(vcolor):
                                vcolor.append([0.0, 0.0, 0.0])
                            if header[i][2][k][1] == 'uchar':
                                vcolor[-1][0] = float(part[index])/255.0
                            elif header[i][2][k][1] == 'float':
                                vcolor[-1][0] = float(part[index])
                        if header[i][2][k][0] == 'green':
                            if j == len(vcolor):
                                vcolor.append([0.0, 0.0, 0.0])
                            if header[i][2][k][1] == 'uchar':
                                vcolor[-1][1] = float(part[index])/255.0
                            elif header[i][2][k][1] == 'float':
                                vcolor[-1][1] = float(part[index])
                        if header[i][2][k][0] == 'blue':
                            if j == len(vcolor):
                                vcolor.append([0.0, 0.0, 0.0])
                            if header[i][2][k][1] == 'uchar':
                                vcolor[-1][2] = float(part[index])/255.0
                            elif header[i][2][k][1] == 'float':
                                vcolor[-1][2] = float(part[index])

                    if header[i][0] == 'face':
                        if (header[i][2][k][0] == 'vertex_index') or \
                           (header[i][2][k][0] == 'vertex_indices'):
                            count = int(part[index])
                            index += 1
                            if count == 3:
                                temp = [0, 0, 0]
                            elif count == 4:
                                temp = [0, 0, 0, 0]
                            else:
                                raise RuntimeError('face entry should have 3 or 4 vertex references. Polygons of arbitrary size not supported by loading function')
                            for vi in range(count):
                                temp[vi] = int(part[index])
                                index += 1
                            index -= 1
                            if count == 3:
                                face.append(temp)
                            else: # if count == 4:
                                if ro.split_polygons:
                                    face.append([temp[0], temp[1], temp[2]])
                                    face.append([temp[0], temp[2], temp[3]])
                                else:
                                    face.append(temp)
                        if header[i][2][k][0] == 'red':
                            if j == len(fcolor):
                                fcolor.append([0.0, 0.0, 0.0])
                            if header[i][2][k][1] == 'uchar':
                                fcolor[-1][0] = float(part[index])/255.0
                            elif header[i][2][k][1] == 'float':
                                fcolor[-1][0] = float(part[index])
                        if header[i][2][k][0] == 'green':
                            if j == len(fcolor):
                                fcolor.append([0.0, 0.0, 0.0])
                            if header[i][2][k][1] == 'uchar':
                                fcolor[-1][1] = float(part[index])/255.0
                            elif header[i][2][k][1] == 'float':
                                fcolor[-1][1] = float(part[index])
                        if header[i][2][k][0] == 'blue':
                            if j == len(fcolor):
                                fcolor.append([0.0, 0.0, 0.0])
                            if header[i][2][k][1] == 'uchar':
                                fcolor[-1][2] = float(part[index])/255.0
                            elif header[i][2][k][1] == 'float':
                                fcolor[-1][2] = float(part[index])

                    index += 1

    # Compose output object
    if len(face) > 0:
        # Create a mesh object
        output = mesh()
        # Vertices and faces
        output.vertex = np.array(vertex)
        output.face = np.array(face, dtype=np.int_)
        output.vcolor = np.array(vcolor)
        output.fcolor = np.array(fcolor)
    elif len(vertex) > 0:
        # Create a point cloud object
        output = pcloud()
        # Points and colors
        output.point = np.array(vertex)
        output.color = np.array(vcolor)
        # Other properties
        if len(normal) > 0:
            if len(normal) == len(vertex):
                output.normal = np.array(normal)
    else:
        raise RuntimeError('no data read from the file')

    # Return output object
    return output
