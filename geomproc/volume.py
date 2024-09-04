#
# GeomProc: geometry processing library in python + numpy
#
# Copyright (c) 2008-2024 Oliver van Kaick <ovankaic@gmail.com>
# under the MIT License.
#
# See file LICENSE.txt for details on the copyright license.
#
"""This module contains the volume class of the GeomProc geometry processing
library used for voxelizing a mesh.
"""


import numpy as np

from .mesh import *
from .creation import create_simple_cube


# Class that stores a volume (set of voxels)
class volume:
    """A class that represents a volume (set of voxels)

    Attributes
    ----------
    cell : numpy.array_like
        Voxels or cells of the volume stored in a 3D array. In the array, cell[i, j, k] is 1.0 if the voxel is occupied (intersects a shape), while it is 0.0 if the cell is empty.
    start : numpy.array_like
        Coordinate of the voxel on the top-left corner of the volume
    end : numpy.array_like
        Coordinate of the voxel on the bottom-right corner of the volume
    num_cubes_per_dim : int
        Number of voxels per each dimension x, y, and z
    cube_size : float
        Size of each cube (width, height, or depth)

    Notes
    -----
    The class stores a volume as a set of cells. The coordinates of a cell (i,
    j, k) in the original shape space can be obtained with x = start[0] +
    i*cube_size[0], y = start[1] + j*cube_size[1], and z = start[2] +
    k*cube_size[2].
    """

    # Initialize an empty volume by default
    def __init__(self):
        self.cell = np.zeros((0, 0))
        self.start = np.array([0, 0, 0])
        self.end = np.array([0, 0, 0])
        self.num_cubes_per_dim = 0
        self.cube_size = 0.0

    # Check if a given axis is a separating axis
    @staticmethod
    def separating(ax, tv, pt):
        # Project all points
        proj1 = np.zeros(3)
        for i in range(3):
            proj1[i] = np.dot(ax, tv[i, :])
        proj2 = np.zeros(8)
        for i in range(8):
            proj2[i] = np.dot(ax, pt[i, :])
        # check projections
        min1 = np.min(proj1)
        max1 = np.max(proj1)
        min2 = np.min(proj2)
        max2 = np.max(proj2)
        if (max1 < min2) or (max2 < min1):
            return True
        return False

    # Check if a triangle intersects a box
    @staticmethod
    def intersects(tv, vn, pt):
        # Part 1:
        # Collect all the axes that have to be tested for separation
        # (candidate axes)
        # Technically speaking, the axes are the normal vectors of the
        # separating planes
        #
        # Start with the axes of axis-aligned cubes by default
        cand_axes = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        # Edges of axis aligned cube
        cube_edges = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        # Append normal of triangle to the candidate axes
        cand_axes.append(vn)
        # Append normals of planes that contain one edge of the cube and
        # one edge of the triangle
        for i in range(3):
            tri_edge = tv[(i+1)%3, :] - tv[i, :]
            for j in range(3):
                cand_axes.append(np.cross(tri_edge, cube_edges[j]))
        # Convert candidate axes into numpy array
        cand_axes = np.array(cand_axes)

        # Part 2:
        # Test if each candidate axis is a separating axis
        for i in range(cand_axes.shape[0]):
            if volume.separating(cand_axes[i, :], tv, pt):
                return False
        # Return true by default
        return True

    # Voxelize a mesh
    #
    # The method uses an efficient intersection test between a triangle and a
    # cube based on the separating axis theorem, so that no subdivision of the
    # triangle is needed
    def voxelize_mesh(self, tm, start, end, num_cubes_per_dim, rough=False):
        """Voxelize a given mesh

        Parameters
        ----------
        tm : mesh
            Mesh to be voxelized
        start : array_like
            Vector of size 3 with the starting coordinates (x, y, z) of the
            volume in the space of the mesh
        end : array_like
            Vector of size 3 with the ending coordinates (x, y, z) of the
            volume in the space of the mesh
        num_cubes_per_dim : int
            Desired number of cubes per dimension

        Returns
        -------
        None

        Notes
        -----
        The method sets up the current volume based on the given mesh. The
        method requires the normals of mesh faces. Empty voxels are set to 0.0,
        while voxels that contain the mesh are set to 1.0. The resulting volume
        only captures the surface (outer shell) of the mesh. To obtain a volume
        where the interior of the mesh is also filled with voxels of value 1.0,
        use the method fill_volume(). 

        See Also
        --------
        geomproc.volume.fill_interior
        """

        # Determine dimensions of each cube based on input parameters
        cube_size = (end - start) / num_cubes_per_dim

        # Save the input parameters
        self.start = start
        self.end = end
        self.num_cubes_per_dim = num_cubes_per_dim
        self.cube_size = cube_size

        # Initialize volume
        self.cell = np.zeros((num_cubes_per_dim, num_cubes_per_dim, num_cubes_per_dim))

        # Initialize cube point coordinates to be filled in later
        cube_point = np.zeros((8, 3))

        # Initialize shifts to determine 8 cube points of each cell
        shifts = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], \
                  [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]

        # Go through each triangle in the mesh
        for f in range(tm.face.shape[0]):
            # Get the cubes that are covered by the bounding box of this
            # triangle

            # Get triangle vertices
            # Each row of tri_ver is a vertex, columns are x, y, z
            tri_ver = tm.vertex[tm.face[f, :], :]

            # Get bounding box of triangle
            # Each vector has three entries, with the minimum and maximum for x, y, z
            tri_min = np.min(tri_ver, axis=0)
            tri_max = np.max(tri_ver, axis=0)

            # Get indices of cubes covered by the bounding box
            # Translate coordinate to start of volume
            mn = tri_min - start 
            mx = tri_max - start
            # Get corresponding index
            start_id = np.floor_divide(mn, cube_size)
            end_id = np.floor_divide(mx, cube_size)

            # Perform accurate intersection test for each cube covered
            # by the triangle's bounding box
            for i in range(int(start_id[2]), \
                           min(int(end_id[2])+1, num_cubes_per_dim-1)):
                for j in range(int(start_id[1]), \
                               min(int(end_id[1])+1, num_cubes_per_dim-1)):
                    for k in range(int(start_id[0]), \
                                   min(int(end_id[0])+1, num_cubes_per_dim-1)):
                        # Get position of current cube
                        x = start[0] + cube_size[0]*float(k)
                        y = start[1] + cube_size[1]*float(j)
                        z = start[2] + cube_size[2]*float(i)

                        # Get cube corners
                        for p, shift in enumerate(shifts):
                            # Determine corner coordinates
                            cube_point[p, :] = np.array([\
                                x + shift[0]*cube_size[0], \
                                y + shift[1]*cube_size[1], \
                                z + shift[2]*cube_size[2]])

                        # Check for intersection
                        if rough:
                            self.cell[i, j, k] = 1.0
                        else:
                            if self.intersects(tri_ver, tm.fnormal[f, :], cube_point):
                                self.cell[i, j, k] = 1.0

    # Flood-fill a volume with a given value
    def flood_fill(self, seed, value, boundary, nt=0):
        # Neighbors to consider
        neighbors = []
        if nt == 0:
            neighbors = [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, -1], [0, 0, 1]]
        else:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    for k in range(-1, 2):
                        if (i != 0) or (j != 0) or (k != 0):
                            neighbors.append([i, j, k])
        # Fill seed cell
        self.cell[seed[0], seed[1], seed[2]] = value
        # Perform flood-fill based on a stack
        stack = [seed]
        while len(stack) > 0:
            # Get element on top of the stack
            c = stack.pop()
            # Add neighbors, if needed
            for neigh in neighbors:
                # Define neighbor
                idx = neigh.copy()
                idx[0] = neigh[0] + c[0]
                idx[1] = neigh[1] + c[1]
                idx[2] = neigh[2] + c[2]
                # Check if neighbor is in volume bounds
                if (idx[0] >= 0) and (idx[0] < self.cell.shape[0]) and \
                   (idx[1] >= 0) and (idx[1] < self.cell.shape[1]) and \
                   (idx[2] >= 0) and (idx[2] < self.cell.shape[2]):
                   # Check if neighbor has not been assigned already
                    if (self.cell[idx[0], idx[1], idx[2]] != boundary) and\
                       (self.cell[idx[0], idx[1], idx[2]] != value):
                        # Assign neighbor
                        self.cell[idx[0], idx[1], idx[2]] = value
                        # Add neighbor to the stack
                        stack.append(idx)

    # Fill interior of the mesh
    # This function assumes that the mesh is closed (no holes)
    def fill_interior(self):
        """Fill the interior of a voxelized shape

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        The method assumes that a volume is given where the voxels that
        intersect a surface have a value of 1.0 and empty voxels have a value
        of 0.0. The method fills the voxels that are inside the surface. Note
        that the method only works properly if the shape is closed with no
        holes.
        """

        # Fill exterior with the value 2.0
        # Stop when finding a value of 1.0
        self.flood_fill([0, 0, 0], 2.0, 1.0)
        
        # Now the exterior has value 2.0
        # Intersecting voxels have value 1.0
        # Interior voxels have value 0.

        # Change voxels with value 0.0 to 1.0 (fill the interior)
        self.cell[self.cell == 0.0] = 1.0
        
        # Change exterior that is 2.0 back to 0.0
        self.cell[self.cell == 2.0] = 0.0

    # Save the volume as a triangle mesh for visualization purposes
    # The resulting mesh is not manifold
    def create_mesh(self):
        """Transform the volume into a mesh for visualization purposes

        Parameters
        ----------
        None

        Returns
        -------
        tm : mesh
            The resulting triangle mesh.

        Notes
        -----
        The method transforms the current volume into a triangle mesh. Note
        that the resulting mesh is not manifold, as each voxel is simply a
        stand-alone cube. Thus, the resulting mesh is for visualization
        purposes only.
        """

        # Create output mesh
        tm = mesh()
        # Create a proxy cube
        cb = create_simple_cube()
        cb.vertex *= self.cube_size
        cb_copy = cb.copy()
        # Add a proxy cube for each filled cell
        z = self.start[2]
        for i in range(self.cell.shape[0]):
            y = self.start[1]
            for j in range(self.cell.shape[1]):
                x = self.start[0]
                for k in range(self.cell.shape[2]):
                    if self.cell[i, j, k] == True:
                        cb_copy.vertex = cb.vertex.copy()
                        cb_copy.vertex += np.array([x, y, z]) 
                        tm.append(cb_copy)
                    x += self.cube_size[0]
                y += self.cube_size[1]
            z += self.cube_size[2]
        # Return the mesh
        return tm
