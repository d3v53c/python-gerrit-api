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
        self.attributes = [
            "username",
            "registered_on",
            "_account_id",
            "name",
            "email",
            "gerrit",
        ]

    @check
    def set_name(self, input_: dict):
        """
        Sets the full name of an account.
        Some realms may not allow to modify the account name.
        In this case the request is rejected with '405 Method Not Allowed'.

        .. code-block:: python

            input_ = {
                "name": "Keven Shi"
            }

            account = gerrit.accounts.get('kevin.shi')
            result = account.set_name(input_)


        :param input_: the AccountNameInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-accounts.html#account-name-input
        :return:
        """
        endpoint = "/accounts/%s/name" % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)

        # update account model's name
        self.name = result
        return result

    def delete_name(self):
        """
        Deletes the name of an account.
        Some realms may not allow to delete the account name.
        In this case the request is rejected with '405 Method Not Allowed'.

        :return:
        """
        endpoint = "/accounts/%s/name" % self.username
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))

        # update account model's name
        self.name = None

    @property
    def status(self) -> str:
        """
        Retrieves the status of an account.
        If the account does not have a status an empty string is returned.

        :return:
        """
        endpoint = "/accounts/%s/status" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @status.setter
    def status(self, status: str):
        """
        Sets the status of an account.

        :param status: account status
        :return:
        """
        endpoint = "/accounts/%s/status" % self.username
        input_ = {"status": status}
        base_url = self.gerrit.get_endpoint_url(endpoint)
        self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )

    @check
    def set_username(self, input_: dict):
        """
        Sets the username of an account.
        Some realms may not allow to modify the account username.
        In this case the request is rejected with '405 Method Not Allowed'.

        .. code-block:: python

            input_ = {
                "username": "shijl0925.shi"
            }

            account = gerrit.accounts.get('kevin.shi')
            result = account.set_username(input_)

        :param input_: the UsernameInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-accounts.html#username-input
        :return:
        """
        endpoint = "/accounts/%s/username" % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)

        # update account model's username
        self.username = result
        return result

    def get_active(self) -> str:
        """
        Checks if an account is active.

        :return:
        """
        endpoint = "/accounts/%s/active" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def set_active(self):
        """
        Sets the account state to active.

        :param status: account status
        :return:
        """
        endpoint = "/accounts/%s/active" % self.username
        self.gerrit.requester.put(self.gerrit.get_endpoint_url(endpoint))

    def delete_active(self):
        """
        Sets the account state to inactive.
        If the account was already inactive the response is '409 Conflict'.

        :param status: account status
        :return:
        """
        endpoint = "/accounts/%s/active" % self.username
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))

    @check
    def set_http_password(self, input_: dict) -> str:
        """
        Sets/Generates the HTTP password of an account.

        .. code-block:: python

            input_ = {
                "generate": 'true',
                "http_password": "the_password"
            }

            account = gerrit.accounts.get('kevin.shi')
            result = account.set_http_password(input_)

        :param input_: the HttpPasswordInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-accounts.html#http-password-input
        :return:
        """
        endpoint = "/accounts/%s/password.http" % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def delete_http_password(self):
        """
        Deletes the HTTP password of an account.

        :return:
        """
        endpoint = "/accounts/%s/password.http" % self.username
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))

    def get_oauth_token(self) -> dict:
        """
        Returns a previously obtained OAuth access token.
        If there is no token available, or the token has already expired, '404 Not Found' is returned as response.
        Requests to obtain an access token of another user are rejected with '403 Forbidden'.

        :return:
        """
        endpoint = "/accounts/%s/oauthtoken" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
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
        endpoint = "/accounts/%s/capabilities" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def check_capability(self, capability: str) -> str:
        """
        Checks if a user has a certain global capability.

        :param capability:
        :return:
        """
        endpoint = "/accounts/%s/capabilities/%s" % (self.username, capability)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @property
    def groups(self) -> list:
        """
        Lists all groups that contain the specified user as a member.

        :return:
        """
        endpoint = "/accounts/%s/groups" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return [self.gerrit.groups.get(item.get("id")) for item in result]

    def get_avatar(self) -> str:
        """
        Retrieves the avatar image of the user.
        :return:
        """
        endpoint = "/accounts/%s/avatar" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def get_avatar_change_url(self) -> str:
        """
        Retrieves the avatar image of the user.
        :return:
        """
        endpoint = "/accounts/%s/avatar.change.url" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def get_user_preferences(self):
        """
        Retrieves the user’s preferences.

        :return:
        """
        endpoint = "/accounts/%s/preferences" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_user_preferences(self, input_: dict) -> dict:
        """
        Sets the user’s preferences.

        .. code-block:: python

            input_ = {
                "changes_per_page": 50,
                "show_site_header": true,
                "use_flash_clipboard": true,
                "expand_inline_diffs": true,
                "download_command": "CHECKOUT",
                "date_format": "STD",
                "time_format": "HHMM_12",
                "size_bar_in_change_table": true,
                "review_category_strategy": "NAME",
                "diff_view": "SIDE_BY_SIDE",
                "mute_common_path_prefixes": true,
            }

            account = gerrit.accounts.get('kevin.shi')
            result = account.set_user_preferences(input_)

        :param input_: the PreferencesInput entity，
          https://gerrit-review.googlesource.com/Documentation/rest-api-accounts.html#preferences-input
        :return:
        """
        endpoint = "/accounts/%s/preferences" % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def get_diff_preferences(self):
        """
        Retrieves the diff preferences of a user.

        :return:
        """
        endpoint = "/accounts/%s/preferences.diff" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_diff_preferences(self, input_: dict) -> dict:
        """
        Sets the diff preferences of a user.

        .. code-block:: python

            input_ = {
                "context": 10,
                "theme": "ECLIPSE",
                "ignore_whitespace": "IGNORE_ALL",
                "intraline_difference": true,
                "line_length": 100,
                "cursor_blink_rate": 500,
                "show_line_endings": true,
                "show_tabs": true,
                "show_whitespace_errors": true,
                "syntax_highlighting": true,
                "tab_size": 8,
                "font_size": 12
            }

            account = gerrit.accounts.get('kevin.shi')
            result = account.set_diff_preferences(input_)

        :param input_: the DiffPreferencesInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-accounts.html#diff-preferences-input
        :return:
        """
        endpoint = "/accounts/%s/preferences.diff" % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def get_edit_preferences(self):
        """
        Retrieves the edit preferences of a user.

        :return:
        """
        endpoint = "/accounts/%s/preferences.edit" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_edit_preferences(self, input_: dict) -> dict:
        """
        Sets the edit preferences of a user.

        .. code-block:: python

            input_ = {
                "theme": "ECLIPSE",
                "key_map_type": "VIM",
                "tab_size": 4,
                "line_length": 80,
                "indent_unit": 2,
                "cursor_blink_rate": 530,
                "hide_top_menu": true,
                "show_tabs": true,
                "show_whitespace_errors": true,
                "syntax_highlighting": true,
                "hide_line_numbers": true,
                "match_brackets": true,
                "line_wrapping": false,
                "auto_close_brackets": true
            }

            account = gerrit.accounts.get('kevin.shi')
            result = account.set_edit_preferences(input_)

        :param input_: the EditPreferencesInfo entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-accounts.html#edit-preferences-info
        :return:
        """
        endpoint = "/accounts/%s/preferences.edit" % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def get_watched_projects(self) -> list:
        """
        Retrieves all projects a user is watching.

        :return:
        """
        endpoint = "/accounts/%s/watched.projects" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def modify_watched_projects(self, input_: list) -> list:
        """
        Add new projects to watch or update existing watched projects.

        :param input_: the ProjectWatchInfo entities as list
        :return:
        """
        endpoint = "/accounts/%s/watched.projects" % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def delete_watched_projects(self, input_: list):
        """
        Projects posted to this endpoint will no longer be watched.

        :param input_: the watched projects as list
        :return:
        """
        endpoint = "/accounts/%s/watched.projects:delete" % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )

    def get_external_ids(self) -> list:
        """
        Retrieves the external ids of a user account.

        :return:
        """
        endpoint = "/accounts/%s/external.ids" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def delete_external_ids(self, input_: list):
        """
        Delete a list of external ids for a user account.

        :param input_: the external ids as list
        :return:
        """
        endpoint = "/accounts/%s/external.ids:delete" % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )

    def list_contributor_agreements(self) -> list:
        """
        Gets a list of the user’s signed contributor agreements.

        :return:
        """
        endpoint = "/accounts/%s/agreements" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def sign_contributor_agreement(self, input_: dict) -> str:
        """
        Signs a contributor agreement.

        .. code-block:: python

            input_ = {
                "name": "Individual"
            }
            account = gerrit.accounts.get('kevin.shi')
            result = account.sign_contributor_agreement(input_)

        :param input_: the ContributorAgreementInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-accounts.html#contributor-agreement-input
        :return:
        """
        endpoint = "/accounts/%s/agreements" % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def delete_draft_comments(self, input_: dict) -> list:
        """
        Deletes some or all of a user’s draft comments.

        :param input_: the DeleteDraftCommentsInput entity
        :return:
        """
        endpoint = "/accounts/%s/drafts:delete" % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result

    def index(self):
        """
        Adds or updates the account in the secondary index.

        :return:
        """
        endpoint = "/accounts/%s/index" % self.username
        self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))

    def get_default_starred_changes(self) -> list:
        """
        Gets the changes that were starred with the default star by the identified user account.

        :return:
        """
        endpoint = "/accounts/%s/starred.changes" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return [self.gerrit.changes.get(item.get("id")) for item in result]

    def put_default_star_on_change(self, change):
        """
        Star a change with the default label.

        :param change:
        :return:
        """
        endpoint = "/accounts/%s/starred.changes/%s" % (self.username, change.id)
        self.gerrit.requester.put(self.gerrit.get_endpoint_url(endpoint))

    def remove_default_star_from_change(self, change):
        """
        Remove the default star label from a change. This stops notifications.

        :param change:
        :return:
        """
        endpoint = "/accounts/%s/starred.changes/%s" % (self.username, change.id)
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))

    def get_starred_changes(self) -> list:
        """
        Gets the changes that were starred with any label by the identified user account.

        :return:
        """
        endpoint = "/accounts/%s/stars.changes" % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return [self.gerrit.changes.get(item.get("id")) for item in result]

    def get_star_labels_from_change(self, change) -> list:
        """
        Get star labels from a change.

        :param change:
        :return:
        """
        endpoint = "/accounts/%s/stars.changes/%s" % (self.username, change.id)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def update_star_labels_on_change(self, change, input_: dict):
        """
        Update star labels on a change.

        .. code-block:: python

            input_ = {
                "add": ["blue", "red"],
                "remove": ["yellow"]
            }

            account = gerrit.accounts.get('kevin.shi')
            result = account.update_star_labels_on_change(change, input_)


        :param change:
        :param input_: the StarsInput entity,
          http://172.16.212.117:8080/Documentation/rest-api-accounts.html#stars-input
        :return:
        """
        endpoint = "/accounts/%s/stars.changes/%s" % (self.username, change.id)
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return result
