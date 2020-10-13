#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.exceptions import UnknownCache
from gerrit.utils.models import BaseModel


class Cache(BaseModel):
    def __init__(self, **kwargs):
        super(Cache, self).__init__(**kwargs)
        self.attributes = ['name', 'type', 'entries', 'average_get', 'hit_ratio', 'gerrit']

    def flush(self):
        """
        Flushes a cache.

        :return:
        """
        endpoint = '/config/server/caches/%s/flush' % self.name
        response = self.gerrit.make_call('post', endpoint)
        response.raise_for_status()


class Caches:
    def __init__(self, gerrit):
        self.gerrit = gerrit

    def list(self) -> list:
        """
        Lists the caches of the server. Caches defined by plugins are included.

        :return:
        """
        endpoint = '/config/server/caches/'
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)

        caches = []
        for key, value in result.items():
            cache = value
            cache.update({'name': key})
            caches.append(cache)

        return Cache.parse_list(caches, gerrit=self.gerrit)

    def get(self, name: str) -> Cache:
        """
        Retrieves information about a cache.

        :param name: cache name
        :return:
        """
        endpoint = '/config/server/caches/%s' % name
        response = self.gerrit.make_call('get', endpoint)
        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            return Cache.parse(result, gerrit=self.gerrit)
        else:
            raise UnknownCache(name)

    def operation(self, CacheOperationInput: dict):
        """
        Cache Operations

        :param CacheOperationInput: the CacheOperationInput entity
        :return:
        """
        endpoint = '/config/server/caches/'
        response = self.gerrit.make_call('post', endpoint, **CacheOperationInput)
        response.raise_for_status()
