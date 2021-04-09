# python-dev-env
Programs and scripts to help set up and maintain development environments
for Python

The current programs available are:
- pyenv-setup

## Requirements
- Python 3.7 or greater
- [OS Prerequisites](https://github.com/pyenv/pyenv/wiki/Common-build-problems)
    - You'll need to ensure the relevant command is run for your OS

## Pyenv Setup
Simply run `pyenv_setup.py [-r <pyenv_root>]`. You may need to prefix the
command with the right Python binary (many systems will call it `python3`
as an example).

The optional `-r <pyenv_root>` allows for multiple installations, if desired.
The default location is `$HOME/.pyenv`.  Log out and back in to initialize
pyenv and add it to one's PATH.
