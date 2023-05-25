# Load and sample a mesh

import geomproc

# Load and normalize the mesh
tm = geomproc.load('meshes/bunny.obj')
tm.normalize()

# Save normalized mesh
tm.save('output/bunny_normalized.obj')

# Compute normal vectors
tm.compute_vertex_and_face_normals()

# Sample the mesh
num_samples = 1000
pc = tm.sample(num_samples)

# Save just the samples
wo = geomproc.write_options()
wo.write_point_normals = True
pc.save('output/bunny_only_samples.obj', wo)

# Save the samples as geometry that can be visualized
wo = geomproc.write_options()
wo.write_vertex_colors = True
points = geomproc.create_points(pc.point, 0.01)
points.save('output/bunny_samples.obj', wo)
