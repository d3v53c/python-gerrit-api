#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.branch import Branch
from gerrit.exceptions import UnknownBranch


class Branches:
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
        return self.create(key.replace('refs/heads/', ''), value)

    def __delitem__(self, key):
        """
        Delete a branch by ref

        :param key:
        :return:
        """
        return self.delete(key.replace('refs/heads/', ''))

    def __iter__(self):
        """

        :return:
        """
        for row in self._data:
            yield Branch(project=self.project, ref=row['ref'], gerrit=self.gerrit)

    def create(self, name: str, BranchInput: dict):
        """
        Creates a new branch.

        :param name: the branch name
        :param BranchInput: the BranchInput entity
        :return:
        """
        ref = 'refs/heads/' + name
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
