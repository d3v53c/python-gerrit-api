#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.common import check
from gerrit.utils.models import BaseModel


class Draft(BaseModel):
    def __init__(self, **kwargs):
        super(Draft, self).__init__(**kwargs)
        self.attributes = [
            "id",
            "path",
            "line",
            "message",
            "unresolved",
            "updated",
            "change",
            "revision",
            "gerrit",
        ]

    @check
    def update(self, input_: dict):
        """
        Updates a draft comment on a revision.

        .. code-block:: python

            input_ = {
                "path": "sonarqube/cloud/duplications.py",
                "line": 25,
                "message": "[nit] trailing whitespace"
            }
            change = gerrit.changes.get('myProject~stable~I10394472cbd17dd12454f229e4f6de00b143a444')
            revision = change.get_revision('3848807f587dbd3a7e61723bbfbf1ad13ad5a00a')
            draft = revision.drafts.get('89f04e8c_9b7fd51d')
            result = draft.update(input_)

        :param input_: the CommentInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#comment-input
        :return:
        """
        endpoint = "/changes/%s/revisions/%s/drafts/%s" % (
            self.change,
            self.revision,
            self.id,
        )
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return Draft.parse(
            result, change=self.change, revision=self.revision, gerrit=self.gerrit
        )

    def delete(self):
        """
        Deletes a draft comment from a revision.

        :return:
        """
        endpoint = "/changes/%s/revisions/%s/drafts/%s" % (
            self.change,
            self.revision,
            self.id,
        )
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))


class Drafts:
    def __init__(self, change, revision, gerrit):
        self.change = change
        self.revision = revision
        self.gerrit = gerrit

    def list(self):
        """
        Lists the draft comments of a revision that belong to the calling user.

        :return:
        """
        endpoint = "/changes/%s/revisions/%s/drafts" % (self.change, self.revision)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        drafts = []
        for key, value in result.items():
            for item in value:
                draft = item
                draft.update({"path": key})
                drafts.append(draft)
        return Draft.parse_list(
            drafts, change=self.change, revision=self.revision, gerrit=self.gerrit
        )

    def get(self, id_: str):
        """
        Retrieves a draft comment of a revision that belongs to the calling user.

        :param id_: the draft comment id
        :return:
        """
        endpoint = "/changes/%s/revisions/%s/drafts/%s" % (
            self.change,
            self.revision,
            id_,
        )
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return Draft.parse(
            result, change=self.change, revision=self.revision, gerrit=self.gerrit
        )

    @check
    def create(self, input_: dict):
        """
        Creates a draft comment on a revision.

        .. code-block:: python

            input_ = {
                "path": "sonarqube/cloud/duplications.py",
                "line": 15,
                "message": "[nit] trailing whitespace"
            }
            change = gerrit.changes.get('myProject~stable~I10394472cbd17dd12454f229e4f6de00b143a444')
            revision = change.get_revision('3848807f587dbd3a7e61723bbfbf1ad13ad5a00a')
            new_draft = revision.drafts.create(input_)

        :param input_: the CommentInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#comment-input
        :return:
        """
        endpoint = "/changes/%s/revisions/%s/drafts" % (self.change, self.revision)
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return Draft.parse(
            result, change=self.change, revision=self.revision, gerrit=self.gerrit
        )

    def delete(self, id_: str):
        """
        Deletes a draft comment from a revision.

        :param id_: the draft comment id
        :return:
        """
        endpoint = "/changes/%s/revisions/%s/drafts/%s" % (
            self.change,
            self.revision,
            id_,
        )
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
