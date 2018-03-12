=====
SLUGS
=====
|pypi-version|
|travis-status|
|codecov-status|
|python-versions|

The Simple, Lightweight User Group Services (SLUGS) library provides a simple
web service that serves user/group membership data over a basic REST interface.

.. code-block:: python

    >>> import requests
    >>> requests.get('http://127.0.0.1:8080/slugs').json()
    {u'users': [u'Jane', u'John'], u'groups': [u'Male', u'Female', u'Human']}
    >>> requests.get('http://127.0.0.1:8080/slugs/users').json()
    {u'users': [u'Jane', u'John']}
    >>> requests.get('http://127.0.0.1:8080/slugs/users/John').status_code
    200
    >>> requests.get('http://127.0.0.1:8080/slugs/users/John/groups').json()
    {u'groups': [u'Male', u'Human']}
    >>> requests.get('http://127.0.0.1:8080/slugs/users/John/groups/Male').status_code
    200

SLUGS is built using `CherryPy`_, a well established object-oriented web
framework for Python. To run SLUGS, simply install the library and then:

.. code-block:: console

    $ slugs -c /path/to/config/file

For more information on SLUGS, check out the project `Documentation`_.

Installation
------------
You can install SLUGS via ``pip``:

.. code-block:: console

    $ pip install slugs

For more information, see `Installation`_.

Community
---------
The SLUGS community has various forums and resources you can use:

* `Source code`_
* `Issue tracker`_


.. |pypi-version| image:: https://img.shields.io/pypi/v/slugs.svg
  :target: https://pypi.python.org/pypi/slugs
  :alt: Latest Version
.. |travis-status| image:: https://travis-ci.org/OpenKMIP/SLUGS.svg?branch=master
  :target: https://travis-ci.org/OpenKMIP/SLUGS
.. |codecov-status| image:: https://codecov.io/github/OpenKMIP/SLUGS/coverage.svg?branch=master
  :target: https://codecov.io/github/OpenKMIP/SLUGS?branch=master
.. |python-versions| image:: https://img.shields.io/pypi/pyversions/SLUGS.svg
  :target: https://github.com/OpenKMIP/SLUGS

.. _`CherryPy`: http://cherrypy.org
.. _`Documentation`: https://slugs.readthedocs.io/en/latest/index.html
.. _`Installation`: https://slugs.readthedocs.io/en/latest/installation.html
.. _`Source code`: https://github.com/openkmip/slugs
.. _`Issue tracker`: https://github.com/openkmip/slugs/issues
