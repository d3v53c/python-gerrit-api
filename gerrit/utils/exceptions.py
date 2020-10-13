"""Module for custom exceptions.

Where possible we try to throw exceptions with non-generic,
meaningful names.
"""


class GerritAPIException(Exception):
    """
    Base class for all errors
    """
    pass


class NotFound(GerritAPIException):
    """
    Resource cannot be found
    """
    pass


class UnknownProject(KeyError, NotFound):
    """
    Gerrit does not recognize the Project requested.
    """
    pass


class UnknownBranch(KeyError, NotFound):
    """
    Gerrit does not recognize the branch requested.
    """
    pass


class UnknownTag(KeyError, NotFound):
    """
    Gerrit does not recognize the tag requested.
    """
    pass


class UnknownCommit(KeyError, NotFound):
    """
    Gerrit does not recognize the commit requested.
    """


class UnknownDashboard(KeyError, NotFound):
    """
    Gerrit does not recognize the dashboard requested.
    """


class UnknownAccount(KeyError, NotFound):
    """
    Gerrit does not recognize the account requested.
    """


class UnknownEmail(KeyError, NotFound):
    """
    Gerrit does not recognize the email requested.
    """


class UnknownSSHKey(KeyError, NotFound):
    """
    Gerrit does not recognize the SSH key requested.
    """


class UnknownGPGKey(KeyError, NotFound):
    """
    Gerrit does not recognize the GPG key requested.
    """


class UnknownGroup(KeyError, NotFound):
    """
    Gerrit does not recognize the Group requested.
    """


class UnknownTask(KeyError, NotFound):
    """
    Gerrit does not recognize the task requested.
    """


class UnknownCache(KeyError, NotFound):
    """
    Gerrit does not recognize the cache requested.
    """


class UnknownPlugin(KeyError, NotFound):
    """
    Gerrit does not recognize the plugin requested.
    """
