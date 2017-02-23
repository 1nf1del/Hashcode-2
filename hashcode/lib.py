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
        self.size = 0.

    def add_video(self, X, video, size_videos):
        """Add video to cache."""
        if video in self.videos:
            return False
        if self.size + size_videos[video] > X:
            return False
        self.size += size_videos[video]
        self.videos.add(video)
        return True


class Endpoint:
    """Class for endpoints."""

    def __init__(self, endpoint, latency, K):
        """Init endpoints."""
        self.endpoint = endpoint  # Id enpoint
        self.latency = latency
        self.K = K
        # (c, L_c) where c: ID cache server, L_c: latency
        self.connections = list()

    def sort_connections(self):
        self.connections.sort(key=lambda x: x[1])


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
        """Validate before save."""
        good = True
        for i in range(len(self.caches)):
            size = 0
            for video_id in self.caches[i].videos:
                # print(video_id, len(self.size_videos))
                size += self.size_videos[video_id]
            if size > self.X:
                good = False
                break

        if good is False:
            raise ValueError('Too much memory use for cache %d' % i)

    def save_data(self):
        """Save data."""
        self.validation()
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
                self.endpoints[i].connections.append(c, L_c)
            self.endpoints[i].sort_connections()
        self.requests = list()
        for i in range(self.R):
            R_v, R_e, R_n = readarray(int)
            self.requests.append(Request(i, R_v, R_e, R_n))

    def scoring(self):
        """Scoring function."""
        average = 0.
        number_requests = 0.
        for request in self.requests:
            maximum = self.endpoints[request.R_e].latency
            for c, L_c in self.endpoints[request.R_e].connections:
                if request.R_v in self.caches[c].videos and L_c < maximum:
                    maximum = L_c
            average += request.R_n * (self.endpoints[request.R_e].latency -
                                      maximum)
            number_requests += request.R_n
        return average * 1000 / number_requests

    def dummy(self):
        """Run dummy."""
        boolean = True
        while boolean:
            boolean = False
            v = 0
            while v < self.V:
                for cache in self.caches:
                    if cache.add_video(self.X, v, self.size_videos):
                        boolean = True
                    v += 1

    def better(self):
        for request in self.requests:
            for connection in self.endpoints[request.R_e].connections:

    def run(self):
        """Main function."""
        self.load_data()
        self.caches = [Cache(i, list()) for i in range(self.C)]
        self.dummy()
        # print(self.scoring())
        self.save_data()
