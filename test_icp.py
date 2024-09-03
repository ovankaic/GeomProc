# Align two point clouds with the ICP algorithm

# Import the geometry processing library
import geomproc

# Import numpy for data arrays
import numpy as np

# Math functions
import math


# Default setting: 1000 points and 50 iterations
#
# Things to try:
# - A Completely random transformation
# - A different set of samples for pc2 (call tm.sample() again)
# - Estimate normals instead of using mesh normals
# - More points and iterations


#### Create a point sample for the test

# Load and normalize the mesh
tm = geomproc.load('meshes/bunny.obj')
tm.normalize()

# Sample a set of points from the surface of the mesh
n = 1000
pc1 = tm.sample(n)

# Apply a transformation to pc1 to create pc2
# Define the transformation
if False: # Choose the transformation by switching True/False
    # Choose a completely random transformation
    orig_rot = geomproc.rotation_random()
    orig_trans = geomproc.translation_random()
else:
    # Choose a specific rotation around the y axis
    angle = math.pi/3
    orig_rot = geomproc.rotation_y(angle)
    orig_trans = geomproc.translation(0, 0, 0)

# Apply the transformation to pc1 to create the second point cloud pc2
pc2 = pc1.copy()
# For a more realistic example, pc2 could be another set of samples
# pc2 = tm.sample(n)
pc2.point = geomproc.apply_transformation(pc2.point, orig_rot, orig_trans)

# Save input data
tm.save('output/bunny_normalized.obj')
pc1.save('output/bunny_sample1.obj')
pc2.save('output/bunny_sample2.obj')


#### Align the point clouds

# Run the ICP method
error_threshold = 0.01
num_iters = 50
[rot, trans, pc1tr, err, iter_count, corr] = geomproc.icp(pc1, pc2, error_threshold, num_iters, 0.8)

# Save registration
pc1tr.save('output/bunny_sample1aligned.obj')

# Save final correspondence so that we can see it
if True: # Turn on/off with True/False
    # Create lines to indicate the correspondences
    line = np.zeros((pc1.point.shape[0], 6))
    for i in range(corr.shape[0]):
        line[i, :] = np.concatenate((pc1tr.point[corr[i, 0], :], pc2.point[corr[i, 1], :]))
    cl = geomproc.create_lines(line, color=[0.7, 0.7, 0.7])
    # Create points for the point sets
    pt1 = geomproc.create_points(pc1tr.point, color=[1, 0, 0])
    pt2 = geomproc.create_points(pc1.point, color=[0, 1, 0])
    pt3 = geomproc.create_points(pc2.point, color=[0, 0, 1])
    # Combine everything together
    result = geomproc.mesh()
    result.append(cl)
    result.append(pt1)
    result.append(pt2)
    result.append(pt3)
    # Save the mesh
    wo = geomproc.write_options()
    wo.write_vertex_colors = True
    result.save('output/bunny_corr.obj', wo)

# Print some information
print('Original transformation = ')
print(orig_rot)
print(orig_trans)
print('Alignment result = ')
print(rot)
print(trans)
print('Number of iterations used = ', iter_count)
print('Error after alignment = ', err)
