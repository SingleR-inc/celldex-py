import tempfile

from biocframe import BiocFrame
from celldex import list_references, list_versions, fetch_latest_version

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


def test_list_references():
    refs = list_references(cache_dir=tempfile.mkdtemp())

    assert isinstance(refs, BiocFrame)
    assert len(refs) >= 7


def test_list_versions():
    vers = list_versions("immgen")

    assert "2024-02-26" in vers

    latest = fetch_latest_version("immgen")
    assert latest in vers
