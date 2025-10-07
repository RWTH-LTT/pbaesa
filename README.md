# pblcia

[![PyPI](https://img.shields.io/pypi/v/pblcia.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/pblcia.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/pblcia)][pypi status]
[![License](https://img.shields.io/pypi/l/pblcia)][license]

[![Read the documentation at https://pblcia.readthedocs.io/](https://img.shields.io/readthedocs/pblcia/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/RWTH-LTT/pblcia/actions/workflows/python-test.yml/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/RWTH-LTT/pblcia/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/pblcia/
[read the docs]: https://pblcia.readthedocs.io/
[tests]: https://github.com/RWTH-LTT/pblcia/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/RWTH-LTT/pblcia
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Installation

You can install _pblcia_ via [pip] from [PyPI]:

```console
$ pip install pblcia
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide][Contributor Guide].

## License

Distributed under the terms of the [BSD 3 Clause license][License],
_pblcia_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue][Issue Tracker] along with a detailed description.


<!-- github-only -->

[command-line reference]: https://pblcia.readthedocs.io/en/latest/usage.html
[License]: https://github.com/RWTH-LTT/pblcia/blob/main/LICENSE
[Contributor Guide]: https://github.com/RWTH-LTT/pblcia/blob/main/CONTRIBUTING.md
[Issue Tracker]: https://github.com/RWTH-LTT/pblcia/issues


## Building the Documentation

You can build the documentation locally by installing the documentation Conda environment:

```bash
conda env create -f docs/environment.yml
```

activating the environment

```bash
conda activate sphinx_pblcia
```

and [running the build command](https://www.sphinx-doc.org/en/master/man/sphinx-build.html#sphinx-build):

```bash
sphinx-build docs _build/html --builder=html --jobs=auto --write-all; open _build/html/index.html
```