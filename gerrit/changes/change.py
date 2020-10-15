#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.common import check
from gerrit.accounts.account import GerritAccount
from gerrit.utils.models import BaseModel


class GerritChange(BaseModel):
    def __init__(self, **kwargs):
        super(GerritChange, self).__init__(**kwargs)
        self.attributes = ['id', 'project', 'branch', 'change_id', 'subject', 'status', 'created', 'updated',
                           'mergeable', 'insertions', 'deletions', '_number', 'owner', 'gerrit']

    @property
    def topic(self) -> str:
        """
        Retrieves the topic of a change.

        :return:
        """
        endpoint = '/changes/%s/topic' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @topic.setter
    def topic(self, topic: str):
        """
        Sets the topic of a change.

        :param topic: The new topic
        :return:
        """
        endpoint = '/changes/%s/topic' % self.id
        input_ = {"topic": topic}
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    @topic.deleter
    def topic(self):
        """
        Deletes the topic of a change.

        :return:
        """
        endpoint = '/changes/%s/topic' % self.id
        response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
        response.raise_for_status()

    def get_assignee(self) -> GerritAccount:
        """
        Retrieves the account of the user assigned to a change.

        :return:
        """
        endpoint = '/changes/%s/assignee' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.accounts.get(result.get('username'))

    @check
    def set_assignee(self, input_: dict) -> GerritAccount:
        """

        :param input_: the AssigneeInput entity
        :return:
        """
        endpoint = '/changes/%s/assignee' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return self.gerrit.accounts.get(result.get('username'))

    def get_past_assignees(self) -> list:
        """
        Returns a list of every user ever assigned to a change, in the order in which they were first assigned.

        :return:
        """
        endpoint = '/changes/%s/past_assignees' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        assignees = [self.gerrit.accounts.get(item.get('username')) for item in result]
        return assignees

    def delete_assignee(self):
        """
        Deletes the assignee of a change.

        :return:
        """
        endpoint = '/changes/%s/assignee' % self.id
        response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.accounts.get(result.get('username'))

    def get_pure_revert(self, commit) -> dict:
        """
        Check if the given change is a pure revert of the change it references in revertOf.

        :param commit: commit id
        :return:
        """
        endpoint = '/changes/%s/pure_revert?o=%s' % (self.id, commit)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def abandon(self):
        """
        Abandons a change.

        :return:
        """
        endpoint = '/changes/%s/abandon' % self.id
        response = self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.changes.get(result.get('id'))

    def restore(self):
        """
        Restores a change.

        :return:
        """
        endpoint = '/changes/%s/restore' % self.id
        response = self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.changes.get(result.get('id'))

    @check
    def rebase(self, input_: dict):
        """
        Rebases a change.
        If the change cannot be rebased, e.g. due to conflicts, the response is “409 Conflict”
        and the error message is contained in the response body.

        :param input_: the RebaseInput entity
        :return:
        """
        endpoint = '/changes/%s/rebase' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return self.gerrit.changes.get(result.get('id'))

    @check
    def move(self, input_: dict):
        """
        Move a change.
        If the change cannot be moved because the change state doesn’t allow moving the change,
        the response is “409 Conflict” and the error message is contained in the response body.

        :param input_: the MoveInput entity
        :return:
        """
        endpoint = '/changes/%s/move' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return self.gerrit.changes.get(result.get('id'))

    @check
    def revert(self, input_: dict):
        """
        Reverts a change.
        If the change cannot be reverted because the change state doesn’t allow reverting the change,
        the response is “409 Conflict” and the error message is contained in the response body.

        :param input_: the RevertInput entity
        :return:
        """
        endpoint = '/changes/%s/revert' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return self.gerrit.changes.get(result.get('id'))

    @check
    def submit(self, input_: dict):
        """
        Submits  a change.
        If the change cannot be submitted because the submit rule doesn’t allow submitting the change,
        the response is “409 Conflict” and the error message is contained in the response body.

        :param input_: the SubmitInput entity
        :return:
        """
        endpoint = '/changes/%s/submit' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return self.gerrit.changes.get(result.get('id'))

    @check
    def delete(self):
        """

        :return:
        """
        endpoint = '/changes/%s' % self.id
        response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
        response.raise_for_status()

    def get_include_in(self) -> dict:
        """
        Retrieves the branches and tags in which a change is included.

        :return:
        """
        endpoint = '/changes/%s/in' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def index(self):
        """
        Adds or updates the change in the secondary index.

        :return:
        """
        endpoint = '/changes/%s/index' % self.id
        response = self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))
        response.raise_for_status()

    def list_comments(self) -> dict:
        """
        Lists the published comments of all revisions of the change.

        :return:
        """
        endpoint = '/changes/%s/comments' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def list_robot_comments(self) -> dict:
        """
        Lists the robot comments of all revisions of the change.

        :return:
        """
        endpoint = '/changes/%s/robotcomments' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def list_drafts(self) -> dict:
        """
        Lists the draft comments of all revisions of the change that belong to the calling user.

        :return:
        """
        endpoint = '/changes/%s/drafts' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def consistency_check(self) -> dict:
        """
        Performs consistency checks on the change, and returns a ChangeInfo entity with the problems field set to
        a list of ProblemInfo entities.

        :return:
        """
        endpoint = '/changes/%s/check' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def fix(self, input_: dict = None) -> dict:
        """
        Performs consistency checks on the change as with GET /check,
        and additionally fixes any problems that can be fixed automatically. The returned field values reflect any fixes.
        Some fixes have options controlling their behavior, which can be set in the FixInput entity body.
        Only the change owner, a project owner, or an administrator may fix changes.

        :param input_: the FixInput entity
        :return:
        """
        endpoint = '/changes/%s/check' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        if input_ is None:
            response = self.gerrit.requester.post(base_url)
        else:
            response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_work_in_progress(self, input_: dict):
        """
        Marks the change as not ready for review yet.
        Changes may only be marked not ready by the owner, project owners or site administrators.

        :param input_: the WorkInProgressInput entity
        :return:
        """
        endpoint = '/changes/%s/wip' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        response.raise_for_status()

    @check
    def set_ready_for_review(self, input_: dict):
        """
        Marks the change as ready for review (set WIP property to false).
        Changes may only be marked ready by the owner, project owners or site administrators.

        :param input_: the WorkInProgressInput entity
        :return:
        """
        endpoint = '/changes/%s/ready' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        response.raise_for_status()

    @check
    def mark_private(self, input_: dict):
        """
        Marks the change to be private. Only open changes can be marked private.
        Changes may only be marked private by the owner or site administrators.

        :param input_: the PrivateInput entity
        :return:
        """
        endpoint = '/changes/%s/private' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        response.raise_for_status()

    @check
    def unmark_private(self, input_: dict = None):
        """
        Marks the change to be non-private. Note users can only unmark own private changes.
        If the change was already not private, the response is “409 Conflict”.

        :param input_: the PrivateInput entity
        :return:
        """
        if input_ is None:
            endpoint = '/changes/%s/private' % self.id
            response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
        else:
            endpoint = '/changes/%s/private.delete' % self.id
            base_url = self.gerrit.get_endpoint_url(endpoint)
            response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        response.raise_for_status()

    def ignore(self):
        """
        Marks a change as ignored. The change will not be shown in the incoming reviews dashboard, and email
        notifications will be suppressed. Ignoring a change does not cause the change’s "updated" timestamp to be
        modified, and the owner is not notified.

        :return:
        """
        endpoint = '/changes/%s/ignore' % self.id
        response = self.gerrit.requester.put(self.gerrit.get_endpoint_url(endpoint))
        response.raise_for_status()

    def unignore(self):
        """
        Un-marks a change as ignored.

        :return:
        """
        endpoint = '/changes/%s/unignore' % self.id
        response = self.gerrit.requester.put(self.gerrit.get_endpoint_url(endpoint))
        response.raise_for_status()

    def mark_as_reviewed(self):
        """
        Marks a change as reviewed.

        :return:
        """
        endpoint = '/changes/%s/reviewed' % self.id
        response = self.gerrit.requester.put(self.gerrit.get_endpoint_url(endpoint))
        response.raise_for_status()

    def mark_as_unreviewed(self):
        """
        Marks a change as unreviewed.

        :return:
        """
        endpoint = '/changes/%s/unreviewed' % self.id
        response = self.gerrit.requester.put(self.gerrit.get_endpoint_url(endpoint))
        response.raise_for_status()

    def get_hashtags(self) -> list:
        """
        Gets the hashtags associated with a change.

        :return:
        """
        endpoint = '/changes/%s/hashtags' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_hashtags(self, input_: dict) -> list:
        """
        Adds and/or removes hashtags from a change.

        :param input_: the HashtagsInput entity
        :return:
        """
        endpoint = '/changes/%s/hashtags' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)
        return result

    def list_messages(self) -> list:
        """
        Lists all the messages of a change including detailed account information.

        :return:
        """
        endpoint = '/changes/%s/messages' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def get_message(self, id_: str):
        """
        Retrieves a change message including detailed account information.

        :param id_: change message id
        :return:
        """
        endpoint = '/changes/%s/messages/%s' % (self.id, id_)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def delete_message(self, id_: str, input_: dict = None):
        """
        Deletes a change message.
        Note that only users with the Administrate Server global capability are permitted to delete a change message.

        :param id_:
        :param input_: the DeleteChangeMessageInput entity
        :return:
        """
        if input_ is None:
            endpoint = '/changes/%s/messages/%s' % (self.id, id_)
            response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
            response.raise_for_status()
        else:
            endpoint = '/changes/%s/messages/%s/delete' % (self.id, id_)
            base_url = self.gerrit.get_endpoint_url(endpoint)
            response = self.gerrit.requester.post(base_url, json=input_, headers=self.gerrit.default_headers)
            result = self.gerrit.decode_response(response)
            return result
