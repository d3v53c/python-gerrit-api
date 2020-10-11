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

    def get_groups(self) -> list:
        """
        Lists all groups that contain the specified user as a member.

        :return:
        """
        endpoint = '/accounts/%s/groups' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def get_avatar(self) -> str:
        """
        Retrieves the avatar image of the user.
        :return:
        """
        endpoint = '/accounts/%s/avatar' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def get_avatar_change_url(self) -> str:
        """
        Retrieves the avatar image of the user.
        :return:
        """
        endpoint = '/accounts/%s/avatar.change.url' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def get_user_preferences(self):
        """
        Retrieves the user’s preferences.

        :return:
        """
        endpoint = '/accounts/%s/preferences' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_user_preferences(self, PreferencesInput: dict) -> dict:
        """
        Sets the user’s preferences.

        :param PreferencesInput: the PreferencesInput entity
        :return:
        """
        endpoint = '/accounts/%s/preferences' % self.username
        response = self.gerrit.make_call('put', endpoint, **PreferencesInput)
        result = self.gerrit.decode_response(response)
        return result

    def get_diff_preferences(self):
        """
        Retrieves the diff preferences of a user.

        :return:
        """
        endpoint = '/accounts/%s/preferences.diff' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_diff_preferences(self, DiffPreferencesInput: dict) -> dict:
        """
        Sets the diff preferences of a user.

        :param DiffPreferencesInput: the DiffPreferencesInput entity
        :return:
        """
        endpoint = '/accounts/%s/preferences.diff' % self.username
        response = self.gerrit.make_call('put', endpoint, **DiffPreferencesInput)
        result = self.gerrit.decode_response(response)
        return result

    def get_edit_preferences(self):
        """
        Retrieves the edit preferences of a user.

        :return:
        """
        endpoint = '/accounts/%s/preferences.edit' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_edit_preferences(self, EditPreferencesInfo: dict) -> dict:
        """
        Sets the edit preferences of a user.

        :param EditPreferencesInfo: the EditPreferencesInfo entity
        :return:
        """
        endpoint = '/accounts/%s/preferences.edit' % self.username
        response = self.gerrit.make_call('put', endpoint, **EditPreferencesInfo)
        result = self.gerrit.decode_response(response)
        return result

    def get_watched_projects(self) -> list:
        """
        Retrieves all projects a user is watching.

        :return:
        """
        endpoint = '/accounts/%s/watched.projects' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def modify_watched_projects(self, ProjectWatchInfo: list) -> list:
        """
        Add new projects to watch or update existing watched projects.

        :param ProjectWatchInfo: the ProjectWatchInfo entities as list
        :return:
        """
        endpoint = '/accounts/%s/watched.projects' % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url,
                                              json=ProjectWatchInfo,
                                              headers={'Content-Type': 'application/json'})
        result = self.gerrit.decode_response(response)
        return result

    def delete_watched_projects(self, ProjectWatchInfo: list):
        """
        Projects posted to this endpoint will no longer be watched.

        :param ProjectWatchInfo: the watched projects as list
        :return:
        """
        endpoint = '/accounts/%s/watched.projects:delete' % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url,
                                              json=ProjectWatchInfo,
                                              headers={'Content-Type': 'application/json'})
        response.raise_for_status()

    def get_external_ids(self) -> list:
        """
        Retrieves the external ids of a user account.

        :return:
        """
        endpoint = '/accounts/%s/external.ids' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def delete_external_ids(self, ExternalIDsInfo: list):
        """
        Delete a list of external ids for a user account.

        :param ExternalIDsInfo: the external ids as list
        :return:
        """
        endpoint = '/accounts/%s/external.ids:delete' % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url,
                                              json=ExternalIDsInfo,
                                              headers={'Content-Type': 'application/json'})
        response.raise_for_status()

    def list_contributor_agreements(self) -> list:
        """
        Gets a list of the user’s signed contributor agreements.

        :return:
        """
        endpoint = '/accounts/%s/agreements' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def sign_contributor_agreement(self, ContributorAgreementInput: dict) -> str:
        """
        Signs a contributor agreement.

        :param ContributorAgreementInput: the ContributorAgreementInput entity
        :return:
        """
        endpoint = '/accounts/%s/agreements' % self.username
        response = self.gerrit.make_call('put', endpoint, **ContributorAgreementInput)
        result = self.gerrit.decode_response(response)
        return result

    def delete_draft_comments(self, DeleteDraftCommentsInput: dict) -> list:
        """
        Deletes some or all of a user’s draft comments.

        :param DeleteDraftCommentsInput: the DeleteDraftCommentsInput entity
        :return:
        """
        endpoint = '/accounts/%s/drafts:delete' % self.username
        response = self.gerrit.make_call('post', endpoint, **DeleteDraftCommentsInput)
        result = self.gerrit.decode_response(response)
        return result

    def index(self):
        """
        Adds or updates the account in the secondary index.

        :return:
        """
        endpoint = '/accounts/%s/index' % self.username
        response = self.gerrit.make_call('post', endpoint)
        response.raise_for_status()
