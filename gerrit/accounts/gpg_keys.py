#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.models import BaseModel
from gerrit.utils.common import check


class GPGKey(BaseModel):
    def __init__(self, **kwargs):
        super(GPGKey, self).__init__(**kwargs)
        self.attributes = ['id', 'fingerprint', 'user_ids', 'key', 'status', 'problems', 'username', 'gerrit']

    def delete(self):
        """
        Deletes a GPG key of a user.

        :return:
        """
        endpoint = '/accounts/%s/gpgkeys/%s' % (self.username, self.id)
        self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))


class GPGKeys:
    def __init__(self, username, gerrit):
        self.username = username
        self.gerrit = gerrit

    def list(self) -> list:
        """
        Returns the GPG keys of an account.

        :return:
        """
        endpoint = '/accounts/%s/gpgkeys' % self.username
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        keys = []
        for key, value in result.items():
            gpg_key = value
            gpg_key.update({'id': key})
            keys.append(gpg_key)

        return GPGKey.parse_list(keys, username=self.username, gerrit=self.gerrit)

    def get(self, gpg_key_id: str) -> GPGKey:
        """
        Retrieves a GPG key of a user.

        :param gpg_key_id: GPG key id
        :return:
        """
        endpoint = '/accounts/%s/gpgkeys/%s' % (self.username, gpg_key_id)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return GPGKey.parse(result, username=self.username, gerrit=self.gerrit)

    @check
    def modify(self, input_: dict):
        """
        Add or delete one or more GPG keys for a user.

        :param input_: the GpgKeysInput entity
        :return:
        """
        endpoint = '/accounts/%s/gpgkeys' % self.username
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    def delete(self, gpg_key_id: str):
        """
        Deletes a GPG key of a user.

        :param gpg_key_id: GPG key id
        :return:
        """
        self.get(gpg_key_id).delete()
