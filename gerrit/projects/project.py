#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.projects.branches import Branches
from gerrit.projects.tags import Tags
from gerrit.projects.commit import Commit
from gerrit.projects.dashboards import Dashboards
from gerrit.projects.webhooks import Webhooks
from gerrit.utils.common import check
from gerrit.utils.models import BaseModel


class GerritProject(BaseModel):
    def __init__(self, **kwargs):
        super(GerritProject, self).__init__(**kwargs)
        self.attributes = ['id', 'name', 'state', 'labels', 'web_links', 'gerrit']

    @property
    def description(self) -> str:
        """
        Retrieves the description of a project.

        :return:
        """
        endpoint = '/projects/%s/description' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_description(self, input_: dict) -> str:
        """
        Sets the description of a project.

        :param input_: the ProjectDescriptionInput entity.
        :return:
        """
        endpoint = '/projects/%s/description' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    def delete_description(self):
        endpoint = '/projects/%s/description' % self.id
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))

    def delete(self):
        """
        Delete the project, requires delete-project plugin

        :return:
        """
        endpoint = '/projects/%s/delete-project~delete' % self.id
        self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))

    @property
    def parent(self) -> str:
        """
        Retrieves the name of a project’s parent project. For the All-Projects root project an empty string is returned.

        :return:
        """
        endpoint = '/projects/%s/parent' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_parent(self, input_: dict) -> str:
        """
        Sets the parent project for a project.

        :param input_: The ProjectParentInput entity.
        :return:
        """
        endpoint = '/projects/%s/parent' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    @property
    def HEAD(self) -> str:
        """
        Retrieves for a project the name of the branch to which HEAD points.

        :return:
        """
        endpoint = '/projects/%s/HEAD' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_HEAD(self, input_: dict) -> str:
        """
        Sets HEAD for a project.

        :param input_: The HeadInput entity.
        :return:
        """
        endpoint = '/projects/%s/HEAD' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    @property
    def config(self) -> dict:
        """
        Gets some configuration information about a project.
        Note that this config info is not simply the contents of project.config; it generally contains fields that may
        have been inherited from parent projects.

        :return:
        """
        endpoint = '/projects/%s/config' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_config(self, input_: dict) -> dict:
        """
        Sets the configuration of a project.

        :param input_: the ConfigInput entity.
        :return:
        """
        endpoint = '/projects/%s/config' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    def get_statistics(self) -> dict:
        """
        Return statistics for the repository of a project.

        :return:
        """
        endpoint = '/projects/%s/statistics.git' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def run_garbage_collection(self, input_: dict) -> str:
        """
        Run the Git garbage collection for the repository of a project.

        :param input_: the GCInput entity
        :return:
        """
        endpoint = '/projects/%s/gc' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def ban_commits(self, input_: dict) -> dict:
        """
        Marks commits as banned for the project.

        :param input_: the BanInput entity.
        :return:
        """
        endpoint = '/projects/%s/ban' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    @property
    def access_rights(self) -> dict:
        """
        Lists the access rights for a single project.

        :return:
        """
        endpoint = '/projects/%s/access' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_access_rights(self, input_: dict) -> dict:
        """
        Sets access rights for the project using the diff schema provided by ProjectAccessInput.

        :param input_: the ProjectAccessInput entity
        :return:
        """
        endpoint = '/projects/%s/access' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    def check_access(self, options: str) -> dict:
        """
        runs access checks for other users.

        :param options:
        Check Access Options
          * Account(account): The account for which to check access. Mandatory.
          * Permission(perm): The ref permission for which to check access.
            If not specified, read access to at least branch is checked.
          * Ref(ref): The branch for which to check access. This must be given if perm is specified.
        :return:
        """
        endpoint = '/projects/%s/check.access?%s' % (self.id, options)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def index(self, input_: dict):
        """
        Adds or updates the current project (and children, if specified) in the secondary index.
        The indexing task is executed asynchronously in background and this command returns immediately
        if async is specified in the input.

        :param input_: the IndexProjectInput entity
        :return:
        """
        endpoint = '/projects/%s/index' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)

    def index_change(self):
        """
        Adds or updates the current project (and children, if specified) in the secondary index.
        The indexing task is executed asynchronously in background and this command returns immediately
        if async is specified in the input.

        :return:
        """
        endpoint = '/projects/%s/index.changes' % self.id
        self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))

    @check
    def check_consistency(self, input_: dict) -> dict:
        """
        Performs consistency checks on the project.

        :param input_: the CheckProjectInput entity
        :return:
        """
        endpoint = '/projects/%s/check' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    @property
    def branches(self) -> Branches:
        """
        List the branches of a project. except the refs/meta/config

        :return:
        """
        return Branches(self.id, self.gerrit)

    @property
    def child_projects(self) -> list:
        """
        List the direct child projects of a project.

        :return:
        """
        endpoint = '/projects/%s/children/' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return [self.gerrit.projects.get(item.get('id')) for item in result]

    @property
    def tags(self) -> Tags:
        """
        List the tags of a project.

        :return:
        """
        return Tags(self.id, self.gerrit)

    def get_commit(self, commit: str) -> Commit:
        """
        Retrieves a commit of a project.

        :return:
        """
        endpoint = '/projects/%s/commits/%s' % (self.id, commit)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return Commit.parse(result, project=self.id, gerrit=self.gerrit)

    @property
    def dashboards(self) -> Dashboards:
        """
        gerrit dashboards operations

        :return:
        """
        return Dashboards(project=self.id, gerrit=self.gerrit)

    @property
    def webhooks(self) -> Webhooks:
        """
        gerrit webhooks operations, requires delete-project plugin

        :return:
        """
        return Webhooks(project=self.id, gerrit=self.gerrit)
