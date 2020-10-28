#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.common import check
from gerrit.utils.models import BaseModel


class Label(BaseModel):
    def __init__(self, **kwargs):
        super(Label, self).__init__(**kwargs)
        self.attributes = [
            "name",
            "function",
            "values",
            "default_value",
            "can_override",
            "copy_min_score",
            "copy_max_score",
            "copy_all_scores_if_no_change",
            "copy_all_scores_if_no_code_change",
            "copy_all_scores_on_trivial_rebase",
            "copy_all_scores_on_merge_first_parent_update",
            "copy_values",
            "allow_post_submit",
            "ignore_self_approval",
            "project",
            "gerrit",
        ]

    def set(self, input_: dict):
        """
        Updates the definition of a label that is defined in this project.
        The calling user must have write access to the refs/meta/config branch of the project.
        Properties which are not set in the input entity are not modified.

        .. code-block:: python

            input_ = {
                "commit_message": "Ignore self approvals for Code-Review label",
                "ignore_self_approval": true
            }

            project = gerrit.projects.get("MyProject")
            label = project.labels.get("foo")
            result = label.set(input_)

        :param input_: the LabelDefinitionInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#label-definition-input
        :return:
        """
        endpoint = "/projects/%s/labels/%s" % (self.project, self.name)
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return self.gerrit.projects.get(self.project).labels.get(result.get("name"))

    def delete(self):
        """
        Deletes the definition of a label that is defined in this project.
        The calling user must have write access to the refs/meta/config branch of the project.

        :return:
        """
        endpoint = "/projects/%s/labels/%s" % (self.project, self.name)
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))


class Labels:
    def __init__(self, project, gerrit):
        self.project = project
        self.gerrit = gerrit

    def list(self):
        """
        Lists the labels that are defined in this project.

        :return:
        """
        endpoint = "/projects/%s/labels/" % self.project
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return Label.parse_list(result, gerrit=self.gerrit)

    def get(self, name: str) -> Label:
        """
        Retrieves the definition of a label that is defined in this project.
        The calling user must have read access to the refs/meta/config branch of the project.

        :param name: label name
        :return:
        """
        endpoint = "/projects/%s/labels/%s" % (self.project, name)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return Label.parse(result, gerrit=self.gerrit)

    @check
    def create(self, name: str, input_: dict) -> Label:
        """
        Creates a new label definition in this project.
        The calling user must have write access to the refs/meta/config branch of the project.
        If a label with this name is already defined in this project, this label definition is updated (see Set Label).

        .. code-block:: python

            input_ = {
                "values": {
                    " 0": "No score",
                    "-1": "I would prefer this is not merged as is",
                    "-2": "This shall not be merged",
                    "+1": "Looks good to me, but someone else must approve",
                    "+2": "Looks good to me, approved"
                },
                "commit_message": "Create Foo Label"
            }
            new_label = project.labels.create('foo', input_)

        :param name: label name
        :param input_: the LabelDefinitionInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#label-definition-input
        :return:
        """
        endpoint = "/projects/%s/labels/%s" % (self.project, name)
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return Label.parse(result, gerrit=self.gerrit)

    def delete(self, name: str):
        """
        Deletes the definition of a label that is defined in this project.
        The calling user must have write access to the refs/meta/config branch of the project.

        :param name: label name
        :return:
        """
        endpoint = "/projects/%s/labels/%s" % (self.project, name)
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
