Welcome to SLUGS
================
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

For more information on the SLUGS REST API, see :doc:`API <api>`.

SLUGS is built using `CherryPy`_, a well established object-oriented web
framework for Python. To run SLUGS, simply install the library and then:

.. code-block:: console

    $ slugs -c /path/to/config/file

For more information on configuring SLUGS, see
:doc:`Configuration <configuration>`.

Installation
------------
You can install SLUGS via ``pip``:

.. code-block:: console

    $ pip install slugs

See :doc:`Installation <installation>` for more information.

Layout
------

.. toctree::
   :maxdepth: 2

   api
   changelog
   configuration
   development
   installation


.. _`CherryPy`: http://cherrypy.org
