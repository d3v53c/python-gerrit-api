#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.models import BaseModel
from gerrit.utils.exceptions import UnknownSSHKey


class SSHKey(BaseModel):
    def __init__(self, **kwargs):
        super(SSHKey, self).__init__(**kwargs)
        self.attributes = ['seq', 'ssh_public_key', 'encoded_key', 'algorithm', 'comment', 'valid', 'username', 'gerrit']

    def delete(self):
        """
        Deletes an SSH key of a user.

        :return:
        """
        endpoint = '/accounts/%s/sshkeys/%s' % (self.username, self.seq)
        response = self.gerrit.make_call('delete', endpoint)
        response.raise_for_status()


class SSHKeys:
    def __init__(self, username, gerrit):
        self.username = username
        self.gerrit = gerrit

    def list(self) -> list:
        """
        Returns the SSH keys of an account.

        :return:
        """
        endpoint = '/accounts/%s/sshkeys' % self.username
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return SSHKey.parse_list(result, username=self.username, gerrit=self.gerrit)

    def get(self, seq: int) -> SSHKey:
        """
        Retrieves an SSH key of a user.

        :param seq: SSH key id
        :return:
        """
        endpoint = '/accounts/%s/sshkeys/%s' % (self.username, seq)
        response = self.gerrit.make_call('get', endpoint)
        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            return SSHKey.parse(result, username=self.username, gerrit=self.gerrit)
        else:
            raise UnknownSSHKey(seq)

    def add(self, ssh_key: str) -> SSHKey:
        """
        Adds an SSH key for a user.
        The SSH public key must be provided as raw content in the request body.

        :param ssh_key: SSH key raw content
        :return:
        """
        endpoint = '/accounts/%s/sshkeys' % self.username
        base_url = self.gerrit._get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, data=ssh_key, headers={'Content-Type': 'plain/text'})
        result = self.gerrit.decode_response(response)
        return SSHKey.parse(result, username=self.username, gerrit=self.gerrit)

    def delete(self, seq: int):
        """
        Deletes an SSH key of a user.

        :param seq: SSH key id
        :return:
        """
        self.get(seq).delete()
