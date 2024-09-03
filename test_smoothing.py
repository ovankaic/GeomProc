# Smooth a mesh with an averaging algorithm

# Import geometry processing library
import geomproc

# Import numpy for data arrays
import numpy as np

# Load the mesh
tm = geomproc.load('meshes/bunny.obj')

# Compute connectivity information
tm.compute_connectivity()

# Perform smoothing
num_iterations = 5;
# Temporary holder for smoothed vertex positions
smooth = np.zeros(tm.vertex.shape)
# Smoothing iterations
for it in range(num_iterations):
    # Smooth each vertex
    for vi in range(tm.vertex.shape[0]):
        # Save averaged position
        smooth[vi, :] = np.average(tm.vertex[tm.viv[vi], :], axis=0)
    # Update all vertex position with averaged positions
    tm.vertex = smooth.copy()

# Save the mesh
wo = geomproc.write_options()
tm.save('output/bunny_smooth.obj', wo)
