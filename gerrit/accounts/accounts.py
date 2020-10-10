#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.accounts.account import GerritAccount
from gerrit.utils.common import check
from gerrit.utils.exceptions import UnknownAccount


class GerritAccounts:
    def __init__(self, gerrit):
        self.gerrit = gerrit

    def search(self, query: str):
        """
        Queries accounts visible to the caller.

        :param query:
        :return:
        """
        endpoint = '/accounts/?suggest&q=%s' % query
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        for item in result:
            yield GerritAccount(json=item, gerrit=self.gerrit)

    def get(self, username: str) -> GerritAccount:
        """
        Returns an account

        :param username:
        :return:
        """
        endpoint = '/accounts/%s/detail' % username
        response = self.gerrit.make_call('get', endpoint)

        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            return GerritAccount(json=result, gerrit=self.gerrit)
        else:
            raise UnknownAccount(username)

    @check
    def create(self, username: str, AccountInput: dict) -> GerritAccount:
        """
        Creates a new account.

        :param username: account username
        :param AccountInput: the AccountInput entity
        :return:
        """
        endpoint = '/accounts/%s' % username
        response = self.gerrit.make_call('put', endpoint, **AccountInput)
        result = self.gerrit.decode_response(response)
        return GerritAccount(json=result, gerrit=self.gerrit)
