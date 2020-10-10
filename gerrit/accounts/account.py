#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.models import BaseModel


class GerritAccount(BaseModel):
    def __init__(self, **kwargs):
        super(GerritAccount, self).__init__(**kwargs)
        self.attributes = ['username', 'registered_on', '_account_id', 'name', 'email', 'gerrit']

    def set_name(self, AccountNameInput: dict) -> str:
        """
        Sets the full name of an account.
        Some realms may not allow to modify the account name.
        In this case the request is rejected with “405 Method Not Allowed”.

        :param AccountNameInput: the AccountNameInput entity
        :return:
        """
        endpoint = '/accounts/%s/name' % self.username
        response = self.gerrit.make_call('put', endpoint, **AccountNameInput)
        result = self.gerrit.decode_response(response)
        return result

    def delete_name(self):
        """
        Deletes the name of an account.
        Some realms may not allow to delete the account name.
        In this case the request is rejected with “405 Method Not Allowed”.

        :return:
        """
        endpoint = '/accounts/%s/name' % self.username
        response = self.gerrit.make_call('delete', endpoint)
        response.raise_for_status()

    @property
    def status(self) -> str:
        """
        Retrieves the status of an account.
        If the account does not have a status an empty string is returned.

        :return:
        """
        endpoint = '/accounts/%s/status' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @status.setter
    def status(self, status: str):
        """
        Sets the status of an account.

        :param status: account status
        :return:
        """
        endpoint = '/accounts/%s/status' % self.username
        options = {"status": status}
        response = self.gerrit.make_call('put', endpoint, **options)
        response.raise_for_status()

    def set_username(self, UsernameInput: dict):
        """
        Sets the username of an account.
        Some realms may not allow to modify the account username.
        In this case the request is rejected with “405 Method Not Allowed”.

        :param UsernameInput: the UsernameInput entity
        :return:
        """
        endpoint = '/accounts/%s/username' % self.username
        response = self.gerrit.make_call('put', endpoint, **UsernameInput)
        result = self.gerrit.decode_response(response)
        return result

    def get_active(self) -> str:
        """
        Checks if an account is active.

        :return:
        """
        endpoint = '/accounts/%s/active' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def set_active(self):
        """
        Sets the account state to active.

        :param status: account status
        :return:
        """
        endpoint = '/accounts/%s/active' % self.username
        response = self.gerrit.make_call('put', endpoint)
        response.raise_for_status()

    def delete_active(self):
        """
        Sets the account state to inactive.
        If the account was already inactive the response is “409 Conflict”.

        :param status: account status
        :return:
        """
        endpoint = '/accounts/%s/active' % self.username
        response = self.gerrit.make_call('delete', endpoint)
        response.raise_for_status()
