#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.models import BaseModel


class Email(BaseModel):
    def __init__(self, **kwargs):
        super(Email, self).__init__(**kwargs)
        self.attributes = ["email", "preferred", "username", "gerrit"]

    def delete(self):
        """
        Deletes an email address of an account.

        :return:
        """
        endpoint = "/accounts/%s/emails/%s" % (self.username, self.email)
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))

    def set_preferred(self):
        """
        Sets an email address as preferred email address for an account.

        :return:
        """
        endpoint = "/accounts/%s/emails/%s/preferred" % (self.username, self.email)
        self.gerrit.requester.put(self.gerrit.get_endpoint_url(endpoint))


class Emails:
    def __init__(self, username, gerrit):
        self.username = username
        self.gerrit = gerrit

    def list(self) -> list:
        """
        Returns the email addresses that are configured for the specified user.

        :return:
        """
        endpoint = "/accounts/%s/emails" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return Email.parse_list(result, username=self.username, gerrit=self.gerrit)

    def get(self, email: str) -> Email:
        """
        Retrieves an email address of a user.

        :return:
        """
        endpoint = "/accounts/%s/emails/%s" % (self.username, email)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return Email.parse(result, username=self.username, gerrit=self.gerrit)

    def set_preferred(self, email: str):
        """
        Sets an email address as preferred email address for an account.

        :param email: account email
        :return:
        """
        self.get(email).set_preferred()
