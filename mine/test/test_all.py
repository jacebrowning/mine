"""Integration tests for the `mine` package."""


import os
import pytest
from mine.test.conftest import FILES

from mine.application import Application
from mine.computer import Computer
from mine.status import State, Status
from mine.settings import ProgramConfiguration, ProgramStatus, Settings

import yorm


@pytest.mark.integration
def test_settings_out():
    """Verify a sample file is created."""
    path = os.path.join(FILES, 'mine-out.yml')

    if os.path.exists(path):
        os.remove(path)

    settings = Settings()
    yorm.store(settings, path)

    itunes = Application('itunes')
    itunes.versions.mac = ''
    itunes.versions.windows = 'iTunes.exe'

    iphoto = Application('iphoto')
    iphoto.versions.mac = 'iPhoto'

    mac = Computer('macbook')
    mac.hostname = 'Jaces-MacBook'
    mac.address.external = '1.2.3.4'

    mac2 = Computer('macbook-pro')

    configuration = ProgramConfiguration()
    configuration.applications = [itunes, iphoto]
    configuration.computers = [mac, mac2]

    settings.configuration = configuration

    mac_state = State('macbook-pro')
    mac_state.timestamps.started = 444

    itunes_status = Status('itunes')
    itunes_status.computers = [mac_state]

    status = ProgramStatus()
    status.applications = [itunes_status]
    status.counter = 499

    settings.status = status

    assert os.path.exists(path)


@pytest.mark.integration
def test_settings_in():
    """Verify a sample file is loaded."""
    path = os.path.join(FILES, 'mine-in.yml')

    settings = Settings()
    yorm.store(settings, path)

    assert settings.configuration.applications
    for application in settings.configuration.applications:
        if application.label == 'slack':
            break
    else:
        assert False
