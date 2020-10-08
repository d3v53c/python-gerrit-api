#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
import re
import json
import inspect
from functools import wraps


def get_args(func):
    """
    Returns a sequence of list (args) for func
    :param func:
    :return:
    """
    argspec = inspect.getargspec(func)

    if not argspec.defaults:
        args = argspec.args[1:]
    else:
        args = argspec.args[1 : -len(argspec.defaults)]

    return args


def get_default_kwargs(func):
    """
    Returns a sequence of tuples (kwarg_name, default_value) for func

    :param func:
    :return:
    """
    argspec = inspect.getargspec(func)

    if not argspec.defaults:
        return []

    return zip(argspec.args[-len(argspec.defaults) :], argspec.defaults)


def translate_params(f, *args, **kwargs):
    """

    :param f:
    :param args:
    :param kwargs:
    :return:
    """
    all_params = dict(get_default_kwargs(f))

    if len(get_args(f)) < len(args):
        additional_values = args[len(get_args(f)) :]
        func_parameters = inspect.getargspec(f).args[1:]
        additional_args = func_parameters[
            len(get_args(f)) : len(get_args(f)) + len(additional_values)
        ]
        all_params.update(dict(zip(additional_args, additional_values)))

    all_params.update(dict(zip(get_args(f), args)))
    all_params.update(kwargs)

    for key in list(all_params.keys()):
        if not all_params[key]:
            del all_params[key]

    return all_params


def endpoint(url_pattern, method="GET"):
    """

    :param url_pattern:
    :param method:
    :param item:
    :return:
    """
    def wrapped_func(f):
        def get_url(*args, **kwargs):
            all_kwargs = dict(get_default_kwargs(f))

            # kwargs for positional arguments passed by caller
            groups = re.findall('{(\w+)}', url_pattern)

            all_kwargs.update(dict(zip(groups, args)))

            # kwargs for keyword arguments passed by caller
            all_kwargs.update(kwargs)

            return url_pattern.format(*args, **all_kwargs)

        @wraps(f)
        def inner_func(self, *args, **kwargs):
            """

            :param self:
            :param args:
            :param kwargs:
            :return:
            """
            url = get_url(*args, **kwargs)
            params = translate_params(f, *args, **kwargs)

            # remove positional arguments from params
            groups = re.findall('{(\w+)}', url_pattern)
            for item in groups:
                del params[item]

            response = self.gerrit.make_call(method, url, **params)
            return self.gerrit.decode_response(response)

        return inner_func

    return wrapped_func


def GET(url_pattern):
    """

    :param url_pattern:
    :return:
    """
    return endpoint(url_pattern, method="get")


def POST(url_pattern):
    """

    :param url_pattern:
    :return:
    """
    return endpoint(url_pattern, method="post")


def PUT(url_pattern):
    """

    :param url_pattern:
    :return:
    """
    return endpoint(url_pattern, method="put")


def DELETE(url_pattern):
    """

    :param url_pattern:
    :return:
    """
    return endpoint(url_pattern, method="delete")
