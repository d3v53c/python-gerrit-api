#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.models import BaseModel


class GerritGroup(BaseModel):
    def __init__(self, **kwargs):
        super(GerritGroup, self).__init__(**kwargs)
        self.attributes = [
            "name",
            "url",
            "options",
            "description",
            "id",
            "group_id",
            "owner",
            "owner_id",
            "created_on",
            "gerrit",
        ]

    def rename(self, input_):
        """
        Renames a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        .. code-block:: python

            input_ = {
                "name": "My Project Committers"
            }

            group = gerrit.groups.get('0017af503a22f7b3fa6ce2cd3b551734d90701b4')
            result = group.rename(input_)

        :param input_:
        :return:
        """
        endpoint = "/groups/%s/name" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)

        # update group model's name
        self.name = result
        return result

    def set_description(self, input_):
        """
        Sets the description of a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        .. code-block:: python

            input_ = {
                "description": "The committers of MyProject."
            }
            group = gerrit.groups.get('0017af503a22f7b3fa6ce2cd3b551734d90701b4')
            result = group.set_description(input_)

        :param input_:
        :return:
        """
        endpoint = "/groups/%s/description" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)

        # update group model's description
        self.description = result
        return result

    def delete_description(self):
        """
        Deletes the description of a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :return:
        """
        endpoint = "/groups/%s/description" % self.id
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))

        # update group model's description
        self.description = None

    def set_options(self, input_):
        """
        Sets the options of a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        .. code-block:: python

            input_ = {
                "visible_to_all": true
            }
            group = gerrit.groups.get('0017af503a22f7b3fa6ce2cd3b551734d90701b4')
            result = group.set_options(input_)


        :param input_: the GroupOptionsInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-groups.html#group-options-input
        :return:
        """
        endpoint = "/groups/%s/options" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)

        # update group model's options
        self.options = result
        return result

    def set_owner(self, input_):
        """
        Sets the owner group of a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        .. code-block:: python

            input_ = {
                "owner": "6a1e70e1a88782771a91808c8af9bbb7a9871389"
            }
            group = gerrit.groups.get('0017af503a22f7b3fa6ce2cd3b551734d90701b4')
            result = group.set_owner(input_)

        :param input_:
        :return:
        """
        endpoint = "/groups/%s/owner" % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)

        # update group model's owner and owner_id
        self.owner = result.get("owner")
        self.owner_id = result.get("owner_id")

        return self.gerrit.groups.get(result.get("owner_id"))

    def get_audit_log(self):
        """
        Gets the audit log of a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :return:
        """
        endpoint = "/groups/%s/log.audit" % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def index(self):
        """
        Adds or updates the internal group in the secondary index.

        :return:
        """
        endpoint = "/groups/%s/index" % self.id
        self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))

    def list_members(self):
        """
        Lists the direct members of a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :return:
        """
        endpoint = "/groups/%s/members/" % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return [self.gerrit.accounts.get(member.get("username")) for member in result]

    def get_member(self, username):
        """
        Retrieves a group member.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param username: account username
        :return:
        """
        account = self.gerrit.accounts.get(username)
        endpoint = "/groups/%s/members/%s" % (self.id, str(account._account_id))
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.accounts.get(result.get("username"))

    def add_member(self, username):
        """
        Adds a user as member to a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param username: account username
        :return:
        """
        endpoint = "/groups/%s/members/%s" % (self.id, username)
        response = self.gerrit.requester.put(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.accounts.get(result.get("username"))

    def remove_member(self, username):
        """
        Removes a user from a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param username: account username
        :return:
        """
        endpoint = "/groups/%s/members/%s" % (self.id, username)
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))

    def list_subgroups(self):
        """
        Lists the direct subgroups of a group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :return:
        """
        endpoint = "/groups/%s/groups/" % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return [self.gerrit.groups.get(item.get("id")) for item in result]

    def get_subgroup(self, id_):
        """
        Retrieves a subgroup.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param id_: sub group id
        :return:
        """
        endpoint = "/groups/%s/groups/%s" % (self.id, id_)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.groups.get(result.get("id"))

    def add_subgroup(self, id_):
        """
        Adds an internal or external group as subgroup to a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param id_: subgroup id
        :return:
        """
        endpoint = "/groups/%s/groups/%s" % (self.id, id_)
        response = self.gerrit.requester.put(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.groups.get(result.get("id"))

    def remove_subgroup(self, id_):
        """
        Removes a subgroup from a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param id_: subgroup id
        :return:
        """
        endpoint = "/groups/%s/groups/%s" % (self.id, id_)
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
