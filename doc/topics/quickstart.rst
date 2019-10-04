Quickstart
==========

Installation
------------

.. code-block:: python

    pip install gentex


Getting started
---------------

Here is a dummy example:

First, we create some dummy ndarray (but could be any nd dataset, from
an image for example) and a mask.

.. code-block:: python

    import numpy as np
    import gentex

    C = np.random.randint(3, size=[5, 5, 5])
    maskC = np.ones([5, 5, 5])

Then, we compute the GLCM from this array along 2 different offsets

.. code-block:: python

    offset3 = [[1, 1, 1], [-1, -1, -1]]
    cm = gentex.comat.comat_mult(C, maskC, offset3, levels=3)

GenTex supports many different type of offsets (rect, conic, angle,
distance, etc.). Refer to :code:`gentex.template` for the one available.

Finally, we get a sample of possible statistics extracted from the GLCM

.. code-block:: python

    texm = ['CM Entropy',
            'EM Entropy',
            'Statistical Complexity',
            'Energy Uniformity',
            'Maximum Probability']
    mytex = gentex.texmeas.Texmeas(cm)
    for meas in texm:
        mytex.calc_measure(meas)
        print(f'{meas} = {mytex.val}')

    CM Entropy = 3.129436250609541
    EM Entropy = 1.5849625007211563
    Statistical Complexity = 1.584962500721156
    Energy Uniformity = 0.117431640625
    Maximum Probability = 0.1484375

Refer to :code:`gentex.texmeas` for the measures available.