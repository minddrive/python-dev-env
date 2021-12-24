"""Manage user's poetry environment.

A module that will allow the user to install poetry into their
environment, ensuring the appropriate configuration for the
user's path is set, along with managing an existing environment.
"""

from __future__ import annotations

import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)


# NOTE: On Debian, needed to ensure 'python3-pip' was installed,
#       as the damn new 'install-poetry.py' uses virtualenv to
#       install Poetry. :-/
class Poetry:
    """Class to manage a Poetry installation."""
    ...
