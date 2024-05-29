import tempfile

import pandas as pd
from celldex import save_reference
from summarizedexperiment import SummarizedExperiment
from delayedarray import DelayedArray, is_sparse
from dolomite_matrix import ReloadedArray
import numpy as np
from biocframe import BiocFrame

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


def test_save_references():
    mat = np.random.exponential(1.3, (100, 10))
    row_names = [f"GENE_{i}" for i in range(mat.shape[0])]
    col_names = list("ABCDEFGHIJ")
    sce = SummarizedExperiment(
        assays={"logcounts": mat},
        row_data=BiocFrame(row_names=row_names),
        column_data=BiocFrame(data={"label.fine": col_names}),
    )

    # Provide metadata for search and findability
    meta = {
        "title": "New reference dataset",
        "description": "This is a new reference dataset",
        "taxonomy_id": ["10090"],  # NCBI ID
        "genome": ["GRCm38"],  # genome build
        "sources": [{"provider": "GEO", "id": "GSE12345"}],
        "maintainer_name": "Jayaram kancherla",
        "maintainer_email": "jayaram.kancherla@gmail.com",
    }

    import shutil
    import tempfile

    cache_dir = tempfile.mkdtemp()

    # Make sure the directory is clean
    shutil.rmtree(cache_dir)

    # Save the reference
    save_reference(sce, cache_dir, meta)
