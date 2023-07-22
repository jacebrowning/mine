import subprocess

import log

from . import CLI
from .manager import Manager
from .models import Application, Versions

application = Application("Mine", versions=Versions(mac=CLI, windows=CLI, linux=CLI))


def stop(manager: Manager):
    manager.stop(application)


def restart(manager: Manager):
    cmd = "nohup {} --daemon --verbose >> /tmp/mine.log 2>&1 &".format(CLI)
    if application and not manager.is_running(application):
        log.warning("Daemon is not running, attempting to restart...")

        log.info("$ %s", cmd)
        subprocess.call(cmd, shell=True)
        if manager.is_running(application):
            return True

        log.error("Manually start daemon: %s", cmd)
        return False

    return True
