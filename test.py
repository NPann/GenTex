"""
Simple script for testing and demonstrating GenTex functionality.
"""

import numpy as np
import gentex


def test_cooccurence_1d():
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


def test_cooccurence_2d():
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


def test_cooccurence_3d():
    print("Co-occurrence 3D... ", end="")

    C = np.random.randint(3, size=[5, 5, 5])

    maskC = np.ones([5, 5, 5])

    offset3 = [1, 1, 1]

    gentex.comat.comat(C, maskC, offset3, levels=3)

    gentex.comat.cmad([C], [maskC], 2.0, [np.pi / 4, np.pi / 4], [3])

    gentex.comat.comat_2T(C, maskC, C, maskC, offset3, levels1=3, levels2=3)

    gentex.comat.cmad([C, C], [maskC, maskC], 2.0, [np.pi / 4, np.pi / 4], [3, 3])

    print("DONE")


def test_cooccurence_4d():
    print("Co-occurrence 4D... ", end="")

    D = np.random.randint(3, size=[3, 3, 3, 3])

    maskD = np.ones([3, 3, 3, 3])

    offset4 = [0, 0, 0, 1]

    gentex.comat.comat(D, maskD, offset4, levels=3)

    gentex.comat.comat_2T(D, maskD, D, maskD, offset4, levels1=3, levels2=3)

    print("DONE")


def test_cooccurence_mult():
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


def test_features_measure():
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

    # Random image
    im = np.random.randint(3, size=[40, 40])

    # Make mask - use threshold re. adding gm + wm + csf
    mask = np.where(im >= 0, 1, 0)

    # Make a cumulative co-occurrence array using a template consisting of a box surrounding the voxel
    # Same as explicit form: box_indices = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    box_indices = gentex.template.Template("RectBox", [3, 3, 3], 2, False).offsets

    # Build cooccurence matrix
    comat = gentex.comat.comat_mult(im, mask, box_indices, levels=3)

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


def test_cluster_features():

    print("Clustering... ", end='')
    # Generate test data (low resolution Shepp-Logan phantom)
    B = [np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 5, 6, 12, 12, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 12, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9,
          4, 7, 15, 1, 1, 1, 1, 1, 1, 9, 8, 4, 4, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 4, 4,
          2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 10, 4, 3, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 17, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 4, 3, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 4, 6, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 4, 3,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 10, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 4,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 14, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 8, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 18,
          4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 4, 1, 1, 1, 1, 1,
          1, 1, 1, 9, 3, 3, 3, 3, 9, 1, 1, 1, 1, 1, 1, 1, 1,
          7, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 1, 1, 1, 1, 1,
          1, 1, 9, 3, 3, 3, 3, 3, 3, 6, 1, 1, 1, 1, 1, 1, 1,
          3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 9, 1, 1, 1, 1, 1, 1,
          1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1,
          1, 8, 10, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 1, 1, 1, 1, 1, 1,
          1, 5, 3, 3, 3, 3, 3, 3, 3, 3, 10, 1, 1, 1, 1, 1, 1,
          1, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 1, 1, 1, 4, 5, 11,
          1, 7, 3, 3, 3, 3, 3, 3, 3, 3, 8, 1, 1, 1, 1, 1, 1,
          1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 9, 18, 1, 1, 1, 1, 2, 2, 2,
          2, 5, 3, 3, 3, 3, 3, 3, 3, 3, 8, 1, 1, 1, 1, 1, 1,
          1, 1, 8, 18, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 12, 1, 1, 1, 1, 3, 2, 2, 2,
          2, 19, 3, 3, 3, 3, 3, 3, 3, 3, 11, 1, 9, 8, 1, 1, 1,
          1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 1, 1, 1, 1, 2, 2, 2,
          2, 2, 11, 3, 3, 3, 3, 3, 3, 3, 5, 3, 2, 2, 1, 1, 1,
          1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 13, 1, 1, 1, 1, 4, 2, 2, 2,
          2, 2, 14, 5, 3, 3, 3, 3, 3, 5, 6, 2, 2, 2, 3, 1, 1,
          1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 12, 1, 1, 1, 1, 1, 2, 2, 2,
          2, 2, 2, 12, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 3, 1, 1,
          1, 1, 1, 10, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 5, 10, 1, 1, 1, 1, 3, 2, 2, 2,
          2, 2, 2, 2, 7, 17, 17, 5, 1, 8, 2, 2, 2, 2, 1, 1, 1,
          1, 1, 1, 4, 6, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 6, 4, 1, 1, 1, 1, 1, 2, 2, 2,
          2, 2, 2, 2, 7, 12, 10, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1,
          1, 1, 1, 3, 9, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 6, 3, 1, 1, 1, 1, 1, 3, 2, 2,
          2, 2, 2, 2, 2, 1, 1, 1, 13, 2, 2, 2, 2, 3, 1, 1, 1,
          1, 1, 1, 1, 10, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 6, 3, 1, 1, 1, 1, 1, 7, 2, 2,
          2, 2, 2, 2, 2, 1, 1, 1, 3, 2, 2, 2, 2, 11, 1, 1, 1,
          1, 1, 1, 1, 10, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 6, 3, 1, 1, 1, 1, 1, 3, 2, 2,
          2, 2, 2, 2, 2, 8, 9, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1,
          1, 1, 1, 1, 10, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 5, 4, 1, 1, 1, 1, 1, 1, 3, 2,
          2, 2, 2, 2, 2, 9, 3, 1, 2, 2, 2, 2, 9, 1, 1, 1, 1,
          1, 1, 1, 3, 6, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 10, 1, 1, 1, 1, 1, 1, 9, 2,
          2, 2, 2, 2, 2, 12, 1, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1,
          1, 1, 1, 4, 10, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 12, 1, 1, 1, 1, 1, 1, 1, 2,
          2, 2, 2, 2, 2, 7, 1, 3, 2, 2, 2, 8, 1, 1, 1, 1, 1,
          1, 1, 1, 15, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 16, 1, 1, 1, 1, 1, 1, 1, 10,
          2, 2, 2, 2, 2, 6, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 10, 1, 1, 1, 1, 1, 1, 1, 1,
          9, 2, 2, 2, 2, 10, 1, 1, 9, 6, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 9, 3, 1, 1, 1, 1, 1, 1, 1,
          1, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 6, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 10, 2, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 15, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 7, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 2, 7, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 8, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          3, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1,
          1, 1, 1, 10, 5, 7, 6, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 9, 1, 1, 1, 1, 1, 1, 1, 1, 16,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 20, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 21,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 12, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 12, 1, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 10, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 15, 3, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
          8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 4, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          16, 4, 12, 4, 1, 1, 1, 1, 4, 15, 4, 4, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 13, 13, 4, 4, 12, 5, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])]

    # Generate mask
    maskB = np.ones(B[0].shape)

    # Offsets
    offset2 = [[0, 1], [1, 1]]

    # Construct features space
    fe = gentex.features.Features(B, maskB, offset2)

    # Cluster space
    fe.clusfs(numclus=5)

    print("DONE")


if __name__ == '__main__':
    print("TEST...")

    test_cooccurence_1d()

    test_cooccurence_2d()

    test_cooccurence_3d()

    test_cooccurence_4d()

    test_cooccurence_mult()

    test_features_measure()

    test_cluster_features()

    print("PASS")
