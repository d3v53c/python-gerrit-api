#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.branch import Branch
from gerrit.tags import Tag
from gerrit.exceptions import UnknownCommit


class Commit:
    def __init__(self, project, commit, gerrit):
        self.project = project
        self.commit = commit
        self.gerrit = gerrit

        self.author = None
        self.committer = None
        self.message = None
        self.parents = None
        self.subject = None

        self.__load__()

    def __load__(self):
        endpoint = '/projects/%s/commits/%s' % (self.project, self.commit)
        response = self.gerrit.make_call('get', endpoint)

        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            self.author = result.get('author')
            self.committer = result.get('committer')
            self.message = result.get('message')
            self.parents = result.get('parents')
            self.subject = result.get('subject')
        else:
            raise UnknownCommit(self.commit)

    def __repr__(self):
        return '%s(%s=%s)' % (self.__class__.__name__, 'commit', self.commit)

    def get_include_in(self):
        """
        Retrieves the branches and tags in which a change is included.

        :return:
        """
        endpoint = '/projects/%s/commits/%s/in' % (self.project, self.commit)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        branches = result.get('branches', [])
        tags = result.get('tags', [])
        return [Branch(self.project, 'refs/heads/'+branch, self.gerrit) for branch in branches] + \
               [Tag(self.project, 'refs/tags/'+tag, self.gerrit) for tag in tags]

    def get_file_content(self, file: str):
        """
        Gets the content of a file from a certain commit.

        :param file:
        :return:
        """
        endpoint = '/projects/%s/commits/%s/files/%s/content' % (self.project, self.commit, file)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def cherry_pick(self, CherryPickInput: dict):
        """

        :param CherryPickInput: the CherryPickInput entity
        :return:
        """
        endpoint = '/projects/%s/commits/%s/cherrypick' % (self.project, self.commit)
        response = self.gerrit.make_call('post', endpoint, **CherryPickInput)
        result = self.gerrit.decode_response(response)
        return result

    def list_change_files(self):
        """
        Lists the files that were modified, added or deleted in a commit.

        :return:
        """
        endpoint = '/projects/%s/commits/%s/files/' % (self.project, self.commit)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result
