#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.common import check
from gerrit.utils.models import BaseModel


class Comment(BaseModel):
    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)
        self.attributes = ["id", "path", "line", "in_reply_to", "message", "updated", "author", "change", "revision",
                           "gerrit"]

    @check
    def delete(self, input_: dict = None):
        """
        Deletes a published comment of a revision. Instead of deleting the whole comment, this endpoint just replaces
        the comment’s message with a new message, which contains the name of the user who deletes the comment and the
        reason why it’s deleted.

        :param input_: the DeleteCommentInput entity
        :return:
        """
        if input_ is None:
            endpoint = '/changes/%s/revisions/%s/comments/%s' % (self.change, self.revision, self.id)
            response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
            result = self.gerrit.decode_response(response)
            return result
        else:
            endpoint = '/changes/%s/revisions/%s/comments/%s/delete' % (self.change, self.revision, self.id)
            base_url = self.gerrit.get_endpoint_url(endpoint)
            response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
            result = self.gerrit.decode_response(response)
            return result


class Comments:
    def __init__(self, change, revision, gerrit):
        self.change = change
        self.revision = revision
        self.gerrit = gerrit

    def list(self):
        """
        Lists the published comments of a revision.

        :return:
        """
        endpoint = '/changes/%s/revisions/%s/comments' % (self.change, self.revision)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        comments = []
        for key, value in result.items():
            for item in value:
                comment = item
                comment.update({"path": key})
                comments.append(comment)
        return Comment.parse_list(comments, change=self.change, revision=self.revision, gerrit=self.gerrit)

    def get(self, id_: str):
        """

        :param id_:
        :return:
        """
        endpoint = '/changes/%s/revisions/%s/comments/%s' % (self.change, self.revision, id_)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return Comment.parse(result, change=self.change, revision=self.revision, gerrit=self.gerrit)