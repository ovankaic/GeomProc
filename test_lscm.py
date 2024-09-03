# Demo of computing a parameterization with least-squares conformal maps
# Using the alternative formulation of LSCM based on preserving triangle
# shapes


# Import geometry processing library
import geomproc

# Import numpy for data arrays
import numpy as np

# Import math for miscellaneous mathematical functions
import math


# Parametrize mesh "tm" with LSCM
def lscm(tm, constr_indx, constr_coord):
    """Compute a parameterization of a mesh with LSCM

    Parameters
    ----------
    tm : mesh
        Mesh object for the input shape
    constr_indx : array_like
        Index of each vertex to be used as a constraint
    constr_coord : array_like
        Constrained coordinates of each vertex listed in constr_indx

    Returns
    -------
    u : array_like
        Array of shape n x 2, where n is the number of vertices in the
        mesh. Each row of the array represents the 2D coordinates of a
        vertex in the parameterization
    A : array_like
        Parameterization matrix used for computing the embedding
    constr : array_like
        Right-hand side constraints used for solving the linear system
    """

    # Create matrix for linear system
    m = tm.face.shape[0]
    n = tm.vertex.shape[0]
    # We have 2*n columns since we are merging u and v into one vector
    # We need to merge them into one vector as they are inter-dependent
    # on each other
    # We have two constraints (equations) per triangle, 
    # and four extra fixed constraints (u and v for 2 points = 4 in total)
    A = np.zeros((2*m + 2*len(constr_indx), 2*n))

    # Set coefficients of linear system
    # Create two equations (t, and m + t) per triangle
    for t in range(m):
        # Get vertices of triangle
        [i0, i1, i2] = tm.face[t, :]
        v0 = tm.vertex[i0, :]
        v1 = tm.vertex[i1, :]
        v2 = tm.vertex[i2, :]
        # Compute edge lengths (norms)
        vec1 = v1 - v0
        vec2 = v2 - v0
        n1 = np.linalg.norm(vec1)
        n2 = np.linalg.norm(vec2)
        # Compute sine and cosine of angle at v0
        vec1 /= n1
        vec2 /= n2
        cs = np.dot(vec1, vec2)
        sn = np.linalg.norm(np.cross(vec1, vec2))
        # Fill entries of matrix A according to formulas
        A[t, i0] = n2*cs - n1 
        A[t, n + i0] = -n2*sn
        A[m + t, i0] = n2*sn
        A[m + t, n + i0] = n2*cs -n1
        
        A[t, i1] = -n2*cs 
        A[t, n + i1] = n2*sn
        A[m + t, i1] = -n2*sn
        A[m + t, n + i1] = -n2*cs
        
        A[t, i2] = n1
        A[m + t, n + i2] = n1
        
    # Set constraints
    constr = np.zeros(2*m + 2*len(constr_indx))
    
    # Assign constraints to A and constr vector
    for i in range(len(constr_indx)):
        constr[2*m + 2*i] = constr_coord[i][0]
        constr[2*m + 2*i + 1] = constr_coord[i][1]
        A[2*m + 2*i, constr_indx[i]] = 1
        A[2*m + 2*i + 1, n + constr_indx[i]] = 1
    
    # Solve linear system in least-squares sense
    #sol = np.linalg.solve(A, constr)
    [sol, _, _, _] = np.linalg.lstsq(A, constr, rcond=None)
    
    # Assign coordinates to output vector in proper order
    # Map (u, v)'s in 1D array to 3D array
    u = np.zeros((tm.vertex.shape[0], 3))
    u[:, 0] = sol[0:n]
    u[:, 1] = sol[n:2*n]
    # Third coordinate is left as all zeros, so that we can save the mesh

    # Return parameterized coordinates
    return [u, A, constr]


# Main function

# Specify input mesh
mesh_name = 'crater'
#mesh_name = 'beetle'
#mesh_name = 'bunny'
#mesh_name = 'camel_cut'
#mesh_name = 'psaddle'

# Set input and output filenames
input_mesh = 'meshes/' + mesh_name + '.obj'
input_boundary = 'meshes/' + mesh_name + '.bnd'
output_prefix_texture = 'output/' + mesh_name + '_textured'
output_prefix_param = 'output/' + mesh_name + '_param'
output_prefix_boundary = 'output/' + mesh_name + '_boundary'

# Load and normalize mesh
tm = geomproc.load(input_mesh)
#tm = geomproc.create_open_surface(30, 30, 1)
tm.normalize()

# Load boundary
bnd = np.loadtxt(input_boundary)
bnd = bnd.astype(int)

# Initialize write options
wo = geomproc.write_options()

# Set constraints
# Points to be used as fixed constraints
constr_indx = [bnd[0], bnd[int(len(bnd)/2)]]
# Respective coordinates of constrained points
constr_coord = [[0.5, 1], [0.5, 0]]

# Compute LSCM embedding
[u, A, constr] = lscm(tm, constr_indx, constr_coord)

# Save mesh with the boundary highlighted (uncomment code)
#tm.vcolor = np.ones((tm.vertex.shape[0], 3))
#tm.vcolor[bnd, :] = [1, 0, 0]
#wo.write_vertex_colors = True
#tm.save(output_prefix_boundary + '_' + lap_type + '.obj', wo)
#tm.vcolor = np.zeros((0, 3)) # Reset colors
#wo.write_vertex_colors = False # Reset this flag

# Save textured mesh
tm.vuv = u[:, 0:2]
wo.write_vertex_uvs = True
wo.texture_name = 'pattern.png'
tm.save(output_prefix_texture + '_lscm.obj', wo)
tm.vuv = np.zeros((0, 2)) # Reset this field
wo.write_vertex_uvs = False # Reset this flag
wo.texture_name = ''

# Save mesh parametrized to 2D
param_tm = tm.copy()
param_tm.vertex = u # Assign parameterized coordinates
param_tm.save(output_prefix_param + '_lscm.obj', wo)

# Save matrix
#output_prefix_operator = mesh_name + '_matrix'
#np.savetxt(output_prefix_operator + '_' + lap_type + '.txt', A)
