# Compute normals of a point cloud

import geomproc
import numpy as np

# Load and normalize the mesh
tm = geomproc.load('meshes/bunny.obj')
tm.normalize()

# Compute normal vectors
tm.compute_vertex_and_face_normals()

# Sample the mesh
num_samples = 10000
pc = tm.sample(num_samples)

# Estimate normals
pc_est = pc.copy()
pc_est.estimate_normals_simple(10)

# Calculate errors between real and estimated normals
dist = (pc.normal - pc_est.normal)**2
dist = np.sum(dist, axis=1)
dist = np.sqrt(dist)
mn = dist.min()
mx = dist.max()
arg_mn = dist.argmin()
arg_mx = dist.argmax()
print('Simple normal estimation')
print('Minimum error: '+str(mn)+' for normals '+str(pc.normal[arg_mn, :])+' and '+str(pc_est.normal[arg_mn, :])+' at index '+str(arg_mn))
print('Maximum error: '+str(mx)+' for normals '+str(pc.normal[arg_mx, :])+' and '+str(pc_est.normal[arg_mx, :])+' at index '+str(arg_mx))

# Estimate normals
pc_est2 = pc.copy()
pc_est2.estimate_normals(10)

# Calculate errors between real and estimated normals
dist2 = (pc.normal - pc_est2.normal)**2
dist2 = np.sum(dist2, axis=1)
dist2 = np.sqrt(dist2)
mn2 = dist2.min()
mx2 = dist2.max()
arg_mn2 = dist2.argmin()
arg_mx2 = dist2.argmax()
print('Normal estimation with flipping')
print('Minimum error: '+str(mn2)+' for normals '+str(pc.normal[arg_mn2, :])+' and '+str(pc_est.normal[arg_mn2, :])+' at index '+str(arg_mn2))
print('Maximum error: '+str(mx2)+' for normals '+str(pc.normal[arg_mx2, :])+' and '+str(pc_est.normal[arg_mx2, :])+' at index '+str(arg_mx2))


if 1:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2)
    ax[0].hist(dist, 20)
    ax[1].hist(dist2, 20)
    plt.show()

# Vertex normals
if 0:
    pnt = geomproc.create_points(pc.point, radius=0.01, color=[1, 0, 0])
    vec = geomproc.create_vectors(pc.point, pc.normal, color=[1, 0, 0])
    vec2 = geomproc.create_vectors(pc.point, pc_est.normal, color=[0, 0, 1])
    vec3 = geomproc.create_vectors(pc.point, pc_est2.normal, color=[0, 1, 0])
    pnt.append(vec)
    pnt.append(vec2)
    pnt.append(vec3)

# Save the mesh
    wo = geomproc.write_options()
    wo.write_vertex_colors = True
    pnt.save('output/bunny_nv.obj', wo)

# Save samples
#pc.save('output/bunny_samples.ply')
