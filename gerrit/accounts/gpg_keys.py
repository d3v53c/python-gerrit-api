#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.models import BaseModel
from gerrit.utils.exceptions import UnknownGPGKey
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
        response = self.gerrit.make_call('delete', endpoint)
        response.raise_for_status()


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
        response = self.gerrit.make_call('get', endpoint)
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
        response = self.gerrit.make_call('get', endpoint)
        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            return GPGKey.parse(result, username=self.username, gerrit=self.gerrit)
        else:
            raise UnknownGPGKey(gpg_key_id)

    @check
    def modify(self, GpgKeysInput: dict):
        """
        Add or delete one or more GPG keys for a user.

        :param GpgKeysInput: the GpgKeysInput entity
        :return:
        """
        endpoint = '/accounts/%s/gpgkeys' % self.username
        response = self.gerrit.make_call('post', endpoint, **GpgKeysInput)
        result = self.gerrit.decode_response(response)
        return result

    def delete(self, gpg_key_id: str):
        """
        Deletes a GPG key of a user.

        :param gpg_key_id: GPG key id
        :return:
        """
        self.get(gpg_key_id).delete()
