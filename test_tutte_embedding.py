# Demo of computing a parameterization with Tutte's embedding

# Import geometry processing library
import geomproc

# Import numpy for data arrays
import numpy as np

# Import math for miscellaneous mathematical functions
import math


def map_boundary_to_circle(tm, bnd):
    """Map the vertices of a boundary to a circle in the given order
   
    Parameters
    ----------
    tm : mesh
        Mesh object for the input shape
    bnd : array_like
        List of vertices representing the boundary to be used for the
        parameterization

    Returns
    -------
    u : array_like
        Array of shape n x 2, where n is the number of vertices in the
        mesh. The array holds the 2D coordinates of each vertex of the
        boundary mapped to a circle. Vertices that are not on the
        boundary are assigned a coordinate [0, 0]

    Notes
    -----
    The method maps a list of vertices along a boundary to a circle of
    radius 0.5 centered at (0.5, 0.5), so that the entire mesh fits
    within the range [0:1, 0:1] required for texture coordinates. The
    list of boundary vertices has to be given in sequential order around
    the boundary.
    """
    
    # Get length of the boundary
    lgt = bnd.shape[0]

    # Initialize output coordinates
    u = np.zeros((tm.vertex.shape[0], 2))

    # Specify points along a circle
    increment = (2*math.pi)/(lgt-1)
    for i in range(lgt):
        u[bnd[i], :] = [0.5*math.cos(i*increment) + 0.5, 0.5*math.sin(i*increment) + 0.5]

    return u


def param_matrix(tm, lap_type, bnd):
    """Create the matrix needed for Tutte embedding based on the given boundary

    Parameters
    ----------
    tm : mesh
        Mesh object for the input shape
    lap_type : string
        The type of Laplacian operator used for creating the
        parameterization matrix. It can be either 'uniform' or
        'geometric'
    bnd : array_like
        List of vertices representing the boundary to be used for the
        parameterization

    Returns
    -------
    A : array_like
        Parameterization matrix that can be used for computing a Tutte
        embedding

    Notes
    -----
    The method builds a matrix that can be used for computing a Tutte
    parameterization of a mesh. The vertices on the boundary are fixed
    to positions around a circle, while other vertices are constrained
    according to the operator.
    """

    # Select the type of operator to use and create corresponding matrix
    if lap_type == 'uniform':
        A = tm.uniform_laplacian()
    elif lap_type == 'geometric':
        [A, negative, boundary] = tm.geometric_laplacian()
    else:
        raise RuntimeError('Invalid type of Laplacian specified: '+str(lap_type))

    # Transform the operator into a parameterization matrix
    for i in range(len(bnd)):
        A[bnd[i], :] = 0
        A[bnd[i], bnd[i]] = 1

    return A


def tutte_embedding(tm, lap_type, bnd):
    """Compute Tutte embedding of a mesh according to a given Laplacian

    Parameters
    ----------
    tm : mesh
        Mesh object for the input shape
    lap_type : string
        The type of Laplacian operator used for creating the
        parameterization matrix. It can be either 'uniform' or
        'geometric'
    bnd : array_like
        List of vertices representing the boundary to be used for the
        parameterization

    Returns
    -------
    u : array_like
        Array of shape n x 2, where n is the number of vertices in the
        mesh. Each row of the array represents the 2D coordinates of a
        vertex in the parameterization
    A : array_like
        Parameterization matrix used for computing the Tutte embedding
    constr : array_like
        Right-hand side constraints used for solving the linear system
    """

    # Map vertices along boundary to a circle of radius 0.5 centered at
    # (0.5, 0.5), so that the entire mesh fits within the range [0:1,
    # 0:1] required for texture coordinates
    constr = map_boundary_to_circle(tm, bnd)

    # Create matrix for linear system
    A = param_matrix(tm, lap_type, bnd)

    # Solve linear systems for u and v coordinates
    u = np.zeros((tm.vertex.shape[0], 3))
    u[:, 0] = np.linalg.solve(A, constr[:, 0])
    u[:, 1] = np.linalg.solve(A, constr[:, 1])
    # Third coordinate is left as all zeros, so that we can save the mesh

    # Return parameterized coordinates
    return [u, A, constr]


# Main function

# Specify input mesh
mesh_name = 'crater'
#mesh_name = 'beetle'
#mesh_name = 'bunny'
#mesh_name = 'camel_cut'

# Set input and output filenames
input_mesh = 'meshes/' + mesh_name + '.obj'
input_boundary = 'meshes/' + mesh_name + '.bnd'
output_prefix_texture = 'output/' + mesh_name + '_textured'
output_prefix_param = 'output/' + mesh_name + '_param'
output_prefix_boundary = 'output/' + mesh_name + '_boundary'

# Load and normalize mesh
tm = geomproc.load(input_mesh)
tm.normalize()

# Load boundary
bnd = np.loadtxt(input_boundary)
bnd = bnd.astype(int)

# Initialize write options
wo = geomproc.write_options()

# Compute parameterizations with different operators
lap_types = ['uniform', 'geometric']

for lap_type in lap_types:

    # Compute Tutte embedding
    [u, A, constr] = tutte_embedding(tm, lap_type, bnd)

    # Save mesh with the boundary highlighted
    tm.vcolor = np.ones((tm.vertex.shape[0], 3))
    tm.vcolor[bnd, :] = [1, 0, 0]
    wo.write_vertex_colors = True
    tm.save(output_prefix_boundary + '_' + lap_type + '.obj', wo)
    tm.vcolor = np.zeros((0, 3)) # Reset colors
    wo.write_vertex_colors = False # Reset this flag

    # Save textured mesh
    tm.vuv = u[:, 0:2]
    wo.write_vertex_uvs = True
    wo.texture_name = 'pattern.png'
    tm.save(output_prefix_texture + '_' + lap_type + '.obj', wo)
    tm.vuv = np.zeros((0, 2)) # Reset this field
    wo.write_vertex_uvs = False # Reset this flag
    wo.texture_name = ''

    # Save mesh parametrized to 2D
    param_tm = tm.copy()
    param_tm.vertex = u # Assign parameterized coordinates
    param_tm.save(output_prefix_param + '_' + lap_type + '.obj', wo)

    # Save operator
    #output_prefix_operator = mesh_name + '_matrix'
    #np.savetxt(output_prefix_operator + '_' + lap_type + '.txt', A)
