#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from urllib.parse import quote
from gerrit.utils.common import check
from gerrit.utils.models import BaseModel


class Commit(BaseModel):
    def __init__(self, **kwargs):
        super(Commit, self).__init__(**kwargs)
        self.attributes = [
            "commit",
            "author",
            "committer",
            "message",
            "parents",
            "subject",
            "project",
            "gerrit",
        ]

    def get_include_in(self) -> dict:
        """
        Retrieves the branches and tags in which a change is included.

        :return:
        """
        endpoint = "/projects/%s/commits/%s/in" % (self.project, self.commit)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def get_file_content(self, file: str) -> str:
        """
        Gets the content of a file from a certain commit.

        :param file: the file path
        :return:
        """
        endpoint = "/projects/%s/commits/%s/files/%s/content" % (
            self.project,
            self.commit,
            quote(file, safe=""),
        )
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def cherry_pick(self, input_: dict) -> dict:
        """
        Cherry-picks a commit of a project to a destination branch.

        .. code-block:: python

            input_ = {
                "message": "Implementing Feature X",
                "destination": "release-branch"
            }
            result = commit.cherry_pick(input_)

        :param input_: the CherryPickInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#cherrypick-input
        :return:
        """
        endpoint = "/projects/%s/commits/%s/cherrypick" % (self.project, self.commit)
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def list_change_files(self) -> dict:
        """
        Lists the files that were modified, added or deleted in a commit.

        :return:
        """
        endpoint = "/projects/%s/commits/%s/files/" % (self.project, self.commit)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result
