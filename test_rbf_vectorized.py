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
n = 2000
pc = tm.sample(n)

# Define vectorized kernel for reconstruction
euclidean = lambda x, y: np.sqrt(np.absolute(-2.0*np.dot(x, y.T) + np.sum(np.square(x), axis=1, keepdims=True) + np.sum(np.square(y), axis=1, keepdims=True).T))
kernel = lambda x, y: np.power(euclidean(x, y), 3.0)

# Define epsilon for displacing samples
epsilon = 0.01

# Run RBF reconstruction
print('Reconstructing implicit function')
start_time = time.time()
surf = geomproc.impsurf()
surf.setup_rbf(pc, epsilon, kernel, True)

# Run marching cubes
print('Running marching cubes')
rec = geomproc.marching_cubes(np.array([-1.5, -1.5, -1.5]), np.array([1.5, 1.5, 1.5]), 64, surf.evaluate)

# Report time
end_time = time.time()
print('Execution time = ' + str(end_time - start_time) +'s')

# Save output mesh
rec.save('output/bunny_rec.obj')
