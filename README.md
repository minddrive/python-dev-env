# python-dev-env
A set of programs to help set up and maintain development environments
for Python

The current modules available are:
- pyenv

## Requirements
- Python 3.7 or greater
- [OS Prerequisites](https://github.com/pyenv/pyenv/wiki/Common-build-problems)
    - You'll need to ensure the relevant command is run for your OS

## Pyenv Setup
***[Note: This is not fully correct at the moment as the program is undergoing
significant changes; it will be updated as things are in place.]***

Simply run `pyenv_setup.py [-r <pyenv_root>]`. You may need to prefix the
command with the right Python binary (many systems will call it `python3`
as an example).

The optional `-r <pyenv_root>` allows for multiple installations, if desired.
The default location is `$HOME/.pyenv`.  Log out and back in to initialize
pyenv and add it to one's PATH.
