#
# GeomProc: geometry processing library in python + numpy
#
# Copyright (c) 2008-2024 Oliver van Kaick <ovankaic@gmail.com>
# under the MIT License.
#
# See file LICENSE.txt for details on copyright licenses.
#
"""This module contains the write_options class of the GeomProc geometry
processing library.
"""


# Options for saving files
class write_options:
    """A class that holds options of what information to write when saving a file

    Attributes
    ----------
    write_vertex_normals : boolean
        Save normal vectors stored at mesh vertices

    write_vertex_colors : boolean
        Save colors stored at mesh vertices

    write_vertex_uvs : boolean
        Save (u, v) texture coordinates stored at mesh vertices

    write_face_normals : boolean
        Save normal vectors stored at mesh faces

    write_face_colors : boolean
        Save colors stored at mesh faces

    write_corner_normals : boolean
        Save normal vectors stored at face corners

    write_corner_uvs : boolean
        Save (u, v) texture coordinates stored at face corners

    texture_name : string
        Filename of image referenced by texture coordinates

    write_point_normals : boolean
        Save normal vectors stored at points in point cloud

    write_point_colors : boolean
        Save colors stored at points in point cloud

    Notes
    -----
    Not all options are accepted by every file format. The class
    collects all the possible options supported by different file
    formats. The structure is relevant to both meshes and point clouds.

    This is a list of features supported by the different formats and
    the implementation:

    - Meshes:
        - obj: supports triangles or quads, write_vertex_colors,
          write_vertex_uvs or write_corner_uvs, write_vertex_normals or
          write_face_normals or write_corner_normals, texture_name
        - off: supports triangles or quads, no other attributes
        - ply: supports triangles or quads, write_vertex_normals,
          write_vertex_colors, write_face_colors
    - Point clouds:
        - obj: write_point_normals, write_point_colors
        - ply: write_point_normals, write_point_colors
    """

    def __init__(self):
        # Not all options are accepted by every file format
        self.write_vertex_normals = False
        self.write_vertex_colors = False
        self.write_vertex_uvs = False
        self.write_face_normals = False
        self.write_face_colors = False
        self.write_corner_normals = False
        self.write_corner_uvs = False
        self.texture_name = ''
        self.write_point_normals = False
        self.write_point_colors = False
