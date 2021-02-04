# kick:render
# ${PROJECT_NAME}

## Usage

## Development

This project uses [invoke](http://www.pyinvoke.org/) (Similar to Rake/Makefiles).
Tasks are located in the [tasks.py](./tasks.py) python code.

To see the list of available tasks run
```bash
inv -l
```

### Development Work
```bash
# Installs development requirements
pip install -r requirements-setup.txt
inv deps-compile

inv clean
inv build

# Links package for development purposes
pip install -e .
```

