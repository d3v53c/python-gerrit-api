#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.common import check
from gerrit.utils.models import BaseModel


class Webhook(BaseModel):
    def __init__(self, **kwargs):
        super(Webhook, self).__init__(**kwargs)
        self.attributes = [
            "name",
            "url",
            "maxTries",
            "sslVerify",
            "events",
            "project",
            "gerrit",
        ]

    def delete(self):
        """
        Delete a webhook for a project.

        :return:
        """
        endpoint = "/config/server/webhooks~projects/%s/remotes/%s" % (
            self.project,
            self.name,
        )
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))


class Webhooks:
    def __init__(self, project, gerrit):
        self.project = project
        self.gerrit = gerrit

    def list(self):
        """
        List existing webhooks for a project.

        :return:
        """
        endpoint = "/config/server/webhooks~projects/%s/remotes/" % self.project
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)

        webhooks = []
        for key, value in result.items():
            webhook = value
            webhook.update({"name": key})
            webhooks.append(webhook)

        return Webhook.parse_list(webhooks, project=self.project, gerrit=self.gerrit)

    @check
    def create(self, name: str, input_: dict) -> Webhook:
        """
        Create or update a webhook for a project.

        .. code-block:: python

            input_ = {
                "url": "https://foo.org/gerrit-events",
                "maxTries": "3",
                "sslVerify": "true"
            }

            project = gerrit.projects.get('myproject')
            new_webhook = project.webhooks.create('test', input_)

        :param name: the webhook name
        :param input_: the RemoteInfo entity
        :return:
        """
        endpoint = "/config/server/webhooks~projects/%s/remotes/%s" % (
            self.project,
            name,
        )
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return Webhook.parse(result, project=self.project, gerrit=self.gerrit)

    def get(self, name: str) -> Webhook:
        """
        Get information about one webhook.

        :param name: the webhook name
        :return:
        """
        endpoint = "/config/server/webhooks~projects/%s/remotes/%s" % (
            self.project,
            name,
        )
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        result.update({"name": name})
        return Webhook.parse(result, project=self.project, gerrit=self.gerrit)
