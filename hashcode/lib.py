"""Hashcode qualification round 2017."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from .helpers import readarray


class Cache:
    """Class cache."""

    def __init__(self, id, videos):
        """Init cache."""
        self.id = id
        self.videos = set(videos)


class Endpoint:
    """Class for endpoints."""

    def __init__(self, endpoint, latency, K):
        """Init endpoints."""
        self.endpoint = endpoint  # Id enpoint
        self.latency = latency
        self.K = K
        # {c: L_c} where c: ID cache server, L_c: latency
        self.connections = dict()


class Request:
    """Class for requests."""

    def __init__(self, request, R_v, R_e, R_n):
        """Init requests."""
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

    def validation(self):
        """Validate save."""

    def save_data(self):
        """Save data."""
        n_caches = len(self.caches)
        print(n_caches)
        for i in range(n_caches):
            print(self.caches[i].id, *self.caches[i].videos)

    def load_data(self):
        """Load data."""
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

    def scoring(self):
        average = 0.
        for request in self.requests:
            maximum = self.endpoints[request.R_e].latency
            for c, L_c in self.enpoints[request.R_e].connections.items:
                if request.R_v in self.caches[c] and L_c < maximum:
                    maximum = L_c
            average += (self.endpoints[request.R_e].latency - maximum)
        return average * 1000 / self.R

    def run(self):
        """Main function."""
        self.load_data()
        self.caches = [Cache(0, [2]), Cache(1, [3, 1]), Cache(2, [0, 1])]
        self.save_data()
