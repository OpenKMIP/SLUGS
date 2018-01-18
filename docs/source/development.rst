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
it, file your issue as normal and the project maintainers wil triage it for
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

Commit Messages
---------------
Commit messages should include a single line title (75 characters max) followed
by a blank line and a description of the change, including feature details,
testing and documentation updates, feature limitations, known issues, etc.

The issue number fo the issue associated with the commit should be included
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
infrastructure currently supports Python 2.7, 3.4, 3.5, and 3.6. Test
coverage results are currently included with each Python test environment. To
test against a specific Python version (e.g., Python 2.7), run:

.. code-block:: console

    $ tox -e py27

SLUGS also provides ``tox`` environments for style and security checks.
The style checks leverage ``flake8`` and can be run like so:

.. code-block:: console

    $ tox -e pep8

The security checks use ``bandit`` and can be run like so:

.. code-block:: console

    $ tox -e bandit

To run the entire testing suite, simple run ``tox`` without any arguments.

.. code-block:: console

    $ tox

For more information on the testing tools used here, see the following
resources:

* `tox`_
* `flake8`_
* `bandit`_

.. _`issue tracker`: https://github.com/OpenKMIP/SLUGS/issues
.. _`What to put in your bug report`: http://www.contribution-guide.org/#what-to-put-in-your-bug-report
.. _`tox`: https://pypi.python.org/pypi/tox
.. _`flake8`: https://pypi.python.org/pypi/flake8
.. _`bandit`: https://pypi.python.org/pypi/bandit
