import os
import platform
from enum import Enum
from functools import wraps

from genes.lib.exceptions import OSNotSupportedError
from genes.lib.logging import log_error, log_warn
from genes.lib.traits import ErrorLevel


class LinuxDistro(Enum):
    alpine = 'alpine'
    arch = 'arch'
    centos = 'centos'
    debian = 'debian'
    fedora = 'fedora'
    gentoo = 'gentoo'
    redhat = 'redhat'
    scientific = 'scientific'
    ubuntu = 'ubuntu'


def is_linux(releases=None):
    """
    Determine whether the operating system is linux or not.
    :param releases: a list of releases to return true on
    :return: bool; True if the operating system meets the above criteria
    """
    is_release = True
    if releases:
        is_release = platform.release() in releases
    return platform.system() == 'Linux' and is_release


def only_linux(error_level=ErrorLevel.warn, releases=None):
    """
    Wrap a function and only execute it if the system is linux of the
    release specified
    :param error_level: how to handle execution for systems that aren't linux
    :param releases: releases of linux which are allowable
    :return: a wrapper function that wraps functions in conditional execution
    """
    msg = "This function can only be run on Linux: "

    def wrapper(func):
        @wraps(func)
        def run_if_linux(*args, **kwargs):
            if is_linux(releases=releases):
                return func(*args, **kwargs)
            elif error_level == ErrorLevel.warn:
                log_warn(msg, func.__name__)
                return None
            elif error_level == ErrorLevel.error:
                log_error(msg, func.__name__)
                raise OSNotSupportedError(msg, func.__name__)
            else:
                return None

        return run_if_linux

    return wrapper


def get_distro():
    distro_options = set([opt.value for opt in LinuxDistro])
    if os.path.isfile('/etc/os-release'):
        with open('/etc/os-release', 'r') as f:
            contents = f.readlines()

        for line in contents:
            if line.startswith('ID='):
                line = line.partition('=')
                distro_options &= {line[-1].rstrip('\n')}

    if os.path.isfile('/etc/lsb-release'):
        # TODO: parse this file
        pass

    if os.path.isfile('/etc/lsb-release.d'):
        # TODO: parse this directory
        pass

    if os.path.isfile('/etc/gentoo-release'):
        distro_options &= {'gentoo'}

    if os.path.isfile('/etc/debian-release'):
        distro_options &= {'debian', 'ubuntu'}

    if os.path.isfile('/etc/redhat-release'):
        distro_options &= {'centos', 'fedora', 'redhat', 'scientific'}

    if len(distro_options) == 1:
        return distro_options.pop()
    elif len(distro_options) > 1:
        return 'AMBIGUOUS'
    else:
        return 'OTHER'


def get_version():
    # TODO: add more find cases
    if os.path.isfile('/etc/os-release'):
        with open('/etc/os-release', 'r') as f:
            contents = f.readlines()

        for line in contents:
            if line.startswith('VERSION_ID='):
                line = line.partition('=')
                return line[-1].rstrip('\n').strip('"').strip("'")
    else:
        # FIXME
        return ''


def get_codename():
    # FIXME: add more find cases
    if os.path.isfile('/etc/lsb-release'):
        with open('/etc/lsb-release', 'r') as f:
            contents = f.readlines()

        for line in contents:
            if line.startswith('DISTRIB_CODENAME='):
                line = line.partition('=')
                return line[-1].rstrip('\n')
    elif os.path.isfile('/etc/os-release'):
        codename_map = {
            'debian': {
                '8': 'jessie'
            },
            'ubuntu': {
                '16.04': 'xenial',
                '15.10': 'wily',
                '15.04': 'vivid',
                '14.04': 'trusty',
            }
        }
        return codename_map.get(get_distro(), {}).get(get_version(), '')
    else:
        # FIXME
        return ''
