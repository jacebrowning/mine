# pylint: disable=misplaced-comparison-constant,no-self-use

import os
import subprocess
import logging

import yorm

from mine import cli
from mine.models import (Application, Computer, Data, ProgramConfig,
                         State, Status, ProgramStatus)

from .conftest import FILES


log = logging.getLogger(__name__)


class TestFiles:
    """Integration tests for creating files."""

    def test_data(self):
        """Verify a sample file is created."""
        path = os.path.join(FILES, 'mine.yml')

        if os.path.exists(path):
            os.remove(path)

        data = Data()
        yorm.sync(data, path)

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

    def test_data_out(self):
        """Verify a sample file is created."""
        path = os.path.join(FILES, 'mine-out.yml')

        if os.path.exists(path):
            os.remove(path)

        data = Data()
        yorm.sync(data, path)

        itunes = Application('itunes')
        itunes.versions.mac = ''
        itunes.versions.windows = 'iTunes.exe'

        iphoto = Application('iphoto')
        iphoto.versions.mac = 'iPhoto'

        mac = Computer('macbook', 'Jaces-MacBook', 'AA:BB:CC:DD:EE:FF')
        mac2 = Computer('macbook-pro', 'Jaces-MacBook-2', '11:22:33:44:55:66')

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

    def test_data_in(self):
        """Verify a sample file is loaded."""
        path = os.path.join(FILES, 'mine-in.yml')

        data = Data()
        yorm.sync(data, path)

        assert data.config.applications
        for application in data.config.applications:
            if application.name == 'slack':
                break
        else:
            assert False


class TestProcesses:
    """Integration tests for tracking and stopping processes."""

    NAME = "example application"

    application = Application(NAME)
    application.versions.linux = 'yes'
    application.versions.mac = 'yes'
    application.versions.windows = 'yes.exe'

    computer = None
    data = None

    path = os.path.join(FILES, 'mine.tmp.yml')

    _process = None

    def _store_data(self):
        """Set up initial data file for tests."""
        self.data = Data()
        self.data.config.applications.append(self.application)
        self.computer = self.data.config.computers.get_current()  # pylint: disable=no-member
        yorm.sync(self.data, self.path)

    def _fetch_data(self):
        """Read the final data file back for verification."""
        data = Data()
        yorm.sync(data, self.path)
        return data

    def _start_application(self):
        """Start the example application."""
        if not self._process:
            # TODO: get filename from the application object
            self._process = subprocess.Popen(['yes'], stdout=subprocess.PIPE)
        log.info("%s is started", self.application)

    def _stop_application(self):
        """Stop the example application."""
        if self._process:
            if self._process.poll() is None:
                self._process.kill()
            self._process = None
        log.info("%s is stopped", self.application)

    def _is_application_running(self):
        """Determine if the sample application is running."""
        return self._process and self._process.poll() is None

    def teardown_method(self, _):
        """Stop the sample application and clean up the file."""
        self._stop_application()
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_case_1(self):
        """Verify a newly running remote application takes over."""

        # Arrange

        self._store_data()

        # start the application and manually mark it as running
        self._start_application()
        status = self.data.status
        status.start(self.application, self.computer)
        self.data.status = status
        assert self.data.status.is_running(self.application, self.computer)

        # manually mark the application as running on a remote computer
        computer = Computer('other', 'Other.local', 'AA:BB:CC:DD:EE:FF')
        status = self.data.status
        status.start(self.application, computer)
        self.data.status = status
        assert self.data.status.is_running(self.application, computer)

        # Act

        cli.run(self.path, cleanup=False)

        # Assert

        # verify the application is no longer running
        assert not self._is_application_running()
        # verify the application is marked as running remotely
        data = self._fetch_data()
        assert not data.status.is_running(self.application, self.computer)
        assert data.status.is_running(self.application, computer)

    def test_case_2(self):
        """Verify a newly running local application takes over."""

        # Arrange

        self._store_data()

        # manually mark the application as running on a remote computer
        computer = Computer('other', 'Other.local', 'AA:BB:CC:DD:EE:FF')
        status = self.data.status
        status.start(self.application, computer)
        self.data.status = status
        assert self.data.status.is_running(self.application, computer)

        # start the application
        self._start_application()

        # Act
        cli.run(self.path, cleanup=False)

        # Assert

        assert self._is_application_running()

        data = self._fetch_data()
        assert data.status.is_running(self.application, self.computer)
        assert data.status.is_running(self.application, computer)

    def test_case_3(self):
        """Verify an already running local application is ignored."""

        # Arrange

        self._store_data()

        status = self.data.status
        status.start(self.application, self.computer)
        self.data.status = status

        self._start_application()

        # Act

        cli.run(self.path)

        # Assert

        assert self._is_application_running()

        data = self._fetch_data()
        assert data.status.is_running(self.application, self.computer)

    def test_case_4(self):
        """Verify a newly stopped local application is noted."""

        # Arrange

        self._store_data()

        status = self.data.status
        status.start(self.application, self.computer)
        self.data.status = status

        self._stop_application()

        # Act

        cli.run(self.path)

        # Assert

        assert not self._is_application_running()

        data = self._fetch_data()
        assert not data.status.is_running(self.application, self.computer)

    def test_case_5(self):
        """Verify an already stopped local application is ignored."""

        # Arrange

        self._store_data()

        self._stop_application()

        # Act

        cli.run(self.path)

        # Assert

        assert not self._is_application_running()

        data = self._fetch_data()
        assert not data.status.is_running(self.application, self.computer)
