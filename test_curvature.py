# Compute curvature values for a variety of analytical shapes
#
# Use the results to compare curvature values computed analytically to
# curvature values computed from the mesh

# Import geometry processing library
import geomproc

# Import os library for checking the output directory
import os

# Check if output directory exists
if not os.path.isdir('curv'):
    os.mkdir('curv')

# Set up write_option to save vertex colors
wo = geomproc.write_options()
wo.write_vertex_colors = True

# Cylinder
if 1: # Change if statement to 0 to disable this block
    cylinder = geomproc.create_cylinder(0.5, 1, 60, 10)
    cylinder.data_to_color_with_zero(cylinder.curv[:, 2])
    cylinder.save('curv/cylinder_mean_analytic.obj', wo)
    cylinder.data_to_color_with_zero(cylinder.curv[:, 3])
    cylinder.save('curv/cylinder_gaussian_analytic.obj', wo)

    cylinder2 = cylinder.copy()
    cylinder2.compute_curvature()
    cylinder2.data_to_color_with_zero(cylinder2.curv[:, 2])
    cylinder2.save('curv/cylinder_mean_discrete.obj', wo)
    cylinder2.data_to_color_with_zero(cylinder2.curv[:, 3])
    cylinder2.save('curv/cylinder_gaussian_discrete.obj', wo)

# Sphere
if 1:
    sphere = geomproc.create_sphere(0.5, 30, 30)
    sphere.data_to_color_with_zero(sphere.curv[:, 2])
    sphere.save('curv/sphere_mean_analytic.obj', wo)
    sphere.data_to_color_with_zero(sphere.curv[:, 3])
    sphere.save('curv/sphere_gaussian_analytic.obj', wo)

    sphere2 = sphere.copy()
    sphere2.compute_curvature()
    sphere2.data_to_color_with_zero(sphere2.curv[:, 2])
    sphere2.save('curv/sphere_mean_discrete.obj', wo)
    sphere2.data_to_color_with_zero(sphere2.curv[:, 3])
    sphere2.save('curv/sphere_gaussian_discrete.obj', wo)

# Cone
if 1:
    cone = geomproc.create_cone(0.5, 1, 60, 10)
    cone.data_to_color_with_zero(cone.curv[:, 2])
    cone.save('curv/cone_mean_analytic.obj', wo)
    cone.data_to_color_with_zero(cone.curv[:, 3])
    cone.save('curv/cone_gaussian_analytic.obj', wo)

    cone2 = cone.copy()
    cone2.compute_curvature()
    cone2.data_to_color_with_zero(cone2.curv[:, 2])
    cone2.save('curv/cone_mean_discrete.obj', wo)
    cone2.data_to_color_with_zero(cone2.curv[:, 3])
    cone2.save('curv/cone_gaussian_discrete.obj', wo)

# Torus
if 1:
    torus = geomproc.create_torus(1.0, 0.33, 90, 30)
    torus.data_to_color_with_zero(torus.curv[:, 2])
    torus.save('curv/torus_mean_analytic.obj', wo)
    torus.data_to_color_with_zero(torus.curv[:, 3])
    torus.save('curv/torus_gaussian_analytic.obj', wo)

    torus2 = torus.copy()
    torus2.compute_curvature()
    torus2.data_to_color_with_zero(torus2.curv[:, 2])
    torus2.save('curv/torus_mean_discrete.obj', wo)
    torus2.data_to_color_with_zero(torus2.curv[:, 3])
    torus2.save('curv/torus_gaussian_discrete.obj', wo)

# Saddle
if 1:
    saddle = geomproc.create_open_surface(30, 30, 1)
    saddle.data_to_color_with_zero(saddle.curv[:, 2])
    saddle.save('curv/saddle_mean_analytic.obj', wo)
    saddle.data_to_color_with_zero(saddle.curv[:, 3])
    saddle.save('curv/saddle_gaussian_analytic.obj', wo)

    saddle2 = saddle.copy()
    saddle2.compute_curvature()
    saddle2.data_to_color_with_zero(saddle2.curv[:, 2])
    saddle2.save('curv/saddle_mean_discrete.obj', wo)
    saddle2.data_to_color_with_zero(saddle2.curv[:, 3])
    saddle2.save('curv/saddle_gaussian_discrete.obj', wo)

# Monkey saddle
if 1:
    monkey_saddle = geomproc.create_open_surface(30, 30, 2)
    monkey_saddle.data_to_color_with_zero(monkey_saddle.curv[:, 2])
    monkey_saddle.save('curv/monkey_saddle_mean_analytic.obj', wo)
    monkey_saddle.data_to_color_with_zero(monkey_saddle.curv[:, 3])
    monkey_saddle.save('curv/monkey_saddle_gaussian_analytic.obj', wo)

    monkey_saddle2 = monkey_saddle.copy()
    monkey_saddle2.compute_curvature()
    monkey_saddle2.data_to_color_with_zero(monkey_saddle2.curv[:, 2])
    monkey_saddle2.save('curv/monkey_saddle_mean_discrete.obj', wo)
    monkey_saddle2.data_to_color_with_zero(monkey_saddle2.curv[:, 3])
    monkey_saddle2.save('curv/monkey_saddle_gaussian_discrete.obj', wo)
