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


====================================================
Python wrapper for the Gerrit V3.x REST API.
====================================================

Installation
============

The easiest way to install the latest version is by using pip to pull it from PyPI::

    pip install  --upgrade python-gerrit-api

You may also use Git to clone the repository from Github and install it manually::

    git clone https://github.com/shijl0925/python-gerrit-api.git
    cd python-gerrit-api
    python setup.py install


Documentation
=============

The full documentation for API is available on `readthedocs
<https://python-gerrit-api.readthedocs.io/en/latest/>`_.

Compatibility
=============

* This package is compatible Python versions 3.5+.
* Tested with Gerrit Code Review (V3.3.0).

Usage
=====
Example::

    from gerrit import GerritClient
    gerrit_client = GerritClient(gerrit_url="https://yourgerrit", username='******', password='xxxxx')


