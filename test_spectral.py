# Manifold harmonics demo
# The demo shows the different basis of the Laplacian operator

# Import geometry processing library
import geomproc

# Import numpy for data arrays
import numpy as np

# Load the mesh
tm = geomproc.load('meshes/bunny.obj')
tm.normalize()

# Compute connectivity information
tm.compute_connectivity()

# Select operator
L = tm.uniform_laplacian()
#[L, negative, boundary] = tm.geometric_laplacian()

# Compute eigenvectors
[W, V] = np.linalg.eig(L)

# Color the mesh according to eigenvectors
wo = geomproc.write_options()
wo.write_vertex_colors = True
# Choose which eigenvectors to show
for i in range(10): # Low frequency
#for i in range(200, 201): # High frequency
    tm.data_to_color(V[:,i], True, 0)
    # Save the mesh    
    tm.save('output/bunny_ev'+str(i)+'.obj', wo)
    
# Save some specific eigenvector
#i = 100
#tm.data_to_color(V[:,i], True, 0)
#tm.save('output/bunny_ev'+str(i)+'.obj', wo)
