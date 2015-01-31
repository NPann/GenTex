######################## gentex package ###########################

""" The gentex or general texture analysis package provides a suite
    of routines that combine standard texture analysis methods and
    entropy/statistical complexity analysis methods to provide a number
    of the standard algorithms required for generating complexity/texture
    measure estimates from multimodal imaging data. These include:
    
          1) Generation of multidimensional feature spaces
             from multimodal 'image' data (i.e. multiple 'co-registered'
             1,2,3, or 4 dimensional data sets, e.g. multiple
             'co-registered' time series, multimodal image data,
             space/time data..) via the use of a set of image templates,
             inculding:
                a) single voxels
                b) linear sequences in cardinal directions
                   (ref.)
                c) notches in cardinal directions
                   (ref.)
                d) light cones in cardinal directions and
                   45 degree angles
                   (ref.)

          2) Clustering methods for generating disrete ('grey') levels
             from the constructed feature space (the levels are then
             typically mapped to the original image space at the anchor
             points of the templates)
             
          3) Building co-occurrence matrices from a discrete level 'image'
             or a pair of discrete level 'images', where the discrete level
             'images' are typically generated via feature space clustering
             of the original multimodal data sets (time series, images,
             space/time data...)

          4) Estimation of various complexity/texture measures from the
             co-occurrence matrices.
"""

import sys

import numpy as np


try:
    from ctypes import c_int, c_uint8, c_double, c_char, Structure, POINTER
except:
    print('Requires ctypes > 1.0.1')
    sys.exit(-1)

try:
    _comat = np.ctypeslib.load_library('libmakecomat_', __file__)
except:
    print(
        'Failed to load libmakecomat_.so.  Compile the library using python setup.py build_ext -i from the package root directory.')
    sys.exit(-1)

array_1d_int = np.ctypeslib.ndpointer(dtype=np.intc, ndim=1,
                                      flags='CONTIGUOUS')
array_2d_int = np.ctypeslib.ndpointer(dtype=np.intc, ndim=2,
                                      flags='CONTIGUOUS')
array_3d_int = np.ctypeslib.ndpointer(dtype=np.intc, ndim=3,
                                      flags='CONTIGUOUS')
array_4d_int = np.ctypeslib.ndpointer(dtype=np.intc, ndim=4,
                                      flags='CONTIGUOUS')

# Define API's

libmakecomat_api = {
    'makecomat1D': (None,
                    [array_1d_int,
                     array_1d_int,
                     c_int,
                     array_1d_int,
                     c_int,
                     array_2d_int],
    ),
    'makecomat2D': (None,
                    [array_2d_int, array_2d_int,
                     c_int, c_int,
                     array_1d_int,
                     c_int,
                     array_2d_int],
    ),
    'makecomat3D': (None,
                    [array_3d_int, array_3d_int,
                     c_int, c_int, c_int,
                     array_1d_int,
                     c_int,
                     array_2d_int],
    ),
    'makecomat4D': (None,
                    [array_4d_int, array_4d_int,
                     c_int, c_int, c_int, c_int,
                     array_1d_int,
                     c_int,
                     array_2d_int],
    ),
    'makecomat1D_2T': (None,
                       [array_1d_int, array_1d_int,
                        c_int,
                        array_1d_int, array_1d_int,
                        c_int,
                        array_1d_int,
                        c_int, c_int,
                        array_2d_int],
    ),
    'makecomat2D_2T': (None,
                       [array_2d_int, array_2d_int,
                        c_int, c_int,
                        array_2d_int, array_2d_int,
                        c_int, c_int,
                        array_1d_int,
                        c_int, c_int,
                        array_2d_int],
    ),
    'makecomat3D_2T': (None,
                       [array_3d_int, array_3d_int,
                        c_int, c_int, c_int,
                        array_3d_int, array_3d_int,
                        c_int, c_int, c_int,
                        array_1d_int,
                        c_int, c_int,
                        array_2d_int],
    ),
    'makecomat4D_2T': (None,
                       [array_4d_int, array_4d_int,
                        c_int, c_int, c_int, c_int,
                        array_4d_int, array_4d_int,
                        c_int, c_int, c_int, c_int,
                        array_1d_int,
                        c_int, c_int,
                        array_2d_int],
    )
}


def register_api(lib, api):
    for f, (restype, argtypes) in api.items():
        func = getattr(lib, f)
        func.restype = restype
        func.argtypes = argtypes


register_api(_comat, libmakecomat_api)


# "Overload" co-occurence matrix calculators
def comat_mult(image, mask, coordset, levels=255):
    """
    Generates and sums co-occurrence histograms of an image given a
    set of offsets.

    Parameters
    ----------
        image: 1-4 dimensional ndarray of dtype int
            Input image.
        mask:  1-4 dimensional ndarray of dtype int
            Input mask (same size as image, 0,1 array)
            Determines which voxels to use for building
            co-occurence matrix
        coordset : 1D ndarray of coordinate offset sets
            array of coordinate offset arrays with the appropriate
            number of dimensions (1-4) for building cooccurence matrices.
        levels : int
            The input image should contain integers in [0, levels-1],
            where levels indicate the number of discrete image or
            grey levels counted (256 for an 8-bit image but any number
            of cluster values for general templated images)
    Returns
    -------
        P : 2-dimensional ndarray
           The summed grey-level co-occurrence histogram. The value
           P[i,j] is the number of times that gray-level j
           occurs at offset coords from gray-level i summed over
           all offsets passed to comat_mult.

    """
    count = 0
    for co in coordset:
        if count == 0:
            thisco = comat(image, mask, co, levels)
        else:
            thisco += comat(image, mask, co, levels)
        count += 1
    return thisco


def comat(image, mask, coords, levels=255):
    """
    Calculates the co-occurrence histogram of an image given an offset.

    Parameters
    ----------
        image: 1-4 dimensional ndarray of dtype int
            Input image.
        mask:  1-4 dimensional ndarray of dtype int
            Input mask (same size as image, 0,1 array)
            Determines which voxels to use for building
            co-occurence matrix
        coords : 1D ndarray
            coordinate offset array with the appropriate number of
            dimensions (1-4) for building cooccurence matrix.
        levels : int
            The input image should contain integers in [0, levels-1],
            where levels indicate the number of discrete image or
            grey levels counted (256 for an 8-bit image but any number
            of cluster values for general templated images)
    Returns
    -------
        P : 2-dimensional ndarray
           The grey-level co-occurrence histogram. The value
           P[i,j] is the number of times that gray-level j
           occurs at offset coords from gray-level i.

    """
    dims = len(image.shape)
    out = np.zeros((levels, levels), dtype=c_int)

    if dims == 1:
        assert image.ndim == 1
        assert image.min() >= 0
        assert image.max() < levels
        assert mask.ndim == 1
        image = image.astype(c_int)
        mask = mask.astype(c_int)
        coords = np.asarray(coords, dtype=c_int)
        assert len(coords) == 1
        _comat.makecomat1D(image, mask,
                           image.shape[0],
                           coords,
                           levels, out)
    if dims == 2:
        assert image.ndim == 2
        assert image.min() >= 0
        assert image.max() < levels
        assert mask.ndim == 2
        image = image.astype(c_int)
        mask = mask.astype(c_int)
        coords = np.asarray(coords, dtype=c_int)
        assert len(coords) == 2
        _comat.makecomat2D(image, mask,
                           image.shape[0],
                           image.shape[1],
                           coords,
                           levels, out)
    if dims == 3:
        assert image.ndim == 3
        assert image.min() >= 0
        assert image.max() < levels
        assert mask.ndim == 3
        image = image.astype(c_int)
        mask = mask.astype(c_int)
        coords = np.asarray(coords, dtype=c_int)
        assert len(coords) == 3
        _comat.makecomat3D(image, mask,
                           image.shape[0],
                           image.shape[1],
                           image.shape[2],
                           coords,
                           levels, out)
    if dims == 4:
        assert image.ndim == 4
        assert image.min() >= 0
        assert image.max() < levels
        assert mask.ndim == 4
        image = image.astype(c_int)
        mask = mask.astype(c_int)
        coords = np.asarray(coords, dtype=c_int)
        assert len(coords) == 4
        _comat.makecomat4D(image, mask,
                           image.shape[0],
                           image.shape[1],
                           image.shape[2],
                           image.shape[3],
                           coords,
                           levels, out)
    return out


# "Overload" 2 image co-occurence matrix calculators
def comat_2T_mult(image1, mask1, image2, mask2, coordset, levels1=255, levels2=255):
    """
    Generates and sums co-occurrence histograms from 2 images given a
    set of offsets.

    Parameters
    ----------
        image1: 1-4 dimensional ndarray of dtype int
            Input image 1.
        mask1:  1-4 dimensional ndarray of dtype int
            Input mask 1 (same size as image, 0,1 array)
            Determines which voxels to use for building
            co-occurence matrix
        image2: 1-4 dimensional ndarray of dtype int
            Input image 2.
        mask2:  1-4 dimensional ndarray of dtype int
            Input mask 2 (same size as image, 0,1 array)            
        coordset : 1D ndarray of coordinate offset sets
            Array of coordinate offset arrays with the appropriate
            number of dimensions (1-4) for building cooccurence matrices.
        levels1 : int
        levels2 : int
            The input images should contain integers in [0, levels(1,2)-1],
            where levels indicate the number of discrete image or
            grey levels counted (256 for an 8-bit image but any number
            of cluster values for general templated images)
    Returns
    -------
        P : 2-dimensional ndarray
           The grey-level co-occurrence histogram. The value
           P[i,j] is the number of times that gray-level j
           occurs at offset coords from gray-level i.

    """
    count = 0
    for co in coordset:
        if count == 0:
            thisco = comat_2T(image1, mask1, image2, mask2, co, levels1, levels2)
        else:
            thisco += comat_2T(image1, mask1, image2, mask2, co, levels1, levels2)
        count += 1
    return thisco


def comat_2T(image1, mask1, image2, mask2, coords, levels1=255, levels2=255):
    """
    Calculate the co-occurrence histogram from 2 images given an offset.

    Parameters
    ----------
        image1: 1-4 dimensional ndarray of dtype int
            Input image 1.
        mask1:  1-4 dimensional ndarray of dtype int
            Input mask 1 (same size as image, 0,1 array)
            Determines which voxels to use for building
            co-occurence matrix
        image2: 1-4 dimensional ndarray of dtype int
            Input image 2.
        mask2:  1-4 dimensional ndarray of dtype int
            Input mask 2 (same size as image, 0,1 array)            
        coords : 1D ndarray
            coordinate offset array with the appropriate number of
            dimensions (1-4) for building cooccurence matrix.
        levels1 : int
        levels2 : int
            The input images should contain integers in [0, levels(1,2)-1],
            where levels indicate the number of discrete image or
            grey levels counted (256 for an 8-bit image but any number
            of cluster values for general templated images)
    Returns
    -------
        P : 2-dimensional ndarray
           The grey-level co-occurrence histogram. The value
           P[i,j] is the number of times that gray-level j
           occurs at offset coords from gray-level i.

    """
    dims = len(image1.shape)
    out = np.zeros((levels1, levels2), dtype=c_int)
    if dims == 1:
        assert image1.ndim == 1
        assert image1.min() >= 0
        assert image1.max() < levels1
        assert mask1.ndim == 1
        assert image2.ndim == 1
        assert image2.min() >= 0
        assert image2.max() < levels2
        assert mask2.ndim == 1
        image1 = image1.astype(c_int)
        mask1 = mask1.astype(c_int)
        image2 = image2.astype(c_int)
        mask2 = mask2.astype(c_int)
        coords = np.asarray(coords, dtype=c_int)
        assert len(coords) == 1
        _comat.makecomat1D_2T(image1, mask1,
                              image1.shape[0],
                              image2, mask2,
                              image2.shape[0],
                              coords,
                              levels1, levels2,
                              out)
    if dims == 2:
        assert image1.ndim == 2
        assert image1.min() >= 0
        assert image1.max() < levels1
        assert mask1.ndim == 2
        assert image2.ndim == 2
        assert image2.min() >= 0
        assert image2.max() < levels2
        assert mask2.ndim == 2
        image1 = image1.astype(c_int)
        mask1 = mask1.astype(c_int)
        image2 = image2.astype(c_int)
        mask2 = mask2.astype(c_int)
        coords = np.asarray(coords, dtype=c_int)
        assert len(coords) == 2
        _comat.makecomat2D_2T(image1, mask1,
                              image1.shape[0],
                              image1.shape[1],
                              image2, mask2,
                              image2.shape[0],
                              image2.shape[1],
                              coords,
                              levels1, levels2,
                              out)
    if dims == 3:
        assert image1.ndim == 3
        assert image1.min() >= 0
        assert image1.max() < levels1
        assert mask1.ndim == 3
        assert image2.ndim == 3
        assert image2.min() >= 0
        assert image2.max() < levels2
        assert mask2.ndim == 3
        image1 = image1.astype(c_int)
        mask1 = mask1.astype(c_int)
        image2 = image2.astype(c_int)
        mask2 = mask2.astype(c_int)
        coords = np.asarray(coords, dtype=c_int)
        assert len(coords) == 3
        _comat.makecomat3D_2T(image1, mask1,
                              image1.shape[0],
                              image1.shape[1],
                              image1.shape[2],
                              image2, mask2,
                              image2.shape[0],
                              image2.shape[1],
                              image2.shape[2],
                              coords,
                              levels1, levels2,
                              out)
    if dims == 4:
        assert image1.ndim == 4
        assert image1.min() >= 0
        assert image1.max() < levels1
        assert mask1.ndim == 4
        assert image2.ndim == 4
        assert image2.min() >= 0
        assert image2.max() < levels2
        assert mask2.ndim == 4
        image1 = image1.astype(c_int)
        mask1 = mask1.astype(c_int)
        image2 = image2.astype(c_int)
        mask2 = mask2.astype(c_int)
        coords = np.asarray(coords, dtype=c_int)
        assert len(coords) == 4
        _comat.makecomat4D_2T(image1, mask1,
                              image1.shape[0],
                              image1.shape[1],
                              image1.shape[2],
                              image1.shape[3],
                              image2, mask2,
                              image2.shape[0],
                              image2.shape[1],
                              image2.shape[2],
                              image2.shape[3],
                              coords,
                              levels1, levels2,
                              out)

    return out


def cmad(images, masks, distance, angles, levels):
    """
    Uses the comat or comat_2T functions to generate co-occurence
    matrices at the specified anlge(s) and distance(s) provided, 
    which is more in the spirit of the original Haralick papers
    on texture analysis. So far this only makes sense for 2 and 3
    dimensions (well 4 might make sense but...)

    Parameters
    ----------
        images: 1 or 2 element 1d python array of 1-4 dimensional ndarray(s)
                of dtype int consisting of an input image(s).
        masks:  1 or 2 element 1d python array of 1-4 dimensional ndarray(s)
                of dtype int consisting of an input mask(s).Determines
                which voxels to use for building co-occurence matrix
        distance: float
            distance in image to use as offset for calculating
            co-occurrence matrix
        angles: float
            1 or 2 element 1d python array of angle(s) to use for
            direction to voxel in calculating co-occurrence matrix.
            For 2D images the only angle, angles[0], corresponds
            to the standard angle from the x-axis in polar co-ordinates.
            For 3D images, angles[0] corresponds to the angle theta in
            spherical co-ordinates, i.e. the angle from the z-axis, and
            angles[1] corresponds to phi, i.e. the angle in the x-y plane. 
        levels : int
            1 or 2 element 1d python array with number of discrete
            levels in the image(s) (256 for an 8-bit image but any number
            of cluster values for general templated images)
    Returns
    -------
        P : 2-dimensional ndarray
           The grey-level co-occurrence histogram. The value
           P[i,j] is the number of times that gray-level j
           occurs at the offset specified by distance and thetas,
           from gray-level i.
    """
    # Calculate integer offsets
    # 2D - angles[0] is traditionally labeled theta
    # 3D - angles[0] is traditionally labeled theta (from z-axis)
    # angles[1] is traditionally labeled phi (in x-y plane)
    angs = len(angles)
    if angs == 1:  # 2D
        assert len(images[0].shape) == 2  # Expect 2 dimensional array(s)
        xc = int(np.floor(np.cos(angles[0]) * distance + 0.5))
        yc = int(np.floor(np.sin(angles[0]) * distance + 0.5))
        coords = [xc, yc]
    if angs == 2:  # 3D
        assert len(images[0].shape) == 3  # Expect 3 dimensional array(s)
        xc = int(np.floor(np.sin(angles[0]) * np.cos(angles[1]) * distance + 0.5))
        yc = int(np.floor(np.sin(angles[0]) * np.sin(angles[1]) * distance + 0.5))
        zc = int(np.floor(np.cos(angles[0]) * distance + 0.5))
        coords = [xc, yc, zc]
    if angs > 3:
        print("cmad can't handle dimensions greater than 3 yet...")
        sys.exit(-1)
    tempnum = len(images)  # Can only have 1 or 2 images/masks
    assert tempnum >= 1
    assert tempnum < 3
    if tempnum == 1:
        out = comat(images[0], masks[0], coords, levels=levels[0])
    if tempnum == 2:
        assert len(levels) == 2
        out = comat_2T(images[0], masks[0], images[1], masks[1], coords, levels1=levels[0], levels2=levels[1])

    return out
