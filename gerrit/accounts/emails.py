#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.models import BaseModel
from gerrit.utils.exceptions import UnknownEmail


class Email(BaseModel):
    def __init__(self, **kwargs):
        super(Email, self).__init__(**kwargs)
        self.attributes = ['email', 'preferred', 'username', 'gerrit']

    def delete(self):
        """
        Deletes an email address of an account.

        :return:
        """
        endpoint = '/accounts/%s/emails/%s' % (self.username, self.email)
        response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
        response.raise_for_status()

    def set_preferred(self):
        """
        Sets an email address as preferred email address for an account.

        :return:
        """
        endpoint = '/accounts/%s/emails/%s/preferred' % (self.username, self.email)
        response = self.gerrit.requester.put(self.gerrit.get_endpoint_url(endpoint))
        print(response.status_code)
        response.raise_for_status()


class Emails:
    def __init__(self, username, gerrit):
        self.username = username
        self.gerrit = gerrit

    def list(self) -> list:
        """
        Returns the email addresses that are configured for the specified user.

        :return:
        """
        endpoint = '/accounts/%s/emails' % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return Email.parse_list(result, username=self.username, gerrit=self.gerrit)

    def get(self, email: str) -> Email:
        """
        Retrieves an email address of a user.

        :return:
        """
        endpoint = '/accounts/%s/emails/%s' % (self.username, email)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            return Email.parse(result, username=self.username, gerrit=self.gerrit)
        else:
            raise UnknownEmail(email)

    def set_preferred(self, email: str):
        """
        Sets an email address as preferred email address for an account.

        :param email:
        :return:
        """
        self.get(email).set_preferred()
