import math
from pytest import approx

from .. import get_right_endpoint_cico
from .cases_func import *


# cases
f_1p = lambda x: 5.0 + (x[0] - 3.0) ** 2  # [100., missing, missing, missing]

f_2p_1im = lambda x: 5.0 + (x[0] - 3.0) ** 2 + 0.0 * x[1]  # [3., missing, missing, missing]

f_2p = lambda x: 5.0 + (x[0] - 3.0) ** 2 + (x[1] - 4.0) ** 2  # [3., 4., missing, missing]

f_3p_1im = lambda x: 5.0 + (x[0] - 3.0) ** 2 + (x[1] / x[2] - 4.0) ** 2  # [3., missing, missing, missing]

f_3p_1im_dep = lambda x: 5.0 + (x[0] - 3.0) ** 2 + (x[0] - x[1] - 1.0) ** 2 + 0 * x[2] ** 2

f_4p_2im = lambda x: 5.0 + (x[0] - 3.0) ** 2 + (x[1] - 4.0) ** 2 + 0.0 * x[2] + 0.0 * x[3]  # [3., 4., missing, missing]

f_4p_3im = lambda x: 5.0 + (x[0] - 3.0) ** 2 + (x[1] / x[2] - 4.0) ** 2 + 0.0 * x[3]  # [3., missing, missing, missing]

f_1p_ex = lambda x: 5.0 + (x[0] - 1e-8) ** 2  # [1e-8, missing, missing, missing]

f_5p_3im = lambda x: 5.0 + (x[0] - 3.0) ** 2 + (math.exp(x[1]) - 1.0) ** 2 + (x[2] / x[3] - 4.0) ** 2 + 0.0 * x[4]

f_3p_im = lambda x: 5.0 + (x[0] - 3.0) ** 2 + (math.exp(x[1]) - 1.0) ** 2 + 0.0 * x[2]


def test_f_2p_1im():
    res0 = [get_right_endpoint_cico(
        [3., 1.],
        i,
        lambda x: f_2p_1im(x) - 9
    ) for i in range(2)]
    assert res0[0][0] == approx(5, abs=1e-2)
    assert res0[0][2] == "BORDER_FOUND_BY_SCAN_TOL"
    assert res0[1][2] == "SCAN_BOUND_REACHED"


def test_f_2p_1im_max_iter_5():
    res0 = [get_right_endpoint_cico(
        [3., 1.],
        i,
        lambda x: f_2p_1im(x) - 9,
        max_iter=5
    ) for i in range(2)]
    assert res0[0][0] == None
    assert res0[0][2] == "MAX_ITER_REACHED"
    assert res0[1][0] == None
    assert res0[1][2] == "MAX_ITER_REACHED"


def test_f_2p():
    res0 = [get_right_endpoint_cico(
        [3., 1.1],
        i,
        lambda x: f_2p(x) - 9,
        scan_tol=1e-6
    ) for i in range(2)]

    assert res0[0][0] == approx(5, abs=1e-6)
    assert res0[0][2] == "BORDER_FOUND_BY_SCAN_TOL"
    assert res0[1][0] == approx(6, abs=1e-6)
    assert res0[1][2] == "BORDER_FOUND_BY_SCAN_TOL"


def test_f_3p_1im():
    res0 = [get_right_endpoint_cico(
        [3., 8., 2.1],
        i,
        lambda x: f_3p_1im(x) - 9
    ) for i in range(3)]

    assert res0[0][0] == approx(5, abs=1e-2)
    assert res0[0][2] == "BORDER_FOUND_BY_SCAN_TOL"
    assert res0[1][2] == "SCAN_BOUND_REACHED"
    assert res0[2][2] == "SCAN_BOUND_REACHED"


def test_f_3p_1im_restricted():
    res0 = [get_right_endpoint_cico(
        [3, 8, 2.1],
        i,
        lambda x: f_3p_1im(x) - 9,
        scan_bound=4
    ) for i in range(3)]

    assert res0[0][2] == "SCAN_BOUND_REACHED"
    assert res0[1][2] == "SCAN_BOUND_REACHED"
    assert res0[2][2] == "SCAN_BOUND_REACHED"


def test_f_3p_1im_dep():
    res0 = [get_right_endpoint_cico(
        [3, 2, 2.1],
        i,
        lambda x: f_3p_1im_dep(x) - 9
    ) for i in range(3)]
    assert res0[0][0] == approx(5, abs=1e-2)
    assert res0[0][2] == "BORDER_FOUND_BY_SCAN_TOL"
    assert res0[1][0] == approx(2.0 + 2.0 * math.sqrt(2), abs=1e-2)
    assert res0[1][2] == "BORDER_FOUND_BY_SCAN_TOL"
    assert res0[2][2] == "SCAN_BOUND_REACHED"


def test_f_3p_1im_dep_scan_bound():
    res0 = [get_right_endpoint_cico(
        [3, 2, 2.1],
        i,
        lambda x: f_3p_1im_dep(x) - 9,
        scan_bound=[4., 10., 10.][i]
    ) for i in range(3)]

    assert res0[0][2] == "SCAN_BOUND_REACHED"
    assert res0[1][0] == approx(2.0 + 2.0 * math.sqrt(2), abs=1e-2)
    assert res0[1][2] == "BORDER_FOUND_BY_SCAN_TOL"
    assert res0[2][2] == "SCAN_BOUND_REACHED"


def test_f_3p_1im_dep_scan_tol():
    res0 = [get_right_endpoint_cico(
        [3, 2, 2.1],
        0,
        lambda x: f_3p_1im_dep(x) - 9,
        scan_tol=[1e-2, 1e-4, 1e-6][i]
    ) for i in range(3)]
    assert res0[0][0] == approx(5, abs=1e-1)
    assert res0[1][0] == approx(5, abs=1e-3)
    assert res0[2][0] == approx(5, abs=1e-5)


def test_f_4p_2im():
    res0 = [get_right_endpoint_cico(
        [3., 4, 1.1, 10.],
        i,
        lambda x: f_4p_2im(x) - 9
    ) for i in range(4)]
    assert res0[0][0] == approx(5, abs=1e-2)
    assert res0[0][2] == "BORDER_FOUND_BY_SCAN_TOL"
    assert res0[1][0] == approx(6, abs=1e-2)
    assert res0[1][2] == "BORDER_FOUND_BY_SCAN_TOL"
    assert res0[2][2] == "SCAN_BOUND_REACHED"
    assert res0[3][2] == "SCAN_BOUND_REACHED"


def test_f_4p_3im():
    res0 = [get_right_endpoint_cico(
        [3., 4, 1.1, 10.],
        i,
        lambda x: f_4p_3im(x) - 9
    ) for i in range(4)]
    assert res0[0][0] == approx(5, abs=1e-2)
    assert res0[0][2] == "BORDER_FOUND_BY_SCAN_TOL"
    assert res0[1][2] == "SCAN_BOUND_REACHED"
    assert res0[2][2] == "SCAN_BOUND_REACHED"
    assert res0[3][2] == "SCAN_BOUND_REACHED"


def test_f_1p_ex():
    res0 = [get_right_endpoint_cico(
        [1.5],
        i,
        lambda x: f_1p_ex(x) - 9
    ) for i in range(1)]
    assert res0[0][0] == approx(2 + 1e-8, abs=1e-2)
    assert res0[0][2] == "BORDER_FOUND_BY_SCAN_TOL"


def test_f_5p_3im():
    res0 = [get_right_endpoint_cico(
        [3., 0.1, 4, 1.1, 8.],
        i,
        lambda x: f_5p_3im(x) - 9
    ) for i in range(5)]
    assert res0[0][0] == approx(5, abs=1e-2)
    assert res0[0][2] == "BORDER_FOUND_BY_SCAN_TOL"
    assert res0[1][0] == approx(math.log(3), abs=1e-2)
    assert res0[1][2] == "BORDER_FOUND_BY_SCAN_TOL"
    assert res0[2][2] == "SCAN_BOUND_REACHED"
    assert res0[3][2] == "SCAN_BOUND_REACHED"
    assert res0[4][2] == "SCAN_BOUND_REACHED"


def test_f_3p_im():
    res0 = [get_right_endpoint_cico(
        [3., 0.1, 4, 1.1, 8.],
        i,
        lambda x: f_3p_im(x) - 9
    ) for i in range(5)]
    assert res0[0][0] == approx(5, abs=1e-2)
    assert res0[0][2] == "BORDER_FOUND_BY_SCAN_TOL"
    assert res0[1][0] == approx(math.log(3), abs=1e-2)
    assert res0[1][2] == "BORDER_FOUND_BY_SCAN_TOL"
    assert res0[2][2] == "SCAN_BOUND_REACHED"
