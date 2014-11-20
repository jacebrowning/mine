#!/usr/bin/env python

"""Sample test module."""

import unittest

from mine import sample


class TestMine(unittest.TestCase):

    """Sample test class."""

    def test_branch_coverage(self):
        """Sample test method for branch coverage."""
        self.assertEquals(sample.function(True), 'True')
        self.assertEquals(sample.function(False), 'False')
        self.assertEquals(sample.function(None), 'None')
