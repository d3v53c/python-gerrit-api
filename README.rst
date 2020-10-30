Project description
===================

.. image:: https://img.shields.io/pypi/pyversions/python-gerrit-api.svg
    :target: https://pypi.python.org/pypi/python-gerrit-api
.. image:: https://img.shields.io/pypi/v/python-gerrit-api.svg
    :target: https://pypi.python.org/pypi/python-gerrit-api
.. image:: https://sonarcloud.io/api/project_badges/measure?project=shijl0925_python-gerrit-api&metric=alert_status
    :target: https://sonarcloud.io/dashboard?id=shijl0925_python-gerrit-api
.. image:: https://img.shields.io/github/license/shijl0925/python-gerrit-api.svg
    :target: LICENSE
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

About this library
-------------------
Gerrit is a code review and project management tool for Git based projects.

Gerrit makes reviews easier by showing changes in a side-by-side display, and allowing inline comments to be added by any reviewer.

Gerrit simplifies Git based project maintainership by permitting any authorized user to submit changes to the master Git repository, rather than requiring all approved changes to be merged in by hand by the project maintainer.

This library allows you to automate most common Gerrit operations using Python, such as:

* Ability to create/delete/query Gerrit projects, and ability to excute project:
    * Retrieves/Set/Delete the description of a project.
    * Retrieves the name of a project's parent project, and set the parent project for a project.
    * Retrieves for a project the name of the branch to which HEAD points, and sets HEAD for a project.
    * Gets some configuration information about a project, and sets the configuration of a project.
    * Lists the access rights for a single project, and sets access rights for a project.
    * Retrieves a commit of a project.
    * Ability to excute project's branches, tags, labels, dashboards and so on:
        * Retrieves/Create/Delete
    * ...

* Ability to create/query Gerrit accounts, and ability to excute account:
    * Sets/Deletes the full name of an account.
    * Retrieves/Sets the status of an account.
    * Sets the username of an account.
    * Sets the display name of an account.
    * Checks if an account is active, and sets the account state to active/inactive.
    * Sets/Generates/Deletes the HTTP password of an account.
    * Retrieves a previously obtained OAuth access token.
    * Retrieves/Sets the user's (diff/edit) preferences.
    * Retrieves/Add/Deletes the watched projects of an account.
    * Retrieves/Delete the external ids of a user account.
    * Ability to excute account's emails, ssh keys, gpg keys.
        * Retrieves/Create/Delete
    * ...

* Ability to create/query Gerrit groups, and ability to excute group:
    * Renames a Gerrit internal group.
    * Sets/Deletes the description of a Gerrit internal group.
    * Sets the options of a Gerrit internal group.
    * Sets the owner group of a Gerrit internal group.
    * Gets the audit log of a Gerrit internal group.
    * Lists the direct members of a Gerrit internal group.
    * Retrieves/Adds/Removes a group member to a Gerrit internal group..
    * Lists/Retrieves/Adds/Removes the direct subgroups of a group.

* Ability to create/delete/query Gerrit changes, and ability to excute change:
    * Update/Abandons/Restores/Rebases/Move/Reverts/Submits an existing change.
    * Creates a new patch set with a new commit message.
    * Retrieves/Sets/Deletes the topic of a change.
    * Retrieves/Sets/Deletes the assignee of a change.
    * Retrieves the branches and tags in which a change is included.
    * Lists the published comments, the robot comments of all revisions of the change.
    * Lists the draft comments of all revisions of the change that belong to the calling user.
    * Marks the change as (not) ready for review.
    * Marks the change to be private/non-private.
    * Marks/Un-marks a change as ignored.
    * Marks a change as reviewed/unreviewed.
    * Gets/Adds/Removes the hashtags associated with a change.
    * Ability to excute change's messages, change edit, reviewers, revision
    * Retrieves all users that are currently in the attention set, Adds a single user to the attention set of a change, Deletes a single user from the attention set of a change.
    * ...

* Ability to excute Gerrit config:
    * Retrieves/Sets the default user/diff/edit preferences for the server.
    * ...

* Ability to install/enable/disable/reload/query Gerrit plugins

For a full documentation spec of what this library supports see `readthedocs
<https://python-gerrit-api.readthedocs.io/en/latest/>`_

Python versions
---------------

The project has been tested against Python versions:

* 3.5
* 3.6
* 3.7
* 3.8

Gerrit versions
---------------

Project tested on latest Gerrit versions.

Installation
============

The easiest way to install the latest version is by using pip to pull it from PyPI.

Using Pip or Setuptools

.. code-block:: bash

	pip install python-gerrit-api

Or:

.. code-block:: bash

	easy_install python-gerrit-api


You may also use Git to clone the repository from Github and install it manually::

    git clone https://github.com/shijl0925/python-gerrit-api.git
    cd python-gerrit-api
    python setup.py install

Compatibility
=============

* This package is compatible Python versions 3.5+.
* Tested with Gerrit Code Review (V3.3.0).

Usage
=====
Example::

    from gerrit import GerritClient
    gerrit_client = GerritClient(gerrit_url="https://yourgerrit", username='******', password='xxxxx')


