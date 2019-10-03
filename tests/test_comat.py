import numpy as np
import gentex

# Generate a few dummy data for test
# 1D
A = np.random.randint(3, size=[100])
maskA = np.ones([100])

# 2D
B = np.random.randint(3, size=[10, 10])
maskB = np.ones([10, 10])

# 3D
C = np.random.randint(3, size=[5, 5, 5])
maskC = np.ones([5, 5, 5])

# 4D
D = np.random.randint(3, size=[3, 3, 3, 3])
maskD = np.ones([3, 3, 3, 3])


def test_cooccurrence_1d():
    offset1 = [10]
    cm = gentex.comat.comat(A, maskA, offset1, levels=3)
    assert cm.shape == (3, 3)


def test_cooccurrence_1d_between_2_images():
    offset1 = [10]
    cm = gentex.comat.comat_2T(A, maskA, A, maskA, offset1, levels1=3, levels2=3)
    assert cm.shape == (3, 3)


def test_cooccurrence_2d():
    offset2 = [0, 1]
    cm = gentex.comat.comat(B, maskB, offset2, levels=3)
    assert cm.shape == (3, 3)


def test_cooccurrence_2d_at_angle_and_distance():
    cm = gentex.comat.cmad([B], [maskB], 2.0, [np.pi / 4], [3])
    assert cm.shape == (3, 3)


def test_coorcurrence_2d_between_2_images():
    offset2 = [0, 1]
    cm = gentex.comat.comat_2T(B, maskB, B, maskB, offset2, levels1=3, levels2=3)
    assert cm.shape == (3, 3)


def test_coorcurrence_2d_at_angle_and_distance_between_2_images():
    cm = gentex.comat.cmad([B, B], [maskB, maskB], 2.0, [np.pi / 4], [3, 3])
    assert cm.shape == (3, 3)


def test_cooccurrence_3d():
    offset3 = [1, 1, 1]
    cm = gentex.comat.comat(C, maskC, offset3, levels=3)
    assert cm.shape == (3, 3)


def test_cooccurrence_3d_at_angle_and_distance():
    cm = gentex.comat.cmad([C], [maskC], 2.0, [np.pi / 4, np.pi / 4], [3])
    assert cm.shape == (3, 3)


def test_cooccurrence_3d_between_2_images():
    offset3 = [1, 1, 1]
    cm = gentex.comat.comat_2T(C, maskC, C, maskC, offset3, levels1=3, levels2=3)
    assert cm.shape == (3, 3)


def test_coorcurrence_3d_at_angle_and_distance_between_2_images():
    cm = gentex.comat.cmad([C, C], [maskC, maskC], 2.0, [np.pi / 4, np.pi / 4], [3, 3])
    assert cm.shape == (3, 3)


def test_cooccurrence_4d():
    offset4 = [0, 0, 0, 1]
    cm = gentex.comat.comat(D, maskD, offset4, levels=3)
    assert cm.shape == (3, 3)


def test_cooccurrence_4d_between_2_images():
    offset4 = [0, 0, 0, 1]
    cm = gentex.comat.comat_2T(D, maskD, D, maskD, offset4, levels1=3, levels2=3)
    assert cm.shape == (3, 3)


def test_cooccurrence_with_multiple_offsets():
    offset2 = [[0, 1], [1, 1]]
    cm = gentex.comat.comat_mult(B, maskB, offset2, levels=3)
    assert cm.shape == (3, 3)


def test_cooccurrence_with_multiple_offsets_between_2_images():
    offset2 = [[0, 1], [1, 1]]
    cm = gentex.comat.comat_2T_mult(B, maskB, B, maskB, offset2, levels1=3, levels2=3)
    assert cm.shape == (3, 3)
