# Approximate geodesic distances on a mesh by computing graph distances

# Import the geometry processing library
import geomproc

# Import numpy for creating data arrays
import numpy as np

# Load and normalize the mesh
tm = geomproc.load('meshes/bunny.obj')
tm.normalize()

# Compute connectivity information
tm.compute_connectivity()

# Compute graph distances on mesh vertices
graph = geomproc.graph()
# Adjacency is vertex neighborhood
graph.adj = tm.viv
# Weights are lengths of edges between vertices
graph.weight = [[] for i in range(tm.vertex.shape[0])]
for i in range(tm.vertex.shape[0]):
    for j in range(len(tm.viv[i])):
        dist = geomproc.distance(tm.vertex[i, :], tm.vertex[tm.viv[i][j], :])
        graph.weight[i].append(dist)
# Source vertex is arbitrarily set to index 0. Modify freely
source = 0
# Compute shortest paths
sp = graph.compute_shortest_paths(source)
# Map graph distances to vertex colors
tm.data_to_color(np.array(sp.dist[0]), True, 0)

# Save the mesh with the colors
wo = geomproc.write_options()
wo.write_vertex_colors = True
tm.save('output/bunny_vgeodesic.obj', wo)

# Compute graph distances on mesh faces
graph = geomproc.graph()
# Adjacency is face neighborhood
graph.adj = tm.fif
# Weights are distances between face centroids
graph.weight = [[] for i in range(tm.face.shape[0])]
for i in range(tm.face.shape[0]):
    for j in range(len(tm.fif[i])):
        centroid1 = tm.vertex[tm.face[i, :]].mean(axis=0)
        centroid2 = tm.vertex[tm.face[tm.fif[i][j], :]].mean(axis=0)
        dist = geomproc.distance(centroid1, centroid2)
        graph.weight[i].append(dist)
# Source face is arbitrarily set to index 0. Modify freely
source = 0
# Compute shortest paths
sp = graph.compute_shortest_paths(source)
# Map graph distances to colors of vertices
data = tm.data_face_to_vertex(np.array(sp.dist[0]))
tm.data_to_color(data, True, 0)

# Save the mesh with the colors
wo = geomproc.write_options()
wo.write_vertex_colors = True
tm.save('output/bunny_fgeodesic.obj', wo)
