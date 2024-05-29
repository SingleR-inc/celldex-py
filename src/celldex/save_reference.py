import json
import os
import shutil
from functools import singledispatch
from typing import Any, List

import dolomite_base as dl
import numpy
from gypsum_client import fetch_metadata_schema, validate_metadata
from summarizedexperiment import SummarizedExperiment

from .utils import format_object_metadata

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


@singledispatch
def save_reference(x: Any, labels: List[str], path: str, metadata: dict):
    """Save a reference dataset to disk.

    Args:
        x:
            An object containing reference data.
            May be a
            :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`
            containing a assay matricx called `logcounts` of
            log-normalized expression values.

            Each row of ``column_data`` corresponds to a column of ``x`` and
            contains the label(s) for that column.
            Each column of ``labels`` represents a different label type;
            typically, the column name has a ``label.`` prefix to distinguish
            between, e.g., ``label.fine``, ``label.broad`` and so on.

            At least one column should be present.

        path:
            Path to a new directory to save the dataset.

        metadata:
            Dictionary containing the metadata for this dataset.
            see the schema returned by
            :py:func:`~gypsum_client.fetch_metadata_schema.fetch_metadata_schema`.

            Note that the ``applications.takane`` property will be automatically
            added by this function and does not have to be supplied.

    See Also:
        `metadata index <https://github.com/ArtifactDB/bioconductor-metadata-index>`_,
        on the expected schema for the metadata.

        :py:func:`~celldex.upload_referene.upload_reference`, to upload the saved contents.

    Example:

        .. code-block:: python

            # create a summarized experiment object
            mat = np.random.poisson(1, (100, 10))
            row_names = [f"GENE_{i}" for i in range(mat.shape[0])]
            col_names = list("ABCDEFGHIJ")
            sce = SummarizedExperiment(
                assays={"logcounts": mat},
                row_data=BiocFrame(row_names=row_names),
                column_data=BiocFrame({
                  "label.fine": col_names
                }),
            )

            # Provide metadata for search and findability
            meta = {
                "title": "New reference dataset",
                "description": "This is a new reference dataset",
                "taxonomy_id": ["10090"], # NCBI ID
                "genome": ["GRCm38"], # genome build
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
            celldex.save_reference(sce, cache_dir, meta)
    """
    raise NotImplementedError(
        f"'save_dataset' is not supported for objects of class: {type(x)}"
    )


def _save_se(x: SummarizedExperiment, path, metadata):
    schema = fetch_metadata_schema()

    if "bioconductor_version" not in metadata:
        metadata["bioconductor_version"] = "3.19"  # current release

    validate_metadata(metadata, schema)

    # checks if columns exist
    _cols = x.get_column_data()
    if len(_cols.get_column_names()) == 0:
        raise ValueError("'SummarizedExperiment' must contain atleast one column.")

    for _cn in _cols.get_column_names():
        _data = _cols.get_column(_cn)
        if not all(isinstance(y, str) for y in _data):
            raise ValueError(
                f"All labels in 'column_data' must be a list of strings; column {_cn} does not."
            )

    _mat = x.assay("logcounts")
    if not numpy.issubdtype(_mat.dtype, numpy.floating):
        raise ValueError("Assay 'logcounts' must be log-normalized values (floats).")

    if numpy.any(numpy.isnan(_mat)):
        raise ValueError("Assay 'logcounts' cannot contain NaN values.")

    _rows = x.get_row_names()
    if len(set(_rows)) != len(_rows):
        raise ValueError("'row_data' must contain unique row names.")

    if os.path.exists(path):
        shutil.rmtree(path)

    dl.save_object(x, path, reloaded_array_reuse_mode="symlink")

    takane = format_object_metadata(x)
    takane["type"] = dl.read_object_file(path)["type"]

    if "applications" not in metadata:
        metadata["applications"] = {}

    metadata["applications"]["takane"] = takane

    # Second validation with the takane metadata.
    contents = json.dumps(metadata, indent=4)
    validate_metadata(json.loads(contents), schema=schema)
    with open(os.path.join(path, "_bioconductor.json"), "w") as f:
        f.write(contents)


@save_reference.register
def save_reference_se(x: SummarizedExperiment, path: str, metadata: dict):
    """Save :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment` to disk."""
    return _save_se(x, path, metadata)
