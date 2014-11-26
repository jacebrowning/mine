"""Integration tests for the `mine` package."""


import os
from mine.test.conftest import FILES

from mine.application import Application
from mine.computer import Computer
from mine.status import State, Status
from mine.settings import Settings, Configuration

import yorm


def test_settings():
    """Verify a sample file is created."""
    PATH = os.path.join(FILES, 'mine.yml')

    if os.path.exists(PATH):
        os.remove(PATH)

    settings = Settings()
    yorm.store(settings, PATH)

    itunes = Application('itunes')
    itunes.versions.mac = ''
    itunes.versions.windows = 'iTunes.exe'

    iphoto = Application('iphoto')
    iphoto.versions.mac = 'iPhoto'

    mac = Computer('macbook')
    mac.hostname = 'Jaces-MacBook'
    mac.address.external = '1.2.3.4'

    mac2 = Computer('macbook-pro')

    configuration = Configuration()
    configuration.applications = [itunes, iphoto]
    configuration.computers = [mac, mac2]

    settings.configuration = configuration

    mac_state = State('macbook-pro')
    mac_state.timestamps.started = 444

    itunes_status = Status('itunes')
    itunes_status.computers = [mac_state]

    settings.status = [itunes_status]

    assert os.path.exists(PATH)
