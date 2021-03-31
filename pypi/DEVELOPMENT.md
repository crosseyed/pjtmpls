# Development

This project uses [invoke](http://www.pyinvoke.org/) (Similar to Rake/Makefiles).
Tasks are located in the [tasks.py](./tasks.py) python code.

To see the list of available tasks run
```bash
inv -l
```

## Development Work

### Requirements

A minimum of

* python
* python version manager (E.G. [pyenv](https://github.com/pyenv/pyenv)). Check out the installer and 
  configuration at [pyenv-installer](https://github.com/pyenv/pyenv-installer).

### Setup for local development
```bash
# Using pyenv install the version of python used by this repo
pyenv install $(cat .python-version)

# NOTE: One can also check the installed versions to see if it is already installed
pyenv versions

# Switch to this version of python
pyenv local $(cat .python-version)

# Installs development requirements
pip install -r requirements-setup.in
inv deps-compile

# Install dependencies from `requirements-setup.in`/`requirements-setup.txt` for development tools
# and `requirements.in`/`requirements.txt` for package dependencies
inv deps

# Build package
inv clean
inv build

# Links package for development purposes
pip install -e .
```

### Adding dependencies
Package dependencies can be added to `requirements.in`

*requirements.in*
```bash
cat requirements.in
  docopt
```

Tools which don't form package dependencies but are needed to support development.
(E.G. `pytest`, `invoke`, `pylint` etc). Can be added to requirements-setup.in.
```bash
cat requirements-setup.in
  boto3-stubs
  coverage
  faker
  invoke
  pip-tools
  pytest
  pytest-cov
  pytest-html
  pytest-mock
  python-dotenv
  radon
  shortuuid
```

*generate requirements.txt and requirements-setup.txt*
```bash
inv deps-compile
```

*install dependencies*
```bash
inv deps
```

### Updating dependencies

There are two sets of dependencies.

1. The dependencies required to test and manage the software project. Stored in `requirements-setup.in` and `requirements-setup.txt`
2. The package dependencies automatically installed when the package is installed this is in `requirements.in` and `requirements.txt`

To upgrade the package simply touch the  `requirements-setup.in` or `requirements.in` then run `inv deps`.
This will update the corresponding `requirements-setup.txt` or `requirements.txt` file with the latest versions.

_Example_
```bash
# Update requirements-setup.txt
touch requirements-setup.in
inv deps

# Update requirements.txt
touch requirements.in
inv deps
```

### Keeping the package version fixed

Although not recommended to avoid code rot and security issues, to keep a package version fixed simply specify a version in.
`requirements.in` or `requirements-setup.in`. Versions follows the regular pip syntax.

_Example: lock coverage to 5.4 but keep all other packages unpinned_
```
# requirements-setup.in
ansi2html
coverage==5.4
faker
invoke
liccheck
pip-tools
pytest
pytest-cov
pytest-html
pytest-mock
python-dotenv
radon
shortuuid
wheel
```

```bash
# Updates the requirements.txt keeping coverage at 5.4
inv deps
```