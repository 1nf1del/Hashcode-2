"""Hashcode qualification round 2017."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from .helpers import test

import numpy as np

def readint(): return int(raw_input())
def readarray(f): return map(f, raw_input().split())



class Main:
    """Main class."""

    def __init__(self):
        """Test init."""
        self._version = 1.0
        self._data = None

    def __str__(self):
        """String representation."""
        return 'Main version %d' % (self._version)

    def load_data(self):
        T = readint()
        
        for t in range(1, T + 1):
            S = raw_input()
            s = S[0]
            for l in range(1, len(S)):
                if S[l] < s[0]:
                    s += S[l]
                else:
                    s = S[l] + s
            print "Case #%d: %s" % (t, s)

    def run(self):
        """Main function."""
        self.load_data()
        print(test(self._data))
