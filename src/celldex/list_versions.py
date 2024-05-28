from typing import List

import gypsum_client as gypc

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


def list_versions(name: str) -> List[str]:
    """List all available versions for a reference.

    Example:

        .. code-block:: python

            versions = list_versions("immgen")

    Args:
        name:
            Name of the dataset.

    Returns:
        A list of version names.
    """
    return gypc.list_versions("celldex", name)


def fetch_latest_version(name: str) -> str:
    """Fetch the latest version for a reference from the gypsum backend.

    See Also:
        :py:func:`~celldex.fetch_reference.fetch_reference`,
        to fetch a reference.

        :py:func:`~celldex.fetch_reference.fetch_metadata`,
        to fetch the metadata for the reference.

    Example:

    .. code-block:: python

        meta = fetch_latest_version("immgen")

    Args:
        name:
            Name of the reference.

    Returns:
        String specifying the latest version for the reference.
    """
    return gypc.fetch_latest("celldex", name)
