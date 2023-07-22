# pylint: disable=unused-variable

import datafiles
import pytest

from mine.models import Data


def describe_data():
    @pytest.fixture
    def data(monkeypatch):
        monkeypatch.setattr(datafiles.settings, "HOOKS_ENABLED", False)
        return Data("../../tests/files/mine.yml")

    def describe_repr():
        def it_should_always_be_a_simple_name(data: Data):
            assert "settings" == repr(data)

    def describe_modified():
        def is_false_initially(data: Data):
            assert False is data.modified

        def is_true_when_the_counter_changes(data: Data):
            data.status.counter += 1

            assert True is data.modified

        def is_false_after_reading(data: Data):
            data.status.counter += 1

            print(data.modified)

            assert False is data.modified

    def describe_prune_status():
        def it_can_preserve_counter(data: Data):
            data.datafile.load()  # type: ignore
            assert data.status.counter > 0
            data.prune_status()
            assert data.status.counter > 0

        def it_can_reset_counter(data: Data):
            data.datafile.load()  # type: ignore
            assert data.status.counter > 0
            data.prune_status(reset_counter=True)
            assert data.status.counter == 0
