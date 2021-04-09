#!/usr/bin/env python3

"""Program to set up pyenv in one's user environment for first time

This program will install pyenv in one's user environment and ensure
things are configured so the program is available in one's path.
"""

from __future__ import annotations

import argparse
import logging
import os
import pathlib
import subprocess
import textwrap


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)


class Pyenv:
    """Class to manage a pyenv installation and its plugins"""
    basedir = "https://github.com/pyenv"

    def __init__(self, root: str) -> None:
        """Set core and plugin parameters, along with root path
        for pyenv

        :param root:
            The base directory to install pyenv
        :type root: `str`
        """
        self.core = "pyenv"
        self.plugins = ["update", "virtualenv"]
        self.pyenv_root = pathlib.Path(root)

    def check_and_install_repo(self, repo: str, plugin=False) -> None:
        """For pyenv or a plugin, check to see if it's installed,
        and if not, install it

        :param repo:
            The name of the repository to check/install
        :param plugin:
            Boolean to determine if repository is a plugin or not
        :type repo: `str`
        :type plugin: `bool`

        :raises: :exc:`RuntimeError` if Git clone fails
        """
        repo_url = f"{self.basedir}/{repo}.git"
        install_root = self.pyenv_root / "plugins" / f"{repo}" if plugin \
            else self.pyenv_root

        logger.info(f"Checking for existing {repo} install...")

        if not install_root.exists():
            logger.info(f"  {repo} not found, installing...")
            install_proc = subprocess.run(
                ["git", "clone", repo_url, install_root], capture_output=True
            )
            if install_proc.returncode:
                raise RuntimeError(install_proc.stderr)
        else:
            logger.info(f"  {repo} seems to be already installed, continuing...")

    def setup(self) -> None:
        """Install pyenv and necessary plugins, ensure pyenv is functional,
        and update the shell's init script if needed

        :raises: :exc:`RuntimeError` if pyenv can't be run
        """
        shell_init_files = {
            "bash": pathlib.Path.home() / ".bashrc",
            "zsh": pathlib.Path.home() / ".zshrc"
        }

        self.check_and_install_repo(self.core)

        for plugin in self.plugins:
            self.check_and_install_repo(f"{self.core}-{plugin}")

        pyenv_bin = self.pyenv_root / "bin" / "pyenv"
        run_proc = subprocess.run([pyenv_bin, "--version"], capture_output=True)
        if run_proc.returncode:
            raise RuntimeError(run_proc.stderr)

        if str(self.pyenv_root / "bin") not in os.environ["PATH"].split(":"):
            logger.info("pyenv not in path, adding to init script...")

            init_file = shell_init_files[pathlib.Path(os.environ["SHELL"]).name]
            with open(init_file, "a") as fh:
                fh.write(textwrap.dedent(f"""
                    # Pyenv setup
                    export PYENV_ROOT={self.pyenv_root}
                    export PATH="$PYENV_ROOT/bin:$PATH"
                    if command -v pyenv 1>/dev/null 2>&1; then
                        eval "$(pyenv init -)"
                        eval "$(pyenv virtualenv-init -)"
                    fi
                """))
        else:
            logger.info("pyenv already in path, continuing...")


if __name__ == "__main__":
    """Set default pyenv install location, parse command line, then
    run the setup
    """
    default_pyenv = str(pathlib.Path.home() / ".pyenv")

    parser = argparse.ArgumentParser(
        description="Program to install pyenv in one's user environment"
    )
    parser.add_argument("-r", "--root", default=default_pyenv,
                        help="Base pyenv directory (default: $HOME/.pyenv)")
    args = parser.parse_args()

    try:
        pyenv = Pyenv(args.root)
        pyenv.setup()
    except RuntimeError as exc:
        logger.error("pyenv install and configuration failed:")
        logger.error(f"    ERROR: {exc}")
