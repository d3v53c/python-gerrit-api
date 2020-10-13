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
        response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
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
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return Dashboard.parse_list(result, project=self.project, gerrit=self.gerrit)

    @check
    def create(self, name: str, input_: dict) -> Dashboard:
        """
        Creates a project dashboard, if a project dashboard with the given dashboard ID doesn’t exist yet.

        :param name: the dashboard name
        :param input_: the DashboardInput entity
        :return:
        """
        endpoint = '/projects/%s/dashboards/%s' % (self.project, name)
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return Dashboard.parse(result, project=self.project, gerrit=self.gerrit)

    def get(self, id: str) -> Dashboard:
        """
        Retrieves a project dashboard. The dashboard can be defined on that project or be inherited from a parent project.
        :param id: dashboard id
        :return:
        """
        endpoint = '/projects/%s/dashboards/%s' % (self.project, id)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))

        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            return Dashboard.parse(result, project=self.project, gerrit=self.gerrit)
        else:
            raise UnknownDashboard(id)
