#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.exceptions import UnknownTask
from gerrit.utils.models import BaseModel


class Task(BaseModel):
    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)
        self.attributes = ['id', 'state', 'command', 'start_time', 'queue_name', 'delay', 'gerrit']

    def delete(self):
        """
        Kills a task from the background work queue that the Gerrit daemon is currently performing,
        or will perform in the near future.

        :return:
        """
        endpoint = '/config/server/tasks/%s' % self.id
        response = self.gerrit.make_call('delete', endpoint)
        response.raise_for_status()


class Tasks:
    def __init__(self, gerrit):
        self.gerrit = gerrit

    def list(self) -> list:
        """
        Lists the tasks from the background work queues that the Gerrit daemon is currently performing,
        or will perform in the near future.

        :return:
        """
        endpoint = '/config/server/tasks/'
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return Task.parse_list(result, gerrit=self.gerrit)

    def get(self, id: str) -> Task:
        """
        Retrieves a task from the background work queue that the Gerrit daemon is currently performing,
        or will perform in the near future.

        :param id: task id
        :return:
        """
        endpoint = '/config/server/tasks/%s' % id
        response = self.gerrit.make_call('get', endpoint)
        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            return Task.parse(result, gerrit=self.gerrit)
        else:
            raise UnknownTask(id)
