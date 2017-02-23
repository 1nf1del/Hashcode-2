"""Hashcode qualification round 2017."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from .helpers import test

import numpy as np

def readint(): return int(input())
def readarray(f): return map(f, input().split())


class Endpoint:

    def __init__(self, endpoint, latency, K):
        self.endpoint = endpoint    # Id enpoint
        self.latency = latency
        self.K = K
        self.connections = dict()   # {c: L_c} where c: ID cache server, L_c: latency

class Request:
    def __init__(self, request, R_v, R_e, R_n):
        self.request = request  # Id request
        self.R_v = R_v  # Id video
        self.R_e = R_e  # Id endpoint
        self.R_n = R_n  # Number of requests

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
        self.V, self.E, self.R, self.C, self.X = readarray(int)
        self.size_videos = readarray(int)
        self.endpoints = list()
        for i in range(self.E):
            l, K = readarray(int)
            self.endpoints.append(Endpoint(i, l, K))
            for j in range(K):
                c, L_c = readarray(int)
                self.endpoints[i].connections[c] = L_c
        self.requests = list()
        for i in range(self.R):
            R_v, R_e, R_n = readarray(int)
            self.requests.append(Request(i, R_v, R_e, R_n))
        print(self.R)
        print(len(self.requests))

    def run(self):
        """Main function."""
        self.load_data()
        print(test(self._data))
