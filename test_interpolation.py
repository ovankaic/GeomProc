# Example of interpolating colors across a mesh with the Laplacian

# Import the geometry processing library
import geomproc

# Use numpy for handling matrices
import numpy as np

# Load and normalize the mesh
tm = geomproc.load('meshes/crater.obj')
tm.normalize()

# Compute connectivity information
tm.compute_connectivity()

# Compute Laplacian operator
[L, negative, boundary] = tm.geometric_laplacian()

# Define starting constraints for the interpolation
# Four corners of the mesh in counterclockwise order
ver = [0, 57, 4999, 4962] 
# Colors to be assigned to the four corners
color = [[1, 0, 0], [0, 1, 0], [0.8, 0.8, 0.8], [0, 0, 1]]
color = np.array(color)

# Initialize interpolation constraints (colors)
col = np.zeros((tm.vertex.shape[0], 3))

# Select type of constraints
if False:
    # Set color constraints only at corners
    for i in range(len(ver)):
        v = ver[i]
        L[v, :] = 0
        L[v, v] = 1
        col[v, :] = color[i, :]
else:
    # Compute geodesic paths between corners to define extra constraints
    # along the borders
    # In this way, the color interpolation will look nicer
    #
    # Find borders by tracing geodesic paths on the mesh graph
    #
    # Create graph for the mesh
    graph = geomproc.graph()
    # Adjacency is vertex neighborhood
    graph.adj = tm.viv
    # Weights are lengths of edges between vertices
    graph.weight = [[] for i in range(tm.vertex.shape[0])]
    for i in range(tm.vertex.shape[0]):
        for j in range(len(tm.viv[i])):
            dist = geomproc.distance(tm.vertex[i, :], tm.vertex[tm.viv[i][j], :])
            graph.weight[i].append(dist)
    # Compute paths starting from four corners
    sp = graph.compute_shortest_paths(ver)

    # Set constraints
    for i in range(len(ver)):
        # Find corner and its successor along the border
        indx = i
        succ_indx = (i + 1) % len(ver)
        curr = ver[indx]
        succ = ver[succ_indx]
        # Get path between corner and its successor
        path = sp.get_path(curr, succ)
        # Set constraints in matrix and col vector
        for j in range(len(path)):
            v = path[j]
            L[v, :] = 0
            L[v, v] = 1
            # Interpolate color along path
            p = float(j)/float(len(path)-1)
            col[v, :] = (1.0-p)*color[indx, :] + p*color[succ_indx, :]

# Solve linear system to get colors for all other vertices
tm.vcolor = np.linalg.solve(L, col)

# Save mesh with colors
wo = geomproc.write_options()
wo.write_vertex_colors = True
tm.save('output/crater_interpolation.obj', wo)
