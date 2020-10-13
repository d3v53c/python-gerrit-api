#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.config.caches import Caches
from gerrit.config.tasks import Tasks
from gerrit.utils.common import check


class GerritConfig:
    def __init__(self, gerrit):
        self.gerrit = gerrit

    def get_version(self) -> str:
        """
        get the version of the Gerrit server.

        :return:
        """
        endpoint = '/config/server/version'
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def get_server_info(self) -> dict:
        """
        get the information about the Gerrit server configuration.

        :return:
        """
        endpoint = '/config/server/info'
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def check_consistency(self, input_: dict) -> dict:
        """
        Runs consistency checks and returns detected problems.

        :param input_: the ConsistencyCheckInput entity
        :return:
        """
        endpoint = '/config/server/check.consistency'
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    def reload_config(self) -> dict:
        """
        Reloads the gerrit.config configuration.

        :return:
        """
        endpoint = '/config/server/reload'
        response = self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def confirm_email(self, input_: dict):
        """
        Confirms that the user owns an email address.

        :param input_: the EmailConfirmationInput entity
        :return:
        """
        endpoint = '/config/server/email.confirm'
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        response.raise_for_status()

    @property
    def caches(self) -> Caches:
        return Caches(gerrit=self.gerrit)

    def get_summary(self) -> dict:
        """
        Retrieves a summary of the current server state.

        :return:
        """
        endpoint = '/config/server/summary'
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def list_capabilities(self) -> dict:
        """
        Lists the capabilities that are available in the system.
        There are two kinds of capabilities: core and plugin-owned capabilities.

        :return:
        """
        endpoint = '/config/server/capabilities'
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @property
    def tasks(self) -> Tasks:
        return Tasks(gerrit=self.gerrit)

    def get_top_menus(self) -> list:
        """
        Returns the list of additional top menu entries.

        :return:
        """
        endpoint = '/config/server/top-menus'
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def get_default_user_preferences(self) -> dict:
        """
        Returns the default user preferences for the server.

        :return:
        """
        endpoint = '/config/server/preferences'
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_default_user_preferences(self, input_: dict) -> dict:
        """
        Sets the default user preferences for the server.

        :param input_: the PreferencesInput entity
        :return:
        """
        endpoint = '/config/server/preferences'
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    def get_default_diff_preferences(self) -> dict:
        """
        Returns the default diff preferences for the server.

        :return:
        """
        endpoint = '/config/server/preferences.diff'
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_default_diff_preferences(self, input_: dict) -> dict:
        """
        Sets the default diff preferences for the server.

        :param input_: the DiffPreferencesInput entity
        :return:
        """
        endpoint = '/config/server/preferences.diff'
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    def get_default_edit_preferences(self) -> dict:
        """
        Returns the default edit preferences for the server.

        :return:
        """
        endpoint = '/config/server/preferences.edit'
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_default_edit_preferences(self, input_: dict) -> dict:
        """
        Sets the default edit preferences for the server.

        :param input_: the EditPreferencesInfo entity
        :return:
        """
        endpoint = '/config/server/preferences.edit'
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    def index_changes(self, input_: dict):
        """
        Index a set of changes

        :param input_: the IndexChangesInput entity
        :return:
        """
        endpoint = '/config/server/index.changes'
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        response.raise_for_status()
