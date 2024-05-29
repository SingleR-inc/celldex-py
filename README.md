<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/celldex.svg?branch=main)](https://cirrus-ci.com/github/<USER>/celldex)
[![ReadTheDocs](https://readthedocs.org/projects/celldex/badge/?version=latest)](https://celldex.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/celldex/main.svg)](https://coveralls.io/r/<USER>/celldex)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/celldex.svg)](https://anaconda.org/conda-forge/celldex)
[![Monthly Downloads](https://pepy.tech/badge/celldex/month)](https://pepy.tech/project/celldex)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/celldex)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![PyPI-Server](https://img.shields.io/pypi/v/celldex.svg)](https://pypi.org/project/celldex/)

# celldex - reference cell type datasets

This package provides reference datasets with annotated cell types for convenient use by [BiocPy](https://github.com/biocpy) packages and workflows in Python.
These references were sourced and uploaded by the [celldex R/Bioconductor](https://bioconductor.org/packages/devel/data/experiment/html/celldex.html) package.

Each dataset is loaded as a [`SummarizedExperiment`](https://bioconductor.org/packages/SummarizedExperiment) that is ready for further analysis, and may be used for downstream analysis, e.g in the [SingleR Python implementation](https://github.com/BiocPy/singler).


## Installation

To get started, install the package from [PyPI](https://pypi.org/project/celldex/):

```shell
pip install celldex
```

## Find reference datasets

The `list_references()` function will display all available reference datasets along with their metadata.

```python
from celldex import list_references

refs = list_references()
print(refs[["name", "version"]].head(3))

## output
# |    | name             | version    |
# |---:|:-----------------|:-----------|
# |  0 | immgen           | 2024-02-26 |
# |  1 | blueprint_encode | 2024-02-26 |
# |  2 | dice             | 2024-02-26 |
```

## Fetch reference datasets

Fetch a dataset as a [SummarizedExperiment](https://github.com/biocpy/summarizedexperiment):

```python
ref = fetch_reference("immgen", version="2024-02-26")
ref2 = fetch_reference("hpca", "2024-02-26")

print(ref)

## output
# class: SummarizedExperiment
# dimensions: (22134, 830)
# assays(1): ['logcounts']
# row_data columns(0): []
# row_names(22134): ['Zglp1', 'Vmn2r65', 'Gm10024', ..., 'Ifi44', 'Tiparp', 'Kdm1a']
# column_data columns(3): ['label.main', 'label.fine', 'label.ont']
# column_names(830): ['GSM1136119_EA07068_260297_MOGENE-1_0-ST-V1_MF.11C-11B+.LU_1.CEL', 'GSM1136120_EA07068_260298_MOGENE-1_0-ST-V1_MF.11C-11B+.LU_2.CEL', 'GSM1136121_EA07068_260299_MOGENE-1_0-ST-V1_MF.11C-11B+.LU_3.CEL', ..., 'GSM920653_EA07068_201207_MOGENE-1_0-ST-V1_TGD.VG4+24AHI.E17.TH_3.CEL', 'GSM920654_EA07068_201214_MOGENE-1_0-ST-V1_TGD.VG4+24ALO.E17.TH_1.CEL', 'GSM920655_EA07068_201215_MOGENE-1_0-ST-V1_TGD.VG4+24ALO.E17.TH_2.CEL']
# metadata(0):
```

## Search for references

There's limited number of references right now, but if you want to search for references,

```python
res = search_references("human")
res = search_references(define_text_query("Immun%", partial="True"))
res = search_references(define_text_query("10090", field="taxonomy_id"))
```

## Adding new reference datasets

These instructions follow the same steps outlined in the [scrnaseq package](https://github.com/biocpy/scrnaseq).

1. Format your dataset as a `SummarizedExperiment`. Let's mock a reference dataset:

     ***Note: Experiment object must include an assay ('logcounts') matrix containing log-normalized counts.***

     ```python
     import numpy as np
     from summarizedexperiment import SummarizedExperiment
     from biocframe import BiocFrame

     mat = np.random.exponential(1.3, (100, 10))
     row_names = [f"GENE_{i}" for i in range(mat.shape[0])]
     col_names = list("ABCDEFGHIJ")
     sce = SummarizedExperiment(
          assays={"logcounts": mat},
          row_data=BiocFrame(row_names=row_names),
          column_data=BiocFrame(data={"label.fine": col_names}),
     )
     ```

2. Assemble the metadata for your reference dataset. This should be a dictionary as specified in the [Bioconductor metadata schema](https://github.com/ArtifactDB/bioconductor-metadata-index). Check out some examples from `fetch_metadata()`. Note that the `application.takane` property will be automatically added later, and so can be omitted from the list that you create.

     ```python
     meta = {
          "title": "New reference dataset",
          "description": "This is a new reference dataset",
          "taxonomy_id": ["10090"],  # NCBI ID
          "genome": ["GRCm38"],  # genome build
          "sources": [{"provider": "GEO", "id": "GSE12345"}],
          "maintainer_name": "Jayaram kancherla",
          "maintainer_email": "jayaram.kancherla@gmail.com",
     }
     ```

3. Save your `SummarizedExperiment`  object to disk with `save_reference()`. This saves the reference dataset into a "staging directory" using language-agnostic file formats - check out the [ArtifactDB](https://github.com/artifactdb) framework for more details.

     ```python
     import tempfile
     from celldex import save_reference

     # replace tmp with a staging directory
     staging_dir = tempfile.mkdtemp()
     save_reference(sce, staging_dir, meta)
     ```

     You can check that everything was correctly saved by reloading the on-disk data for inspection:

     ```python
     import dolomite_base as dl

     dl.read_object(staging_dir)
     ```

4. Wait for us to grant temporary upload permissions to your GitHub account.

5. Upload your staging directory to [**gypsum** backend](https://github.com/ArtifactDB/gypsum-worker) with `upload_reference()`. On the first call to this function, it will automatically prompt you to log into GitHub so that the backend can authenticate you. If you are on a system without browser access (e.g., most computing clusters), a [token](https://github.com/settings/tokens) can be manually supplied via `set_access_token()`.

     ```python
     from celldex import upload_reference

     upload_reference(staging_dir, "my_dataset_name", "my_version")
     ```

     You can check that everything was successfully uploaded by calling `fetch_reference()` with the same name and version:

     ```python
     from celldex import fetch_reference

     fetch_reference("my_dataset_name", "my_version")
     ```

     If you realized you made a mistake, no worries. Use the following call to clear the erroneous dataset, and try again:

     ```python
     from gypsum_client import reject_probation

     reject_probation("celldex", "my_dataset_name", "my_version")
     ```

6. Comment on the PR to notify us that the dataset has finished uploading and you're happy with it. We'll review it and make sure everything's in order. If some fixes are required, we'll just clear the dataset so that you can upload a new version with the necessary changes. Otherwise, we'll approve the dataset. Note that once a version of a dataset is approved, no further changes can be made to that version; you'll have to upload a new version if you want to modify something.

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
