# Align two point clouds with descriptor matching

# Import the geometry processing library
import geomproc

# Import numpy for data arrays
import numpy as np

# Math functions
import math


#### Create point samples for the test

# Load and normalize the mesh
tm1 = geomproc.load('meshes/bunny.obj')
tm1.normalize()

# Apply a transformation to the mesh to create a misaligned version
# Define the transformation
if False: # Choose the transformation by switching True/False
    # Choose a completely random transformation
    rnd = np.random.random((3, 3))
    [q, r] = np.linalg.qr(rnd)
    orig_rot = q
    orig_trans = np.random.random((3, 1))
else:
    # Choose a specific rotation around the y axis
    angle = math.pi/3
    orig_rot = np.array([[math.cos(angle), 0, math.sin(angle)],
                         [0, 1, 0],
                         [-math.sin(angle), 0, math.cos(angle)]])
    orig_trans = np.zeros((3, 1))

# Copy the mesh and apply the transformation to the mesh
tm2 = tm1.copy()
tm2.vertex = geomproc.apply_transformation(tm1.vertex, orig_rot, orig_trans)
# Update normals: important! As the spin images descriptor depends on them
tm2.compute_vertex_and_face_normals() 

# Sample two sets of points from the surfaces of the meshes
n1 = 1000 # We are going to compute a descriptor for each of these points
n2 = 10000 # We are going to use these points only for reference in the descriptor computation
pc1 = tm1.sample(n1)
pc1full = tm1.sample(n2)
pc2 = tm2.sample(n1)
pc2full = tm2.sample(n2)

# Save input data
tm1.save('output/bunny_normalized.obj')
pc1.save('output/bunny_sample1.obj')
pc2.save('output/bunny_sample2.obj')


#### Align the point clouds

# Compute the spin images descriptor for the two point clouds
opt = geomproc.spin_image_options()
desc1 = geomproc.spin_images(pc1, pc1full, opt)
desc2 = geomproc.spin_images(pc2, pc2full, opt)

# Match the descriptors
corr = geomproc.best_match(desc1, desc2)
corr = geomproc.filter_correspondences(corr, 0.3)

# Derive a transformation from the point match
[rot, trans] = geomproc.transformation_from_correspondences(pc1, pc2, corr)

# Apply the transformation to align the meshes
pc1tr = pc1.copy()
pc1tr.point = geomproc.apply_transformation(pc1.point, rot, trans)

# Save registration
pc1tr.save('output/bunny_sample1aligned.obj')

# Save final correspondence so that we can see it
if True: # Turn on/off with True/False
    # Create lines to indicate the correspondences
    line = np.zeros((corr.shape[0], 6))
    for i in range(corr.shape[0]):
        line[i, :] = np.concatenate((pc1tr.point[corr[i, 0], :], pc2.point[corr[i, 1], :]))
    cl = geomproc.create_lines(line, color=[0.7, 0.7, 0.7])
    # Create points for the point sets
    pt1 = geomproc.create_points(pc1tr.point, color=[1, 0, 0])
    pt2 = geomproc.create_points(pc1.point, color=[0, 1, 0])
    pt3 = geomproc.create_points(pc2.point, color=[0, 0, 1])
    # Combine everything together
    result = geomproc.mesh()
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
