# pb-aesa

[![PyPI](https://img.shields.io/pypi/v/pb-aesa.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/pb-aesa.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/pb-aesa)][pypi status]
[![License](https://img.shields.io/pypi/l/pb-aesa)][license]

[![Read the documentation at https://pb-aesa.readthedocs.io/](https://img.shields.io/readthedocs/pb-aesa/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/RWTH-LTT/pb-aesa/actions/workflows/python-test.yml/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/RWTH-LTT/pb-aesa/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/pb-aesa/
[read the docs]: https://pb-aesa.readthedocs.io/
[tests]: https://github.com/RWTH-LTT/pb-aesa/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/RWTH-LTT/pb-aesa
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Installation

You can install _pb-aesa_ via [pip] from [PyPI]:

```console
$ pip install pb-aesa
```

## Usage

Here's a simple example of how to use pb-aesa for planetary boundary-based absolute environmental sustainability assessment:

```python
import bw2data as bd
import bw2calc as bc
import pb_aesa

# 1. Set up your Brightway project and load databases
bd.projects.set_current('your_project_name')
bio = bd.Database("ecoinvent-3.10.1-biosphere")
ei = bd.Database("ecoinvent-3.10.1-cutoff")

# 2. Create planetary boundary LCIA methods
pb_aesa.create_pbaesa_methods(bio)

# 3. Get allocation factors for a specific sector
allocation_factors = pb_aesa.get_all_allocation_factor(
    geographical_scope="DE",
    sector="Cultivation of wheat", 
    year=2022
)

# 4. Run your LCA assessment
methods = [m for m in bd.methods if "Planetary Boundaries" in str(m)]
activity = [act for act in ei if 'wheat grain production' in act['name']][0]

functional_unit = {activity: 1.0}
mlca = bc.MultiLCA(
    demands=functional_unit,
    method_config={"impact_categories": methods}
)
mlca.lci()
mlca.lcia()

# 5. Calculate and visualize exploitation of Safe Operating Space
exploitation = pb_aesa.calculate_exploitation_of_SOS(mlca.scores)
pb_aesa.plot_exploitation_of_SOS(exploitation)
```

For more detailed examples, see the [examples](examples/) directory.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide][Contributor Guide].

## License

Distributed under the terms of the [BSD 3 Clause license][License],
_pb-aesa_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue][Issue Tracker] along with a detailed description.


<!-- github-only -->

[command-line reference]: https://pb-aesa.readthedocs.io/en/latest/usage.html
[License]: https://github.com/RWTH-LTT/pb-aesa/blob/main/LICENSE
[Contributor Guide]: https://github.com/RWTH-LTT/pb-aesa/blob/main/CONTRIBUTING.md
[Issue Tracker]: https://github.com/RWTH-LTT/pb-aesa/issues


## Building the Documentation

You can build the documentation locally by installing the documentation Conda environment:

```bash
conda env create -f docs/environment.yml
```

activating the environment

```bash
conda activate sphinx_pb-aesa
```

and [running the build command](https://www.sphinx-doc.org/en/master/man/sphinx-build.html#sphinx-build):

```bash
sphinx-build docs _build/html --builder=html --jobs=auto --write-all; open _build/html/index.html
```