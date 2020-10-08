#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.project import GerritProject


class GerritProjects:
    def __init__(self, gerrit):
        self.gerrit = gerrit

    def list(self):
        """
        Lists the projects accessible by the caller.

        :return:
        """
        endpoint = '/projects/?all'
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        for item in result.values():
            yield GerritProject(id=item.get('id'), gerrit=self.gerrit)

    def search(self, query):
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
        endpoint = '/projects/?query=%s' % query
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        for item in result:
            yield GerritProject(id=item.get('id'), gerrit=self.gerrit)

    def get(self, project_name):
        """
        Retrieves a project.

        :param project_name: the name of the project
        :return:
        """
        return GerritProject(id=project_name, gerrit=self.gerrit)

    def create(self, project_name, ProjectInput):
        """
        Creates a new project.

        :param project_name: the name of the project
        :param ProjectInput: the ProjectInput entity
        :return:
        """
        endpoint = '/projects/%s' % project_name
        response = self.gerrit.make_call('put', endpoint, **ProjectInput)
        result = self.gerrit.decode_response(response)
        return GerritProject(id=result.get('id'), gerrit=self.gerrit)
