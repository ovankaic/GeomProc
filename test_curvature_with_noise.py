# Compute curvature values for a given mesh and its noisy version

# Import the geometry processing library
import geomproc

# Import os library for checking the output directory
import os

# Check if output directory exists
if not os.path.isdir('curv'):
    os.mkdir('curv')

# Load and normalize the mesh
tm = geomproc.load('meshes/bunny.obj')
tm.normalize()

# Compute curvature of the mesh
tm.compute_vertex_and_face_normals()
tm.compute_curvature()

# Set up write_option to save vertex colors
wo = geomproc.write_options()
wo.write_vertex_colors = True

# Save curvature information as colors of a mesh
[mn, mx] = tm.data_to_color_with_zero(tm.curv[:, 3], percent=0.1)
tm.save('curv/bunny_gaussian_discrete.obj', wo)

# Add noise to the mesh
tm.add_noise(0.02);

# Recompute curvature of the mesh
# Note: we also need to recompute normals
tm.compute_vertex_and_face_normals()
tm.compute_curvature()

# Save curvature information as colors of a mesh
tm.data_to_color_with_zero(tm.curv[:, 3], percent=0.1, minimum=mn, maximum=mx)
tm.save('curv/bunny_with_noise_gaussian_discrete.obj', wo)
