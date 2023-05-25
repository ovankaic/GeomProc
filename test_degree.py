# Color a mesh according to the degrees of its vertices

# Import the geometry processing library
import geomproc

# Import numpy for creating data arrays
import numpy as np

# Load and normalize the mesh
tm = geomproc.load('meshes/bunny.obj')
tm.normalize()

# Compute connectivity information
tm.compute_connectivity()

# Collect vertex degrees
degree = np.zeros(tm.vertex.shape[0])
for i in range(tm.vertex.shape[0]):
    degree[i] = len(tm.viv[i])

# Color the mesh according to degrees
tm.data_to_color(degree, True, 0)

# Save the mesh
wo = geomproc.write_options()
wo.write_vertex_colors = True
tm.save('output/bunny_degree.obj', wo)
