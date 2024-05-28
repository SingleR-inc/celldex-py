from biocframe import BiocFrame
from delayedarray import is_sparse, to_dense_array, to_scipy_sparse_matrix
from dolomite_base import read_object
from summarizedexperiment import SummarizedExperiment

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


def celldex_load_object(
    path: str,
    metadata: dict = None,
    celldex_realize_assays: bool = False,
    **kwargs,
):
    """Load a ``SummarizedExperiment`` object from a file.

    Args:
        path:
            Path to the dataset.

        metadata:
            Metadata for the dataset.
            Defaults to None.

        celldex_realize_assays:
            Whether to realize assays into memory.
            Defaults to False.

        **kwargs:
            Further arguments to pass to
            :py:func:`~dolomite_base.read_object.read_object`.

    Returns:
        A `SummarizedExperiment` derivative of the object.
    """
    obj = read_object(
        path,
        metadata=metadata,
        celldex_realize_assays=celldex_realize_assays,
        **kwargs,
    )

    if isinstance(obj, SummarizedExperiment):
        if celldex_realize_assays:
            _assays = {}
            for y in obj.get_assay_names():
                _assays[y] = realize_array(obj.assay(y))

            obj = obj.set_assays(_assays)

    return obj


def realize_array(x):
    """Realize a `ReloadedArray` into a dense array or sparse matrix.

    Args:
        x:
            `ReloadedArray` object.

    Returns:

        Realized array or matrix.
    """
    from dolomite_matrix import ReloadedArray

    if isinstance(x, ReloadedArray):
        if is_sparse(x):
            x = to_scipy_sparse_matrix(x, "csc")
        else:
            x = to_dense_array(x)

    return x


def format_object_metadata(x) -> dict:
    """Format object related metadata.

    Create object-related metadata to validate against the default
    schema from
    :py:func:`~gypsum_client.fetch_metadata_schema.fetch_metadata_schema`.
    This is intended for downstream package developers who are
    auto-generating metadata documents to be validated by
    :py:func:`~gypsum_client.validate_metadata.validate_metadata`.

    Args:
        x:
            An Python object, typically an instance of a BiocPy class.

    Returns:
        Dictionary containing metadata for the object.
    """
    _meta = {}

    if isinstance(x, SummarizedExperiment):
        _meta["summarized_experiment"] = {
            "rows": x.shape[0],
            "columns": x.shape[1],
            "assays": list(x.get_assay_names()),
            "column_annotations": list(x.get_column_names()),
        }

    elif isinstance(x, BiocFrame):
        _meta["data_frame"] = {
            "rows": len(x),
            "column_names": list(x.get_column_names()),
        }

    return _meta
