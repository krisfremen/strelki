# Changelog

## [1.4.0] (2025-10-18)

### Features

- Added `week_start` parameter to `floor()` and `ceil()`
  methods. [PR #1222](https://github.com/arrow-py/arrow/pull/1222)

- Added `FORMAT_RFC3339_STRICT` with a T separator. [PR
  #1201](https://github.com/arrow-py/arrow/pull/1201)

- Added Macedonian in Latin locale support. [PR
  #1200](https://github.com/arrow-py/arrow/pull/1200)

- Added Persian/Farsi locale support. [PR
  #1190](https://github.com/arrow-py/arrow/pull/1190)

- Added week and weeks to Thai locale timeframes. [PR
  #1218](https://github.com/arrow-py/arrow/pull/1218)

- Added weeks to Catalan locale. [PR
  #1189](https://github.com/arrow-py/arrow/pull/1189)

- Added Persian names of months, month-abbreviations and
  day-abbreviations in Gregorian calendar. [PR
  #1172](https://github.com/arrow-py/arrow/pull/1172)

### Bug Fixes

- Fixed humanize month limits. [PR
  #1224](https://github.com/arrow-py/arrow/pull/1224)

- Fixed type hint of `Arrow.__getattr__`. [PR
  #1171](https://github.com/arrow-py/arrow/pull/1171)

- Fixed spelling and removed poorly used expressions in Korean
  locale. [PR #1181](https://github.com/arrow-py/arrow/pull/1181)

- Updated `shift()` method for issue #1145. [PR
  #1194](https://github.com/arrow-py/arrow/pull/1194)

- Improved Greek locale translations (seconds, days, "ago",
  and month typo). [PR
  #1184](https://github.com/arrow-py/arrow/pull/1184), [PR
  #1186](https://github.com/arrow-py/arrow/pull/1186)

- Addressed `datetime.utcnow` deprecation warning. [PR
  #1182](https://github.com/arrow-py/arrow/pull/1182)

### Miscellaneous Chores

- Migrated Arrow to use ZoneInfo for timezones instead of
  pytz. [PR #1217](https://github.com/arrow-py/arrow/pull/1217)

- Added codecov test results. [PR
  #1223](https://github.com/arrow-py/arrow/pull/1223)

- Updated CI dependencies (actions/setup-python,
  actions/checkout, codecov/codecov-action, actions/cache).

- Added docstrings to parser.py. [PR
  #1010](https://github.com/arrow-py/arrow/pull/1010)

- Updated Python versions support and bumped CI
  dependencies. [PR #1177](https://github.com/arrow-py/arrow/pull/1177)

- Added dependabot for GitHub actions. [PR
  #1193](https://github.com/arrow-py/arrow/pull/1193)

- Moved dateutil types to test requirements. [PR
  #1183](https://github.com/arrow-py/arrow/pull/1183)

- Added documentation link for `arrow.format`. [PR
  #1180](https://github.com/arrow-py/arrow/pull/1180)

## [1.3.0] (2023-09-30)

### Features

- Added official support for Python 3.11 and 3.12.

- Added dependency on `types-python-dateutil` to improve Arrow
  mypy compatibility. [PR
  #1102](https://github.com/arrow-py/arrow/pull/1102)

### Bug Fixes

- Updates to Italian, Romansh, Hungarian, Finish and Arabic
  locales.

- Handling parsing of UTC prefix in timezone strings.

### Miscellaneous Chores

- Update documentation to improve readability.

- Dropped support for Python 3.6 and 3.7, which are
  end-of-life.

- Migrate from `setup.py`/Twine to `pyproject.toml`/Flit
  for packaging and distribution.

- Adopt `.readthedocs.yaml` configuration file for
  continued ReadTheDocs support.

## [1.2.3] (2022-06-25)

### Features

- Added Amharic, Armenian, Georgian, Laotian and Uzbek locales.

### Bug Fixes

- Updated Danish locale and associated tests.

### Miscellaneous Chores

- Small fixes to CI.

## [1.2.2] (2022-01-19)

### Features

- Added Kazakh locale.

### Bug Fixes

- The Belarusian, Bulgarian, Czech, Macedonian, Polish, Russian,
  Slovak and Ukrainian locales now support `dehumanize`.

- Minor bug fixes and improvements to ChineseCN, Indonesian,
  Norwegian, and Russian locales.

- Expanded testing for multiple locales.

### Miscellaneous Chores

- Started using `xelatex` for pdf generation in
  documentation.

- Split requirements file into `requirements.txt`,
  `requirements-docs.txt` and `requirements-tests.txt`.

- Added `flake8-annotations` package for type linting in
  `pre-commit`.

## [1.2.1] (2021-10-24)

### Features

- Added quarter granularity to humanize, for example:

``` python
>>> import arrow
>>> now = arrow.now()
>>> four_month_shift = now.shift(months=4)
>>> now.humanize(four_month_shift, granularity="quarter")
'a quarter ago'
>>> four_month_shift.humanize(now, granularity="quarter")
'in a quarter'
>>> thirteen_month_shift = now.shift(months=13)
>>> thirteen_month_shift.humanize(now, granularity="quarter")
'in 4 quarters'
>>> now.humanize(thirteen_month_shift, granularity="quarter")
'4 quarters ago'
```


- Added Sinhala and Urdu locales.

- Added official support for Python 3.10.

### Miscellaneous Chores

- Updated Azerbaijani, Hebrew, and Serbian locales and added
  tests.

- Passing an empty granularity list to `humanize` now raises
  a `ValueError`.

## [1.2.0] (2021-09-12)

### Features

- Added Albanian, Tamil and Zulu locales.

- Added support for `Decimal` as input to `arrow.get()`.

### Bug Fixes

- The Estonian, Finnish, Nepali and Zulu locales now support
  `dehumanize`.

- Improved validation checks when using parser tokens `A` and
  `hh`.

- Minor bug fixes to Catalan, Cantonese, Greek and Nepali
  locales.

## [1.1.1] (2021-06-24)

### Features

- Added Odia, Maltese, Serbian, Sami, and Luxembourgish locales.

### Bug Fixes

- All calls to `arrow.get()` should now properly pass the
  `tzinfo` argument to the Arrow constructor. See PR
  [#968](https://github.com/arrow-py/arrow/pull/968/) for more info.

- Humanize output is now properly truncated when a locale
  class overrides `_format_timeframe()`.

### Miscellaneous Chores

- Renamed `requirements.txt` to `requirements-dev.txt` to
  prevent confusion with the dependencies in `setup.py`.

- Updated Turkish locale and added tests.

## [1.1.0] (2021-04-26)

### Features

- Implemented the `dehumanize` method for `Arrow` objects. This
  takes human readable input and uses it to perform relative time
  shifts, for example:

``` python
>>> arw
<Arrow [2021-04-26T21:06:14.256803+00:00]>
>>> arw.dehumanize("8 hours ago")
<Arrow [2021-04-26T13:06:14.256803+00:00]>
>>> arw.dehumanize("in 4 days")
<Arrow [2021-04-30T21:06:14.256803+00:00]>
>>> arw.dehumanize("in an hour 34 minutes 10 seconds")
<Arrow [2021-04-26T22:40:24.256803+00:00]>
>>> arw.dehumanize("hace 2 años", locale="es")
<Arrow [2019-04-26T21:06:14.256803+00:00]>
```


- Made the start of the week adjustable when using
  `span("week")`, for example:

``` python
>>> arw
<Arrow [2021-04-26T21:06:14.256803+00:00]>
>>> arw.isoweekday()
1 # Monday
>>> arw.span("week")
(<Arrow [2021-04-26T00:00:00+00:00]>, <Arrow [2021-05-02T23:59:59.999999+00:00]>)
>>> arw.span("week", week_start=4)
(<Arrow [2021-04-22T00:00:00+00:00]>, <Arrow [2021-04-28T23:59:59.999999+00:00]>)
```


- Added Croatian, Latin, Latvian, Lithuanian and Malay locales.

### Bug Fixes

- Internally standardize locales and improve locale validation.
  Locales should now use the ISO notation of a dash (`"en-gb"`) rather
  than an underscore (`"en_gb"`) however this change is backward
  compatible.

- Correct type checking for internal locale mapping by using
  `_init_subclass`. This now allows subclassing of locales, for example:

``` python
>>> from arrow.locales import EnglishLocale
>>> class Klingon(EnglishLocale):
...     names = ["tlh"]
...
>>> from arrow import locales
>>> locales.get_locale("tlh")
<__main__.Klingon object at 0x7f7cd1effd30>
```


- Correct type checking for `arrow.get(2021, 3, 9)`
  construction.

- Audited all docstrings for style, typos and outdated info.

## [1.0.3] (2021-03-05)

### Bug Fixes

- Updated internals to avoid issues when running
  `mypy --strict`.

- Corrections to Swedish locale.

### Miscellaneous Chores

- Lowered required coverage limit until `humanize` month
  tests are fixed.

## [1.0.2] (2021-02-28)

### Bug Fixes

- Fixed an `OverflowError` that could occur when running Arrow
  on a 32-bit OS.

## [1.0.1] (2021-02-27)

### Bug Fixes

- A `py.typed` file is now bundled with the Arrow package to
  conform to PEP 561.

## [1.0.0] (2021-02-26)

After 8 years we're pleased to announce Arrow v1.0. Thanks to the entire
Python community for helping make Arrow the amazing package it is today!

### Features

- Added support for Python 3.9.

- Added a new keyword argument "exact" to `span`, `span_range`
  and `interval` methods. This makes timespans begin at the start time
  given and not extend beyond the end time given, for example:

``` python
>>> start = Arrow(2021, 2, 5, 12, 30)
>>> end = Arrow(2021, 2, 5, 17, 15)
>>> for r in arrow.Arrow.span_range('hour', start, end, exact=True):
...     print(r)
...
(<Arrow [2021-02-05T12:30:00+00:00]>, <Arrow [2021-02-05T13:29:59.999999+00:00]>)
(<Arrow [2021-02-05T13:30:00+00:00]>, <Arrow [2021-02-05T14:29:59.999999+00:00]>)
(<Arrow [2021-02-05T14:30:00+00:00]>, <Arrow [2021-02-05T15:29:59.999999+00:00]>)
(<Arrow [2021-02-05T15:30:00+00:00]>, <Arrow [2021-02-05T16:29:59.999999+00:00]>)
(<Arrow [2021-02-05T16:30:00+00:00]>, <Arrow [2021-02-05T17:14:59.999999+00:00]>)
```


- Arrow now natively supports PEP 484-style type annotations.

### Bug Fixes

- Fixed handling of maximum permitted timestamp on Windows
  systems.

- Corrections to French, German, Japanese and Norwegian locales.

### Miscellaneous Chores

- Arrow has **dropped support** for Python 2.7 and 3.5.

- There are multiple **breaking changes** with this release,
  please see the [migration
  guide](https://github.com/arrow-py/arrow/issues/832) for a complete
  overview.

- Arrow is now following [semantic
  versioning](https://semver.org/).

- Made `humanize` granularity="auto" limits more accurate to
  reduce strange results.

- Raise more appropriate errors when string parsing fails
  to match.

## [0.17.0] (2020-10-2)

### Features

- Arrow now properly handles imaginary datetimes during DST
  shifts. For example:

``` python
>>> just_before = arrow.get(2013, 3, 31, 1, 55, tzinfo="Europe/Paris")
>>> just_before.shift(minutes=+10)
<Arrow [2013-03-31T03:05:00+02:00]>
```

``` python
>>> before = arrow.get("2018-03-10 23:00:00", "YYYY-MM-DD HH:mm:ss", tzinfo="US/Pacific")
>>> after = arrow.get("2018-03-11 04:00:00", "YYYY-MM-DD HH:mm:ss", tzinfo="US/Pacific")
>>> result=[(t, t.to("utc")) for t in arrow.Arrow.range("hour", before, after)]
>>> for r in result:
...     print(r)
...
(<Arrow [2018-03-10T23:00:00-08:00]>, <Arrow [2018-03-11T07:00:00+00:00]>)
(<Arrow [2018-03-11T00:00:00-08:00]>, <Arrow [2018-03-11T08:00:00+00:00]>)
(<Arrow [2018-03-11T01:00:00-08:00]>, <Arrow [2018-03-11T09:00:00+00:00]>)
(<Arrow [2018-03-11T03:00:00-07:00]>, <Arrow [2018-03-11T10:00:00+00:00]>)
(<Arrow [2018-03-11T04:00:00-07:00]>, <Arrow [2018-03-11T11:00:00+00:00]>)
```


- Added `humanize` week granularity translation for Tagalog.

### Bug Fixes

- Fixed a bug that caused `Arrow.range()` to incorrectly cut off
  ranges in certain scenarios when using month, quarter, or year
  endings.

- Fixed a bug that caused day of week token parsing to be case
  sensitive.

### Miscellaneous Chores

- Arrow will **drop support** for Python 2.7 and 3.5 in the
  upcoming 1.0.0 release. This is the last major release to support
  Python 2.7 and Python 3.5.

- Calls to the `timestamp` property now emit a
  `DeprecationWarning`. In a future release, `timestamp` will be changed
  to a method to align with Python's datetime module. If you would like
  to continue using the property, please change your code to use the
  `int_timestamp` or `float_timestamp` properties instead.

- Expanded and improved Catalan locale.

- A number of functions were reordered in arrow.py for
  better organization and grouping of related methods. This change will
  have no impact on usage.

- A minimum tox version is now enforced for compatibility
  reasons. Contributors must use tox \>3.18.0 going forward.

## [0.16.0] (2020-08-23)

### Features

- Implemented [PEP
  495](https://www.python.org/dev/peps/pep-0495/) to handle ambiguous
  datetimes. This is achieved by the addition of the `fold` attribute
  for Arrow objects. For example:

``` python
>>> before = Arrow(2017, 10, 29, 2, 0, tzinfo='Europe/Stockholm')
<Arrow [2017-10-29T02:00:00+02:00]>
>>> before.fold
0
>>> before.ambiguous
True
>>> after = Arrow(2017, 10, 29, 2, 0, tzinfo='Europe/Stockholm', fold=1)
<Arrow [2017-10-29T02:00:00+01:00]>
>>> after = before.replace(fold=1)
<Arrow [2017-10-29T02:00:00+01:00]>
```


- Added `normalize_whitespace` flag to `arrow.get`. This is
  useful for parsing log files and/or any files that may contain
  inconsistent spacing. For example:

``` python
>>> arrow.get("Jun 1 2005     1:33PM", "MMM D YYYY H:mmA", normalize_whitespace=True)
<Arrow [2005-06-01T13:33:00+00:00]>
>>> arrow.get("2013-036 \t  04:05:06Z", normalize_whitespace=True)
<Arrow [2013-02-05T04:05:06+00:00]>
```


### Miscellaneous Chores

- Arrow will **drop support** for Python 2.7 and 3.5 in the
  upcoming 1.0.0 release. The 0.16.x and 0.17.x releases are the last to
  support Python 2.7 and 3.5.

## [0.15.8] (2020-07-23)

### Features

- Added `humanize` week granularity translation for Czech.

### Bug Fixes

- `arrow.get` will now pick sane defaults when weekdays are
  passed with particular token combinations, see
  [#446](https://github.com/arrow-py/arrow/issues/446).

### Miscellaneous Chores

- Arrow will **drop support** for Python 2.7 and 3.5 in the
  upcoming 1.0.0 release. The 0.15.x, 0.16.x, and 0.17.x releases are
  the last to support Python 2.7 and 3.5.

- Moved arrow to an organization. The repo can now be found
  [here](https://github.com/arrow-py/arrow).

- Started issuing deprecation warnings for Python 2.7 and
  3.5.

- Added Python 3.9 to CI pipeline.

## [0.15.7] (2020-06-19)

### Features

- Added a number of built-in format strings. See the
  [docs](https://arrow.readthedocs.io/#built-in-formats) for a complete
  list of supported formats. For example:

``` python
>>> arw = arrow.utcnow()
>>> arw.format(arrow.FORMAT_COOKIE)
'Wednesday, 27-May-2020 10:30:35 UTC'
```


- Arrow is now fully compatible with Python 3.9 and PyPy3.

- Added Makefile, tox.ini, and requirements.txt files to the
  distribution bundle.

- Added French Canadian and Swahili locales.

- Added `humanize` week granularity translation for Hebrew,
  Greek, Macedonian, Swedish, Slovak.

### Bug Fixes

- ms and μs timestamps are now normalized in `arrow.get()`,
  `arrow.fromtimestamp()`, and `arrow.utcfromtimestamp()`. For example:

``` python
>>> ts = 1591161115194556
>>> arw = arrow.get(ts)
<Arrow [2020-06-03T05:11:55.194556+00:00]>
>>> arw.timestamp
1591161115
```


- Refactored and updated Macedonian, Hebrew, Korean, and
  Portuguese locales.

## [0.15.6] (2020-04-29)

### Features

- Added support for parsing and formatting [ISO 8601 week
  dates](https://en.wikipedia.org/wiki/ISO_week_date) via a new token
  `W`, for example:

``` python
>>> arrow.get("2013-W29-6", "W")
<Arrow [2013-07-20T00:00:00+00:00]>
>>> utc=arrow.utcnow()
>>> utc
<Arrow [2020-01-23T18:37:55.417624+00:00]>
>>> utc.format("W")
'2020-W04-4'
```


- Formatting with `x` token (microseconds) is now possible, for
  example:

``` python
>>> dt = arrow.utcnow()
>>> dt.format("x")
'1585669870688329'
>>> dt.format("X")
'1585669870'
```


- Added `humanize` week granularity translation for German,
  Italian, Polish & Taiwanese locales.

### Bug Fixes

- Consolidated and simplified German locales.

### Miscellaneous Chores

- Moved testing suite from nosetest/Chai to
  pytest/pytest-mock.

- Converted xunit-style setup and teardown functions in
  tests to pytest fixtures.

- Setup GitHub Actions for CI alongside Travis.

- Help support Arrow's future development by donating to
  the project on [Open Collective](https://opencollective.com/arrow).

## [0.15.5] (2020-01-03)

### Features

- Added bounds parameter to `span_range`, `interval` and `span`
  methods. This allows you to include or exclude the start and end
  values.

- `arrow.get()` can now create arrow objects from a timestamp
  with a timezone, for example:

``` python
>>> arrow.get(1367900664, tzinfo=tz.gettz('US/Pacific'))
<Arrow [2013-05-06T21:24:24-07:00]>
```


- `humanize` can now combine multiple levels of granularity, for
  example:

``` python
>>> later140 = arrow.utcnow().shift(seconds=+8400)
>>> later140.humanize(granularity="minute")
'in 139 minutes'
>>> later140.humanize(granularity=["hour", "minute"])
'in 2 hours and 19 minutes'
```


- Added Hong Kong locale (`zh_hk`).

- Added `humanize` week granularity translation for Dutch.

- Numbers are now displayed when using the seconds granularity
  in `humanize`.

### Bug Fixes

- Improved parsing of strings that contain punctuation.

- Improved behaviour of `humanize` when singular seconds are
  involved.


### Miscellaneous Chores

- Python 2 reached EOL on 2020-01-01. arrow will **drop
  support** for Python 2 in a future release to be decided (see
  [#739](https://github.com/arrow-py/arrow/issues/739)).

- `range` now supports both the singular and plural forms of
  the `frames` argument (e.g. day and days).

## [0.15.4] (2019-11-02)

### Bug Fixes

- Fixed an issue that caused package installs to fail on Conda
  Forge.

## [0.15.3] (2019-11-02)

### Features

- `factory.get()` can now create arrow objects from a ISO
  calendar tuple, for example:

``` python
>>> arrow.get((2013, 18, 7))
<Arrow [2013-05-05T00:00:00+00:00]>
```


- Added a new token `x` to allow parsing of integer timestamps
  with milliseconds and microseconds.

- Formatting now supports escaping of characters using the same
  syntax as parsing, for example:

``` python
>>> arw = arrow.now()
>>> fmt = "YYYY-MM-DD h [h] m"
>>> arw.format(fmt)
'2019-11-02 3 h 32'
```


- Added `humanize` week granularity translations for Chinese,
  Spanish and Vietnamese.

### Bug Fixes

- Added support for midnight at end of day. See
  [#703](https://github.com/arrow-py/arrow/issues/703) for details.

### Miscellaneous Chores

- Added `ParserError` to module exports.

- Created Travis build for macOS.

- Test parsing and formatting against full timezone
  database.

## [0.15.2] (2019-09-14)

### Features

- Added `humanize` week granularity translations for Portuguese
  and Brazilian Portuguese.

- Embedded changelog within docs and added release dates to
  versions.

### Bug Fixes

- Fixed a bug that caused test failures on Windows only, see
  [#668](https://github.com/arrow-py/arrow/issues/668) for details.

## [0.15.1] (2019-09-10)

### Features

- Added `humanize` week granularity translations for Japanese.

### Bug Fixes

- Fixed a bug that caused Arrow to fail when passed a negative
  timestamp string.

- Fixed a bug that caused Arrow to fail when passed a datetime
  object with `tzinfo` of type `StaticTzInfo`.

## [0.15.0] (2019-09-08)

### Features

- Added support for DDD and DDDD ordinal date tokens. The
  following functionality is now possible: `arrow.get("1998-045")`,
  `arrow.get("1998-45", "YYYY-DDD")`,
  `arrow.get("1998-045", "YYYY-DDDD")`.

- ISO 8601 basic format for dates and times is now supported
  (e.g. `YYYYMMDDTHHmmssZ`).

- Added `humanize` week granularity translations for French,
  Russian and Swiss German locales.

### Bug Fixes

- The timestamp token (`X`) will now only match on strings that
  **strictly contain integers and floats**, preventing incorrect
  matches.

- Most instances of `arrow.get()` returning an incorrect `Arrow`
  object from a partial parsing match have been eliminated. The
  following issue have been addressed:
  [#91](https://github.com/arrow-py/arrow/issues/91),
  [#196](https://github.com/arrow-py/arrow/issues/196),
  [#396](https://github.com/arrow-py/arrow/issues/396),
  [#434](https://github.com/arrow-py/arrow/issues/434),
  [#447](https://github.com/arrow-py/arrow/issues/447),
  [#456](https://github.com/arrow-py/arrow/issues/456),
  [#519](https://github.com/arrow-py/arrow/issues/519),
  [#538](https://github.com/arrow-py/arrow/issues/538),
  [#560](https://github.com/arrow-py/arrow/issues/560).


### Miscellaneous Chores

- Timestamps of type `str` are no longer supported **without
  a format string** in the `arrow.get()` method. This change was made to
  support the ISO 8601 basic format and to address bugs such as
  [#447](https://github.com/arrow-py/arrow/issues/447).

The following will NOT work in v0.15.0:

``` python
>>> arrow.get("1565358758")
>>> arrow.get("1565358758.123413")
```

The following will work in v0.15.0:

``` python
>>> arrow.get("1565358758", "X")
>>> arrow.get("1565358758.123413", "X")
>>> arrow.get(1565358758)
>>> arrow.get(1565358758.123413)
```


- When a meridian token (a\|A) is passed and no meridians are
  available for the specified locale (e.g. unsupported or untranslated)
  a `ParserError` is raised.

- The timestamp token (`X`) will now match float timestamps
  of type `str`: `arrow.get(“1565358758.123415”, “X”)`.

- Strings with leading and/or trailing whitespace will no
  longer be parsed without a format string. Please see [the
  docs](https://arrow.readthedocs.io/#regular-expressions) for ways to
  handle this.

## [0.14.7] (2019-09-04)

### Miscellaneous Chores

- `ArrowParseWarning` will no longer be printed on every call
  to `arrow.get()` with a datetime string. The purpose of the warning
  was to start a conversation about the upcoming 0.15.0 changes and we
  appreciate all the feedback that the community has given us!

## [0.14.6] (2019-08-28)

### Features

- Added support for `week` granularity in `Arrow.humanize()`.
  For example,
  `arrow.utcnow().shift(weeks=-1).humanize(granularity="week")` outputs
  "a week ago". This change introduced two new untranslated words,
  `week` and `weeks`, to all locale dictionaries, so locale
  contributions are welcome!

- Fully translated the Brazilian Portuguese locale.

### Bug Fixes

- Fixed a bug that caused `arrow.get()` to ignore tzinfo
  arguments of type string (e.g. `arrow.get(tzinfo="Europe/Paris")`).

- Fixed a bug that occurred when `arrow.Arrow()` was
  instantiated with a `pytz` tzinfo object.

- Fixed a bug that caused Arrow to fail when passed a sub-second
  token, that when rounded, had a value greater than 999999 (e.g.
  `arrow.get("2015-01-12T01:13:15.9999995")`). Arrow should now
  accurately propagate the rounding for large sub-second tokens.


### Miscellaneous Chores

- Updated the Macedonian locale to inherit from a Slavic
  base.

## [0.14.5] (2019-08-09)

### Features

- Added Afrikaans locale.

### Bug Fixes

- Fixed bug that occurred when `factory.get()` was passed a
  locale kwarg.


### Miscellaneous Chores

- Removed deprecated `replace` shift functionality. Users
  looking to pass plural properties to the `replace` function to shift
  values should use `shift` instead.

## [0.14.4] (2019-07-30)

### Bug Fixes

- Fixed a regression in 0.14.3 that prevented a tzinfo argument
  of type string to be passed to the `get()` function. Functionality
  such as `arrow.get("2019072807", "YYYYMMDDHH", tzinfo="UTC")` should
  work as normal again.

### Miscellaneous Chores

- Moved `backports.functools_lru_cache` dependency from
  `extra_requires` to `install_requires` for `Python 2.7` installs to
  fix [#495](https://github.com/arrow-py/arrow/issues/495).

## [0.14.3] (2019-07-28)

### Features

- Added full support for Python 3.8.

### Bug Fixes

- Extensive refactor and update of documentation.

- factory.get() can now construct from kwargs.

- Added meridians to Spanish Locale.


### Miscellaneous Chores

- Added warnings for upcoming factory.get() parsing changes
  in 0.15.0. Please see
  [#612](https://github.com/arrow-py/arrow/issues/612) for full
  details.

## [0.14.2] (2019-06-06)

### Bug Fixes

- Fixed UnicodeDecodeError on certain locales (#600).


### Miscellaneous Chores

- Travis CI builds now use tox to lint and run tests.

## [0.14.1] (2019-06-06)

### Bug Fixes

- Fixed `ImportError: No module named 'dateutil'` (#598).

## [0.14.0] (2019-06-06)

### Features

- Added provisional support for Python 3.8.

### Bug Fixes

- Updated setup.py with modern Python standards.

- Upgraded dependencies to latest versions.

- Enabled flake8 and black on travis builds.

- Formatted code using black and isort.


### Miscellaneous Chores

- Removed support for EOL Python 3.4.

## [0.13.2] (2019-05-30)

### Features

- Add is_between method.

### Bug Fixes

- Improved humanize behaviour for near zero durations (#416).

- Correct humanize behaviour with future days (#541).

- Documentation updates.

- Improvements to German Locale.

## [0.13.1] (2019-02-17)

### Features

- Add support for Python 3.7.

### Bug Fixes

- Documentation and docstring updates.


### Miscellaneous Chores

- Remove deprecation decorators for Arrow.range(),
  Arrow.span_range() and Arrow.interval(), all now return generators,
  wrap with list() to get old behavior.

## [0.13.0] (2019-01-09)

### Features

- Added support for Python 3.6.

- Added support for ZZZ when formatting.

- Added Estonian Locale.

### Bug Fixes

- Make arrow.get() work with str & tzinfo combo.

- Make sure special RegEx characters are escaped in format
  string.

- Stop using datetime.utcnow() in internals, use
  datetime.now(UTC) instead.

- Return NotImplemented instead of TypeError in arrow math
  internals.

- Small fixes to Greek locale.

- TagalogLocale improvements.

- Added test requirements to setup.

- Improve docs for get, now and utcnow methods.

- Correct typo in depreciation warning.


### Miscellaneous Chores

- Drop support for Python 2.6/3.3.

- Return generator instead of list for Arrow.range(),
  Arrow.span_range() and Arrow.interval().

## [0.12.1]

### Bug Fixes

- Allow universal wheels to be generated and reliably installed.

- Make humanize respect only_distance when granularity argument
  is also given.

## [0.12.0]

### Bug Fixes

- Compatibility fix for Python 2.x

## [0.11.0]

### Features

- Add Nepali Locale

- Add Indonesian Locale


### Bug Fixes

- Fix grammar of ArabicLocale

- Fix month name + rename AustriaLocale -\> AustrianLocale

- Fix typo in Basque Locale

- Fix grammar in PortugueseBrazilian locale

- Remove pip --user-mirrors flag

## [0.10.0]

### Bug Fixes

- Fix getattr off by one for quarter

- Fix negative offset for UTC

- Update arrow.py

## [0.9.0]

### Features

- Remove duplicate code

- Support gnu date iso 8601

- Add support for universal wheels

- Slovenian locale

- Slovak locale

- Romanian locale

- Added tox

- Azerbaijani locale added, locale issue fixed in Turkish.

### Bug Fixes

- respect limit even if end is defined range

- Separate replace & shift functions

- Fix supported Python versions in documentation

- Format ParserError's raise message

## [0.8.0]

### Miscellaneous Chores

- []

## [0.7.1]

### Features

- Esperanto locale (batisteo)

## [0.7.0]

### Features

- Humanize for time duration #232 (ybrs)

- Add Thai locale (sipp11)

- Adding Belarusian (be) locale (oire)

- Search date in strings (beenje)

- Note that arrow's tokens differ from strptime's. (offby1)


### Bug Fixes

- Parse localized strings #228 (swistakm)

- Modify tzinfo parameter in `get` api #221 (bottleimp)

- Fix Czech locale (PrehistoricTeam)

- Raise TypeError when adding/subtracting non-dates
  (itsmeolivia)

- Fix pytz conversion error (Kudo)

- Fix overzealous time truncation in span_range (kdeldycke)

## [0.6.0]

### Features

- Add minimal support for fractional seconds longer than six
  digits.

- Adding locale support for Marathi (mr)

- Add count argument to span method

- Improved docs


### Bug Fixes

- Added support for Python 3

- Avoid truncating oversized epoch timestamps. Fixes #216.

- Fixed month abbreviations for Ukrainian

- Fix typo timezone

- A couple of dialect fixes and two new languages

- Spanish locale: `Miercoles` should have acute accent

- Fix typo in 'Arrow.floor' docstring

- Use read() utility to open README

- span_range for week frame

### Miscellaneous Chores

- [Fix] Fix Finnish grammar

## [0.5.1 - 0.5.4]

### Bug Fixes

- test the behavior of simplejson instead of calling for_json
  directly (tonyseek)

- Add Hebrew Locale (doodyparizada)

- Update documentation location (andrewelkins)

- Update setup.py Development Status level (andrewelkins)

- Case insensitive month match (cshowe)

## [0.5.0]

### Features

- struct_time addition. (mhworth)

- Version grep (eirnym)

- Default to ISO 8601 format (emonty)

- Raise TypeError on comparison (sniekamp)

- Adding Macedonian(mk) locale (krisfremen)

### Bug Fixes

- Fix for ISO seconds and fractional seconds (sdispater)
  (andrewelkins)

- Use correct Dutch wording for "hours" (wbolster)

- Complete the list of english locales (indorilftw)

- Change README to reStructuredText (nyuszika7h)

- Parse lower-cased 'h' (tamentis)

- Slight modifications to Dutch locale (nvie)

## [0.4.4]

### Features

- Include the docs in the released tarball

- Czech localization Czech localization for Arrow

- Add fa_ir to locales

### Bug Fixes

- Fixes parsing of time strings with a final Z

- Fixes ISO parsing and formatting for fractional seconds

- test_fromtimestamp sp

- some typos fixed

- removed an unused import statement

- docs table fix

- Issue with specify 'X' template and no template at all to
  arrow.get

- Fix "import" typo in docs/index.rst

- Fix unit tests for zero passed

- Update layout.html

- In Norwegian and new Norwegian months and weekdays should not
  be capitalized

- Fixed discrepancy between specifying 'X' to arrow.get and
  specifying no template

## [0.4.3]

### Features

- Turkish locale (Emre)

- Arabic locale (Mosab Ahmad)

- Danish locale (Holmars)

- Icelandic locale (Holmars)

- Hindi locale (Atmb4u)

- Malayalam locale (Atmb4u)

- Finnish locale (Stormpat)

- Portuguese locale (Danielcorreia)

- `h` and `hh` strings are now supported (Averyonghub)

### Bug Fixes

- An incorrect inflection in the Polish locale has been fixed
  (Avalanchy)

- `arrow.get` now properly handles `Date` (Jaapz)

- Tests are now declared in `setup.py` and the manifest
  (Pypingou)

- `__version__` has been added to `__init__.py` (Sametmax)

- ISO 8601 strings can be parsed without a separator
  (Ivandiguisto / Root)

- Documentation is now more clear regarding some inputs on
  `arrow.get` (Eriktaubeneck)

- Some documentation links have been fixed (Vrutsky)

- Error messages for parse errors are now more descriptive
  (Maciej Albin)

- The parser now correctly checks for separators in strings
  (Mschwager)

## [0.4.2]

### Features

- Factory `get` method now accepts a single `Arrow` argument.

- Tokens SSSS, SSSSS and SSSSSS are supported in parsing.

- `Arrow` objects have a `float_timestamp` property.

- Vietnamese locale (Iu1nguoi)

- Factory `get` method now accepts a list of format strings
  (Dgilland)

- A MANIFEST.in file has been added (Pypingou)

- Tests can be run directly from `setup.py` (Pypingou)

### Bug Fixes

- Arrow docs now list 'day of week' format tokens correctly
  (Rudolphfroger)

- Several issues with the Korean locale have been resolved
  (Yoloseem)

- `humanize` now correctly returns unicode (Shvechikov)

- `Arrow` objects now pickle / unpickle correctly (Yoloseem)

## [0.4.1]

### Features

- Table / explanation of formatting & parsing tokens in docs

- Brazilian locale (Augusto2112)

- Dutch locale (OrangeTux)

- Italian locale (Pertux)

- Austrian locale (LeChewbacca)

- Tagalog locale (Marksteve)

### Bug Fixes

- Corrected spelling and day numbers in German locale
  (LeChewbacca)

- Factory `get` method should now handle unicode strings
  correctly (Bwells)

- Midnight and noon should now parse and format correctly
  (Bwells)

## [0.4.0]

### Features

- Format-free ISO 8601 parsing in factory `get` method

- Support for 'week' / 'weeks' in `span`, `range`, `span_range`,
  `floor` and `ceil`

- Support for 'weeks' in `replace`

- Norwegian locale (Martinp)

- Japanese locale (CortYuming)

### Bug Fixes

- Timezones no longer show the wrong sign when formatted (Bean)

- Microseconds are parsed correctly from strings (Bsidhom)

- Locale day-of-week is no longer off by one (Cynddl)

- Corrected plurals of Ukrainian and Russian nouns (Catchagain)

### Miscellaneous Chores

- Old 0.1 `arrow` module method removed

- Dropped timestamp support in `range` and `span_range`
  (never worked correctly)

- Dropped parsing of single string as tz string in factory
  `get` method (replaced by ISO 8601)

## [0.3.5]

### Features

- French locale (Cynddl)

- Spanish locale (Slapresta)

### Bug Fixes

- Ranges handle multiple timezones correctly (Ftobia)

## [0.3.4]

### Bug Fixes

- Humanize no longer sometimes returns the wrong month delta

- `__format__` works correctly with no format string

## [0.3.3]

### Features

- Python 2.6 support

- Initial support for locale-based parsing and formatting

- ArrowFactory class, now proxied as the module API

- `factory` api method to obtain a factory for a custom type

### Bug Fixes

- Python 3 support and tests completely ironed out

## [0.3.2]

### Features

- Python 3+ support

## [0.3.1]

### Bug Fixes

- The old `arrow` module function handles timestamps correctly
  as it used to

## [0.3.0]

### Features

- `Arrow.replace` method

- Accept timestamps, datetimes and Arrows for datetime inputs,
  where reasonable

### Bug Fixes

- `range` and `span_range` respect end and limit parameters
  correctly

### Miscellaneous Chores

- Arrow objects are no longer mutable

- Plural attribute name semantics altered: single -\>
  absolute, plural -\> relative

- Plural names no longer supported as properties (e.g.
  `arrow.utcnow().years`)

## [0.2.1]

### Features

- Support for localized humanization

- English, Russian, Greek, Korean, Chinese locales

## [0.2.0]

### Features

- Date parsing

- Date formatting

- `floor`, `ceil` and `span` methods

- `datetime` interface implementation

- `clone` method

- `get`, `now` and `utcnow` API methods


### Miscellaneous Chores

- **REWRITE**

## [0.1.6]

### Features

- Humanized time deltas

- `__eq__` implemented

### Bug Fixes

- Issues with conversions related to daylight savings time
  resolved

### Miscellaneous Chores

- `__str__` uses ISO formatting

## [0.1.5]

### Features

- Parsing of ISO-formatted time zone offsets (e.g. '+02:30',
  '-05:00')

- Resolved some issues with timestamps and delta / Olson time
  zones

### Miscellaneous Chores

- **Started tracking changes**
