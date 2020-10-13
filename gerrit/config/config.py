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
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def get_server_info(self) -> dict:
        """
        get the information about the Gerrit server configuration.

        :return:
        """
        endpoint = '/config/server/info'
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def check_consistency(self, ConsistencyCheckInput: dict) -> dict:
        """
        Runs consistency checks and returns detected problems.

        :param ConsistencyCheckInput: the ConsistencyCheckInput entity
        :return:
        """
        endpoint = '/config/server/check.consistency'
        response = self.gerrit.make_call('post', endpoint, **ConsistencyCheckInput)
        result = self.gerrit.decode_response(response)
        return result

    def reload_config(self) -> dict:
        """
        Reloads the gerrit.config configuration.

        :return:
        """
        endpoint = '/config/server/reload'
        response = self.gerrit.make_call('post', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def confirm_email(self, EmailConfirmationInput: dict):
        """
        Confirms that the user owns an email address.

        :param EmailConfirmationInput: the EmailConfirmationInput entity
        :return:
        """
        endpoint = '/config/server/email.confirm'
        response = self.gerrit.make_call('put', endpoint, **EmailConfirmationInput)
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
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def list_capabilities(self) -> dict:
        """
        Lists the capabilities that are available in the system.
        There are two kinds of capabilities: core and plugin-owned capabilities.

        :return:
        """
        endpoint = '/config/server/capabilities'
        response = self.gerrit.make_call('get', endpoint)
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
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def get_default_user_preferences(self) -> dict:
        """
        Returns the default user preferences for the server.

        :return:
        """
        endpoint = '/config/server/preferences'
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_default_user_preferences(self, PreferencesInput: dict) -> dict:
        """
        Sets the default user preferences for the server.

        :param PreferencesInput: the PreferencesInput entity
        :return:
        """
        endpoint = '/config/server/preferences'
        response = self.gerrit.make_call('put', endpoint, **PreferencesInput)
        result = self.gerrit.decode_response(response)
        return result

    def get_default_diff_preferences(self) -> dict:
        """
        Returns the default diff preferences for the server.

        :return:
        """
        endpoint = '/config/server/preferences.diff'
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_default_diff_preferences(self, DiffPreferencesInput: dict) -> dict:
        """
        Sets the default diff preferences for the server.

        :param DiffPreferencesInput: the DiffPreferencesInput entity
        :return:
        """
        endpoint = '/config/server/preferences.diff'
        response = self.gerrit.make_call('put', endpoint, **DiffPreferencesInput)
        result = self.gerrit.decode_response(response)
        return result

    def get_default_edit_preferences(self) -> dict:
        """
        Returns the default edit preferences for the server.

        :return:
        """
        endpoint = '/config/server/preferences.edit'
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_default_edit_preferences(self, EditPreferencesInfo: dict) -> dict:
        """
        Sets the default edit preferences for the server.

        :param EditPreferencesInfo: the EditPreferencesInfo entity
        :return:
        """
        endpoint = '/config/server/preferences.edit'
        response = self.gerrit.make_call('put', endpoint, **EditPreferencesInfo)
        result = self.gerrit.decode_response(response)
        return result

    def index_changes(self, IndexChangesInput: dict):
        """
        Index a set of changes

        :param IndexChangesInput: the IndexChangesInput entity
        :return:
        """
        endpoint = '/config/server/index.changes'
        response = self.gerrit.make_call('post', endpoint, **IndexChangesInput)
        response.raise_for_status()
