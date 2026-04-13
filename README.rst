Strelki: Better dates & times for Python
======================================

.. start-inclusion-marker-do-not-remove

.. image:: https://github.com/krisfremen/strelki/workflows/tests/badge.svg?branch=master
   :alt: Build Status
   :target: https://github.com/krisfremen/strelki/actions?query=workflow%3Atests+branch%3Amaster

.. image:: https://codecov.io/gh/krisfremen/strelki/branch/master/graph/badge.svg
   :alt: Coverage
   :target: https://codecov.io/gh/krisfremen/strelki

.. image:: https://img.shields.io/pypi/v/strelki.svg
   :alt: PyPI Version
   :target: https://pypi.python.org/pypi/strelki

.. image:: https://img.shields.io/pypi/pyversions/strelki.svg
   :alt: Supported Python Versions
   :target: https://pypi.python.org/pypi/strelki

.. image:: https://img.shields.io/pypi/l/strelki.svg
   :alt: License
   :target: https://pypi.python.org/pypi/strelki

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :alt: Code Style: Black
   :target: https://github.com/psf/black


**Strelki** is a Python library that offers a sensible and human-friendly approach to creating, manipulating, formatting and converting dates, times and timestamps. It implements and updates the datetime type, plugging gaps in functionality and providing an intelligent module API that supports many common creation scenarios. Simply put, it helps you work with dates and times with fewer imports and a lot less code.

Strelki is plural for arrow in Macedonian. Strelki takes its name from the `arrow of time <https://en.wikipedia.org/wiki/Arrow_of_time>`_ and is heavily inspired by `moment.js <https://github.com/moment/moment>`_ and `requests <https://github.com/psf/requests>`_.

Strelki is an experimental fork for testing new ideas. Upstream `Arrow <https://github.com/arrow-py/arrow>`_ should still be your default choice unless you specifically need features that are experimental and only implemented here.

Why use Strelki over built-in modules?
------------------------------------

Python's standard library and some other low-level modules have near-complete date, time and timezone functionality, but don't work very well from a usability perspective:

- Too many modules: datetime, time, calendar, dateutil, pytz and more
- Too many types: date, time, datetime, tzinfo, timedelta, relativedelta, etc.
- Timezones and timestamp conversions are verbose and unpleasant
- Timezone naivety is the norm
- Gaps in functionality: ISO 8601 parsing, timespans, humanization

Features
--------

- Fully-implemented, drop-in replacement for datetime
- Support for Python 3.8+
- Timezone-aware and UTC by default
- Super-simple creation options for many common input scenarios
- ``shift`` method with support for relative offsets, including weeks
- Format and parse strings automatically
- Wide support for the `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_ standard
- Timezone conversion
- Support for ``dateutil``, ``pytz``, and ``ZoneInfo`` tzinfo objects
- Generates time spans, ranges, floors and ceilings for time frames ranging from microsecond to year
- Humanize dates and times with a growing list of contributed locales
- Extensible for your own Arrow-derived types
- Full support for PEP 484-style type hints

Quick Start
-----------

Installation
~~~~~~~~~~~~

To install Strelki, use `pip <https://pip.pypa.io/en/stable/quickstart/>`_ or `pipenv <https://docs.pipenv.org>`_:

.. code-block:: console

    $ pip install -U strelki

Example Usage
~~~~~~~~~~~~~

.. code-block:: python

    >>> import strelki
    >>> strelki.get('2013-05-11T21:23:58.970460+07:00')
    <Arrow [2013-05-11T21:23:58.970460+07:00]>

    >>> utc = strelki.utcnow()
    >>> utc
    <Arrow [2013-05-11T21:23:58.970460+00:00]>

    >>> utc = utc.shift(hours=-1)
    >>> utc
    <Arrow [2013-05-11T20:23:58.970460+00:00]>

    >>> local = utc.to('US/Pacific')
    >>> local
    <Arrow [2013-05-11T13:23:58.970460-07:00]>

    >>> local.timestamp()
    1368303838.970460

    >>> local.format()
    '2013-05-11 13:23:58 -07:00'

    >>> local.format('YYYY-MM-DD HH:mm:ss ZZ')
    '2013-05-11 13:23:58 -07:00'

    >>> local.humanize()
    'an hour ago'

    >>> local.humanize(locale='ko-kr')
    '한시간 전'

.. end-inclusion-marker-do-not-remove

Documentation
-------------

For full documentation, please visit `strelki.readthedocs.io <https://strelki.readthedocs.io>`_.

Contributing
------------

Contributions are welcome for both code and localizations (adding and updating locales). Begin by gaining familiarity with the Arrow library and its features. Then, jump into contributing:

#. Find an issue or feature to tackle on the `issue tracker <https://github.com/krisfremen/strelki/issues>`_. Issues marked with the `"good first issue" label <https://github.com/krisfremen/strelki/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22>`_ may be a great place to start!
#. Fork `this repository <https://github.com/krisfremen/strelki>`_ on GitHub and begin making changes in a branch.
#. Add a few tests to ensure that the bug was fixed or the feature works as expected.
#. Run the entire test suite and linting checks by running one of the following commands: ``tox && tox -e lint,docs`` (if you have `tox <https://tox.readthedocs.io>`_ installed) **OR** ``make build39 && make test && make lint`` (if you do not have Python 3.9 installed, replace ``build39`` with the latest Python version on your system).
#. Submit a pull request and await feedback 😃.

If you have any questions along the way, feel free to ask them `here <https://github.com/krisfremen/strelki/discussions>`_.

Support Strelki
-------------

`Open Collective <https://opencollective.com/>`_ is an online funding platform that provides tools to raise money and share your finances with full transparency. It is the platform of choice for individuals and companies to make one-time or recurring donations directly to the project. If you are interested in making a financial contribution, please visit the `Strelki collective <https://opencollective.com/strelki>`_.
