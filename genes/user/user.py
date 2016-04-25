from genes.os.traits import get_os
from genes.package import Package


class User(Package):
    def __init__(self, os_name=get_os()):
        self.os_name = os_name

        if self.os_name == 'osx':
            pass
        elif self.os_name in ('debian', 'ubuntu'):
            pass

    def uninstall(self, *args, **kwargs):
        pass

    def configure(self, *args, **kwargs):
        pass

    def is_installed(self, *args, **kwargs):
        pass

    def install(self, *args, **kwargs):
        pass
