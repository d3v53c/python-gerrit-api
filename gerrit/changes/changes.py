#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.changes.change import GerritChange
from gerrit.utils.common import check
from gerrit.utils.exceptions import UnknownChange


class GerritChanges:
    def __init__(self, gerrit):
        self.gerrit = gerrit

    def search(self, query: str) -> list:
        """
        Queries changes visible to the caller.

        :return:
        """
        endpoint = '/changes/?%s' % query
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return GerritChange.parse_list(result, gerrit=self.gerrit)

    def get(self, id_: str) -> GerritChange:
        """
        Retrieves a change.

        :param id_: change id
        :return:
        """
        endpoint = '/changes/%s' % id_
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))

        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            return GerritChange.parse(result, gerrit=self.gerrit)
        else:
            raise UnknownChange(id_)

    @check
    def create(self, input_: dict) -> GerritChange:
        """
        create a change

        :param input_: the ChangeInput entity
        :return:
        """
        endpoint = '/changes/'
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return GerritChange.parse(result, gerrit=self.gerrit)

    @check
    def create_merge_patch_set(self, id_: str, input_: dict) -> GerritChange:
        """
        Update an existing change by using a MergePatchSetInput entity.
        Gerrit will create a merge commit based on the information of MergePatchSetInput and add a new patch set to
        the change corresponding to the new merge commit.

        :param id_: change id
        :param input_: the MergePatchSetInput entity
        :return:
        """
        endpoint = '/changes/%s/merge' % id_
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return GerritChange.parse(result, gerrit=self.gerrit)

    @check
    def set_commit_message(self, id_: str, input_: dict) -> str:
        """
        Creates a new patch set with a new commit message.

        :param id_: change id
        :param input_: the CommitMessageInput entity
        :return:
        """
        endpoint = '/changes/%s/message' % id_
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

