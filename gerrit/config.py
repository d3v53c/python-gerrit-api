#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.common import GET, POST


class GerritConfig:
    def __init__(self, gerrit):
        self.gerrit = gerrit

    @GET('/config/server/version')
    def get_version(self):
        """
        get the version of the Gerrit server.

        :return:
        """

    @GET('/config/server/info')
    def get_server_info(self):
        """
        get the information about the Gerrit server configuration.

        :return:
        """

    # @POST('/config/server/check.consistency')
    # def check_consistency(self, check_accounts=None, check_account_external_ids=None):
    #     """
    #     Runs consistency checks and returns detected problems.
    #
    #     :return:
    #     """

    @POST('/config/server/reload')
    def reload_config(self):
        """
        Reloads the gerrit.config configuration.

        :return:
        """

