"""Auxiliary functions for hashcode qualification round 2017."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np


def test(data):
    """Test function."""
    return np.exp(data)


def readint():
    """Read array on standard input."""
    return int(raw_input())


def readarray(f):
    """Read array on standard output."""
    return map(f, raw_input().split())
