# -*- coding: utf-8 -*-

import pytest
from markdown_for_science.skeleton import fib

__author__ = "Evan"
__copyright__ = "Evan"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
