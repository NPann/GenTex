"""
Simple script for testing and demonstrating GenTex functionality.
"""

import numpy as np
from scipy import misc
import gentex


def test_cooccurrence_1d():
    print("Co-occurrence 1D... ", end="")

    # Generate test data
    A = np.random.randint(3, size=[100])

    # Generate mask
    maskA = np.ones([100])

    # Offsets
    offset1 = [10]

    # Building co-occurrence matrix
    gentex.comat.comat(A, maskA, offset1, levels=3)

    # Building co-occurrence matrix from 2 images
    gentex.comat.comat_2T(A, maskA, A, maskA, offset1, levels1=3, levels2=3)

    print("DONE")


def test_cooccurrence_2d():
    print("Co-occurrence 2D... ", end="")

    # Generate test data
    B = np.random.randint(3, size=[10, 10])

    # Generate mask
    maskB = np.ones([10, 10])

    # Offsets
    offset2 = [0, 1]

    gentex.comat.comat(B, maskB, offset2, levels=3)

    gentex.comat.cmad([B], [maskB], 2.0, [np.pi / 4], [3])

    gentex.comat.comat_2T(B, maskB, B, maskB, offset2, levels1=3, levels2=3)

    gentex.comat.cmad([B, B], [maskB, maskB], 2.0, [np.pi / 4], [3, 3])

    print("DONE")


def test_cooccurrence_3d():
    print("Co-occurrence 3D... ", end="")

    C = np.random.randint(3, size=[5, 5, 5])

    maskC = np.ones([5, 5, 5])

    offset3 = [1, 1, 1]

    gentex.comat.comat(C, maskC, offset3, levels=3)

    gentex.comat.cmad([C], [maskC], 2.0, [np.pi / 4, np.pi / 4], [3])

    gentex.comat.comat_2T(C, maskC, C, maskC, offset3, levels1=3, levels2=3)

    gentex.comat.cmad([C, C], [maskC, maskC], 2.0, [np.pi / 4, np.pi / 4], [3, 3])

    print("DONE")


def test_cooccurrence_4d():
    print("Co-occurrence 4D... ", end="")

    D = np.random.randint(3, size=[3, 3, 3, 3])

    maskD = np.ones([3, 3, 3, 3])

    offset4 = [0, 0, 0, 1]

    gentex.comat.comat(D, maskD, offset4, levels=3)

    gentex.comat.comat_2T(D, maskD, D, maskD, offset4, levels1=3, levels2=3)

    print("DONE")


def test_cooccurrence_mult():
    print("Co-occurrence with multiple offsets... ", end="")

    # Generate test data
    B = np.random.randint(3, size=[10, 10])

    # Generate mask
    maskB = np.ones([10, 10])

    # Offsets
    offset2 = [[0, 1], [1, 1]]

    gentex.comat.comat_mult(B, maskB, offset2, levels=3)

    gentex.comat.comat_2T_mult(B, maskB, B, maskB, offset2, levels1=3, levels2=3)

    print("DONE")


def test_cluster_features():

    print("Clustering... ", end='')

    # Load test data
    im = misc.imread('test_image.png')
    B = [im]

    # Generate mask
    maskB = np.ones(B[0].shape)

    # Offsets
    offset2 = [[0, 1], [1, 1]]

    # Construct features space
    fe = gentex.features.Features(B, maskB, offset2)

    # Cluster space
    fe.clusfs(numclus=4)

    print("DONE")


def test_texture_measure():
    print("Texture measure... ", end='')

    # Complexity/Texture measures to compute
    texm = ['CM Entropy',
            'EM Entropy',
            'Statistical Complexity',
            'Energy Uniformity',
            'Maximum Probability',
            'Contrast',
            'Inverse Difference Moment',
            'Correlation',
            'Probability of Run Length',
            'Epsilon Machine Run Length',
            'Run Length Asymmetry',
            'Homogeneity',
            'Cluster Tendency',
            'Multifractal Spectrum Energy Range',
            'Multifractal Spectrum Entropy Range']

    # Load image
    im = misc.imread('test_image.png')

    # Make mask - use threshold re. adding gm + wm + csf
    mask = np.where(im >= 0, 1, 0)

    # Make a cumulative co-occurrence array using a template consisting of a box surrounding the voxel
    # Same as explicit form: box_indices = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    box_indices = gentex.template.Template("RectBox", [3, 3, 3], 2, False).offsets

    # Cluster image in bins/levels (i.e data quantization)
    levels = 4
    fe = gentex.features.Features([im], mask, box_indices)
    fe.clusfs(numclus=levels)

    # Build cooccurrence matrix
    comat = gentex.comat.comat_mult(fe.clusim, mask, box_indices, levels=levels)

    # Compute texture measures
    mytex = gentex.texmeas.Texmeas(comat)

    # Add complexty/texture parameters to compute specific measures (can also be defined when constructing
    # an instance of Texmeas)
    # Coordinate moment for "Contrast" and "Inverse Difference Moment"
    mytex.coordmom = 2
    # Probability moment for "Contrast" and "Inverse Difference Moment"
    mytex.probmom = 2
    # Cluster moment for "Cluster Tendency"
    mytex.clusmom = 2
    # Run length for "Probability of Run Length", "Epsilon Machine Run Length" and "Run Length Asymetry"
    mytex.rllen = 0.1

    print("DONE")
    for meas in texm:
        mytex.calc_measure(meas)
        print('\t', meas, '= ', mytex.val)


if __name__ == '__main__':
    print("TEST...")

    test_cooccurrence_1d()

    test_cooccurrence_2d()

    test_cooccurrence_3d()

    test_cooccurrence_4d()

    test_cooccurrence_mult()

    test_cluster_features()

    test_texture_measure()

    print("PASS")
