#
# GeomProc: geometry processing library in python + numpy
#
# Copyright (c) 2008-2024 Oliver van Kaick <ovankaic@gmail.com>
# under the MIT License.
#
# See file LICENSE.txt for details on copyright licenses.
#
"""This module contains functions for defining geometric transformations in the
GeomProc geometry processing library.

Rotations and scaling are represented as 3x3 matrices in column-major order

Translations are represented as 3x1 vectors
"""


import numpy as np
import math
import random


#### Geometric transformation functions

# Rotation around the X axis
def rotation_x(angle):
    """Define a 3D rotation around the X axis

    Parameters
    ----------
    angle : float
        Angle of rotation around the axis

    Returns
    -------
    mat : numpy.array_like 
        3x3 matrix representing the rotation
    """

    # Create and return matrix
    rot = np.array([[1, 0, 0],
                    [0, math.cos(angle), -math.sin(angle)],
                    [0, math.sin(angle), math.cos(angle)]])
    
    return rot


# Rotation around the Y axis
def rotation_y(angle):
    """Define a 3D rotation around the Y axis

    Parameters
    ----------
    angle : float
        Angle of rotation around the axis

    Returns
    -------
    mat : numpy.array_like 
        3x3 matrix representing the rotation
    """

    # Create and return matrix
    rot = np.array([[math.cos(angle), 0, math.sin(angle)],
                    [0, 1, 0],
                    [-math.sin(angle), 0, math.cos(angle)]])
    
    return rot


# Rotation around the Z axis
def rotation_z(angle):
    """Define a 3D rotation around the Z axis

    Parameters
    ----------
    angle : float
        Angle of rotation around the axis

    Returns
    -------
    mat : numpy.array_like 
        3x3 matrix representing the rotation
    """

    # Create and return matrix
    rot = np.array([[math.cos(angle), -math.sin(angle), 0],
                    [math.sin(angle), math.cos(angle), 0],
                    [0, 0, 1]])
    
    return rot


# Random rotation
def rotation_random():
    """Sample a random rotation in 3D

    Parameters
    ----------
    None

    Returns
    -------
    mat : numpy.array_like 
        3x3 matrix representing the rotation
    """

    # Create and return matrix
    rnd = np.random.random((3, 3))
    [q, r] = np.linalg.qr(rnd)
    return q


# Scaling
def scaling(x, y, z):
    """Define a 3D scaling transformation

    Parameters
    ----------
    x : float
        Scaling amount along x axis
    y : float
        Scaling amount along y axis
    z : float
        Scaling amount along z axis

    Returns
    -------
    mat : numpy.array_like 
        3x3 matrix representing the scaling
    """

    # Create and return matrix
    scl = np.array([[x, 0, 0],
                    [0, y, 0],
                    [0, 0, z]])

    return scl


# Translation
def translation(x, y, z):
    """Define a 3D translation

    Parameters
    ----------
    x : float
        Translation amount along x axis
    y : float
        Translation amount along y axis
    z : float
        Translation amount along z axis

    Returns
    -------
    vec : numpy.array_like 
        3x1 vector representing the translation
    """

    # Create and return the vector
    tr = np.array([x, y, z])
    tr.shape = (3, 1)
    return tr


# Random translation
def translation_random():
    """Sample a random 3D translation

    Parameters
    ----------
    None

    Returns
    -------
    vec : numpy.array_like 
        3x1 vector representing the translation
    """

    # Create and return the vector
    tr = np.random.random((3, 1))
    tr.shape = (3, 1)
    return tr
