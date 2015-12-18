import os
from typing import Tuple

from genes.mac.traits import only_osx
from genes.process.commands import get_env_run_as


class Config:
    # FIXME: this structure should not exist
    ENV = os.environ.copy()
    USER = 'splicer'
    GROUP = 'admin'


env_run_as = get_env_run_as(Config.ENV)


@only_osx()
def update() -> None:
    env_run_as(['brew, update'], Config.USER, Config.GROUP)


@only_osx()
def install(*packages: Tuple[str, ...]) -> None:
    env_run_as(['brew', 'install'] + list(packages), Config.USER, Config.GROUP)


@only_osx()
def cask_install(*packages: Tuple[str, ...]) -> None:
    env_run_as(['brew', 'cask', 'install'] + list(packages),
               Config.USER,
               Config.GROUP)
