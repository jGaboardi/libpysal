"""
For completeness, we need to test a shuffled dataframe
(i.e. always send unsorted data) with:
- numeric ids
- string ids
- point dataframe
- coordinates
- check two kernel functions
- numba/nonumba
"""

import geodatasets
import geopandas
import numpy as np
import pandas as pd
import pytest
import shapely

from libpysal.graph._kernel import _kernel_functions
from libpysal.graph._triangulation import (
    _delaunay,
    _gabriel,
    _relative_neighborhood,
    _voronoi,
)
from libpysal.graph._utils import CoplanarError
from libpysal.graph.base import Graph


@pytest.fixture(scope="session")
def stores():
    stores = geopandas.read_file(geodatasets.get_path("geoda liquor_stores")).explode(
        index_parts=False
    )
    return stores


@pytest.fixture(scope="session")
def stores_unique(stores):
    stores_unique = stores.drop_duplicates(subset="geometry")
    return stores_unique


kernel_functions = [None] + list(_kernel_functions.keys())


def my_kernel(distances, bandwidth):
    output = np.cos(distances / distances.max())
    output[distances < bandwidth] = 0
    return output


kernel_functions.append(my_kernel)

# optimal, small, and larger than largest distance.
bandwidths = [None, "auto", 0.5]

np.random.seed(6301)
# create a 2-d laplace distribution as a "degenerate"
# over-concentrated distribution
lap_coords = np.random.laplace(size=(5, 2))

# create a 2-d cauchy as a "degenerate"
# spatial outlier-y distribution
cau_coords = np.random.standard_cauchy(size=(5, 2))

parametrize_ids = pytest.mark.parametrize(
    "ids", [None, "id", "placeid"], ids=["no id", "id", "placeid"]
)

parametrize_kernelfunctions = pytest.mark.parametrize(
    "kernel", kernel_functions, ids=kernel_functions[:-2] + ["None", "custom callable"]
)
parametrize_bw = pytest.mark.parametrize(
    "bandwidth", bandwidths, ids=["no bandwidth", "auto", "fixed"]
)
parametrize_constructors = pytest.mark.parametrize(
    "constructor",
    [_delaunay, _gabriel, _relative_neighborhood, _voronoi],
    ids=["delaunay", "gabriel", "relhood", "voronoi"],
)

# @parametrize_constructors
# @parametrize_ids
# @parametrize_kernelfunctions``
# @parametrize_bw
# def test_option_combinations(constructor, ids, kernel, bandwidth):
#     """
#     NOTE: This does not check for the *validity* of the output, just
#     the structure of the output.
#     """
#     heads, tails, weights = constructor(
#         stores_unique,
#         ids=stores_unique[ids] if ids is not None else None,
#         kernel=kernel,
#         bandwidth=bandwidth
#         )
#     assert heads.dtype == tails.dtype
#     assert (
#         heads.dtype == stores_unique.get(ids, stores_unique.index).dtype,
#         'ids failed to propagate'
#     )
#     if kernel is None and bandwidth is None:
#         np.testing.assert_array_equal(weights, np.ones_like(heads))
#     assert (
#         set(zip(heads, tails)) == set(zip(tails, heads)),
#         "all triangulations should be symmetric, this is not"
#     )


def test_correctness_voronoi_clipping():
    noclip = _voronoi(lap_coords, coplanar="raise", clip=None, rook=True)
    extent = _voronoi(lap_coords, coplanar="raise", clip="bounding_box", rook=True)
    alpha = _voronoi(lap_coords, coplanar="raise", clip="alpha_shape", rook=True)

    g_noclip = Graph.from_arrays(*noclip)
    g_extent = Graph.from_arrays(*extent)
    g_alpha = Graph.from_arrays(*alpha)

    assert g_alpha < g_extent
    assert g_extent <= g_noclip

    extent_known = [
        np.array([0, 0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4]),
        np.array([1, 2, 3, 4, 0, 3, 4, 0, 3, 0, 1, 2, 0, 1]),
    ]
    alpha_known = [
        np.array([0, 0, 0, 1, 2, 2, 3, 3, 4, 4]),
        np.array([2, 3, 4, 4, 0, 3, 0, 2, 0, 1]),
    ]

    np.testing.assert_array_equal(
        g_extent.adjacency.index.get_level_values(0), extent_known[0]
    )
    np.testing.assert_array_equal(
        g_extent.adjacency.index.get_level_values(1), extent_known[1]
    )

    np.testing.assert_array_equal(
        g_alpha.adjacency.index.get_level_values(0), alpha_known[0]
    )
    np.testing.assert_array_equal(
        g_alpha.adjacency.index.get_level_values(1), alpha_known[1]
    )


def test_correctness_delaunay():
    head, tail, weight = _delaunay(cau_coords)

    known_head = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4])
    known_tail = np.array([1, 2, 4, 0, 2, 3, 0, 1, 3, 4, 1, 2, 4, 0, 2, 3])

    np.testing.assert_array_equal(known_head, head)
    np.testing.assert_array_equal(known_tail, tail)
    np.testing.assert_array_equal(np.ones(head.shape), weight)

    head, tail, weight = _delaunay(lap_coords)
    known_head = np.array([0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4])
    known_tail = np.array([1, 2, 3, 4, 0, 3, 4, 0, 3, 4, 0, 1, 2, 0, 1, 2])

    np.testing.assert_array_equal(known_head, head)
    np.testing.assert_array_equal(known_tail, tail)
    np.testing.assert_array_equal(np.ones(head.shape), weight)


def test_correctness_voronoi():
    head, tail, weight = _voronoi(cau_coords)

    known_head = np.array([0, 0, 0, 1, 1, 2, 2, 2, 2, 3, 4, 4])
    known_tail = np.array([1, 2, 4, 0, 2, 0, 1, 3, 4, 2, 0, 2])

    np.testing.assert_array_equal(known_head, head)
    np.testing.assert_array_equal(known_tail, tail)
    np.testing.assert_array_equal(np.ones(head.shape), weight)

    head, tail, weight = _voronoi(lap_coords)
    known_head = np.array([0, 0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4])
    known_tail = np.array([1, 2, 3, 4, 0, 3, 4, 0, 3, 0, 1, 2, 0, 1])

    np.testing.assert_array_equal(known_head, head)
    np.testing.assert_array_equal(known_tail, tail)
    np.testing.assert_array_equal(np.ones(head.shape), weight)


def test_correctness_gabriel():
    head, tail, weight = _gabriel(cau_coords)

    known_head = np.array([0, 0, 1, 1, 2, 2, 2, 3, 4, 4])
    known_tail = np.array([1, 4, 0, 2, 1, 3, 4, 2, 0, 2])

    np.testing.assert_array_equal(known_head, head)
    np.testing.assert_array_equal(known_tail, tail)
    np.testing.assert_array_equal(np.ones(head.shape), weight)

    head, tail, weight = _gabriel(lap_coords)
    known_head = np.array([0, 0, 0, 1, 2, 2, 3, 3, 4, 4])
    known_tail = np.array([2, 3, 4, 4, 0, 3, 0, 2, 0, 1])

    np.testing.assert_array_equal(known_head, head)
    np.testing.assert_array_equal(known_tail, tail)
    np.testing.assert_array_equal(np.ones(head.shape), weight)


def test_correctness_relative_n():
    head, tail, weight = _relative_neighborhood(cau_coords)

    known_head = np.array([0, 1, 2, 2, 2, 3, 4, 4])
    known_tail = np.array([4, 2, 1, 3, 4, 2, 0, 2])

    np.testing.assert_array_equal(known_head, head)
    np.testing.assert_array_equal(known_tail, tail)
    np.testing.assert_array_equal(np.ones(head.shape), weight)

    head, tail, weight = _relative_neighborhood(lap_coords)
    known_head = np.array([0, 0, 1, 2, 2, 3, 4, 4])
    known_tail = np.array([2, 4, 4, 0, 3, 2, 0, 1])

    np.testing.assert_array_equal(known_head, head)
    np.testing.assert_array_equal(known_tail, tail)
    np.testing.assert_array_equal(np.ones(head.shape), weight)


@pytest.mark.network
@parametrize_ids
def test_ids(ids, stores_unique):
    data = stores_unique.sample(frac=1)
    if ids is not None:
        data = data.set_index(ids)
    head, tail, weight = _delaunay(data)

    assert head.shape[0] == 3368
    assert tail.shape == head.shape
    assert weight.shape == head.shape
    np.testing.assert_array_equal(pd.unique(head), data.index)

    head, tail, weight = _voronoi(data)

    assert head.shape[0] == 3308
    assert tail.shape == head.shape
    assert weight.shape == head.shape
    np.testing.assert_array_equal(pd.unique(head), data.index)

    head, tail, weight = _gabriel(data)

    assert head.shape[0] == 2024
    assert tail.shape == head.shape
    assert weight.shape == head.shape
    np.testing.assert_array_equal(pd.unique(head), data.index)

    head, tail, weight = _relative_neighborhood(data)

    # assert head.shape[0] == 3346  # relativehood returns unstable results atm see #573
    assert tail.shape == head.shape
    assert weight.shape == head.shape
    np.testing.assert_array_equal(pd.unique(head), data.index)


def test_kernel():
    _, _, weight = _delaunay(cau_coords, kernel="gaussian")
    expected = np.array(
        [
            0.231415,
            0.307681,
            0.395484,
            0.231415,
            0.237447,
            0.057774,
            0.307681,
            0.237447,
            0.123151,
            0.319563,
            0.057774,
            0.123151,
            0.035525,
            0.395484,
            0.319563,
            0.035525,
        ]
    )

    np.testing.assert_array_almost_equal(weight, expected)


@pytest.mark.network
def test_coplanar_raise_voronoi(stores):
    with pytest.raises(ValueError, match="There are"):
        _voronoi(stores, clip=False)


@pytest.mark.network
def test_coplanar_jitter_voronoi(stores, stores_unique):
    cp_heads, cp_tails, cp_w = _voronoi(stores, clip=False, coplanar="jitter")
    unique_heads, unique_tails, unique_w = _voronoi(stores_unique, clip=False)
    assert not np.array_equal(cp_heads, unique_heads)
    assert not np.array_equal(cp_tails, unique_tails)
    assert not np.array_equal(cp_w, unique_w)

    assert cp_heads.shape[0] == 3384
    assert unique_heads.shape[0] == 3360


class TestCoplanar:
    def setup_method(self):
        self.geom = [
            shapely.Point(0, 0),
            shapely.Point(1, 1),
            shapely.Point(2, 0),
            shapely.Point(3, 1),
            shapely.Point(0, 0),  # coplanar point
            shapely.Point(0, 5),
        ]
        self.df_int = geopandas.GeoDataFrame(
            geometry=self.geom,
        )
        self.df_string = geopandas.GeoDataFrame(
            geometry=self.geom, index=["zero", "one", "two", "three", "four", "five"]
        )
        self.mapping = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}

    def test_delaunay_error(self):
        with pytest.raises(
            CoplanarError,
            match="There are 5 unique locations in the dataset, but 6 observations",
        ):
            _delaunay(self.df_int)

    def test_delaunay_jitter(self):
        heads, tails, weights = _delaunay(self.df_int, coplanar="jitter", seed=0)

        exp_heads = np.array(
            [0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]
        )
        exp_tails = np.array(
            [1, 2, 4, 0, 2, 3, 4, 5, 0, 1, 3, 1, 2, 5, 0, 1, 5, 1, 3, 4]
        )
        exp_w = np.ones(exp_heads.shape, dtype="int8")

        np.testing.assert_array_equal(heads, exp_heads)
        np.testing.assert_array_equal(tails, exp_tails)

        heads, tails, weights = _delaunay(self.df_string, coplanar="jitter", seed=0)

        np.testing.assert_array_equal(heads, np.vectorize(self.mapping.get)(exp_heads))
        np.testing.assert_array_equal(tails, np.vectorize(self.mapping.get)(exp_tails))
        np.testing.assert_array_equal(weights, exp_w)

    def test_delaunay_clique(self):
        # TODO: fix the implemntation to make this pass
        heads, tails, weights = _delaunay(self.df_int, coplanar="clique")

        exp_heads = np.array(
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5]
        )
        exp_tails = np.array(
            [1, 2, 4, 5, 0, 2, 3, 4, 5, 0, 1, 3, 4, 1, 2, 5, 0, 1, 2, 5, 0, 1, 3, 4]
        )
        exp_w = np.ones(exp_heads.shape, dtype="int8")

        np.testing.assert_array_equal(heads, exp_heads)
        np.testing.assert_array_equal(tails, exp_tails)

        heads, tails, weights = _delaunay(self.df_string, coplanar="clique")

        np.testing.assert_array_equal(heads, np.vectorize(self.mapping.get)(exp_heads))
        np.testing.assert_array_equal(tails, np.vectorize(self.mapping.get)(exp_tails))
        np.testing.assert_array_equal(weights, exp_w)

    def test_gabriel_error(self):
        with pytest.raises(
            CoplanarError,
            match="There are 5 unique locations in the dataset, but 6 observations",
        ):
            _gabriel(self.df_int)

    def test_gabriel_jitter(self):
        heads, tails, weights = _gabriel(self.df_int, coplanar="jitter", seed=0)

        exp_heads = np.array([0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5])
        exp_tails = np.array([2, 4, 2, 3, 4, 5, 0, 1, 3, 1, 2, 5, 0, 1, 1, 3])
        exp_w = np.ones(exp_heads.shape, dtype="int8")

        np.testing.assert_array_equal(heads, exp_heads)
        np.testing.assert_array_equal(tails, exp_tails)

        heads, tails, weights = _gabriel(self.df_string, coplanar="jitter", seed=0)

        np.testing.assert_array_equal(heads, np.vectorize(self.mapping.get)(exp_heads))
        np.testing.assert_array_equal(tails, np.vectorize(self.mapping.get)(exp_tails))
        np.testing.assert_array_equal(weights, exp_w)

    def test_gabriel_clique(self):
        # TODO: fix the implemntation to make this pass
        heads, tails, weights = _gabriel(self.df_int, coplanar="clique")

        exp_heads = np.array([0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 5])
        exp_tails = np.array([1, 2, 4, 0, 2, 3, 4, 5, 0, 1, 3, 4, 1, 2, 0, 1, 2, 1])
        exp_w = np.ones(exp_heads.shape, dtype="int8")

        np.testing.assert_array_equal(heads, exp_heads)
        np.testing.assert_array_equal(tails, exp_tails)

        heads, tails, weights = _gabriel(self.df_string, coplanar="clique")

        np.testing.assert_array_equal(heads, np.vectorize(self.mapping.get)(exp_heads))
        np.testing.assert_array_equal(tails, np.vectorize(self.mapping.get)(exp_tails))
        np.testing.assert_array_equal(weights, exp_w)

    def test_relative_neighborhood_error(self):
        with pytest.raises(
            CoplanarError,
            match="There are 5 unique locations in the dataset, but 6 observations",
        ):
            _relative_neighborhood(self.df_int)

    def test_relative_neighborhood_jitter(self):
        heads, tails, weights = _relative_neighborhood(
            self.df_int, coplanar="jitter", seed=0
        )

        exp_heads = np.array([0, 0, 1, 1, 2, 3, 3, 4, 4, 5])
        exp_tails = np.array([2, 4, 3, 4, 0, 1, 5, 0, 1, 3])
        exp_w = np.ones(exp_heads.shape, dtype="int8")

        np.testing.assert_array_equal(heads, exp_heads)
        np.testing.assert_array_equal(tails, exp_tails)

        heads, tails, weights = _relative_neighborhood(
            self.df_string, coplanar="jitter", seed=0
        )

        np.testing.assert_array_equal(heads, np.vectorize(self.mapping.get)(exp_heads))
        np.testing.assert_array_equal(tails, np.vectorize(self.mapping.get)(exp_tails))
        np.testing.assert_array_equal(weights, exp_w)

    def test_relative_neighborhood_clique(self):
        # TODO: fix the implemntation to make this pass
        heads, tails, weights = _relative_neighborhood(self.df_int, coplanar="clique")

        exp_heads = np.array([0, 0, 1, 1, 1, 1, 2, 2, 3, 4, 4, 5])
        exp_tails = np.array([1, 4, 0, 2, 4, 5, 1, 3, 2, 0, 1, 1])
        exp_w = np.ones(exp_heads.shape, dtype="int8")

        np.testing.assert_array_equal(heads, exp_heads)
        np.testing.assert_array_equal(tails, exp_tails)

        heads, tails, weights = _relative_neighborhood(
            self.df_string, coplanar="clique"
        )

        np.testing.assert_array_equal(heads, np.vectorize(self.mapping.get)(exp_heads))
        np.testing.assert_array_equal(tails, np.vectorize(self.mapping.get)(exp_tails))
        np.testing.assert_array_equal(weights, exp_w)

    def test_voronoi_error(self):
        with pytest.raises(
            CoplanarError,
            match="There are 5 unique locations in the dataset, but 6 observations",
        ):
            _voronoi(self.df_int)

    def test_voronoi_jitter(self):
        heads, tails, weights = _voronoi(self.df_int, coplanar="jitter", seed=0)

        exp_heads = np.array([0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5])
        exp_tails = np.array([1, 2, 4, 0, 2, 3, 4, 5, 0, 1, 3, 1, 2, 5, 0, 1, 1, 3])
        exp_w = np.ones(exp_heads.shape, dtype="int8")

        np.testing.assert_array_equal(heads, exp_heads)
        np.testing.assert_array_equal(tails, exp_tails)

        heads, tails, weights = _voronoi(self.df_string, coplanar="jitter", seed=0)

        np.testing.assert_array_equal(heads, np.vectorize(self.mapping.get)(exp_heads))
        np.testing.assert_array_equal(tails, np.vectorize(self.mapping.get)(exp_tails))
        np.testing.assert_array_equal(weights, exp_w)

    def test_voronoi_clique(self):
        # TODO: fix the implemntation to make this pass
        heads, tails, weights = _voronoi(self.df_int, coplanar="clique", seed=0)

        exp_heads = np.array([0, 0, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5])
        exp_tails = np.array([1, 4, 0, 2, 3, 4, 5, 1, 3, 1, 2, 5, 0, 1, 1, 3])
        exp_w = np.ones(exp_heads.shape, dtype="int8")

        np.testing.assert_array_equal(heads, exp_heads)
        np.testing.assert_array_equal(tails, exp_tails)

        heads, tails, weights = _voronoi(self.df_string, coplanar="clique", seed=0)

        np.testing.assert_array_equal(heads, np.vectorize(self.mapping.get)(exp_heads))
        np.testing.assert_array_equal(tails, np.vectorize(self.mapping.get)(exp_tails))
        np.testing.assert_array_equal(weights, exp_w)

    def test_wrong_resolver(self):
        with pytest.raises(
            ValueError,
            match="Recieved option coplanar='nonsense'",
        ):
            _delaunay(self.df_int, coplanar="nonsense")
