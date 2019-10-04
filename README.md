[![Documentation Status](https://readthedocs.org/projects/gentex/badge/?version=latest)](https://gentex.readthedocs.io/en/latest/?badge=latest)
[![CircleCI](https://circleci.com/gh/NPann/GenTex.svg?style=svg)](https://circleci.com/gh/NPann/GenTex)

GenTex stands for General Texture analysis.  

This package provides a suite of routines that combines standard texture analysis methods 
based on [GLCM](https://en.wikipedia.org/wiki/Co-occurrence_matrix) 
and entropy/statistical complexity analysis methods.

## What is this package for?

GenTex provides a number of the standard algorithms required for generating 
complexity/texture measure estimates from multimodal imaging data. These include:

1. Generation of multidimensional feature spaces from multimodal 'image' data 
(i.e. multiple 'co-registered' 1,2,3, or 4 dimensional data sets, e.g. 
multiple 'co-registered' time series, multimodal image data, space/time data..) 
via the use of a set of image templates, including:  

    - single voxels
    - linear sequences in cardinal directions (ref.)
    - notches in cardinal directions (ref.)
    - light cones in cardinal directions and 45 degree angles (ref.)

2. Clustering methods for generating discrete ('grey') levels from the constructed 
feature space (the levels are then typically mapped to the original image space at 
the anchor points of the templates)

3. Building co-occurrence matrices from a discrete level 'image' or a pair of 
discrete level 'images', where the discrete level 'images' are typically generated 
via feature space clustering of the original multimodal data sets (time series, images, 
space/time data...)

4. Estimation of various complexity/texture measures from the co-occurrence matrices.
(Haralick measures and epsilon machine related quantities) such as:

    - CM Entropy
    - EM Entropy
    - Statistical Complexity
    - Energy Uniformity
    - Maximum Probability
    - Contrast
    - Inverse Difference Moment
    - Correlation
    - Probability of Run Length
    - Epsilon Machine Run Length
    - Run Length Asymmetry
    - Homogeneity
    - Cluster Tendency
    - Multifractal Spectrum Energy Range
    - Multifractal Spectrum Entropy Range

### Documentation

The documentation on GenTex in hosted [here](https://gentex.readthedocs.io/en/latest/topics/quickstart.html)

### Installation ###

``` bash
pip install gentex
```

### Who do I talk to?

- Karl Young (original developer)
- Nicolas Pannetier 
- Norbert Schuff


### License

GenTex is licensed under the terms of the BSD license.
Please see the License file in the GenTex distribution


### References

* K. Young, Y. Chen, J. Kornak, G. B. Matson, N. Schuff,
'Summarizing complexity in high dimensions',
Phys Rev Lett. (2005) Mar 11;94(9):098701.

* C. R. Shalizi and J. P. Crutchfield, 'Computational
Mechanics: Pattern and Prediction, Structure and Simplicity',
Journal of Statistical Physics 104 (2001) 819--881.

* K. Young and J. P. Crutchfield, 'Fluctuation Spectroscopy',
Chaos, Solitons, and Fractals 4 (1993) 5-39.

* J. P. Crutchfield and K. Young, 'Computation at the
Onset of Chaos', in Entropy, Complexity, and Physics of
Information, W. Zurek, editor, SFI Studies in the Sciences
of Complexity, VIII, Addison-Wesley, Reading, Massachusetts
(1990) 223-269.

* C. R. Shalizi and J. P. Crutchfield, 'Computational
Mechanics: Pattern and Prediction, Structure and Simplicity',
Journal of Statistical Physics 104 (2001) 819--881.