#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.accounts.account import GerritAccount
from gerrit.utils.common import check


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
            yield GerritAccount(username=item.get('username'), gerrit=self.gerrit)

    def get(self, username: str) -> GerritAccount:
        """
        Returns an account

        :param username:
        :return:
        """
        return GerritAccount(username=username, gerrit=self.gerrit)

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
        return GerritAccount(username=result.get('username'), gerrit=self.gerrit)

