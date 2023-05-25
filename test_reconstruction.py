# Test reconstruction of an implicit function with the marching cubes
# algorithm

# Import geometry processing library
import geomproc

# Import numpy for data arrays
import numpy as np

# Set up an implicit function for a surface
surf = geomproc.impsurf()
#surf.setup_sphere(0.5)
surf.setup_torus(0.6, 0.3)

# Reconstruct the surface
tm = geomproc.marching_cubes(np.array([-1, -1, -1]), np.array([1, 1, 1]), 32, surf.evaluate)

# Save surface
tm.save('output/reconstruction.obj')
