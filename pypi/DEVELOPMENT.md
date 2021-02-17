# Development

This project uses [invoke](http://www.pyinvoke.org/) (Similar to Rake/Makefiles).
Tasks are located in the [tasks.py](./tasks.py) python code.

To see the list of available tasks run
```bash
inv -l
```

## Development Work

### Setup for local development
```bash
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
