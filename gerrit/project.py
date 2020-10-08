#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.branches import Branches
from gerrit.tags import Tags
from gerrit.commit import Commit
from gerrit.exceptions import UnknownProject


class GerritProject:
    def __init__(self, id, gerrit):
        self.id = id
        self.gerrit = gerrit

        self.name = None
        self.labels = None
        self.state = None
        self.web_links = None

        self.__load__()

    def __load__(self):
        endpoint = '/projects/%s' % self.id
        response = self.gerrit.make_call('get', endpoint)

        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            self.name = result.get('name')
            self.labels = result.get('labels')
            self.state = result.get('state')
            self.web_links = result.get('web_links')
        else:
            raise UnknownProject(self.id)

    def __repr__(self):
        return '%s(%s=%s)' % (self.__class__.__name__, 'id', self.id)

    @property
    def description(self):
        """s
        Retrieves the description of a project.

        :return:
        """
        endpoint = '/projects/%s/description' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def set_description(self, ProjectDescriptionInput: dict):
        """
        Sets the description of a project.

        :param ProjectDescriptionInput: the ProjectDescriptionInput entity.
        :return:
        """
        endpoint = '/projects/%s/description' % self.id
        self.gerrit.make_call('put', endpoint, **ProjectDescriptionInput)

    def delete_description(self):
        endpoint = '/projects/%s/description' % self.id
        self.gerrit.make_call('delete', endpoint)

    @property
    def parent(self):
        """
        Retrieves the name of a project’s parent project. For the All-Projects root project an empty string is returned.

        :return:
        """
        endpoint = '/projects/%s/parent' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def set_parent(self, ProjectParentInput: dict):
        """
        Sets the parent project for a project.

        :param ProjectParentInput: The ProjectParentInput entity.
        :type dict
        :return:
        """
        endpoint = '/projects/%s/parent' % self.id
        self.gerrit.make_call('put', endpoint, **ProjectParentInput)

    @property
    def HEAD(self):
        """
        Retrieves for a project the name of the branch to which HEAD points.

        :return:
        """
        endpoint = '/projects/%s/HEAD' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def set_HEAD(self, HeadInput: dict):
        """
        Sets HEAD for a project.

        :param HeadInput: The HeadInput entity.
        :return:
        """
        endpoint = '/projects/%s/HEAD' % self.id
        self.gerrit.make_call('put', endpoint, **HeadInput)

    @property
    def config(self):
        """
        Gets some configuration information about a project.
        Note that this config info is not simply the contents of project.config; it generally contains fields that may
        have been inherited from parent projects.

        :return:
        """
        endpoint = '/projects/%s/config' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def set_config(self, ConfigInput: dict):
        """
        Sets the configuration of a project.

        :param ConfigInput: the ConfigInput entity.
        :return:
        """
        endpoint = '/projects/%s/config' % self.id
        self.gerrit.make_call('put', endpoint, **ConfigInput)

    def get_statistics(self):
        """
        Return statistics for the repository of a project.

        :return:
        """
        endpoint = '/projects/%s/statistics.git' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def run_garbage_collection(self, GCInput: dict):
        """
        Run the Git garbage collection for the repository of a project.

        :param GCInput: the GCInput entity
        :return:
        """
        endpoint = '/projects/%s/gc' % self.id
        response = self.gerrit.make_call('post', endpoint, **GCInput)
        result = self.gerrit.decode_response(response)
        return result

    def ban_commits(self, BanInput: dict):
        """
        Marks commits as banned for the project.

        :param BanInput: the BanInput entity.
        :return:
        """
        endpoint = '/projects/%s/ban' % self.id
        response = self.gerrit.make_call('put', endpoint, **BanInput)
        result = self.gerrit.decode_response(response)
        return result

    @property
    def access_rights(self):
        """
        Lists the access rights for a single project.

        :return:
        """
        endpoint = '/projects/%s/access' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def set_access_rights(self, ProjectAccessInput: dict):
        """
        Sets access rights for the project using the diff schema provided by ProjectAccessInput.

        :param ProjectAccessInput: the ProjectAccessInput entity
        :return:
        """
        endpoint = '/projects/%s/access' % self.id
        response = self.gerrit.make_call('post', endpoint, **ProjectAccessInput)
        result = self.gerrit.decode_response(response)
        return result

    def check_access(self, options: str):
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
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def index(self, IndexProjectInput: dict):
        """
        Adds or updates the current project (and children, if specified) in the secondary index.
        The indexing task is executed asynchronously in background and this command returns immediately
        if async is specified in the input.

        :param IndexProjectInput: the IndexProjectInput entity
        :return:
        """
        endpoint = '/projects/%s/index' % self.id
        self.gerrit.make_call('post', endpoint, **IndexProjectInput)

    def index_change(self):
        """
        Adds or updates the current project (and children, if specified) in the secondary index.
        The indexing task is executed asynchronously in background and this command returns immediately
        if async is specified in the input.

        :return:
        """
        endpoint = '/projects/%s/index.changes' % self.id
        self.gerrit.make_call('post', endpoint)

    def check_consistency(self, CheckProjectInput: dict):
        """
        Performs consistency checks on the project.

        :param CheckProjectInput: the CheckProjectInput entity
        :return:
        """
        endpoint = '/projects/%s/check' % self.id
        response = self.gerrit.make_call('post', endpoint, **CheckProjectInput)
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
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)

        child_projects = []
        for item in result:
            child_projects.append(GerritProject(id=item['id'], gerrit=self.gerrit))
        return child_projects

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
        return Commit(self.id, commit, self.gerrit)