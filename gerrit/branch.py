#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi


class Branch:
    def __init__(self, project, ref, gerrit):
        self.project = project
        self.ref = ref
        self.gerrit = gerrit

        self.branch = None
        self.web_links = None
        self.revision = None
        self.can_delete = None

        self.__load__()

    def __repr__(self):
        return '%s(%s=%s)' % (self.__class__.__name__, 'ref', self.ref)

    def __load__(self):
        self.branch = self.ref.replace('refs/heads/', '')
        endpoint = '/projects/%s/branches/%s' % (self.project, self.branch)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)

        self.web_links = result.get('web_links', [])
        self.revision = result.get('revision')
        self.can_delete = result.get('can_delete', False)

    def get_file_content(self, file: str):
        """
        Gets the content of a file from the HEAD revision of a certain branch.
        The content is returned as base64 encoded string.

        :param file:
        :return:
        """
        endpoint = '/projects/%s/branches/%s/files/%s/content' % (self.project, self.branch, file)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def get_mergeable_information(self, MergeInput: dict):
        """
        Gets whether the source is mergeable with the target branch.

        :param MergeInput: the MergeInput entity
        :return:
        """
        endpoint = '/projects/%s/branches/%s/mergeable' % (self.project, self.branch)
        response = self.gerrit.make_call('get', endpoint, **MergeInput)
        result = self.gerrit.decode_response(response)
        return result

    def get_reflog(self):
        """
        Gets the reflog of a certain branch.

        :return:
        """
        endpoint = '/projects/%s/branches/%s/reflog' % (self.project, self.branch)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result
