# Test reconstruction of a set of samples with the RBF method

# Import geometry processing library
import geomproc

# Import numpy for data arrays
import numpy as np

# Import math functions
import math

# Measure execution time
import time

# Load and normalize the mesh
tm = geomproc.load('meshes/bunny.obj')
tm.normalize()

# Save normalized mesh
tm.save('output/bunny_normalized.obj')

# Compute normal vectors
tm.compute_vertex_and_face_normals()

# Sample a point cloud from the mesh
n = 1000
pc = tm.sample(n)

# Define kernel for reconstruction
#kernel = lambda x, y: math.pow(np.linalg.norm(x - y), 3)
wendland = lambda r, h: max(math.pow(1 - r/h, 4), 0.0)*(4.0*r/h + 1)
kernel = lambda x, y: wendland(np.linalg.norm(x - y), 0.01)

# Define epsilon for displacing samples
epsilon = 0.01

# Run RBF reconstruction
print('Reconstructing implicit function')
start_time = time.time()
surf = geomproc.impsurf()
surf.setup_rbf(pc, epsilon, kernel)

# Run marching cubes
print('Running marching cubes')
rec = geomproc.marching_cubes(np.array([-1.5, -1.5, -1.5]), np.array([1.5, 1.5, 1.5]), 16, surf.evaluate)

# Report time
end_time = time.time()
print('Execution time = ' + str(end_time - start_time) +'s')

# Save output mesh
rec.save('output/bunny_rec.obj')
