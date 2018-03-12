Installation
============
You can install SLUGS via ``pip``:

.. code-block:: console

    $ pip install slugs

Supported platforms
-------------------
SLUGS is tested on Python 2.7, 3.4, 3.5, and 3.6 on the following
operating systems:

* Ubuntu 12.04, 14.04, and 16.04

Building SLUGS on Linux
-----------------------
You can install SLUGS from source via ``git``:

.. code-block:: console

    $ git clone https://github.com/openkmip/slugs.git
    $ cd slugs
    $ python setup.py install

If you are on a fresh Linux build, you may also need several additional system
dependencies, including headers for Python.

Ubuntu
~~~~~~
Replace ``python-dev`` with ``python3-dev`` if you are using Python 3.0+.

.. code-block:: console

    $ sudo apt-get install python-dev
