Development
===========
Development for SLUGS is open to all contributors. Use the information
provided here to inform your contributions and help the project maintainers
review and accept your work.

Getting Started
---------------
File a new issue on the project `issue tracker`_ on GitHub describing the
work you intend on doing. Provide as much information on your feature
request as possible.

The issue number for your new issue should be included at the end of the
commit message of each patch related to that issue.

If you simply want to request a new feature but do not intend on working on
it, file your issue as normal and the project maintainers will triage it for
future work.

.. _writing-code:

Writing Code
------------
New code should be written in its own Git branch, ideally branched from
``HEAD`` on ``master``. If other commits are merged into ``master`` after your
branch was created, be sure to rebase your work on the current state of
``master`` before submitting a pull request to GitHub.

New code should generally follow ``PEP 8`` style guidelines, though there are
exceptions that will be allowed in special cases. Run the ``flake8`` tests to
check your code before submitting a pull request (see :ref:`running-tests`).

To prepare your local Python environment for SLUGS development, install the
project requirements:

.. code:: console

    $ pip install -r requirements.txt

Writing Documentation
---------------------
Like new code, new documentation should be written in its own Git branch.
All SLUGS documentation is written in `RST`_ format and managed using
``sphinx``. It can be found under ``docs/source``.

If you are interested in contributing to the project documentation, install
the project documentation requirements:

.. code:: console

    $ pip install -r doc-requirements.txt

To build the documentation, navigate into the ``docs`` directory and run:

.. code:: console

    $ make html

This will build the SLUGS documentation as HTML and place it under the new
``docs/build/html`` directory. View it using your preferred web browser.

Commit Messages
---------------
Commit messages should include a single line title (75 characters max) followed
by a blank line and a description of the change, including feature details,
testing and documentation updates, feature limitations, known issues, etc.

The issue number for the issue associated with the commit should be included
at the end of the commit message, if it exists. If the commit is the final one
for a specific issue, use ``Closes #XXX`` or ``Fixes #XXX`` to link the issue
and close it simultaneously.

Bug Fixes
---------
If you have found a bug in SLUGS, file a new issue and use the title format
``Bug: <brief description here>``. In the body of the issue please provide as
much information as you can, including Python version, SLUGS version,
operating system version, and any stacktraces or logging information produced
by SLUGS related to the bug. See `What to put in your bug report`_ for a
breakdown of bug reporting best practices.

If you are working on a bug fix for a bug in ``master``, follow the general
guidelines above for branching and code development (see :ref:`writing-code`).

If you are working on a bug fix for an older version of SLUGS, your branch
should be based on the latest commit of the repository branch for the version
of SLUGS the bug applies to (e.g., branch ``release-1.0.0`` for SLUGS 1.0).
The pull request for your bug fix should also target the version branch in
question. If applicable, it will be pulled forward to newer versions of SLUGS,
up to and including ``master``.

.. _running-tests:

Running Tests
-------------
SLUGS uses ``tox`` to manage testing across multiple Python versions. Test
infrastructure currently supports Python 2.7, 3.4, 3.5, and 3.6. Additional
test environments are provided for security, style, and documentation checks.

.. note::
   All of the ``tox`` commands discussed in this section should be run from
   the root of the SLUGS repository, in the same directory as the ``tox.ini``
   configuration file.

The style checks leverage ``flake8`` and can be run like so:

.. code-block:: console

    $ tox -e pep8

The security checks use ``bandit`` and can be run like so:

.. code-block:: console

    $ tox -e bandit

The documentation checks leverage ``sphinx`` to build the HTML documentation
in a temporary directory, verifying that there are no errors. These checks
can be run like so:

.. code-block:: console

    $ tox -e docs

To run the above checks along with the entire unit test suite, simple run
``tox`` without any arguments.

.. code-block:: console

    $ tox


Unit Tests
~~~~~~~~~~
The unit test suite tests each individual component of the SLUGS code base,
verifying that each component works correctly in isolation. Ideal code
coverage would include the entire code base. To facilitate improving coverage,
test coverage results are included with each Python unit test environment.

To test against a specific Python version (e.g., Python 2.7), run:

.. code-block:: console

    $ tox -e py27

Integration Tests
~~~~~~~~~~~~~~~~~
The integration test suite tests the REST API provided by SLUGS, verifying
that the right response data and response status codes are returned for
specific queries. An instance of SLUGS must already be running and serving
the ``examples/user_group_mapping.csv`` data file for the integration test
cases to pass.

Code base coverage is not a goal of the integration test suite. Code coverage
statistics are therefore not included in the output of the integration tests.
For code coverage, run the unit tests above.

To run the integration test suite, the URL to the SLUGS instance must be
passed to the test suite using the ``--url`` configuration argument. Assuming
the SLUGS URL is ``http://127.0.0.1:8080/slugs``, the following ``tox``
command will set up and execute the integration tests:

.. code-block:: console

    $ tox -r -e integration -- --url http://127.0.0.1:8080/slugs

For more information on the testing tools used here, see the following
resources:

* `bandit`_
* `flake8`_
* `sphinx`_
* `tox`_

.. _`issue tracker`: https://github.com/OpenKMIP/SLUGS/issues
.. _`RST`: http://docutils.sourceforge.net/rst.html
.. _`What to put in your bug report`: http://www.contribution-guide.org/#what-to-put-in-your-bug-report
.. _`tox`: https://pypi.python.org/pypi/tox
.. _`flake8`: https://pypi.python.org/pypi/flake8
.. _`bandit`: https://pypi.python.org/pypi/bandit
.. _`sphinx`: http://www.sphinx-doc.org/en/stable/
