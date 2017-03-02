"""Hashcode qualification round 2017."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from operator import itemgetter
from .helpers import readarray
import numpy as np
from math import log2


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

    def add_video2(self, X, video, size_videos):
        """Add video to cache."""
        if video in self.videos:
            return True
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

    def _sort_connections(self):
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

    def save_data(self, validation=False):
        """Save data."""
        if validation is True:
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
                self.endpoints[i].connections.append((c, L_c))
            self.endpoints[i]._sort_connections()
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

    def _score_request(self, x, cache_id=None):
        if len(self.endpoints[x.R_e].connections) == 0:
            return 0
        if cache_id is None:
            return x.R_n * (self.endpoints[x.R_e].latency -
                            self.endpoints[x.R_e].connections[0][1])
        else:
            return [x.R_n * (self.endpoints[x.R_e].latency -
                             self.endpoints[x.R_e].connections[cid][1])
                    for cid in range(self.endpoints[x.R_e].K)]

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

    def romain(self):
        """Run Romain."""
        video_stats = [[list(), 0, set(), 0, 0] for _ in range(self.V)]
        for video_idx in range(self.V):
            for request in self.requests:
                if request.R_v == video_idx:
                    # ~available memory for the video
                    score1 = self.endpoints[request.R_e].K
                    score1 /= self.size_videos[video_idx] ** 3
                    # ~sum latency on caches
                    score2 = np.sum(self._score_request(request, 'all'))
                    score2 /= self.size_videos[video_idx] ** 3
                    video_stats[video_idx][0].append([request.R_e,
                                                      score1, score2])
                    video_stats[video_idx][1] = video_idx
                    video_stats[video_idx][2].add(request.R_e)
                    global_score1 = np.mean(
                        [tlp[1] for tlp in video_stats[video_idx][0]])
                    global_score2 = np.mean(
                        [tlp[2] for tlp in video_stats[video_idx][0]])
                    # print(global_score1)
                    # print(global_score2 / 1000000)
                    video_stats[video_idx][3] = global_score1
                    video_stats[video_idx][4] = global_score2
        video_stats.sort(key=itemgetter(4), reverse=True)
        video_stats.sort(key=itemgetter(3), reverse=True)

        for video in video_stats:
            if video[3] == 0:
                break
            for endpoint_id in video[2]:
                for c, L_v in self.endpoints[endpoint_id].connections:
                    # charge = 0
                    # charge = abs(self.X - self.caches[c].size) * .5
                    # charge = np.inf
                    # charge = self.size_videos[video[1]] / self.X
                    # if charge > .5 and abs(video[3]) < 10000:
                    #     break
                    if self.caches[c].add_video2(self.X, video[1],
                                                 self.size_videos):
                        break
        # print([video[3] for video in video_stats])
        # print([video[4] for video in video_stats])
        # print(self.size_videos[15], self.X)
        # print(self.endpoints[0].connections)

    def better(self):
        """Run better."""
        def score_request(x):
            if len(self.endpoints[x.R_e].connections) == 0:
                return 0
            return x.R_n * (self.endpoints[x.R_e].latency -
                            self.endpoints[x.R_e].connections[0][1])

        def score_new_request(x):
            if len(self.endpoints[x.R_e].connections) == 0:
                return 0
            previous_score = self.endpoints[x.R_e].latency
            for c, L_c in self.endpoints[x.R_e].connections:
                if x.R_v in self.caches[c].videos and L_c < previous_score:
                    previous_score = L_c
            return x.R_n * (previous_score -
                            self.endpoints[x.R_e].connections[0][1]) - \
                previous_score

        # 1. Sort requests by interest
        new_requests = list()
        for request in self.requests:
            heuristic = self._score_request(request)
            new_requests.append((heuristic, request))
        new_requests.sort(key=lambda x: x[0], reverse=True)

        # 2. Deal with requests in the specified order
        n = 0
        recompute = set([2**i for i in range(int(log2(self.R)))])
        while True:
            for _, request in new_requests:
                n += 1
                for c, L_c in self.endpoints[request.R_e].connections:
                    # connection is (c, L_c)
                    if self.caches[c].add_video2(self.X, request.R_v,
                                                 self.size_videos):
                        break
                if n in recompute:
                    break
            new_requests = new_requests[n:]
            if len(new_requests) == 0:
                break
            tmp_requests = list()
            for _, request in new_requests:
                heuristic = score_new_request(request)
                tmp_requests.append((heuristic, request))
            new_requests = sorted(tmp_requests, key=lambda x: x[0],
                                  reverse=True)

    def run_test(self):
        """Main test function."""
        pass

    def run(self):
        """Main function."""
        self.load_data()
        self.caches = [Cache(i, list()) for i in range(self.C)]
        # self.romain()
        # self.dummy()
        self.better()
        # print(self.scoring())
        self.save_data()
