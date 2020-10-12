#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.models import BaseModel
from gerrit.accounts.account import GerritAccount
from gerrit.utils.common import check


class GerritGroup(BaseModel):
    def __init__(self, **kwargs):
        super(GerritGroup, self).__init__(**kwargs)
        self.attributes = ['name', 'url', 'options', 'description',
                           'id', 'group_id', 'owner', 'owner_id', 'created_on', 'gerrit']

    @check
    def set_name(self, GroupNameInput: dict) -> str:
        """
        Renames a Gerrit internal group.

        :param GroupNameInput: the GroupNameInput entity
        :return:
        """
        endpoint = '/groups/%s/name' % self.id
        response = self.gerrit.make_call('put', endpoint, **GroupNameInput)
        result = self.gerrit.decode_response(response)

        # update group model's name
        self.name = result

        return result

    @check
    def set_description(self, GroupDescriptionInput: dict) -> str:
        """
        Sets the description of a Gerrit internal group.

        :param GroupDescriptionInput: the GroupDescriptionInput entity
        :return:
        """
        endpoint = '/groups/%s/description' % self.id
        response = self.gerrit.make_call('put', endpoint, **GroupDescriptionInput)
        result = self.gerrit.decode_response(response)

        # update group model's description
        self.description = result

        return result

    def delete_description(self):
        """
        Sets the description of a Gerrit internal group.

        :return:
        """
        endpoint = '/groups/%s/description' % self.id
        response = self.gerrit.make_call('delete', endpoint)
        response.raise_for_status()

        # update group model's description
        self.description = None

    @check
    def set_options(self, GroupOptionsInput: dict) -> dict:
        """
        Sets the options of a Gerrit internal group.

        :param GroupOptionsInput: the GroupOptionsInput entity
        :return:
        """
        endpoint = '/groups/%s/options' % self.id
        response = self.gerrit.make_call('put', endpoint, **GroupOptionsInput)
        result = self.gerrit.decode_response(response)

        # update group model's options
        self.options = result

        return result

    @check
    def set_owner(self, GroupOwnerInput: dict):
        """
        Sets the owner group of a Gerrit internal group.

        :param GroupOwnerInput: the GroupOwnerInput entity
        :return:
        """
        endpoint = '/groups/%s/owner' % self.id
        response = self.gerrit.make_call('put', endpoint, **GroupOwnerInput)
        result = self.gerrit.decode_response(response)

        # update group model's owner and owner_id
        self.owner = result.get('owner')
        self.owner_id = result.get('owner_id')

        return self.gerrit.groups.get(result.get('owner_id'))

    def get_audit_log(self) -> list:
        """
        Gets the audit log of a Gerrit internal group.

        :return:
        """
        endpoint = '/groups/%s/log.audit' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    def index(self):
        """

        :return:
        """
        endpoint = '/groups/%s/index' % self.id
        response = self.gerrit.make_call('post', endpoint)
        response.raise_for_status()

    def list_members(self) -> list:
        """
        Lists the direct members of a Gerrit internal group.

        :return:
        """
        endpoint = '/groups/%s/members/' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return [self.gerrit.accounts.get(member.get('username')) for member in result]

    def get_member(self, username: str) -> GerritAccount:
        """
        Retrieves a group member.

        :param username: account username
        :return:
        """
        account = self.gerrit.accounts.get(username)
        endpoint = '/groups/%s/members/%s' % (self.id, str(account._account_id))
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return self.gerrit.accounts.get(result.get('username'))

    def add_member(self, account: GerritAccount) -> GerritAccount:
        """
        Adds a user as member to a Gerrit internal group.

        :param account:
        :return:
        """
        endpoint = '/groups/%s/members/%s' % (self.id, str(account._account_id))
        response = self.gerrit.make_call('put', endpoint)
        result = self.gerrit.decode_response(response)
        return self.gerrit.accounts.get(result.get('username'))

    def remove_member(self, account: GerritAccount):
        """
        Removes a user from a Gerrit internal group.

        :param account:
        :return:
        """
        endpoint = '/groups/%s/members/%s' % (self.id, str(account._account_id))
        response = self.gerrit.make_call('delete', endpoint)
        response.raise_for_status()
