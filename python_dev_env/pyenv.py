"""Manage user's pyenv environment.

A module that will allow the user to install pyenv into their
environment, ensuring the appropriate configuration for the
user's path is set, along with managing an existing environment.
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
    """Class to manage a pyenv installation and its plugins."""
    base_url = "https://github.com/pyenv"

    def __init__(self, root: str) -> None:
        """Set core, plugin parameters, and root path.

        :param root: The base directory to install pyenv.
        :type root: str
        """
        self.core = "pyenv"
        self.plugins = ["update", "virtualenv"]
        self.pyenv_root = pathlib.Path(root)

    def check_and_clone_repo(self, repo: str, plugin=False) -> None:
        """Clone repository if necessary.

        For pyenv or a plugin, check to see if it's checked out,
        and if not, clone it.

        :param repo: The name of the repository to check/clone.
        :type repo: str
        :param plugin:
            Boolean to determine if repository is a plugin or not.
        :type plugin: bool

        :raises RuntimeError: Occurs if Git clone fails.
        """
        repo_url = f"{self.base_url}/{repo}.git"
        clone_root = self.pyenv_root / "plugins" / f"{repo}" if plugin \
            else self.pyenv_root

        logger.info(f"Checking for existing {repo} checkout...")

        if not clone_root.exists():
            logger.info(f"  {repo} not found, cloning...")
            clone_proc = subprocess.run(
                ["git", "clone", repo_url, clone_root], capture_output=True
            )
            if clone_proc.returncode:
                raise RuntimeError(clone_proc.stderr)
        else:
            logger.info(f"  {repo} seems to be already checked out, continuing...")

    def setup(self) -> None:
        """Setup and configure pyenv and related plugins.

        Clone pyenv and desired plugins, ensure pyenv is functional,
        and update the shell's init script if needed.

        :raises RuntimeError: Occurs if pyenv can't be run
        """
        shell_init_files = {
            "bash": pathlib.Path.home() / ".bashrc",
            "zsh": pathlib.Path.home() / ".zshrc"
        }

        self.check_and_clone_repo(self.core)

        for plugin in self.plugins:
            self.check_and_clone_repo(f"{self.core}-{plugin}", plugin=True)

        pyenv_bin = self.pyenv_root / "bin" / "pyenv"
        run_proc = subprocess.run([pyenv_bin, "--version"], capture_output=True)
        if run_proc.returncode:
            raise RuntimeError(run_proc.stderr)

        if str(self.pyenv_root / "bin") not in os.environ["PATH"].split(":"):
            logger.info("pyenv not in path, adding to init script...")

            init_file = shell_init_files[pathlib.Path(os.environ["SHELL"]).name]

            # First check to ensure init file hasn't already been updated.
            with open(init_file) as fh:
                for line in fh.readlines():
                    if line.strip() == "# Pyenv setup":
                        logger.info(f"pyenv setup already in {init_file}, continuing...")
                        return

            with open(init_file, "a") as fh:
                fh.write(textwrap.dedent(f"""
                    # Pyenv setup
                    export PYENV_ROOT={self.pyenv_root}
                    export PATH="$PYENV_ROOT/bin:$PATH"
                    if command -v pyenv 1>/dev/null 2>&1; then
                        eval "$(pyenv init --path)"
                        eval "$(pyenv init -)"
                        eval "$(pyenv virtualenv-init -)"
                    fi
                """))
        else:
            logger.info("pyenv already in path, continuing...")


if __name__ == "__main__":
    """Set default pyenv install location, parse command line, then
    run the setup.
    """
    default_pyenv = str(pathlib.Path.home() / ".pyenv")

    parser = argparse.ArgumentParser(
        description="Program to manage pyenv in one's user environment"
    )
    parser.add_argument("-r", "--root", default=default_pyenv,
                        help="Base pyenv directory (default: $HOME/.pyenv)")
    args = parser.parse_args()

    try:
        pyenv = Pyenv(args.root)
        pyenv.setup()
    except RuntimeError as exc:
        logger.error("pyenv clone and configuration failed:")
        logger.error(f"    ERROR: {exc}")
