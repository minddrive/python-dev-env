#!/usr/bin/env python3

"""Program to set up pyenv in one's user environment for first time

This program will install pyenv in one's user environment and ensure
things are configured so the program is available in one's path.
"""

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


def install_pyenv(pyenv_root: str) -> None:
    """"""
    pyenv_repo = "https://github.com/pyenv/pyenv.git"
    pyenv_root = pathlib.Path(pyenv_root)
    pyenv_bin = pyenv_root / "bin" / "pyenv"
    pyenv_venv_repo = "https://github.com/pyenv/pyenv-virtualenv.git"
    pyenv_venv_root = pyenv_root / "plugins" / "pyenv-virtualenv"

    shell_init_files = {
        "bash": pathlib.Path.home() / ".bashrc",
        "zsh": pathlib.Path.home() / ".zshrc"
    }

    logger.info("Checking for existing pyenv install...")

    if not pyenv_root.exists():
        logger.info("  pyenv not found, installing...")
        install_proc = subprocess.run(
            ["git", "clone", pyenv_repo, pyenv_root], capture_output=True
        )
        if install_proc.returncode:
            raise RuntimeError(install_proc.stderr)
    else:
        logger.info("  pyenv seems to be already installed, continuing...")

    logger.info("Checking for existing pyenv-virtualenv install...")

    if not pyenv_venv_root.exists():
        logger.info("  pyenv-virtualenv not found, installing...")
        install_proc = subprocess.run(
            ["git", "clone", pyenv_venv_repo, pyenv_venv_root], capture_output=True
        )
        if install_proc.returncode:
            raise RuntimeError(install_proc.stderr)
    else:
        logger.info("  pyenv-virtualenv seems to be already installed, continuing...")

    logger.info("Verifying the installed pyenv works...")

    run_proc = subprocess.run([pyenv_bin, "--version"], capture_output=True)
    if run_proc.returncode:
        raise RuntimeError(run_proc.stderr)

    if str(pyenv_root / "bin") not in os.environ["PATH"].split(":"):
        logger.info("pyenv not in path, adding to init script...")

        init_file = shell_init_files[pathlib.Path(os.environ["SHELL"]).name]
        with open(init_file, "a") as fh:
            fh.write(textwrap.dedent(f"""
                # Pyenv setup
                export PYENV_ROOT={pyenv_root}
                export PATH="$PYENV_ROOT/bin:$PATH"
                if command -v pyenv 1>/dev/null 2>&1; then
                    eval "$(pyenv init -)"
                    eval "$(pyenv virtualenv-init -)"
                fi
            """))
    else:
        logger.info("pyenv already in path, continuing...")


if __name__ == "__main__":
    """"""
    default_pyenv = str(pathlib.Path.home() / ".pyenv")

    parser = argparse.ArgumentParser(
        description="Program to install pyenv in one's user environment"
    )
    parser.add_argument("-r", "--root", default=default_pyenv,
                        help="Base pyenv directory (default: $HOME/.pyenv)")
    args = parser.parse_args()

    try:
        install_pyenv(args.root)
    except RuntimeError as exc:
        logger.error("pyenv install and configuration failed:")
        logger.error(f"    ERROR: {exc}")
