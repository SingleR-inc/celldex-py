import tempfile

import pandas as pd
from celldex import list_references

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


def test_list_references():
    refs = list_references(cache_dir=tempfile.mkdtemp())

    assert isinstance(refs, pd.DataFrame)
    assert len(refs) >= 7
