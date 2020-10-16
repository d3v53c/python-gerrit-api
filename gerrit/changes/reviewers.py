#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.common import check
from gerrit.utils.exceptions import UnknownReviewer
from gerrit.utils.models import BaseModel


class Reviewer(BaseModel):
    def __init__(self, **kwargs):
        super(Reviewer, self).__init__(**kwargs)
        self.attributes = ['username', '_account_id', 'name', 'email', 'approvals', 'change', 'gerrit']

    @check
    def delete(self, input_: dict = None):
        """
        Deletes a reviewer from a change.

        :param input_: the DeleteReviewerInput entity
        :return:
        """
        if input_ is None:
            endpoint = '/changes/%s/reviewers/%s' % (self.change, self.username)
            response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
        else:
            endpoint = '/changes/%s/reviewers/%s/delete' % (self.change, self.username)
            base_url = self.gerrit.get_endpoint_url(endpoint)
            response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        response.raise_for_status()

    def list_votes(self) -> dict:
        """
        Lists the votes for a specific reviewer of the change.

        :return:
        """
        endpoint = '/changes/%s/reviewers/%s/votes/' % (self.change, self.username)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def delete_vote(self, label: str, input_: dict = None):
        """
        Deletes a single vote from a change.
        Note, that even when the last vote of a reviewer is removed the reviewer itself is still listed on the change.

        :param label:
        :param input_: the DeleteVoteInput entity.
        :return:
        """
        if input_ is None:
            endpoint = '/changes/%s/reviewers/%s/votes/%s' % (self.change, self.username, label)
            response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
        else:
            endpoint = '/changes/%s/reviewers/%s/votes/%s/delete' % (self.change, self.username, label)
            base_url = self.gerrit.get_endpoint_url(endpoint)
            response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        response.raise_for_status()


class Reviewers:
    def __init__(self, change, gerrit):
        self.change = change
        self.gerrit = gerrit

    def list(self) -> list:
        """
        Lists the reviewers of a change.

        :return:
        """
        endpoint = '/changes/%s/reviewers/' % self.change
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return Reviewer.parse_list(result, change=self.change, gerrit=self.gerrit)

    def get(self, query: str):
        """
        Retrieves a reviewer of a change.

        :param query: _account_id, name, username or email
        :return:
        """
        endpoint = '/changes/%s/reviewers/%s' % (self.change, query)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            return Reviewer.parse(result[0], change=self.change, gerrit=self.gerrit)
        else:
            raise UnknownReviewer(query)

    @check
    def add(self, input_: dict) -> dict:
        """
        Adds one user or all members of one group as reviewer to the change.

        :param input_: the ReviewerInput entity
        :return:
        """
        endpoint = '/changes/%s/reviewers' % self.change
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result
