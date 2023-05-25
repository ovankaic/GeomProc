# Smooth a mesh with the Laplacian operator

# Import geometry processing library
import geomproc

# Import numpy for data arrays
import numpy as np

# Load the mesh
tm = geomproc.load('meshes/bunny.obj')
tm.normalize()

# Compute connectivity information
tm.compute_connectivity()

# Perform smoothing with different operators
lap_types = ['uniform', 'geometric']
for j in range(len(lap_types)):
    # Build operator
    if j == 0:
        L = tm.uniform_laplacian()
    else:
        [L, negative, boundary] = tm.geometric_laplacian()

    # Apply operator
    num_iterations = 20
    for i in range(num_iterations):
        tm.vertex += np.dot(L, tm.vertex)

    # Save resulting mesh
    tm.save('output/bunny_smooth_' + lap_types[j] + '.obj')
