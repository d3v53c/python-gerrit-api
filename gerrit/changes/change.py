#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.common import check
from gerrit.utils.exceptions import UnknownChange
from gerrit.accounts.account import GerritAccount
from gerrit.utils.models import BaseModel


class GerritChange(BaseModel):
    def __init__(self, **kwargs):
        super(GerritChange, self).__init__(**kwargs)
        self.attributes = ['id', 'project', 'branch', 'change_id', 'subject', 'status', 'created', 'updated',
                           'mergeable', 'insertions', 'deletions', '_number', 'owner', 'gerrit']

    @property
    def topic(self) -> str:
        """
        Retrieves the topic of a change.

        :return:
        """
        endpoint = '/changes/%s/topic' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @topic.setter
    def topic(self, topic: str):
        """
        Sets the topic of a change.

        :param topic: The new topic
        :return:
        """
        endpoint = '/changes/%s/topic' % self.id
        input_ = {"topic": topic}
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    @topic.deleter
    def topic(self):
        """
        Deletes the topic of a change.

        :return:
        """
        endpoint = '/changes/%s/topic' % self.id
        response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
        response.raise_for_status()

    def get_assignee(self) -> GerritAccount:
        """
        Retrieves the account of the user assigned to a change.

        :return:
        """
        endpoint = '/changes/%s/assignee' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        if result:
            return self.gerrit.accounts.get(result.get('username'))

    @check
    def set_assignee(self, input_: dict) -> GerritAccount:
        """

        :param input_: the AssigneeInput entity
        :return:
        """
        endpoint = '/changes/%s/assignee' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        if result:
            return self.gerrit.accounts.get(result.get('username'))

    def get_past_assignees(self) -> list:
        """
        Returns a list of every user ever assigned to a change, in the order in which they were first assigned.

        :return:
        """
        endpoint = '/changes/%s/past_assignees' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        assignees = [self.gerrit.accounts.get(item.get('username')) for item in result]
        return assignees

    def delete_assignee(self):
        """
        Deletes the assignee of a change.

        :return:
        """
        endpoint = '/changes/%s/assignee' % self.id
        response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        if result:
            return self.gerrit.accounts.get(result.get('username'))

    def get_pure_revert(self, commit) -> dict:
        """
        Check if the given change is a pure revert of the change it references in revertOf.

        :param commit: commit id
        :return:
        """
        endpoint = '/changes/%s/pure_revert?o=%s' % (self.id, commit)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def abandon(self):
        """
        Abandons a change.

        :return:
        """
        endpoint = '/changes/%s/abandon' % self.id
        response = self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.changes.get(result.get('id'))

    def restore(self):
        """
        Restores a change.

        :return:
        """
        endpoint = '/changes/%s/restore' % self.id
        response = self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.changes.get(result.get('id'))

    @check
    def rebase(self, input_: dict):
        """
        need test.
        Rebases a change.

        :param input_: the RebaseInput entity
        :return:
        """
        endpoint = '/changes/%s/rebase' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return self.gerrit.changes.get(result.get('id'))
