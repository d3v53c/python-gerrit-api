#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.exceptions import UnknownPlugin
from gerrit.utils.models import BaseModel


class GerritPlugin(BaseModel):
    def __init__(self, **kwargs):
        super(GerritPlugin, self).__init__(**kwargs)
        self.attributes = ['id', 'index_url', 'filename', 'api_version', 'disabled', 'version', 'gerrit']

    def enable(self):
        """
        Enables a plugin on the Gerrit server.

        :return:
        """
        endpoint = '/plugins/%s/gerrit~enable' % self.id
        response = self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.plugins.get(result.get('id'))

    def disable(self):
        """
        Disables a plugin on the Gerrit server.

        :return:
        """
        endpoint = '/plugins/%s/gerrit~disable' % self.id
        response = self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.plugins.get(result.get('id'))

    def reload(self):
        """
        Reloads a plugin on the Gerrit server.

        :return:
        """
        endpoint = '/plugins/%s/gerrit~reload' % self.id
        response = self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.plugins.get(result.get('id'))


class GerritPlugins:
    def __init__(self, gerrit):
        self.gerrit = gerrit

    def list(self) -> list:
        """
        Lists the plugins installed on the Gerrit server.

        :return:
        """
        endpoint = '/plugins/?all'
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        plugins = [item for item in result.values()]
        return GerritPlugin.parse_list(plugins, gerrit=self.gerrit)

    def get(self, id: str) -> GerritPlugin:
        """

        :param id: plugin id
        :return:
        """
        endpoint = '/plugins/%s/gerrit~status' % id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))

        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            return GerritPlugin.parse(result, gerrit=self.gerrit)
        else:
            raise UnknownPlugin(id)

    def install(self, id: str, input_: dict) -> GerritPlugin:
        """
        Installs a new plugin on the Gerrit server.

        :param id: plugin id
        :param input_: the PluginInput entity
        :return:
        """
        endpoint = '/plugins/%s.jar' % id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return GerritPlugin.parse(result, gerrit=self.gerrit)
