#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.common import check
from gerrit.utils.exceptions import UnknownDashboard


class Dashboard:
    def __init__(self, project, id, gerrit):
        self.project = project
        self.id = id
        self.gerrit = gerrit

        self.ref = None
        self.path = None
        self.description = None
        self.url = None
        self.is_default = None
        self.title = None
        self.sections = None

        self.__load__()

    def __repr__(self):
        return '%s(%s=%s)' % (self.__class__.__name__, 'id', self.id)

    def __load__(self):
        endpoint = '/projects/%s/dashboards/%s' % (self.project, self.id)
        response = self.gerrit.make_call('get', endpoint)
        if response.status_code < 300:
            result = self.gerrit.decode_response(response)

            self.ref = result.get('ref')
            self.path = result.get('path')
            self.description = result.get('description')
            self.url = result.get('url')
            self.is_default = result.get('is_default', False)
            self.title = result.get('title')
            self.sections = result.get('sections', [])
        raise UnknownDashboard(self.id)


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

        for item in result:
            yield Dashboard(project=self.project, id=item.get('id'), gerrit=self.gerrit)

    @check
    def create(self, name: str, DashboardInput: dict) -> Dashboard:
        """
        Creates a project dashboard, if a project dashboard with the given dashboard ID doesn’t exist yet.

        :param name: the dashboard name
        :param DashboardInput: the DashboardInput entity
        :return:
        """
        endpoint = '/projects/%s/dashboards/%s' % (self.project, name)
        response = self.gerrit.make_call('put', endpoint, **DashboardInput)
        result = self.gerrit.decode_response(response)
        return Dashboard(project=self.project, id=result.get('id'), gerrit=self.gerrit)

    def get(self, name: str) -> Dashboard:
        """
        Retrieves a project dashboard. The dashboard can be defined on that project or be inherited from a parent project.
        :param name:
        :return:
        """
        return Dashboard(project=self.project, id=name, gerrit=self.gerrit)

    def delete(self, name: str):
        """
        Deletes a project dashboard.

        :param name:
        :return:
        """
        endpoint = '/projects/%s/dashboards/%s' % (self.project, name)
        self.gerrit.make_call('delete', endpoint)
