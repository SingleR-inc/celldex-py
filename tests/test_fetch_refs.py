import tempfile

import pandas as pd
from celldex import fetch_reference
from summarizedexperiment import SummarizedExperiment
from delayedarray import DelayedArray, is_sparse
from dolomite_matrix import ReloadedArray

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


def test_fetch_references():
    ref = fetch_reference("hpca", "2024-02-26")
    assert isinstance(ref, SummarizedExperiment)

    # Correctly creates ReloadedMatrix objects.
    asy = ref.assay(0)
    assert isinstance(asy, ReloadedArray)
    assert not is_sparse(asy)

    # Works with realization options.
    ref = fetch_reference("hpca", "2024-02-26", realize_assays=True)
    asy = ref.assay(0)
    assert not isinstance(asy, ReloadedArray)
