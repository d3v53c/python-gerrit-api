#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
import json
from gerrit.utils.requester import Requester
from gerrit.config.config import GerritConfig
from gerrit.projects.projects import GerritProjects
from gerrit.accounts.accounts import GerritAccounts
from gerrit.groups.groups import GerritGroups


class GerritClient:
    GERRIT_AUTH_SUFFIX = '/a'
    default_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    def __init__(
            self,
            base_url: str,
            username: str,
            password: str,
            ssl_verify: bool = True,
            cert: str = None,
            timeout: int = 60,
            max_retries: int = None):
        self._base_url = self.strip_trailing_slash(base_url)

        self.requester = Requester(
            username=username,
            password=password,
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

    def get_endpoint_url(self, endpoint):
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

    @property
    def config(self):
        return GerritConfig(gerrit=self)

    @property
    def projects(self):
        return GerritProjects(gerrit=self)

    @property
    def accounts(self):
        return GerritAccounts(gerrit=self)

    @property
    def groups(self):
        return GerritGroups(gerrit=self)
