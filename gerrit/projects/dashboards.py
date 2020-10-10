#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.common import check
from gerrit.utils.exceptions import UnknownDashboard


class Dashboard:
    def __init__(self, project, json, gerrit):
        self.project = project
        self.json = json
        self.gerrit = gerrit

        self.id = None
        self.ref = None
        self.path = None
        self.description = None
        self.url = None
        self.is_default = None
        self.title = None
        self.sections = None

        if self.json is not None:
            self.__load__()

    def __repr__(self):
        return '%s(%s=%s)' % (self.__class__.__name__, 'id', self.id)

    def __load__(self):
        self.id = self.json.get('id')
        self.ref = self.json.get('ref')
        self.path = self.json.get('path')
        self.description = self.json.get('description')
        self.url = self.json.get('url')
        self.is_default = self.json.get('is_default', False)
        self.title = self.json.get('title')
        self.sections = self.json.get('sections', [])


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
            yield Dashboard(project=self.project, json=item, gerrit=self.gerrit)

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
        return Dashboard(project=self.project, json=result, gerrit=self.gerrit)

    def get(self, id: str) -> Dashboard:
        """
        Retrieves a project dashboard. The dashboard can be defined on that project or be inherited from a parent project.
        :param id: dashboard id
        :return:
        """
        endpoint = '/projects/%s/dashboards/%s' % (self.project, id)
        response = self.gerrit.make_call('get', endpoint)

        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            return Dashboard(project=self.project, json=result, gerrit=self.gerrit)
        else:
            raise UnknownDashboard(id)

    def delete(self, id: str):
        """
        Deletes a project dashboard.

        :param id: dashboard id
        :return:
        """
        endpoint = '/projects/%s/dashboards/%s' % (self.project, id)
        self.gerrit.make_call('delete', endpoint)
