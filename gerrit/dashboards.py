#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.common import check


class Dashboards:
    def __init__(self, project, gerrit):
        self.project = project
        self.gerrit = gerrit

    def list(self):
        """
        List custom dashboards for a project.

        :return:
        """
        endpoint = '/projects/%s/dashboards/' % self.project
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def create(self, name: str, DashboardInput: dict) -> dict:
        """
        Creates a project dashboard, if a project dashboard with the given dashboard ID doesn’t exist yet.

        :param name: the dashboard name
        :param DashboardInput: the DashboardInput entity
        :return:
        """
        endpoint = '/projects/%s/dashboards/%s' % (self.project, name)
        response = self.gerrit.make_call('put', endpoint, **DashboardInput)
        result = self.gerrit.decode_response(response)
        return result

    def get(self, name: str) -> dict:
        """
        Retrieves a project dashboard. The dashboard can be defined on that project or be inherited from a parent project.
        :param name:
        :return:
        """
        endpoint = '/projects/%s/dashboards/%s' % (self.project, name)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def delete(self, name: str):
        """
        Deletes a project dashboard.

        :param name:
        :return:
        """
        endpoint = '/projects/%s/dashboards/%s' % (self.project, name)
        self.gerrit.make_call('delete', endpoint)
