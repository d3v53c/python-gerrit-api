#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
import inspect


def check(fn):
    def wrapper(*args, **kwargs):
        sig = inspect.signature(fn)
        params = sig.parameters
        argspec = list(params.keys())

        # check args and kwargs type
        for i, p in enumerate(args):
            arg_type = fn.__annotations__.get(argspec[i], None)
            if arg_type and not isinstance(p, arg_type):
                raise RuntimeError("{} should be {}, not {}".format(argspec[i], arg_type.__name__, type(p).__name__))
        for k, v in kwargs.items():
            kwarg_type = fn.__annotations__.get(k, None)
            if kwarg_type and not isinstance(v, kwarg_type):
                raise RuntimeError("{} should be {}, not {}".format(k, kwarg_type.__name__, type(v).__name__))

        result = fn(*args, **kwargs)

        # check return type
        return_type = fn.__annotations__.get('return', None)
        if return_type and not isinstance(result, return_type):
            raise RuntimeError("{} should return {}, not {}".format(fn.__name__,
                                                                    return_type.__name__,
                                                                    type(result).__name__))

        return result
    return wrapper

