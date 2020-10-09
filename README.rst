====================================================
Python wrapper for the Gerrit V3.x API.
====================================================

Installation
============

The easiest way to install the latest version is by using pip to pull it from PyPI::

    pip install  --upgrade xxx

You may also use Git to clone the repository from Github and install it manually::

    git clone https://github.com/shijl0925/pygerrit3.git
    cd pygerrit3
    python setup.py install


Documentation
=============

Compatibility
=============

* This package is compatible Python versions 3.5+.

Usage
=====
Example::

    from gerrit import GerritClient
    gerrit_client = GerritClient(gerrit_url="https://sonarcloud.io", username='******', password='xxxxx')


API example
-----------



