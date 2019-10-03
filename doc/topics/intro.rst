Introduction
============

GenTex stands for General Texture analysis.

This package provides a suite of routines that combines standard texture analysis methods
based on GLC and entropy/statistical complexity analysis methods.

What is this package for?
==========================

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