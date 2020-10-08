#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.common import GET, POST, PUT, DELETE


class GerritProjects:
    def __init__(self, gerrit):
        self.gerrit = gerrit

    @GET('/projects/')
    def list(self):
        """
        Lists the projects accessible by the caller.

        :return:
        """

    @GET('/projects/?{options}')
    def list_options(self, options):
        """
        Limit the results to the projects with project options.
        options possible value is for:

          * Get projects that have a 'master' branch: b=master
          * Get all the projects with their description: d
          * Get all the projects of type 'PERMISSIONS': type=PERMISSIONS
          * Get all projects, including those whose state is "HIDDEN". May not be used together with the state option.: all.
          * Get all projects with the given state: state=HIDDEN
          * Get all the projects with tree option: t
          * Limit the results to those projects that start with the specified prefix: p=platform

        :return:
        """

    @GET('/projects/?query={query}')
    def query(self, query):
        """
        Queries projects visible to the caller. The query string must be provided by the query parameter.
        The start and limit parameters can be used to skip/limit results.

        query parameter
          * name:'NAME' Matches projects that have exactly the name 'NAME'.
          * parent:'PARENT' Matches projects that have 'PARENT' as parent project.
          * inname:'NAME' Matches projects that a name part that starts with 'NAME' (case insensitive).
          * description:'DESCRIPTION' Matches projects whose description contains 'DESCRIPTION', using a full-text search.
          * state:'STATE' Matches project’s state. Can be either 'active' or 'read-only'.


        :param query: query parameter
        :return:
        """

    @GET('/projects/{project_name}')
    def get(self, project_name):
        """
        Retrieves a project.

        :param project_name: the name of the project
        :return:
        """


    @PUT('/projects/{project_name}')
    def create(self, project_name, options=None):
        """
        Creates a new project.

        :param project_name: the name of the project
        :param options: the ProjectInput entity
        :return:
        """

    @GET('/projects/{project_name}/description')
    def get_description(self, project_name):
        """
        Retrieves the description of a project.

        :param project_name: the name of the project
        :return:
        """

    @PUT('/projects/{project_name}/description')
    def set_description(self, project_name, options=None):
        """
        Sets the description of a project.

        :param project_name: the name of the project
        :param options: the ProjectDescriptionInput entity
        :return:
        """

    @DELETE('/projects/{project_name}/description')
    def delete_description(self, project_name):
        """
        Deletes the description of a project.

        :param project_name: the name of the project
        :return:
        """

    @GET('/projects/{project_name}/parent')
    def get_parent(self, project_name):
        """
        Retrieves the name of a project’s parent project. For the All-Projects root project an empty string is returned.

        :param project_name: the name of the project
        :return:
        """
    @PUT('/projects/{project_name}/parent')
    def set_parent(self, project_name, options):
        """
        Sets the parent project for a project.

        :param project_name: the name of the project
        :param options: the ProjectParentInput entity
        :return:
        """

    @GET('/projects/{project_name}/HEAD')
    def get_head(self, project_name):
        """

        :param project_name: the name of the project
        :return:
        """

    @PUT('/projects/{project_name}/HEAD')
    def set_head(self, project_name, options):
        """
        Sets HEAD for a project.

        :param project_name: the name of the project
        :param options: HeadInput entity.
        :return:
        """

    @GET('/projects/{project_name}/statistics.git')
    def get_statistics(self, project_name):
        """
        Return statistics for the repository of a project.

        :param project_name: the name of the project
        :return:
        """

    @GET('/projects/{project_name}/config')
    def get_config(self, project_name):
        """
        Gets some configuration information about a project.
        Note that this config info is not simply the contents of project.config; it generally contains fields that may
        have been inherited from parent projects.

        :param project_name: the name of the project
        :return:
        """

    @PUT('/projects/{project_name}/config')
    def set_config(self, project_name, options):
        """
        Sets the configuration of a project.

        :param project_name: the name of the project
        :param options: the ConfigInput entity.
        :return:
        """

    @POST('/projects/{project_name}/gc')
    def run_garbage_collection(self, project_name, options):
        """
        Run the Git garbage collection for the repository of a project.

        :param project_name: the name of the project
        :param options: the GCInput entity
        :return:
        """

    @PUT('/projects/{project_name}/ban')
    def ban_commits(self, project_name, options):
        """
        Marks commits as banned for the project.

        :param project_name: the name of the project
        :param options: the BanInput entity
        :return:
        """

    @GET('/projects/{project_name}/access')
    def list_access_rights(self, project_name):
        """
        Lists the access rights for a single project.

        :param project_name: the name of the project
        :return:
        """

    @POST('/projects/{project_name}/access')
    def modify_access_rights(self, project_name, options):
        """
        Sets access rights for the project using the diff schema provided by ProjectAccessInput.

        :param project_name: the name of the project
        :param options: the ProjectAccessInput entity
        :return:
        """

    @PUT('/projects/{project_name}/access:review')
    def create_access_rights_change_for_review(self, project_name, options):
        """
        Sets access rights for the project using the diff schema provided by ProjectAccessInput

        :param project_name: the name of the project
        :param options: the ProjectAccessInput v
        :return:
        """
    @GET('/projects/{project_name}/check.access?{options}')
    def check_access(self, project_name, options):
        """
        runs access checks for other users.

        :param project_name: the name of the project
        :param options:
        Check Access Options
          * Account(account): The account for which to check access. Mandatory.
          * Permission(perm): The ref permission for which to check access.
            If not specified, read access to at least branch is checked.
          * Ref(ref): The branch for which to check access. This must be given if perm is specified.
        :return:
        """

    @POST('/projects/{project_name}/index')
    def index(self, project_name, options):
        """
        Adds or updates the current project (and children, if specified) in the secondary index.
        The indexing task is executed asynchronously in background and this command returns immediately
        if async is specified in the input.

        :param project_name: the name of the project
        :param options: the IndexProjectInput entity
        :return:
        """

    @POST('/projects/{project_name}/index.changes')
    def index_changes(self, project_name):
        """
        Adds or updates all the changes belonging to a project in the secondary index.
        The indexing task is executed asynchronously in background, so this command returns immediately.

        :param project_name: the name of the project
        :return:
        """

    @POST('/projects/{project_name}/check')
    def check_consistency(self, project_name, options):
        """
        Performs consistency checks on the project.
        (有问题)

        :param project_name: the name of the project
        :param options: the CheckProjectInput entity
        :return:
        """

    @GET('/projects/{project_name}/branches/')
    def list_branches(self, project_name):
        """
        List the branches of a project.

        :param project_name: the name of the project
        :return:
        """

    @GET('/projects/{project_name}/branches/{branch}')
    def get_branch(self, project_name, branch):
        """
        Retrieves a branch of a project.

        :param project_name: the name of the project
        :param branch: The name of a branch or HEAD. The prefix refs/heads/ can be omitted.
        :return:
        """

    @PUT('/projects/{project_name}/branches/{branch}')
    def create_branch(self, project_name, branch):
        """
        Creates a new branch.

        :param project_name: the name of the project
        :param branch: the BranchInput entity
        :return:
        """

    @DELETE('/projects/{project_name}/branches/{branch}')
    def delete_branch(self, project_name, branch):
        """
        Deletes a branch.

        :param project_name: the name of the project
        :param branch: The name of a branch or HEAD. The prefix refs/heads/ can be omitted.
        :return:
        """

    @POST('/projects/{project_name}/branches:delete')
    def delete_branches(self, project_name, options):
        """
        Delete one or more branches.

        :param project_name: the name of the project
        :param options: the DeleteBranchesInput entity
        :return:
        """

    @GET('/projects/{project_name}/branches/{branch}/files/{file}/content')
    def get_file_content_from_branch(self, project_name, branch, file):
        """
        Gets the content of a file from the HEAD revision of a certain branch.
        The content is returned as base64 encoded string.
        (有问题，file 路径解码待解决)

        :param project_name: the name of the project
        :param branch: The name of a branch or HEAD. The prefix refs/heads/ can be omitted.
        :param file: file path
        :return:
        """

    @GET('/projects/{project_name}/branches/{branch}/mergeable')
    def get_mergeable_information(self, project_name, branch, options):
        """
        Gets whether the source is mergeable with the target branch.

        :param project_name: the name of the project
        :param branch: The name of a branch or HEAD. The prefix refs/heads/ can be omitted.
        :param options: the MergeInput entity
        :return:
        """

    @GET('/projects/{project_name}/branches/{branch}/reflog')
    def get_reflog(self, project_name, branch):
        """
        Gets the reflog of a certain branch.

        :param project_name: the name of the project
        :param branch: The name of a branch or HEAD. The prefix refs/heads/ can be omitted.
        :return:
        """

    @GET('/projects/{project_name}/children/')
    def list_child_projects(self, project_name):
        """
        List the direct child projects of a project.

        :param project_name: the name of the project
        :return:
        """

    @GET('/projects/{parent_project_name}/children/{child_project_name}')
    def get_child_project(self, parent_project_name, child_project_name):
        """
        Retrieves a child project. If a non-direct child project should be retrieved the parameter recursive must be set.

        :param parent_project_name:
        :param child_project_name:
        :return:
        """

    @PUT('/projects/{project_name}/tags/{tag}')
    def create_tag(self, project_name, tag, options):
        """
        Create a new tag on the project.

        :param project_name: the name of the project
        :param tag: The name of a tag. The prefix refs/tags/ can be omitted.
        :param options: the TagInput entity
        :return:
        """

    @GET('/projects/{project_name}/tags/')
    def list_tags(self, project_name):
        """
        List the tags of a project.

        :param project_name: the name of the project
        :return:
        """

    @GET('/projects/{project_name}/tags/{tag}')
    def get_tag(self, project_name, tag):
        """
        Retrieves a tag of a project.

        :param project_name: the name of the project
        :param tag: The name of a tag. The prefix refs/tags/ can be omitted.
        :return:
        """

    @DELETE('/projects/{project_name}/tags/{tag}')
    def delete_tag(self, project_name, tag):
        """
        Deletes a tag.

        :param project_name: the name of the project
        :param tag: The name of a tag. The prefix refs/tags/ can be omitted.
        :return:
        """

    @POST('/projects/{project_name}/tags:delete')
    def delete_tags(self, project_name, options):
        """
        Delete one or more tags.

        :param project_name: the the name of the project
        :param options: the DeleteTagsInput entity
        :return:
        """

    @GET('/projects/{project_name}/commits/{commit}')
    def get_commit(self, project_name, commit):
        """
        Retrieves a commit of a project.

        :param project_name: the the name of the project
        :param commit: Commit ID.
        :return:
        """

    @GET('/projects/{project_name}/commits/{commit}/in')
    def get_include_in(self, project_name, commit):
        """
        Retrieves the branches and tags in which a change is included.

        :param project_name: the the name of the project
        :param commit: Commit ID.
        :return:
        """

    @GET('/projects/{project_name}/commits/{commit}/files/{file}/content')
    def get_file_content_from_commit(self, project_name, commit, file):
        """
        Gets the content of a file from a certain commit.

        :param project_name: the the name of the project
        :param commit: Commit ID.
        :param file: file path
        :return:
        """

    @POST('/projects/{project_name}/commits/{commit}/cherrypick')
    def cherry_pick_commit(self, project_name, commit, options):
        """
        Cherry-picks a commit of a project to a destination branch.

        :param project_name: the the name of the project
        :param commit: Commit ID.
        :param options: the CherryPickInput entity
        :return:
        """

    @GET('/projects/{project_name}/commits/{commit}/files/')
    def list_change_files_in_commit(self, project_name, commit):
        """
        Lists the files that were modified, added or deleted in a commit.

        :param project_name: the the name of the project
        :param commit: Commit ID.
        :return:
        """