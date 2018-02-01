Configuration
=============
SLUGS uses the CherryPy configuration system to manage both global and
application level configuration settings.

By default, SLUGS will look for a ``slugs.conf`` configuration file in
``/etc/slugs/`` when first starting up. This file path can be changed
using the ``-c`` option:

.. code-block:: console

    $ python slugs/app.py -c /path/to/config/file

The same flag can be used with the ``slugs`` entry point:

.. code-block:: console

    $ slugs -c /path/to/config/file

The following is an example ``slugs.conf`` file, which can be found under
the ``examples/`` directory in the SLUGS repository.

.. code-block:: console

    [global]
    environment = 'production'
    server.socket_host = '127.0.0.1'
    server.socket_port = 8080
    log.access_file = '/var/log/cherrypy/slugs/access.log'
    log.error_file = '/var/log/cherrypy/slugs/error.log'

    [data]
    user_group_mapping = '/etc/slugs/user_group_mapping.csv'

    [/slugs]
    tools.trailing_slash.on = True

Global Settings
---------------
The ``[global]`` configuration block contains site-wide configuration settings
that will apply to every application mounted via CherryPy. The SLUGS setup
assumes that SLUGS will be the only CherryPy application running on the host
machine.

The different configuration options are defined below. For more information on
these CherryPy settings, see `CherryPy Configuration`_.

* ``environment``
    A string indicating the type of environment hosting the application. Tells
    CherryPy to load in additional preset configuration settings appropriate
    for the environment. Should be set to ``'production'`` when running SLUGS
    in production or commented out when in development. For more information,
    see `CherryPy Environments`_.
* ``server.socket_host``
    The IP address of the host machine running the application.
* ``server.socket_port``
    The port number on which to host the application.

    .. note::
       SLUGS must have permission to bind to the specified port, specifically
       if the port is a privileged port.
* ``log.access_file``
    The path to the access log file. This log contains entries for all external
    accesses to the application (e.g., all GET requests).

    .. note::
       The log directory must exist before SLUGS is run; the service will not
       create the log directory for you. SLUGS must also have permission to
       access the log directory.
* ``log.error_file``
    The path to the error log file. This log contains entries pertaining to the
    startup, maintenance, and shutdown of the application, including any errors
    that may occur during the lifetime of the application.

    .. note::
       The log directory must exist before SLUGS is run; the service will not
       create the log directory for you. SLUGS must also have permission to
       access the log directory.

Application Settings
--------------------
The SLUGS application is configured with two different configuration blocks:
``[data]`` and ``[/slugs]``. The ``[data]`` block contains custom configuration
settings that define the data sources SLUGS should use to serve user/group
information.

* ``user_group_mapping``
    The path to the CSV file containing user/group data in ``user,group``
    format. See :ref:`data-management` for more information.

    .. note::
       The CSV file must exist before SLUGS is run; the service will not
       create the CSV file for you. SLUGS must also have permission to
       access the directory containing the CSV file.

The ``[/slugs]`` block is an application-level block that contains additional
CherryPy settings for the SLUGS application.

* ``tools.trailing_slash.on``
    A boolean flag that allows CherryPy to redirect incoming requests to a URL
    without a trailing ``/`` to the same URL with a trailing ``/``. A ``301``
    redirect message will be logged in ``log.access_file`` when this redirect
    occurs.

.. _data-management:

Data Management
---------------
The user/group information served by SLUGS is stored in a backing CSV file that
is configured on application startup (see ``user_group_mapping`` above). The
following is an example CSV file, which can be found under the ``examples/``
directory in the SLUGS repository.

.. code-block:: console

    John,Human
    Jane,Human
    John,Male
    Jane,Female

In this example, there are two users ``John`` and ``Jane``. Each belongs to
two different groups, both belonging to the ``Human`` group, but each belonging
to the ``Male`` and ``Female`` groups respectively.

User and group names can contain additional characters, like whitespaces and
symbols. The following example is still a valid CSV file.

.. code-block:: console

    John Doe,Blood Type: AB-
    Jane Doe,Blood Type: O+

The only user/group naming restriction is that neither can contain the
delimiting character ``,``. Blank lines can be included throughout the file;
they are simply ignored. Lines starting with a ``#`` are considered comments
and are also ignored. Extra whitespace at the beginning or ending of a user
or group name is treated similarly:

.. code-block:: console

    John,    Male
       Jane,Female

The users in the above example are still ``John`` and ``Jane``, not ``John``
and ``___Jane``. The groups are still ``Male`` and ``Female``, not ``____Male``
and ``Female``.

Finally, the backing CSV file can be edited and updated while SLUGS is running.
The application will automatically detect the change and reload the data file.
A log message acknowledging this data update will be logged in
``log.error_file`` when the reload occurs.

.. code-block:: console

    [timestamp] ENGINE Monitored file (<path/here>) updated. Reloading data.

If an error occurs during data reload, SLUGS will stop processing the new data
and will retain the prior data set it was serving. This allows data updates to
be made to SLUGS without potentially breaking the application. A log message
acknowledging this data update error will be logged in ``log.error_file`` when
the error is detected.

.. code-block:: console

    [timestamp] ENGINE Error parsing monitored file (<path/here>). Halting
    data reload.

.. _`CherryPy Configuration`: http://docs.cherrypy.org/en/latest/config.html
.. _`CherryPy Environments`: http://docs.cherrypy.org/en/latest/config.html#environments
