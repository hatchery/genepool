from genes.apt.get import APTGet
from genes.brew import commands as brew
from genes.debian.traits import is_debian
from genes.mac.traits import is_osx
from genes.ubuntu.traits import is_ubuntu


def main():
    if is_debian() or is_ubuntu():
        apt_get = APTGet()
        apt_get.update()
        packages = (
            "aria2",
            "atop",
            "byobu",
            "curl",
            "elinks",
            "emacs",
            "hatop",
            "htop",
            "httpie",
            "iftop",
            "iptraf",
            "iptraf-ng",
            "ipcalc",
            "jq",
            "less",
            "links",
            "links2",
            "lynx",
            "most",
            "netcat",
            "nethogs",
            "netpipes",
            "nmap",
            "rsync",
            "rsyncrypto",
            "rtorrent",
            "screen",
            "siege",
            "socat",
            "squid3",
            "tmux",
            "vim",
            "vim-gtk",
            "wget"
        )
        apt_get.install(*packages)

    elif is_osx():
        brew.update()

    else:
        pass
