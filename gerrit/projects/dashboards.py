#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.common import check
from gerrit.utils.exceptions import UnknownDashboard
from gerrit.utils.models import BaseModel


class Dashboard(BaseModel):
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)
        self.attributes = ['id', 'ref', 'path', 'description', 'url', 'is_default', 'title', 'sections', 'project',
                           'gerrit']

    def delete(self):
        """
        Deletes a project dashboard.

        :return:
        """
        endpoint = '/projects/%s/dashboards/%s' % (self.project, self.id)
        response = self.gerrit.make_call('delete', endpoint)
        response.raise_for_status()


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
        return Dashboard.parse_list(result, project=self.project, gerrit=self.gerrit)

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
        return Dashboard.parse(result, project=self.project, gerrit=self.gerrit)

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
            return Dashboard.parse(result, project=self.project, gerrit=self.gerrit)
        else:
            raise UnknownDashboard(id)
