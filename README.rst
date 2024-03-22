===========
richreports
===========

Library that supports the construction of human-readable, interactive static analysis reports that consist of decorated concrete syntax representations of programs.

|pypi| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/richreports.svg#
   :target: https://badge.fury.io/py/richreports
   :alt: PyPI version and link.

.. |coveralls| image:: https://coveralls.io/repos/github/reity/richreports-py/badge.svg?branch=main
   :target: https://coveralls.io/github/reity/richreports-py?branch=main
   :alt: Coveralls test coverage summary.

Installation and Usage
----------------------
This library is available as a `package on PyPI <https://pypi.org/project/richreports>`__:

.. code-block:: bash

    python -m pip install richreports

The library can be imported in the usual way:

.. code-block:: python

    from richreports import *

Examples
^^^^^^^^

This library supports the enrichment of concrete syntax strings with delimiters. A ``report`` instance can be created from a concrete string and then enriched:

.. code-block:: python

    >>> r = report(
    ...    'def f(x, y):\n' +
    ...    '    return x + y'
    ... )
    >>> r.enrich((2, 11), (2, 15), '(', ')')
    >>> for line in r.render().split('\n'):
    ...     print(line)
    def f(x, y):
        return (x + y)

This makes it possible to succinctly build up reports that correspond to structured representation formats such as HTML:

.. code-block:: python

    >>> r.enrich((1, 0), (2, 15), '<b>', '</b>', True)
    >>> for line in r.render().split('\n'):
    ...     print(line)
    <b>def f(x, y):</b>
    <b>    return (x + y)</b>
    >>> r.enrich((1, 0), (2, 15), '<div>\n', '\n</div>')
    >>> for line in r.render().split('\n'):
    ...     print(line)
    <div>
    <b>def f(x, y):</b>
    <b>    return (x + y)</b>
    </div>

Development
-----------
All installation and development dependencies are fully specified in ``pyproject.toml``. The ``project.optional-dependencies`` object is used to `specify optional requirements <https://peps.python.org/pep-0621>`__ for various development tasks. This makes it possible to specify additional options (such as ``test``, ``lint``, and so on) when performing installation using `pip <https://pypi.org/project/pip>`__:

.. code-block:: bash

    python -m pip install .[test,lint]

Testing and Conventions
^^^^^^^^^^^^^^^^^^^^^^^
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org>`__ (see the ``pyproject.toml`` file for configuration details):

.. code-block:: bash

    python -m pip install .[test]
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`__:

.. code-block:: bash

    python src/richreports/richreports.py -v

Style conventions are enforced using `Pylint <https://pylint.readthedocs.io>`__:

.. code-block:: bash

    python -m pip install .[lint]
    python -m pylint src/richreports

Contributions
^^^^^^^^^^^^^
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/reity/richreports-py>`__ for this library.

Versioning
^^^^^^^^^^
Beginning with version 0.1.0, the version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`__.

Publishing
^^^^^^^^^^
This library can be published as a `package on PyPI <https://pypi.org/project/richreports>`__ by a package maintainer. First, install the dependencies required for packaging and publishing:

.. code-block:: bash

    python -m pip install .[publish]

Ensure that the correct version number appears in ``pyproject.toml``. Create and push a tag for this version (replacing ``?.?.?`` with the version number):

.. code-block:: bash

    git tag ?.?.?
    git push origin ?.?.?

Remove any old build/distribution files. Then, package the source into a distribution archive:

.. code-block:: bash

    rm -rf build dist src/*.egg-info
    python -m build --sdist --wheel .

Finally, upload the package distribution archive to `PyPI <https://pypi.org>`__:

.. code-block:: bash

    python -m twine upload dist/*
