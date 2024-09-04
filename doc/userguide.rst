User Guide
----------

Note that there is no need to load submodules of the library, as all the
classes and functions in the submodules are made visible in the main
module *geomproc*.

**Main classes**

 - Triangle mesh: :py:class:`geomproc.mesh`
 - Point cloud: :py:class:`geomproc.pcloud`
 - Implicit function: :py:class:`geomproc.impsurf`
 - Volume: :py:class:`geomproc.volume`

**Data loading**

 - :py:func:`geomproc.loading.load` - Load data from a file and create a
   triangle mesh or point cloud object

**Mesh creation**

 - :py:func:`geomproc.creation.create_cone` - Create a cone
 - :py:func:`geomproc.creation.create_cylinder` - Create a cylinder
 - :py:func:`geomproc.creation.create_open_surface` - Create a 2D parametric surface
 - :py:func:`geomproc.creation.create_sphere` - Create a sphere
 - :py:func:`geomproc.creation.create_subdivided_cube` - Create a cube subdivided into smaller faces
 - :py:func:`geomproc.creation.create_torus` - Create a torus

**Misc mesh creation**

 - :py:func:`geomproc.creation.create_points` - Create mesh geometry to display a set of points
 - :py:func:`geomproc.creation.create_vectors` - Create mesh geometry to display a set of vectors
 - :py:func:`geomproc.creation.create_lines` - Create mesh geometry to display a set of lines

**Point cloud creation**

 - :py:func:`geomproc.creation.create_sphere_samples` - Sample a set of points from a sphere

**Point cloud alignment**

 - :py:func:`geomproc.alignment.icp` - Align two point clouds with the ICP method
 - :py:func:`geomproc.alignment.spin_images` - Compute shape descriptors for
   points in a cloud
 - :py:func:`geomproc.alignment.best_match` - Match two point clouds based on
   shape descriptors

**Surface reconstruction**

 - :py:func:`geomproc.impsurf.impsurf.setup_rbf` - Reconstruct an implicit surface from a set of point samples
 - :py:func:`geomproc.marching_cubes.marching_cubes` - Reconstruct a mesh from an implicit surface 

**Voxelization**

 - :py:func:`geomproc.volume.voxelize_mesh` - Voxelize a mesh

**Auxiliary/miscellaneous functions**

 - :py:func:`geomproc.misc.map_val` - Linearly map a set of values to a new range
 - :py:func:`geomproc.misc.hsv2rgb` - Transform a color from the HSV to the RGB color system
 - :py:func:`geomproc.misc.rotation_matrix` - Create a rotation matrix from an axis and angle
 - :py:func:`geomproc.misc.random_triangle_sample` - Randomly sample a point from a triangle
 - :py:func:`geomproc.misc.distance` - Euclidean distance between two points
 - :py:func:`geomproc.transform` - Initialize geometric transformations

**Axuliary classes**

 - :py:class:`geomproc.graph` - Graph
 - :py:class:`geomproc.kdtree.KDTree` - KDTree for efficient point queries (partially third-party software)
