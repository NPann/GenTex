"""
Simple test function that test simple functionality of GenTex.
"""

import numpy as np
import gentex


def test_cooccurence_1D():
    print("Cooccurence 1D... ", end="")
    A = np.random.randint(3, size=[100])
    maskA = np.ones([100])
    offset1 = [10]
    gentex.comat.comat(A, maskA, offset1, levels=3)
    gentex.comat.comat_2T(A, maskA, A, maskA, offset1, levels1=3, levels2=3)
    print("DONE")


def test_cooccurence_2D():
    print("Cooccurence 2D... ", end="")
    B = np.random.randint(3, size=[10, 10])
    maskB = np.ones([10, 10])
    offset2 = [1, 1]

    gentex.comat.comat(B, maskB, offset2, levels=3)

    gentex.comat.cmad([B], [maskB], 2.0, [np.pi / 4], [3])

    gentex.comat.comat_2T(B, maskB, B, maskB, offset2, levels1=3, levels2=3)

    gentex.comat.cmad([B, B], [maskB, maskB], 2.0, [np.pi / 4], [3, 3])
    print("DONE")


def test_cooccurence_3D():
    print("Cooccurence 3D... ", end="")

    C = np.random.randint(3, size=[5, 5, 5])
    maskC = np.ones([5, 5, 5])
    offset3 = [1, 1, 1]

    gentex.comat.comat(C, maskC, offset3, levels=3)

    gentex.comat.cmad([C], [maskC], 2.0, [np.pi / 4, np.pi / 4], [3])

    gentex.comat.comat_2T(C, maskC, C, maskC, offset3, levels1=3, levels2=3)

    gentex.comat.cmad([C, C], [maskC, maskC], 2.0, [np.pi / 4, np.pi / 4], [3, 3])
    print("DONE")


def test_cooccurence_4D():
    print("Cooccurence 4D... ", end="")

    D = np.random.randint(3, size=[3, 3, 3, 3])
    maskD = np.ones([3, 3, 3, 3])
    offset4 = [0, 0, 0, 1]

    gentex.comat.comat(D, maskD, offset4, levels=3)

    gentex.comat.comat_2T(D, maskD, D, maskD, offset4, levels1=3, levels2=3)
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
           'Run Length Asymetry',
           'Homogeneity',
           'Cluster Tendency',
           'Multifractal Spectrum Energy Range',
           'Multifractal Spectrum Entropy Range'
           ]

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


if __name__ == '__main__':
    print("TEST...")
    test_cooccurence_1D()
    test_cooccurence_2D()
    test_cooccurence_3D()
    test_cooccurence_4D()
    test_features_measure()

    print("PASS")
