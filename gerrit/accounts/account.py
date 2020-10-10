#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.models import BaseModel
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

    def list_emails(self) -> list:
        """
        Returns the email addresses that are configured for the specified user.

        :return:
        """
        endpoint = '/accounts/%s/emails' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def get_email(self, email: str) -> dict:
        """
        Retrieves an email address of a user.

        :param email:
        :return:
        """
        endpoint = '/accounts/%s/emails/%s' % (self.username, email)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def delete_email(self, email: str):
        """
        Deletes an email address of an account.

        :param email:
        :return:
        """
        endpoint = '/accounts/%s/emails/%s' % (self.username, email)
        response = self.gerrit.make_call('delete', endpoint)
        response.raise_for_status()

    def set_preferred_email(self, email: str):
        """
        Sets an email address as preferred email address for an account.

        :param email:
        :return:
        """
        endpoint = '/accounts/%s/emails/%s/preferred' % (self.username, email)
        response = self.gerrit.make_call('put', endpoint)
        response.raise_for_status()

    def list_ssh_keys(self) -> list:
        """
        Returns the SSH keys of an account.

        :return:
        """
        endpoint = '/accounts/%s/sshkeys' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def get_ssh_key(self, ssh_key_id: int) -> dict:
        """
        Retrieves an SSH key of a user.

        :param ssh_key_id: ssh key id
        :return:
        """
        endpoint = '/accounts/%s/sshkeys/%s' % (self.username, ssh_key_id)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def add_ssh_key(self, ssh_key: str) -> dict:
        """

        :param ssh_key:
        :return:
        """
        endpoint = '/accounts/%s/sshkeys' % self.username
        base_url = self.gerrit._get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, data=ssh_key, headers={'Content-Type': 'plain/text'})
        result = self.gerrit.decode_response(response)
        return result

    def delete_ssh_key(self, ssh_key_id: int):
        """

        :param ssh_key_id:
        :return:
        """
        endpoint = '/accounts/%s/sshkeys/%s' % (self.username, ssh_key_id)
        response = self.gerrit.make_call('delete', endpoint)
        response.raise_for_status()

    def list_gpg_keys(self) -> dict:
        """
        Returns the GPG keys of an account.

        :return:
        """
        endpoint = '/accounts/%s/gpgkeys' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def get_gpg_key(self, gpg_key_id: str) -> dict:
        """
        Retrieves a GPG key of a user.

        :param gpg_key_id: gpg key id
        :return:
        """
        endpoint = '/accounts/%s/gpgkeys/%s' % (self.username, gpg_key_id)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def modify_gpg_keys(self, GpgKeysInput: dict) -> dict:
        """
        Add or delete one or more GPG keys for a user.

        :param GpgKeysInput: the GpgKeysInput entity
        :return:
        """
        endpoint = '/accounts/%s/gpgkeys' % self.username
        response = self.gerrit.make_call('post', endpoint, **GpgKeysInput)
        result = self.gerrit.decode_response(response)
        return result

    def delete_gpg_key(self, gpg_key_id: str):
        """
        Deletes a GPG key of a user.

        :param gpg_key_id: gpg key id
        :return:
        """
        endpoint = '/accounts/%s/gpgkeys/%s' % (self.username, gpg_key_id)
        response = self.gerrit.make_call('delete', endpoint)
        response.raise_for_status()

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
