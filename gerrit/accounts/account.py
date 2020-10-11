#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.models import BaseModel
from gerrit.accounts.emails import Emails
from gerrit.accounts.ssh_keys import SSHKeys
from gerrit.accounts.gpg_keys import GPGKeys
from gerrit.utils.common import check


class GerritAccount(BaseModel):
    def __init__(self, **kwargs):
        super(GerritAccount, self).__init__(**kwargs)
        self.attributes = ['username', 'registered_on', '_account_id', 'name', 'email', 'gerrit']

    @check
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

    @check
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

    @check
    def set_http_password(self, HttpPasswordInput: dict) -> str:
        """
        Sets/Generates the HTTP password of an account.

        :param HttpPasswordInput: the HttpPasswordInput entity
        :return:
        """
        endpoint = '/accounts/%s/password.http' % self.username
        response = self.gerrit.make_call('put', endpoint, **HttpPasswordInput)
        result = self.gerrit.decode_response(response)
        return result

    def delete_http_password(self):
        """
        Deletes the HTTP password of an account.

        :return:
        """
        endpoint = '/accounts/%s/password.http' % self.username
        response = self.gerrit.make_call('delete', endpoint)
        response.raise_for_status()

    def get_oauth_token(self) -> dict:
        """
        Returns a previously obtained OAuth access token.
        If there is no token available, or the token has already expired, “404 Not Found” is returned as response.
        Requests to obtain an access token of another user are rejected with “403 Forbidden”.

        :return:
        """
        endpoint = '/accounts/%s/oauthtoken' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @property
    def emails(self):
        return Emails(username=self.username, gerrit=self.gerrit)

    @property
    def ssh_keys(self):
        return SSHKeys(username=self.username, gerrit=self.gerrit)

    @property
    def gpg_keys(self):
        return GPGKeys(username=self.username, gerrit=self.gerrit)

    def list_capabilities(self) -> dict:
        """
        Returns the global capabilities that are enabled for the specified user.

        :return:
        """
        endpoint = '/accounts/%s/capabilities' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def check_capability(self, capability: str) -> str:
        """
        Checks if a user has a certain global capability.

        :param capability:
        :return:
        """
        endpoint = '/accounts/%s/capabilities/%s' % (self.username, capability)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @property
    def groups(self):
        """
        Lists all groups that contain the specified user as a member.

        :return:
        """
        endpoint = '/accounts/%s/groups' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @property
    def avatar(self):
        """
        Retrieves the avatar image of the user.
        :return:
        """
        endpoint = '/accounts/%s/avatar' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def get_avatar_change_url(self):
        """
        Retrieves the avatar image of the user.
        :return:
        """
        endpoint = '/accounts/%s/avatar.change.url' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result
