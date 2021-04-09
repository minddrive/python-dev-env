# python-dev-env
Programs and scripts to help set up and maintain development environments
for Python

The current programs available are:
- pyenv-setup

## Requirements
- Python 3.7 or greater
- [OS Prerequisites](https://github.com/pyenv/pyenv/wiki/Common-build-problems)

## Pyenv Setup
Simply run `pyenv_setup.py [-r <pyenv_root>]`

The optional `-r <pyenv_root>` allows for multiple installations, if desired.
The default location is `$HOME/.pyenv`.  Log out and back in to initialize
pyenv and add it to one's PATH.
