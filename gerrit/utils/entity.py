#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
import json
from gerrit.utils.common import logger


class Entity(object):
    required = ()
    optional = ()

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        self.attributes = self.required + self.optional

        for item in self.required:
            if item not in kwargs.keys():
                logger.warning(
                    "*** Warning! {} missing a required keyword argument '{}' ***".format(
                        self.__class__.__name__, item
                    )
                )

        for (k, v) in kwargs.items():
            if k in self.attributes:
                setattr(self, k, v)
            else:
                logger.warning(
                    "*** Warning! {} got an unexpected keyword argument: '{}' ***".format(
                        self.__class__.__name__, k
                    )
                )

    def __getattr__(self, key):
        return self.__dict__.get(key, None)

    def __str__(self):
        """

        :return:
        """
        review_input = {}
        for key in self.attributes:
            value = getattr(self, key)
            if value:
                review_input.update({key: value})

        return json.dumps(review_input, sort_keys=True)
