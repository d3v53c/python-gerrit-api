#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from urllib.parse import quote
from gerrit.exceptions import UnknownBranch
from gerrit.common import check


class Branch:
    branch_prefix = 'refs/heads/'

    def __init__(self, project, ref, gerrit):
        self.project = project
        self.ref = ref
        self.gerrit = gerrit

        self.name = None
        self.web_links = None
        self.revision = None
        self.can_delete = None

        self.__load__()

    def __repr__(self):
        return '%s(%s=%s)' % (self.__class__.__name__, 'ref', self.ref)

    def __load__(self):
        self.name = self.ref.replace('refs/heads/', '')
        endpoint = '/projects/%s/branches/%s' % (self.project, self.name)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)

        self.web_links = result.get('web_links', [])
        self.revision = result.get('revision')
        self.can_delete = result.get('can_delete', False)

    def get_file_content(self, file: str) -> str:
        """
        Gets the content of a file from the HEAD revision of a certain branch.
        The content is returned as base64 encoded string.

        :param file:
        :return:
        """
        endpoint = '/projects/%s/branches/%s/files/%s/content' % (self.project, self.name, quote(file, safe=''))
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def get_mergeable_information(self, MergeInput: dict) -> dict:
        """
        Gets whether the source is mergeable with the target branch.

        :param MergeInput: the MergeInput entity
        :return:
        """
        endpoint = '/projects/%s/branches/%s/mergeable' % (self.project, self.name)
        response = self.gerrit.make_call('get', endpoint, **MergeInput)
        result = self.gerrit.decode_response(response)
        return result

    def get_reflog(self) -> list:
        """
        Gets the reflog of a certain branch.

        :return:
        """
        endpoint = '/projects/%s/branches/%s/reflog' % (self.project, self.name)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result


class Branches:
    branch_prefix = 'refs/heads/'

    def __init__(self, project, gerrit):
        self.project = project
        self.gerrit = gerrit
        self._data = self.poll()

    def poll(self):
        """

        :return:
        """
        endpoint = '/projects/%s/branches/' % self.project
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        for item in result:
            if item['ref'] == 'refs/meta/config':
                result.remove(item)
        return result

    def iterkeys(self):
        """
        Iterate over the names of all available branches
        """
        for row in self._data:
            yield row['ref']

    def keys(self):
        """
        Return a list of the names of all branches
        """
        return list(self.iterkeys())

    def __len__(self):
        """

        :return:
        """
        return len(self.keys())

    def __contains__(self, ref):
        """
        True if ref exists in project
        """
        return ref in self.keys()

    def __getitem__(self, ref):
        """
        get a branch by ref

        :param ref:
        :return:
        """
        result = [row for row in self._data if row['ref'] == ref]
        if result:
            ref_date = result[0]
            return Branch(project=self.project, ref=ref_date['ref'], gerrit=self.gerrit)
        else:
            raise UnknownBranch(ref)

    def __setitem__(self, key, value):
        """
        create a branch by ref
        :param key:
        :param value:
        :return:
        """
        return self.create(key.replace(self.branch_prefix, ''), value)

    def __delitem__(self, key):
        """
        Delete a branch by ref

        :param key:
        :return:
        """
        return self.delete(key.replace(self.branch_prefix, ''))

    def __iter__(self):
        """

        :return:
        """
        for row in self._data:
            yield Branch(project=self.project, ref=row['ref'], gerrit=self.gerrit)

    @check
    def create(self, name: str, BranchInput: dict) -> Branch:
        """
        Creates a new branch.

        :param name: the branch name
        :param BranchInput: the BranchInput entity
        :return:
        """
        ref = self.branch_prefix + name
        if ref in self.keys():
            return self[ref]

        endpoint = '/projects/%s/branches/%s' % (self.project, name)
        response = self.gerrit.make_call('put', endpoint, **BranchInput)
        result = self.gerrit.decode_response(response)
        return Branch(project=self.project, ref=result['ref'], gerrit=self.gerrit)

    def delete(self, name: str):
        """
        Delete a branch.

        :param name: The name of a branch or HEAD. The prefix refs/heads/ can be omitted.
        :return:
        """
        endpoint = '/projects/%s/branches/%s' % (self.project, name)
        self.gerrit.make_call('delete', endpoint)
