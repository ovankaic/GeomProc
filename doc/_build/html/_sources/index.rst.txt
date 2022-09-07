Welcome to GeomProc's documentation!
====================================

.. image:: images/geomproc.png
  :target: https://graphics.stanford.edu/software/scanview/models/bunny.html
  :width: 1024
  :alt: Example outputs of the library

**GeomProc** is a geometry processing library intended for educational
purposes. Thus, the library was developed with an emphasis on legibility
of the code, documentation, and ease of use, rather than efficiency,
although the efficiency should not lag behind similar implementations in
interpreted languages, as the included methods are based on
state-of-the-art algorithms.  However, there is no guarantee that the
code is as efficient as a C++ implementation, or applicable to large
triangle meshes. To ensure ease of use, the library has only one
dependency: Python 3 with numpy. Note that an external mesh viewer such
as `MeshLab <https://www.meshlab.net/>`__ is required for visualizing the
output of the library.

The library comprises a set of example implementations of geometry
processing methods applicable to triangle meshes, point clouds, and
implicit functions. The basic classes of the library implement triangle
mesh and point cloud data structures. The library was developed from
code initially written in Matlab.


Demos
=====

.. toctree::
   :maxdepth: 2

   demos

User Guide
==========

.. toctree::
   :maxdepth: 2

   userguide

Modules
=======

.. toctree::
   :maxdepth: 2

   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
