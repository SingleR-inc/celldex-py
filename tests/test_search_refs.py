import pandas as pd
from gypsum_client import define_text_query
from celldex import search_references

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


def test_search_references():
    res = search_references("human")
    assert len(res) > 3
    assert isinstance(res, pd.DataFrame)

    res = search_references(define_text_query("Immun%", partial=True))
    assert isinstance(res, pd.DataFrame)
    assert len(res) > 0

    res = search_references(define_text_query("10090", field="taxonomy_id"))
    assert isinstance(res, pd.DataFrame)
    assert len(res) > 0
