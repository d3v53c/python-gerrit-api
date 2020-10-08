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
