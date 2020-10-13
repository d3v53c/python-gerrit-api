#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.exceptions import UnknownTag
from gerrit.utils.common import check
from gerrit.utils.models import BaseModel


class Tag(BaseModel):
    tag_prefix = 'refs/tags/'

    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)
        self.attributes = ['ref', 'object', 'message', 'revision', 'tagger', 'project', 'gerrit']

    @property
    def name(self):
        return self.ref.replace(self.tag_prefix, '')

    def delete(self):
        """
        Delete a tag.

        :return:
        """
        endpoint = '/projects/%s/tags/%s' % (self.project, self.name)
        response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
        response.raise_for_status()


class Tags:
    tag_prefix = 'refs/tags/'

    def __init__(self, project, gerrit):
        self.project = project
        self.gerrit = gerrit
        self._data = self.poll()

    def poll(self):
        """

        :return:
        """
        endpoint = '/projects/%s/tags/' % self.project
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def iterkeys(self):
        """
        Iterate over the names of all available tags
        """
        for row in self._data:
            yield row['ref']

    def keys(self):
        """
        Return a list of the names of all tags
        """
        return list(self.iterkeys())

    def __len__(self):
        """

        :return:
        """
        return len(self.keys())

    def __contains__(self, ref):
        """
        True if ref exists in project
        """
        return ref in self.keys()

    def __getitem__(self, ref):
        """
        get a tag by ref

        :param ref:
        :return:
        """
        if not ref.startswith(self.tag_prefix):
            raise KeyError("tag ref should start with {}".format(self.tag_prefix))

        result = [row for row in self._data if row['ref'] == ref]
        if result:
            ref_date = result[0]
            return Tag.parse(ref_date, project=self.project, gerrit=self.gerrit)
        else:
            raise UnknownTag(ref)

    def __setitem__(self, key, value):
        """
        create a tag by ref
        :param key:
        :param value:
        :return:
        """
        if not key.startswith(self.tag_prefix):
            raise KeyError("tag ref should start with {}".format(self.tag_prefix))

        self.create(key.replace(self.tag_prefix, ''), value)

    def __delitem__(self, key):
        """
        Delete a tag by ref

        :param key:
        :return:
        """
        self[key].delete()

    def __iter__(self):
        """

        :return:
        """
        for row in self._data:
            yield Tag.parse(row, project=self.project, gerrit=self.gerrit)

    @check
    def create(self, name: str, input_: dict) -> Tag:
        """
        Creates a new tag on the project.

        :param name: the tag name
        :param input_: the TagInput entity
        :return:
        """
        ref = self.tag_prefix + name
        if ref in self.keys():
            return self[ref]

        endpoint = '/projects/%s/tags/%s' % (self.project, name)
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return Tag.parse(result, project=self.project, gerrit=self.gerrit)
