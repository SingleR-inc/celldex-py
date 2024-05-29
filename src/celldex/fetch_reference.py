import atexit
import json
import os

from dolomite_base import alt_read_object, alt_read_object_function
from gypsum_client import cache_directory, save_file, save_version
from summarizedexperiment import SummarizedExperiment

from .utils import celldex_load_object

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


def fetch_reference(
    name: str,
    version: str,
    path: str = None,
    package: str = "celldex",
    cache_dir: str = cache_directory(),
    overwrite: bool = False,
    realize_assays: bool = False,
    **kwargs,
) -> SummarizedExperiment:
    """Fetch a reference dataset from the gypsum backend.

    See Also:
        `metadata index <https://github.com/ArtifactDB/bioconductor-metadata-index>`_,
        on the expected schema for the metadata.

        :py:func:`~celldex.save_reference.save_reference` and
        :py:func:`~gypsum_client.upload_file_operations.upload_directory`,
        to save and upload a reference.

        :py:func:`~celldex.list_references.list_references` and :py:func:`~celldex.list_versions.list_versions`,
        to get possible values for `name` and `version`.

        :py:func:`~.fetch_metadata`,
        to fetch the metadata for the reference.

    Example:

        .. code-block:: python

            ref = fetch_reference("immgen", "2024-02-26")

    Args:
        name:
            Name of the reference dataset.

        version:
            Version of the reference dataset.

        path:
            Path to a subdataset, if name contains multiple datasets.
            Defaults to None.

        package:
            Name of the package.
            Defaults to "celldex".

        cache_dir:
            Path to cache directory.

        overwrite:
            Whether to overwrite existing files.
            Defaults to False.

        realize_assays:
            Whether to realize assays into memory.
            Defaults to False.

        **kwargs:
            Further arguments to pass to
            :py:func:`~dolomite_base.read_object.read_object`.

    Returns:
        The dataset as a
        :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`
        or one of its subclasses.
    """

    version_path = save_version(
        package, name, version, cache_dir=cache_dir, overwrite=overwrite
    )
    obj_path = (
        version_path if path is None else os.path.join(version_path, path.rstrip("/"))
    )

    old = alt_read_object_function(celldex_load_object)

    def reset_alt_read_func():
        alt_read_object_function(old)

    atexit.register(reset_alt_read_func)
    return alt_read_object(
        obj_path,
        celldex_realize_assays=realize_assays,
        **kwargs,
    )


def fetch_metadata(
    name: str,
    version: str,
    path: str = None,
    package: str = "celldex",
    cache_dir: str = cache_directory(),
    overwrite: bool = False,
):
    """Fetch metadata for a reference from the gypsum backend.

    See Also:
        :py:func:`~.fetch_reference`,
        to fetch a reference.

    Example:

    .. code-block:: python

        meta = fetch_metadata("immgen", "2024-02-26")

    Args:
        name:
            Name of the reference dataset.

        version:
            Version of the reference dataset.

        path:
            Path to a subdataset, if name contains multiple datasets.
            Defaults to None.

        package:
            Name of the package.
            Defaults to "celldex".

        cache_dir:
            Path to the cache directory.

        overwrite:
            Whether to overwrite existing files.
            Defaults to False.

    Returns:
        Dictionary containing metadata for the specified dataset.
    """
    remote_path = "_bioconductor.json" if path is None else f"{path}/_bioconductor.json"
    local_path = save_file(
        package, name, version, remote_path, cache_dir=cache_dir, overwrite=overwrite
    )

    with open(local_path, "r") as f:
        metadata = json.load(f)

    return metadata
