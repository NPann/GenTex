import gentex
import numpy as np
import imageio
from PIL import Image
from pathlib import Path

FIXTURE_DIR = Path(__file__).parents[0]/'fixtures'


def test_texture_measure():

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
    im = imageio.imread(FIXTURE_DIR/'test_image.png')

    # Make mask - use threshold re. adding gm + wm + csf
    mask = np.where(im > 0, 1, 0)

    # Make a cumulative co-occurrence array using a template consisting of a box surrounding the voxel
    # Same as explicit form: box_indices = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    box_indices = gentex.template.Template("RectBox", [7, 7, 7], 2, False).offsets

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

    for meas in texm:
        mytex.calc_measure(meas)
        print('\t', meas, '= ', mytex.val)


def test_texture_measure_voxel_wise():
    # Complexity/Texture measures to compute
    texm = ['CM Entropy']

    # Load image
    im = Image.open(FIXTURE_DIR/'test_image.png')

    # Downsampling for testing
    im = np.asarray(im.resize(tuple(map(lambda x: x//4, im.size))))

    # Make mask - use threshold re. adding gm + wm + csf
    mask2 = np.where(im > 0, 1, 0)
    idx, idy = np.where(mask2 == 1)
    mask1 = np.zeros(im.shape, dtype=int)

    # Initiate texture output
    res = np.zeros(im.shape + (len(texm), ))

    # Make a cumulative co-occurrence array using a template consisting of a box surrounding the voxel
    # Same as explicit form: box_indices = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    box_indices = gentex.template.Template("RectBox", [7, 7, 7], 2, False).offsets

    # Data quantization
    levels = 8
    bins = np.linspace(im.min(), im.max(), levels + 1)
    im_q = np.digitize(im.ravel(), bins).reshape(im.shape) - 1

    for a, b in zip(idx, idy):
        # set voxel of interest to 1
        mask1[a, b] = 1
        # Build co-occurrence matrix
        comat = gentex.comat.comat_2T_mult(im_q, mask1, im_q, mask2, box_indices,
                                           levels1=levels+1, levels2=levels+1)
        # Compute texture measures
        mytex = gentex.texmeas.Texmeas(comat)
        for c, meas in enumerate(texm):
            mytex.calc_measure(meas)
            res[a, b, c] = mytex.val

        # restore mask
        mask1[a, b] = 0
