#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
import json
from gerrit.requester import Requester
from gerrit.config import GerritConfig
from gerrit.projects import GerritProjects


class GerritClient:
    GERRIT_AUTH_SUFFIX = '/a'

    def __init__(
            self,
            base_url,
            username,
            password,
            ssl_verify=True,
            cert=None,
            timeout=60,
            max_retries=None):
        self._base_url = self.strip_trailing_slash(base_url)

        self.requester = Requester(
            username,
            password,
            base_url=self._base_url,
            ssl_verify=ssl_verify,
            cert=cert,
            timeout=timeout,
            max_retries=max_retries
        )

    @classmethod
    def strip_trailing_slash(cls, url):
        """
        remove url's trailing slash
        :param url:
        :return:
        """
        while url.endswith('/'):
            url = url[:-1]
        return url

    def _get_endpoint_url(self, endpoint):
        """
        Return the complete url including host and port for a given endpoint.
        :param endpoint: service endpoint as str
        :return: complete url (including host and port) as str
        """
        return '{}{}{}'.format(self._base_url, self.GERRIT_AUTH_SUFFIX, endpoint)

    @staticmethod
    def decode_response(response):
        """Strip off Gerrit's magic prefix and decode a response.
        :returns:
            Decoded JSON content as a dict, or raw text if content could not be
            decoded as JSON.
        :raises:
            requests.HTTPError if the response contains an HTTP error status code.
        """
        magic_json_prefix = ")]}'\n"
        content_type = response.headers.get("content-type", "")
        response.raise_for_status()
        content = response.content.strip()
        if response.encoding:
            content = content.decode(response.encoding)
        if not content:
            return content
        if content_type.split(";")[0] != "application/json":
            return content
        if content.startswith(magic_json_prefix):
            index = len(magic_json_prefix)
            content = content[index:]
        try:
            return json.loads(content)
        except ValueError:
            raise ValueError("Invalid json content: %s", content)

    def make_call(self, method, endpoint, **data):
        call = getattr(self.requester, method.lower())
        base_url = self._get_endpoint_url(endpoint)

        if method.lower() == 'get' or method.lower() == 'delete':
            res = call(base_url, params=data or {})
        else:
            res = call(base_url, json=data or {}, headers={'content-type': 'application/json'})

        return res

    @property
    def config(self):
        return GerritConfig(gerrit=self)

    @property
    def projects(self):
        return GerritProjects(gerrit=self)