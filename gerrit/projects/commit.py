#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from urllib.parse import quote
from gerrit.utils.common import check


class Commit:
    def __init__(self, project, json, gerrit):
        self.project = project
        self.json = json
        self.gerrit = gerrit

        self.commit_id = None
        self.author = None
        self.committer = None
        self.message = None
        self.parents = None
        self.subject = None

        if self.json is not None:
            self.__load__()

    def __load__(self):
        self.commit_id = self.json.get('commit')
        self.author = self.json.get('author')
        self.committer = self.json.get('committer')
        self.message = self.json.get('message')
        self.parents = self.json.get('parents')
        self.subject = self.json.get('subject')

    def __repr__(self):
        return '%s(%s=%s)' % (self.__class__.__name__, 'commit', self.commit_id)

    def get_include_in(self) -> dict:
        """
        Retrieves the branches and tags in which a change is included.

        :return:
        """
        endpoint = '/projects/%s/commits/%s/in' % (self.project, self.commit_id)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def get_file_content(self, file: str) -> str:
        """
        Gets the content of a file from a certain commit.

        :param file:
        :return:
        """
        endpoint = '/projects/%s/commits/%s/files/%s/content' % (self.project, self.commit_id, quote(file, safe=''))
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def cherry_pick(self, CherryPickInput: dict) -> dict:
        """

        :param CherryPickInput: the CherryPickInput entity
        :return:
        """
        endpoint = '/projects/%s/commits/%s/cherrypick' % (self.project, self.commit_id)
        response = self.gerrit.make_call('post', endpoint, **CherryPickInput)
        result = self.gerrit.decode_response(response)
        return result

    def list_change_files(self) -> dict:
        """
        Lists the files that were modified, added or deleted in a commit.

        :return:
        """
        endpoint = '/projects/%s/commits/%s/files/' % (self.project, self.commit_id)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result
