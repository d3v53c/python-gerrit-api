#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.groups.group import GerritGroup
from gerrit.utils.common import check
from gerrit.utils.exceptions import UnknownGroup


class GerritGroups:
    def __init__(self, gerrit):
        self.gerrit = gerrit

    def list(self) -> list:
        """
        Lists the groups accessible by the caller.

        :return:
        """
        endpoint = '/groups/'
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)

        groups = []
        for key, value in result.items():
            group = value
            group.update({'name': key})
            groups.append(group)

        return GerritGroup.parse_list(groups, gerrit=self.gerrit)

    def search(self, name: str) -> list:
        """
        Query Groups

        :param name:
        :return:
        """
        endpoint = '/groups/?query2=inname:%s' % name
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return GerritGroup.parse_list(result, gerrit=self.gerrit)

    def get(self, id: str) -> GerritGroup:
        """
        Retrieves a group.

        :param id:
        :return:
        """
        endpoint = '/groups/%s' % id
        response = self.gerrit.make_call('get', endpoint)
        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            return GerritGroup.parse(result, gerrit=self.gerrit)
        else:
            raise UnknownGroup(id)

    def create(self, name: str, GroupInput: dict) -> GerritGroup:
        """
        Creates a new Gerrit internal group.

        :param name: group name
        :param GroupInput: the GroupInput entity
        :return:
        """
        endpoint = '/groups/%s' % name
        response = self.gerrit.make_call('put', endpoint, **GroupInput)
        result = self.gerrit.decode_response(response)
        return GerritGroup.parse(result, gerrit=self.gerrit)
