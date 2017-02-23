"""Hashcode qualification round 2017."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from .helpers import test

import numpy as np


class Main:
    """Main class."""

    def __init__(self):
        """Test init."""
        self._version = 1.0
        self._data = None

    def __str__(self):
        """String representation."""
        return 'Main version %d' % (self._version)

    def load_data(self, filename):
        """Load datafile."""
        with open(filename, 'r') as file:
            header = file.readline()
            print(header)

            line = file.readline()
            n_lines, n_cases = [int(num) for num in line.split()]

            self._data = np.empty((n_lines, n_cases))
            for i in range(n_lines):
                line = file.readline()
                self._data[i, :] = [int(num) for num in line.split()]

    def run(self):
        """Main function."""
        print(self)
        self.load_data('./data/dummy.dat')
        print(test(self._data))
