"""Auxiliary functions for hashcode qualification round 2017."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np


def readint():
    """Read array on standard input."""
    return int(input())


def readarray(f):
    """Read array on standard output."""
    return map(f, input().split())
