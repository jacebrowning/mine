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
