#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.projects.project import GerritProject
from gerrit.utils.common import check


class GerritProjects:
    def __init__(self, gerrit):
        self.gerrit = gerrit

    def list(self) -> list:
        """
        Lists the projects accessible by the caller.

        :return:
        """
        endpoint = "/projects/?all"
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return GerritProject.parse_list(list(result.values()), gerrit=self.gerrit)

    def search(self, query: str) -> list:
        """
        Queries projects visible to the caller. The query string must be provided by the query parameter.
        The start and limit parameters can be used to skip/limit results.

        query parameter
          * name:'NAME' Matches projects that have exactly the name 'NAME'.
          * parent:'PARENT' Matches projects that have 'PARENT' as parent project.
          * inname:'NAME' Matches projects that a name part that starts with 'NAME' (case insensitive).
          * description:'DESCRIPTION' Matches projects whose description contains 'DESCRIPTION', using a full-text search.
          * state:'STATE' Matches project’s state. Can be either 'active' or 'read-only'.

        :param query:
        :return:
        """
        endpoint = "/projects/?query=%s" % query
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return GerritProject.parse_list(result, gerrit=self.gerrit)

    def get(self, project_name: str) -> GerritProject:
        """
        Retrieves a project.

        :param project_name: the name of the project
        :return:
        """
        endpoint = "/projects/%s" % project_name
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return GerritProject.parse(result, gerrit=self.gerrit)

    @check
    def create(self, project_name: str, input_: dict) -> GerritProject:
        """
        Creates a new project.

        .. code-block:: python

            input_ = {
                "description": "This is a demo project.",
                "submit_type": "INHERIT",
                "owners": [
                  "MyProject-Owners"
                ]
            }
            project = gerrit.projects.create('MyProject', input_)

        :param project_name: the name of the project
        :param input_: the ProjectInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#project-input

        :return:
        """
        endpoint = "/projects/%s" % project_name
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return GerritProject.parse(result, gerrit=self.gerrit)
