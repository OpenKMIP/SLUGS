API
===
The SLUGS REST API allows clients to query for membership information about
a many-to-many relationship between a set of users and a set of groups.
Queries can be made from a user-centric or group-centric point-of-view.

All REST queries are rooted under ``/slugs``. If the base URL is
``http://127.0.0.1:8080``, then the full service URL is
``http://127.0.0.1:8080/slugs``. For example, to retrieve the list of
recognized users, ``GET /users``, the full API call would be:
``http://127.0.0.1:8080/slugs/users``.

GET
---
/
~
List all users and groups recognized by the service.

Response
^^^^^^^^
========  =============  ==============================
Response  Response Code  Details
========  =============  ==============================
Normal    200            User and group lists returned.
========  =============  ==============================

======  =====  ========================================================
Name    Type   Description
======  =====  ========================================================
users   array  A list of strings, representing users recognized by the
               service.
groups  array  A list of strings, representing groups recognized by the
               service.
======  =====  ========================================================

A response example would look like:

.. code-block:: json

    {
        "users": [
            "John",
            "Jane"
        ],
        "groups": [
            "Human",
            "Male",
            "Female"
        ]
    }

/users
~~~~~~
List all users recognized by the service.

Response
^^^^^^^^
========  =============  ===================
Response  Response Code  Details
========  =============  ===================
Normal    200            User list returned.
========  =============  ===================

======  =====  ========================================================
Name    Type   Description
======  =====  ========================================================
users   array  A list of strings, representing users recognized by the
               service.
======  =====  ========================================================

A response example would look like:

.. code-block:: json

    {
        "users": [
            "John",
            "Jane"
        ]
    }

/groups
~~~~~~~
List all groups recognized by the service.

Response
^^^^^^^^
========  =============  ====================
Response  Response Code  Details
========  =============  ====================
Normal    200            Group list returned.
========  =============  ====================

======  =====  ========================================================
Name    Type   Description
======  =====  ========================================================
groups  array  A list of strings, representing groups recognized by the
               service.
======  =====  ========================================================

A response example would look like:

.. code-block:: json

    {
        "groups": [
            "Human",
            "Male",
            "Female"
        ]
    }

/users/{user}
~~~~~~~~~~~~~
Query if ``{user}`` is a user recognized by the service.

Response
^^^^^^^^
========  =============  ===================================================
Response  Response Code  Details
========  =============  ===================================================
Normal    200            ``{user}`` is a user recognized by the service.
Error     404            ``{user}`` is not a user recognized by the service.
========  =============  ===================================================

/groups/{group}
~~~~~~~~~~~~~~~
Query if ``{group}`` is a group recognized by the service.

Response
^^^^^^^^
========  =============  =====================================================
Response  Response Code  Details
========  =============  =====================================================
Normal    200            ``{group}`` is a group recognized by the service.
Error     404            ``{group}`` is not a group recognized by the service.
========  =============  =====================================================

/users/{user}/groups
~~~~~~~~~~~~~~~~~~~~
List all groups associated with user ``{user}``.

Response
^^^^^^^^
========  =============  ===================================================
Response  Response Code  Details
========  =============  ===================================================
Normal    200            Group list returned.
Error     404            ``{user}`` is not a user recognized by the service.
========  =============  ===================================================

======  =====  ===========================================================
Name    Type   Description
======  =====  ===========================================================
groups  array  A list of strings, representing groups associated with user
               ``{user}``.
======  =====  ===========================================================

A response example would look like:

.. code-block:: json

    {
        "groups": [
            "Human",
            "Male"
        ]
    }

/groups/{group}/users
~~~~~~~~~~~~~~~~~~~~~
List all users associated with group ``{group}``.

Response
^^^^^^^^
========  =============  =====================================================
Response  Response Code  Details
========  =============  =====================================================
Normal    200            User list returned.
Error     404            ``{group}`` is not a group recognized by the service.
========  =============  =====================================================

=====  =====  ===========================================================
Name   Type   Description
=====  =====  ===========================================================
users  array  A list of strings, representing users associated with group
              ``{group}``.
=====  =====  ===========================================================

A response example would look like:

.. code-block:: json

    {
        "users": [
            "Jane",
            "John"
        ]
    }

/users/{user}/groups/{group}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Query if ``{group}`` is a group associated with user ``{user}``.

Response
^^^^^^^^
========  =============  =====================================================
Response  Response Code  Details
========  =============  =====================================================
Normal    200            ``{group}`` is a group associated with user
                         ``{user}``.
Error     404            ``{user}`` is not a user recognized by the service,
                         or
                         ``{group}`` is not a group associated with user
                         ``{user}``.
========  =============  =====================================================

/groups/{group}/users/{user}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Query if ``{user}`` is a user associated with group ``{group}``.

Response
^^^^^^^^
========  =============  =====================================================
Response  Response Code  Details
========  =============  =====================================================
Normal    200            ``{user}`` is a user associated with group
                         ``{group}``.
Error     404            ``{group}`` is not a group recognized by the service,
                         or
                         ``{user}`` is not a user associated with group
                         ``{group}``.
========  =============  =====================================================
