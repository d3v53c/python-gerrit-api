#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
import six.moves.urllib.parse as urlparse
from requests import Session
from requests.adapters import HTTPAdapter


class Requester:

    """
    A class which carries out HTTP requests. You can replace this
    class with one of your own implementation if you require some other
    way to access Gerrit.
    This default class can handle simple authentication only.
    """

    VALID_STATUS_CODES = [200, ]
    AUTH_COOKIE = None

    def __init__(self, **kwargs):
        """
        :param kwargs:
        """
        timeout = 10
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.ssl_verify = kwargs.get('ssl_verify')
        self.cert = kwargs.get('cert')
        self.timeout = kwargs.get('timeout', timeout)
        self.session = Session()

        self.max_retries = kwargs.get('max_retries')
        if self.max_retries is not None:
            retry_adapter = HTTPAdapter(max_retries=self.max_retries)
            self.session.mount('http://', retry_adapter)
            self.session.mount('https://', retry_adapter)

    def get_request_dict(self, params=None, data=None, files=None, headers=None, **kwargs):
        """
        :param params:
        :param data:
        :param files:
        :param headers:
        :param kwargs:
        :return:
        """
        request_kwargs = kwargs
        if self.username and self.password:
            request_kwargs['auth'] = (self.username, self.password)

        if params:
            assert isinstance(
                params, dict), 'Params must be a dict, got %s' % repr(params)
            request_kwargs['params'] = params

        if headers:
            assert isinstance(
                headers, dict), \
                'headers must be a dict, got %s' % repr(headers)
            request_kwargs['headers'] = headers

        if self.AUTH_COOKIE:
            currentheaders = request_kwargs.get('headers', {})
            currentheaders.update({'Cookie': self.AUTH_COOKIE})
            request_kwargs['headers'] = currentheaders

        request_kwargs['verify'] = self.ssl_verify
        request_kwargs['cert'] = self.cert

        if data:
            # It may seem odd, but some Gerrit operations require posting
            # an empty string.
            request_kwargs['data'] = data

        if files:
            request_kwargs['files'] = files

        request_kwargs['timeout'] = self.timeout

        return request_kwargs

    def get(self, url, params=None, headers=None, allow_redirects=True, stream=False):
        """
        :param url:
        :param params:
        :param headers:
        :param allow_redirects:
        :param stream:
        :return:
        """
        request_kwargs = self.get_request_dict(
            params=params,
            headers=headers,
            allow_redirects=allow_redirects,
            stream=stream
        )
        return self.session.get(url, **request_kwargs)

    def post(self, url, params=None, data=None, json=None, files=None, headers=None, allow_redirects=True, **kwargs):
        """
        :param url:
        :param params:
        :param data:
        :param json:
        :param files:
        :param headers:
        :param allow_redirects:
        :param kwargs:
        :return:
        """
        request_kwargs = self.get_request_dict(
            params=params,
            data=data,
            json=json,
            files=files,
            headers=headers,
            allow_redirects=allow_redirects,
            **kwargs)
        return self.session.post(url, **request_kwargs)

    def put(self, url, params=None, data=None, json=None, files=None, headers=None, allow_redirects=True, **kwargs):
        """
        :param url:
        :param params:
        :param data:
        :param json:
        :param files:
        :param headers:
        :param allow_redirects:
        :param kwargs:
        :return:
        """
        request_kwargs = self.get_request_dict(
            params=params,
            data=data,
            json=json,
            files=files,
            headers=headers,
            allow_redirects=allow_redirects,
            **kwargs)
        return self.session.put(url, **request_kwargs)

    def delete(self, url, params=None, data=None, headers=None, allow_redirects=True, **kwargs):
        """
        :param url:
        :param params:
        :param data:
        :param headers:
        :param allow_redirects:
        :param kwargs:
        :return:
        """
        request_kwargs = self.get_request_dict(
            params=params,
            data=data,
            headers=headers,
            allow_redirects=allow_redirects,
            **kwargs)
        return self.session.delete(url, **request_kwargs)