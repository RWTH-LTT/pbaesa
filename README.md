# pbaesa

[![PyPI](https://img.shields.io/pypi/v/pbaesa.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/pbaesa.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/pbaesa)][pypi status]
[![License](https://img.shields.io/pypi/l/pbaesa)][license]

[![Read the documentation at https://pbaesa.readthedocs.io/](https://img.shields.io/readthedocs/pbaesa/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/RWTH-LTT/pbaesa/actions/workflows/python-test.yml/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/RWTH-LTT/pbaesa/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/pbaesa/
[read the docs]: https://pbaesa.readthedocs.io/
[tests]: https://github.com/RWTH-LTT/pbaesa/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/RWTH-LTT/pbaesa
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Installation

You can install _pbaesa_ via [pip] from [PyPI]:

```console
$ pip install pbaesa
```

## Usage

### Basic Example

```python
import bw2data as bd
import pbaesa

# Set your Brightway project
bd.projects.set_current('your_project_name')

# Load your biosphere database
bio = bd.Database("ecoinvent-3.10.1-biosphere")

# Create all planetary boundary LCIA methods
pbaesa.create_pbaesa_methods(biosphere_db=bio)

# Get allocation factors for a specific sector and location
allocation_factors = pbaesa.get_all_allocation_factor(
    geographical_scope="DE",  
    sector="Cultivation of wheat",
    year=2022
)

print(allocation_factors)
```

### Key Functions

- **`create_pbaesa_methods(biosphere_db, process_ids=[])`**: Creates and registers LCIA methods for all global planetary boundary categories except novel entities (climate change, ocean acidification, biosphere integrity, phosphorus cycle, atmospheric aerosol loading, freshwater use, stratospheric ozone depletion, land-system change, and nitrogen cycle).

- **`get_all_allocation_factor(geographical_scope, sector, year)`**: Retrieves allocation factors for a specific sector and geographical scope. If the allocation factors file is not present, the function will generate it automatically.

For more detailed examples, see the `examples/` directory.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide][Contributor Guide].

## License and Data Use

## License and Attribution

This repository is released under the same non-commercial license as EXIOBASE v3.9, 
a customized derivative of the [CC BY-NC-SA 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

© 2025 Institute of Technical Thermodynamics  
Uses data from EXIOBASE v3.9 © 2024 EXIOBASE Consortium, released under non-commercial license terms.  
See [https://exiobase.eu](https://exiobase.eu) for full details.

This repository does **not** include any EXIOBASE data or derived coefficients.
Users must obtain EXIOBASE data directly from the official source.
Commercial use of this repository or derived works is not permitted.

## Issues

If you encounter any problems,
please [file an issue][Issue Tracker] along with a detailed description.


<!-- github-only -->

[command-line reference]: https://pbaesa.readthedocs.io/en/latest/usage.html
[License]: https://github.com/RWTH-LTT/pbaesa/blob/main/LICENSE
[Contributor Guide]: https://github.com/RWTH-LTT/pbaesa/blob/main/CONTRIBUTING.md
[Issue Tracker]: https://github.com/RWTH-LTT/pbaesa/issues


## Building the Documentation

You can build the documentation locally by installing the documentation Conda environment:

```bash
conda env create -f docs/environment.yml
```

activating the environment

```bash
conda activate sphinx_pbaesa
```

and [running the build command](https://www.sphinx-doc.org/en/master/man/sphinx-build.html#sphinx-build):

```bash
sphinx-build docs _build/html --builder=html --jobs=auto --write-all; open _build/html/index.html
```