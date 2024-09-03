#
# GeomProc: geometry processing library in python + numpy
#
# Copyright (c) 2008-2024 Oliver van Kaick <ovankaic@gmail.com>
# under the MIT License.
#
# See file LICENSE.txt for details on copyright licenses.
#
"""This module contains the read_options class of the GeomProc geometry
processing library.
"""


# Options for reading files
class read_options:
    """A class that holds options of what information to read when loading a file

    Attributes
    ----------
    split_polygons : boolean
        Split polygons into triangles when reading a file. The default
        value is True

    Notes
    -----
    Not all options are relevant to every file format. The class
    collects all the possible options supported by different file
    formats. The structure is relevant to both meshes and point clouds.
    """

    def __init__(self):
        # Not all options are accepted by every file format
        self.split_polygons = True
