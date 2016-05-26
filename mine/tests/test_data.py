# pylint: disable=misplaced-comparison-constant,unused-variable

import pytest

from mine.data import Data


def describe_data():

    @pytest.fixture
    def data():
        return Data()

    def describe_repr():

        def it_should_always_be_a_simple_name(data):
            assert "settings" == repr(data)

    def describe_modified():

        def is_false_initially(data):
            assert False is data.modified

        def is_true_when_the_counter_changes(data):
            data.status.counter += 1

            assert True is data.modified

        def is_false_after_reading(data):
            data.status.counter += 1

            print(data.modified)

            assert False is data.modified
