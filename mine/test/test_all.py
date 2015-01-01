"""Integration tests for the `mine` package."""


import os
import pytest
from mine.test.conftest import FILES

from mine.application import Application
from mine.computer import Computer
from mine.status import State, Status, ProgramStatus
from mine.config import ProgramConfig
from mine.data import Data

import yorm


@pytest.mark.integration
def test_data():
    """Verify a sample file is created."""
    path = os.path.join(FILES, 'mine.yml')

    if os.path.exists(path):
        os.remove(path)

    data = Data()
    yorm.store(data, path)

    itunes = Application('itunes')
    itunes.versions.mac = ''
    itunes.versions.windows = 'iTunes.exe'

    iphoto = Application('iphoto')
    iphoto.versions.mac = 'iPhoto'

    mac = Computer('macbook', 'Other.local')
    mac2 = Computer('macbook-pro')

    configuration = ProgramConfig()
    configuration.applications = [itunes, iphoto]
    configuration.computers = [mac, mac2]

    data.config = configuration

    mac_state = State('macbook-pro')
    mac_state.timestamp.started = 444

    itunes_status = Status('itunes')
    itunes_status.computers = [mac_state]

    status = ProgramStatus()
    status.applications = [itunes_status]
    status.counter = 499

    data.status = status

    assert os.path.exists(path)


@pytest.mark.integration
def test_data_out():
    """Verify a sample file is created."""
    path = os.path.join(FILES, 'mine-out.yml')

    if os.path.exists(path):
        os.remove(path)

    data = Data()
    yorm.store(data, path)

    itunes = Application('itunes')
    itunes.versions.mac = ''
    itunes.versions.windows = 'iTunes.exe'

    iphoto = Application('iphoto')
    iphoto.versions.mac = 'iPhoto'

    mac = Computer('macbook', 'Jaces-MacBook', '1.1.1.1', '2.2.2.2')
    mac2 = Computer('macbook-pro', 'Jaces-MacBook-2', '3.3.3.3', '4.4.4.4')

    configuration = ProgramConfig()
    configuration.applications = [itunes, iphoto]
    configuration.computers = [mac, mac2]

    data.config = configuration

    mac_state = State('macbook-pro')
    mac_state.timestamp.started = 444

    itunes_status = Status('itunes')
    itunes_status.computers = [mac_state]

    status = ProgramStatus()
    status.applications = [itunes_status]
    status.counter = 499

    data.status = status

    assert os.path.exists(path)


@pytest.mark.integration
def test_data_in():
    """Verify a sample file is loaded."""
    path = os.path.join(FILES, 'mine-in.yml')

    data = Data()
    yorm.store(data, path)

    assert data.config.applications
    for application in data.config.applications:
        if application.label == 'slack':
            break
    else:
        assert False
