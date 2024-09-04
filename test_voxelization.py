# Voxelize a given mesh

# Import the geometry processing library
import geomproc

# Use numpy
import numpy as np

# Main function
if __name__ == '__main__':
    filename = 'sphere'
    #filename = 'bunny'

    # Load and normalize the mesh
    tm = geomproc.load('meshes/' + filename + '.obj')
    tm.normalize()

    # Compute normal vectors
    tm.compute_vertex_and_face_normals()

    # Voxelize the mesh
    n = 32 # Number of voxels per dimensions
    vol = geomproc.volume()
    vol.voxelize_mesh(tm, np.array([-1.2, -1.2, -1.2]), np.array([1.2, 1.2, 1.2]), n)

    # Fill the interior of the mesh
    vol.fill_interior()

    # Save normalized mesh
    tm = vol.create_mesh()
    tm.save('output/' + filename + '_volume.obj')
    tm.save('output/' + filename + '_normalized.obj')
