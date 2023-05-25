# Load a mesh and compute some geometric information

# Import the geometry processing library
import geomproc

# Load and normalize the mesh
tm = geomproc.load('meshes/bunny.obj')
tm.normalize()

# Save normalized mesh
tm.save('output/bunny_normalized.obj')

# Compute normal vectors
tm.compute_vertex_and_face_normals()

# Create geometry for normals

# Vertex normals
vn = geomproc.create_vectors(tm.vertex, tm.vnormal, color=[0, 0, 1])

# Face normals
centroid = (tm.vertex[tm.face[:, 0], :] + \
            tm.vertex[tm.face[:, 1], :] + \
            tm.vertex[tm.face[:, 2], :])/3.0
fn = geomproc.create_vectors(centroid, tm.fnormal, color=[1, 0, 0])

# Save the meshes for normals
wo = geomproc.write_options()
wo.write_vertex_colors = True
vn.save('output/bunny_vnormal.obj', wo)
fn.save('output/bunny_fnormal.obj', wo)

# Combine all geometries into one, if needed
#tm.append(vn)
#tm.append(fn)
#tm.save('output/bunny_all.obj', wo)
