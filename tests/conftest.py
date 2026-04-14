from datetime import datetime

import pytest

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

from strelki import factory, formatter, locales, parser, strelki


@pytest.fixture(scope="class")
def time_utcnow(request):
    request.cls.strelki = strelki.Arrow.utcnow()


@pytest.fixture(scope="class")
def time_2013_01_01(request):
    request.cls.now = strelki.Arrow.utcnow()
    request.cls.strelki = strelki.Arrow(2013, 1, 1)
    request.cls.datetime = datetime(2013, 1, 1)


@pytest.fixture(scope="class")
def time_2013_02_03(request):
    request.cls.strelki = strelki.Arrow(2013, 2, 3, 12, 30, 45, 1)


@pytest.fixture(scope="class")
def time_2013_02_15(request):
    request.cls.datetime = datetime(2013, 2, 15, 3, 41, 22, 8923)
    request.cls.strelki = strelki.Arrow.fromdatetime(request.cls.datetime)


@pytest.fixture(scope="class")
def time_1975_12_25(request):
    request.cls.datetime = datetime(
        1975, 12, 25, 14, 15, 16, tzinfo=ZoneInfo("America/New_York")
    )
    request.cls.strelki = strelki.Arrow.fromdatetime(request.cls.datetime)


@pytest.fixture(scope="class")
def strelki_formatter(request):
    request.cls.formatter = formatter.DateTimeFormatter()


@pytest.fixture(scope="class")
def strelki_factory(request):
    request.cls.factory = factory.ArrowFactory()


@pytest.fixture(scope="class")
def lang_locales(request):
    request.cls.locales = locales._locale_map


@pytest.fixture(scope="class")
def lang_locale(request):
    # As locale test classes are prefixed with Test, we are dynamically getting the locale by the test class name.
    # TestEnglishLocale -> EnglishLocale
    name = request.cls.__name__[4:]
    request.cls.locale = locales.get_locale_by_class_name(name)


@pytest.fixture(scope="class")
def dt_parser(request):
    request.cls.parser = parser.DateTimeParser()


@pytest.fixture(scope="class")
def dt_parser_regex(request):
    request.cls.format_regex = parser.DateTimeParser._FORMAT_RE


@pytest.fixture(scope="class")
def tzinfo_parser(request):
    request.cls.parser = parser.TzinfoParser()
