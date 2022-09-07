Demos
=====

Note in these code listings that there is no need to load submodules of
the library, as all the classes and functions in the submodules are made
visible as part of the package *geomproc*.


Load a mesh and visualize normal vectors
----------------------------------------

test_mesh.py

.. literalinclude:: ../test_mesh.py
    :language: python

Result: bunny with vertex normals (blue) and face normals (red)

.. image:: images/bunny_normals.png
  :width: 320
  :alt: Bunny with vertex normals (blue) and face normals (red)


Visualize mesh degree
---------------------

test_degree.py

.. literalinclude:: ../test_degree.py
    :language: python

Result: deviation from degree 6 shown with colors

.. image:: images/bunny_degree.png
  :width: 320
  :alt: Bunny with degree denoted by color


Curvature computation
---------------------

Curvature comparison on various primitive surfaces: test_curvature.py

.. literalinclude:: ../test_curvature.py
    :language: python

Curvature comparison on a shape with and without noise:
test_curvature_with_noise.py

.. literalinclude:: ../test_curvature_with_noise.py
    :language: python

Result: curvature plot on bunny without and with noise

.. image:: images/bunny_curvature.png
  :width: 320
  :alt: Bunny with colors denoting Gaussian curvature

.. image:: images/bunny_with_noise_curvature.png
  :width: 320
  :alt: Noisy bunny with colors denoting Gaussian curvature


Mesh smoothing
--------------

With averaging method: test_smoothing.py

.. literalinclude:: ../test_smoothing.py
    :language: python

With Laplacian operator: test_smoothing_with_operator.py

.. literalinclude:: ../test_smoothing_with_operator.py
    :language: python

Result: smooth bunny obtained with uniform and geometric Laplacians

.. image:: images/bunny_smooth_uniform.png
  :width: 320
  :alt: Smooth bunny obtained with uniform Laplacian

.. image:: images/bunny_smooth_geometric.png
  :width: 320
  :alt: Smooth bunny obtained with geometric Laplacian


Mesh parameterization
---------------------

test_tutte_embedding.py

.. literalinclude:: ../test_tutte_embedding.py
    :language: python

Result: parameterization of Crater Lake and texture mapping

.. image:: images/crater_param.png
  :width: 320
  :alt: Parameterization of Crater Lake

.. image:: images/pattern.png
  :width: 200
  :alt: Texture

.. image:: images/crater_with_texture.png
  :width: 320
  :alt: Textured Crater Lake


Sample a mesh
-------------

test_sample.py

.. literalinclude:: ../test_sample.py
    :language: python


Estimate normals of a point cloud
---------------------------------

test_normal.py

.. literalinclude:: ../test_normal.py
    :language: python


Align two point clouds
----------------------

With the ICP method: test_icp.py

.. literalinclude:: ../test_icp.py
    :language: python

Result: green samples transformed to red samples to align with blue
samples

.. image:: images/bunny_aligned.png
  :width: 320
  :alt: Aligned samples of bunny model

With descriptor matching: test_spin_images.py

.. literalinclude:: ../test_spin_images.py
    :language: python


Reconstruction of an implicit surface
-------------------------------------

test_reconstruction.py

.. literalinclude:: ../test_reconstruction.py
    :language: python

Result: torus reconstructed from implicit function

.. image:: images/torus_rec.png
  :width: 320
  :alt: Reconstruction of a torus


RBF surface reconstruction
--------------------------

Simple version: test_rbf.py

.. literalinclude:: ../test_rbf.py
    :language: python

Faster, vectorized version: test_rbf_vectorized.py

.. literalinclude:: ../test_rbf_vectorized.py
    :language: python


Approximate geodesic distances
------------------------------

test_geodesic.py

.. literalinclude:: ../test_geodesic.py
    :language: python

Result: approximate geodesic distance from a source vertex (blue region)

.. image:: images/bunny_geodesic.png
  :width: 320
  :alt: Bunny with color denoting geodesic distances


