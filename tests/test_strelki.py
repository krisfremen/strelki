try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

import pickle
import sys
import time
from datetime import date, datetime, timedelta, timezone
from typing import List

import dateutil
import pytest
import pytz
import simplejson as json
from dateutil import tz
from dateutil.relativedelta import FR, MO, SA, SU, TH, TU, WE

from strelki import strelki, locales

from .utils import assert_datetime_equality


class TestTestStrelkiInit:
    def test_init_bad_input(self):
        with pytest.raises(TypeError):
            strelki.Arrow(2013)

        with pytest.raises(TypeError):
            strelki.Arrow(2013, 2)

        with pytest.raises(ValueError):
            strelki.Arrow(2013, 2, 2, 12, 30, 45, 9999999)

    def test_init(self):
        result = strelki.Arrow(2013, 2, 2)
        self.expected = datetime(2013, 2, 2, tzinfo=tz.tzutc())
        assert result._datetime == self.expected

        result = strelki.Arrow(2013, 2, 2, 12)
        self.expected = datetime(2013, 2, 2, 12, tzinfo=tz.tzutc())
        assert result._datetime == self.expected

        result = strelki.Arrow(2013, 2, 2, 12, 30)
        self.expected = datetime(2013, 2, 2, 12, 30, tzinfo=tz.tzutc())
        assert result._datetime == self.expected

        result = strelki.Arrow(2013, 2, 2, 12, 30, 45)
        self.expected = datetime(2013, 2, 2, 12, 30, 45, tzinfo=tz.tzutc())
        assert result._datetime == self.expected

        result = strelki.Arrow(2013, 2, 2, 12, 30, 45, 999999)
        self.expected = datetime(2013, 2, 2, 12, 30, 45, 999999, tzinfo=tz.tzutc())
        assert result._datetime == self.expected

        result = strelki.Arrow(
            2013, 2, 2, 12, 30, 45, 999999, tzinfo=ZoneInfo("Europe/Paris")
        )
        self.expected = datetime(
            2013, 2, 2, 12, 30, 45, 999999, tzinfo=ZoneInfo("Europe/Paris")
        )
        assert result._datetime == self.expected

    # regression tests for issue #626
    def test_init_pytz_timezone(self):
        result = strelki.Arrow(
            2013, 2, 2, 12, 30, 45, 999999, tzinfo=pytz.timezone("Europe/Paris")
        )
        self.expected = datetime(
            2013, 2, 2, 12, 30, 45, 999999, tzinfo=ZoneInfo("Europe/Paris")
        )
        assert result._datetime == self.expected
        assert_datetime_equality(result._datetime, self.expected, 1)

    def test_init_zoneinfo_timezone(self):
        result = strelki.Arrow(
            2024, 7, 10, 18, 55, 45, 999999, tzinfo=ZoneInfo("Europe/Paris")
        )
        self.expected = datetime(
            2024, 7, 10, 18, 55, 45, 999999, tzinfo=ZoneInfo("Europe/Paris")
        )
        assert result._datetime == self.expected
        assert_datetime_equality(result._datetime, self.expected, 1)

    def test_init_dateutil_timezone(self):
        result = strelki.Arrow(
            2024, 7, 10, 18, 55, 45, 999999, tzinfo=tz.gettz("Europe/Paris")
        )
        self.expected = datetime(
            2024, 7, 10, 18, 55, 45, 999999, tzinfo=ZoneInfo("Europe/Paris")
        )
        assert result._datetime == self.expected
        assert_datetime_equality(result._datetime, self.expected, 1)

    def test_init_with_fold(self):
        before = strelki.Arrow(2017, 10, 29, 2, 0, tzinfo="Europe/Stockholm")
        after = strelki.Arrow(2017, 10, 29, 2, 0, tzinfo="Europe/Stockholm", fold=1)

        assert hasattr(before, "fold")
        assert hasattr(after, "fold")

        # PEP-495 requires the comparisons below to be true
        assert before == after
        assert before.utcoffset() != after.utcoffset()


class TestTestStrelkiFactory:
    def test_now(self):
        result = strelki.Arrow.now()

        assert_datetime_equality(result._datetime, datetime.now().astimezone())

    def test_utcnow(self):
        result = strelki.Arrow.utcnow()

        assert_datetime_equality(
            result._datetime, datetime.now(timezone.utc).replace(tzinfo=timezone.utc)
        )

        assert result.fold == 0

    def test_fromtimestamp(self):
        timestamp = time.time()

        result = strelki.Arrow.fromtimestamp(timestamp)
        assert_datetime_equality(result._datetime, datetime.now().astimezone())

        result = strelki.Arrow.fromtimestamp(timestamp, tzinfo=ZoneInfo("Europe/Paris"))
        assert_datetime_equality(
            result._datetime,
            datetime.fromtimestamp(timestamp, ZoneInfo("Europe/Paris")),
        )

        result = strelki.Arrow.fromtimestamp(timestamp, tzinfo="Europe/Paris")
        assert_datetime_equality(
            result._datetime,
            datetime.fromtimestamp(timestamp, ZoneInfo("Europe/Paris")),
        )

        with pytest.raises(ValueError):
            strelki.Arrow.fromtimestamp("invalid timestamp")

    def test_utcfromtimestamp(self):
        timestamp = time.time()

        result = strelki.Arrow.utcfromtimestamp(timestamp)
        assert_datetime_equality(
            result._datetime, datetime.now(timezone.utc).replace(tzinfo=timezone.utc)
        )

        with pytest.raises(ValueError):
            strelki.Arrow.utcfromtimestamp("invalid timestamp")

    def test_fromdatetime(self):
        dt = datetime(2013, 2, 3, 12, 30, 45, 1)

        result = strelki.Arrow.fromdatetime(dt)

        assert result._datetime == dt.replace(tzinfo=tz.tzutc())

    def test_fromdatetime_dt_tzinfo(self):
        dt = datetime(2013, 2, 3, 12, 30, 45, 1, tzinfo=ZoneInfo("US/Pacific"))

        result = strelki.Arrow.fromdatetime(dt)

        assert result._datetime == dt.replace(tzinfo=ZoneInfo("US/Pacific"))

    def test_fromdatetime_tzinfo_arg(self):
        dt = datetime(2013, 2, 3, 12, 30, 45, 1)

        result = strelki.Arrow.fromdatetime(dt, ZoneInfo("US/Pacific"))

        assert result._datetime == dt.replace(tzinfo=ZoneInfo("US/Pacific"))

    def test_fromdate(self):
        dt = date(2013, 2, 3)

        result = strelki.Arrow.fromdate(dt, ZoneInfo("US/Pacific"))

        assert result._datetime == datetime(2013, 2, 3, tzinfo=ZoneInfo("US/Pacific"))

    def test_strptime(self):
        formatted = datetime(2013, 2, 3, 12, 30, 45).strftime("%Y-%m-%d %H:%M:%S")

        result = strelki.Arrow.strptime(formatted, "%Y-%m-%d %H:%M:%S")
        assert result._datetime == datetime(2013, 2, 3, 12, 30, 45, tzinfo=tz.tzutc())

        result = strelki.Arrow.strptime(
            formatted, "%Y-%m-%d %H:%M:%S", tzinfo=ZoneInfo("Europe/Paris")
        )
        assert result._datetime == datetime(
            2013, 2, 3, 12, 30, 45, tzinfo=ZoneInfo("Europe/Paris")
        )

    def test_fromordinal(self):
        timestamp = 1607066909.937968
        with pytest.raises(TypeError):
            strelki.Arrow.fromordinal(timestamp)
        with pytest.raises(ValueError):
            strelki.Arrow.fromordinal(int(timestamp))

        ordinal = strelki.Arrow.utcnow().toordinal()

        with pytest.raises(TypeError):
            strelki.Arrow.fromordinal(str(ordinal))

        result = strelki.Arrow.fromordinal(ordinal)
        dt = datetime.fromordinal(ordinal)

        assert result.naive == dt


@pytest.mark.usefixtures("time_2013_02_03")
class TestTestStrelkiRepresentation:
    def test_repr(self):
        result = self.strelki.__repr__()

        assert result == f"<Arrow [{self.strelki._datetime.isoformat()}]>"

    def test_str(self):
        result = self.strelki.__str__()

        assert result == self.strelki._datetime.isoformat()

    def test_hash(self):
        result = self.strelki.__hash__()

        assert result == self.strelki._datetime.__hash__()

    def test_format(self):
        result = f"{self.strelki:YYYY-MM-DD}"

        assert result == "2013-02-03"

    def test_bare_format(self):
        result = self.strelki.format()

        assert result == "2013-02-03 12:30:45+00:00"

    def test_format_no_format_string(self):
        result = f"{self.strelki}"

        assert result == str(self.strelki)

    def test_clone(self):
        result = self.strelki.clone()

        assert result is not self.strelki
        assert result._datetime == self.strelki._datetime


@pytest.mark.usefixtures("time_2013_01_01")
class TestStrelkiAttribute:
    def test_getattr_base(self):
        with pytest.raises(AttributeError):
            self.strelki.prop

    def test_getattr_week(self):
        assert self.strelki.week == 1

    def test_getattr_quarter(self):
        # start dates
        q1 = strelki.Arrow(2013, 1, 1)
        q2 = strelki.Arrow(2013, 4, 1)
        q3 = strelki.Arrow(2013, 8, 1)
        q4 = strelki.Arrow(2013, 10, 1)
        assert q1.quarter == 1
        assert q2.quarter == 2
        assert q3.quarter == 3
        assert q4.quarter == 4

        # end dates
        q1 = strelki.Arrow(2013, 3, 31)
        q2 = strelki.Arrow(2013, 6, 30)
        q3 = strelki.Arrow(2013, 9, 30)
        q4 = strelki.Arrow(2013, 12, 31)
        assert q1.quarter == 1
        assert q2.quarter == 2
        assert q3.quarter == 3
        assert q4.quarter == 4

    def test_getattr_dt_value(self):
        assert self.strelki.year == 2013

    def test_tzinfo(self):
        assert self.strelki.tzinfo == timezone.utc

    def test_naive(self):
        assert self.strelki.naive == self.strelki._datetime.replace(tzinfo=None)

    def test_timestamp(self):
        assert self.strelki.timestamp() == self.strelki._datetime.timestamp()

    def test_int_timestamp(self):
        assert self.strelki.int_timestamp == int(self.strelki._datetime.timestamp())

    def test_float_timestamp(self):
        assert self.strelki.float_timestamp == self.strelki._datetime.timestamp()

    def test_getattr_fold(self):
        # UTC is always unambiguous
        assert self.now.fold == 0

        ambiguous_dt = strelki.Arrow(
            2017, 10, 29, 2, 0, tzinfo="Europe/Stockholm", fold=1
        )
        assert ambiguous_dt.fold == 1

        with pytest.raises(AttributeError):
            ambiguous_dt.fold = 0

    def test_getattr_ambiguous(self):
        assert not self.now.ambiguous

        ambiguous_dt = strelki.Arrow(2017, 10, 29, 2, 0, tzinfo="Europe/Stockholm")

        assert ambiguous_dt.ambiguous

    def test_getattr_imaginary(self):
        assert not self.now.imaginary

        imaginary_dt = strelki.Arrow(2013, 3, 31, 2, 30, tzinfo="Europe/Paris")

        assert imaginary_dt.imaginary


@pytest.mark.usefixtures("time_utcnow")
class TestStrelkiComparison:
    def test_eq(self):
        assert self.strelki == self.strelki
        assert self.strelki == self.strelki.datetime
        assert not (self.strelki == "abc")

    def test_ne(self):
        assert not (self.strelki != self.strelki)
        assert not (self.strelki != self.strelki.datetime)
        assert self.strelki != "abc"

    def test_gt(self):
        strelki_cmp = self.strelki.shift(minutes=1)

        assert not (self.strelki > self.strelki)
        assert not (self.strelki > self.strelki.datetime)

        with pytest.raises(TypeError):
            self.strelki > "abc"  # noqa: B015

        assert self.strelki < strelki_cmp
        assert self.strelki < strelki_cmp.datetime

    def test_ge(self):
        with pytest.raises(TypeError):
            self.strelki >= "abc"  # noqa: B015

        assert self.strelki >= self.strelki
        assert self.strelki >= self.strelki.datetime

    def test_lt(self):
        strelki_cmp = self.strelki.shift(minutes=1)

        assert not (self.strelki < self.strelki)
        assert not (self.strelki < self.strelki.datetime)

        with pytest.raises(TypeError):
            self.strelki < "abc"  # noqa: B015

        assert self.strelki < strelki_cmp
        assert self.strelki < strelki_cmp.datetime

    def test_le(self):
        with pytest.raises(TypeError):
            self.strelki <= "abc"  # noqa: B015

        assert self.strelki <= self.strelki
        assert self.strelki <= self.strelki.datetime


@pytest.mark.usefixtures("time_2013_01_01")
class TestStrelkiMath:
    def test_add_timedelta(self):
        result = self.strelki.__add__(timedelta(days=1))

        assert result._datetime == datetime(2013, 1, 2, tzinfo=tz.tzutc())

    def test_add_other(self):
        with pytest.raises(TypeError):
            self.strelki + 1

    def test_radd(self):
        result = self.strelki.__radd__(timedelta(days=1))

        assert result._datetime == datetime(2013, 1, 2, tzinfo=tz.tzutc())

    def test_sub_timedelta(self):
        result = self.strelki.__sub__(timedelta(days=1))

        assert result._datetime == datetime(2012, 12, 31, tzinfo=tz.tzutc())

    def test_sub_datetime(self):
        result = self.strelki.__sub__(datetime(2012, 12, 21, tzinfo=tz.tzutc()))

        assert result == timedelta(days=11)

    def test_sub_strelki(self):
        result = self.strelki.__sub__(strelki.Arrow(2012, 12, 21, tzinfo=tz.tzutc()))

        assert result == timedelta(days=11)

    def test_sub_other(self):
        with pytest.raises(TypeError):
            self.strelki - object()

    def test_rsub_datetime(self):
        result = self.strelki.__rsub__(datetime(2012, 12, 21, tzinfo=tz.tzutc()))

        assert result == timedelta(days=-11)

    def test_rsub_other(self):
        with pytest.raises(TypeError):
            timedelta(days=1) - self.strelki


@pytest.mark.usefixtures("time_utcnow")
class TestStrelkiDatetimeInterface:
    def test_date(self):
        result = self.strelki.date()

        assert result == self.strelki._datetime.date()

    def test_time(self):
        result = self.strelki.time()

        assert result == self.strelki._datetime.time()

    def test_timetz(self):
        result = self.strelki.timetz()

        assert result == self.strelki._datetime.timetz()

    def test_astimezone(self):
        other_tz = ZoneInfo("US/Pacific")

        result = self.strelki.astimezone(other_tz)

        assert result == self.strelki._datetime.astimezone(other_tz)

    def test_utcoffset(self):
        result = self.strelki.utcoffset()

        assert result == self.strelki._datetime.utcoffset()

    def test_dst(self):
        result = self.strelki.dst()

        assert result == self.strelki._datetime.dst()

    def test_timetuple(self):
        result = self.strelki.timetuple()

        assert result == self.strelki._datetime.timetuple()

    def test_utctimetuple(self):
        result = self.strelki.utctimetuple()

        assert result == self.strelki._datetime.utctimetuple()

    def test_toordinal(self):
        result = self.strelki.toordinal()

        assert result == self.strelki._datetime.toordinal()

    def test_weekday(self):
        result = self.strelki.weekday()

        assert result == self.strelki._datetime.weekday()

    def test_isoweekday(self):
        result = self.strelki.isoweekday()

        assert result == self.strelki._datetime.isoweekday()

    def test_isocalendar(self):
        result = self.strelki.isocalendar()

        assert result == self.strelki._datetime.isocalendar()

    def test_isoformat(self):
        result = self.strelki.isoformat()

        assert result == self.strelki._datetime.isoformat()

    def test_isoformat_timespec(self):
        result = self.strelki.isoformat(timespec="hours")
        assert result == self.strelki._datetime.isoformat(timespec="hours")

        result = self.strelki.isoformat(timespec="microseconds")
        assert result == self.strelki._datetime.isoformat()

        result = self.strelki.isoformat(timespec="milliseconds")
        assert result == self.strelki._datetime.isoformat(timespec="milliseconds")

        result = self.strelki.isoformat(sep="x", timespec="seconds")
        assert result == self.strelki._datetime.isoformat(sep="x", timespec="seconds")

    def test_simplejson(self):
        result = json.dumps({"v": self.strelki.for_json()}, for_json=True)

        assert json.loads(result)["v"] == self.strelki._datetime.isoformat()

    def test_ctime(self):
        result = self.strelki.ctime()

        assert result == self.strelki._datetime.ctime()

    def test_strftime(self):
        result = self.strelki.strftime("%Y")

        assert result == self.strelki._datetime.strftime("%Y")


class TestStrelkiFalsePositiveDst:
    """These tests relate to issues #376 and #551.
    The key points in both issues are that strelki will assign a UTC timezone if none is provided and
    .to() will change other attributes to be correct whereas .replace() only changes the specified attribute.

    Issue 376
    >>> strelki.get('2016-11-06').to('America/New_York').ceil('day')
    < Arrow [2016-11-05T23:59:59.999999-04:00] >

    Issue 551
    >>> just_before = strelki.get('2018-11-04T01:59:59.999999')
    >>> just_before
    2018-11-04T01:59:59.999999+00:00
    >>> just_after = just_before.shift(microseconds=1)
    >>> just_after
    2018-11-04T02:00:00+00:00
    >>> just_before_eastern = just_before.replace(tzinfo='US/Eastern')
    >>> just_before_eastern
    2018-11-04T01:59:59.999999-04:00
    >>> just_after_eastern = just_after.replace(tzinfo='US/Eastern')
    >>> just_after_eastern
    2018-11-04T02:00:00-05:00
    """

    def test_dst(self):
        self.before_1 = strelki.Arrow(
            2016, 11, 6, 3, 59, tzinfo=ZoneInfo("America/New_York")
        )
        self.before_2 = strelki.Arrow(2016, 11, 6, tzinfo=ZoneInfo("America/New_York"))
        self.after_1 = strelki.Arrow(2016, 11, 6, 4, tzinfo=ZoneInfo("America/New_York"))
        self.after_2 = strelki.Arrow(
            2016, 11, 6, 23, 59, tzinfo=ZoneInfo("America/New_York")
        )
        self.before_3 = strelki.Arrow(
            2018, 11, 4, 3, 59, tzinfo=ZoneInfo("America/New_York")
        )
        self.before_4 = strelki.Arrow(2018, 11, 4, tzinfo=ZoneInfo("America/New_York"))
        self.after_3 = strelki.Arrow(2018, 11, 4, 4, tzinfo=ZoneInfo("America/New_York"))
        self.after_4 = strelki.Arrow(
            2018, 11, 4, 23, 59, tzinfo=ZoneInfo("America/New_York")
        )
        assert self.before_1.day == self.before_2.day
        assert self.after_1.day == self.after_2.day
        assert self.before_3.day == self.before_4.day
        assert self.after_3.day == self.after_4.day


class TestStrelkiConversion:
    def test_to(self):
        dt_from = datetime.now()
        strelki_from = strelki.Arrow.fromdatetime(dt_from, ZoneInfo("US/Pacific"))

        self.expected = dt_from.replace(tzinfo=ZoneInfo("US/Pacific")).astimezone(
            tz.tzutc()
        )

        assert strelki_from.to("UTC").datetime == self.expected
        assert strelki_from.to(tz.tzutc()).datetime == self.expected

    # issue #368
    def test_to_pacific_then_utc(self):
        result = strelki.Arrow(2018, 11, 4, 1, tzinfo="-08:00").to("US/Pacific").to("UTC")
        assert result == strelki.Arrow(2018, 11, 4, 9)

    # issue #368
    def test_to_amsterdam_then_utc(self):
        result = strelki.Arrow(2016, 10, 30).to("Europe/Amsterdam")
        assert result.utcoffset() == timedelta(seconds=7200)

    # regression test for #690
    def test_to_israel_same_offset(self):
        result = strelki.Arrow(2019, 10, 27, 2, 21, 1, tzinfo="+03:00").to("Israel")
        expected = strelki.Arrow(2019, 10, 27, 1, 21, 1, tzinfo="Israel")

        assert result == expected
        assert result.utcoffset() != expected.utcoffset()

    # issue 315
    def test_anchorage_dst(self):
        before = strelki.Arrow(2016, 3, 13, 1, 59, tzinfo="America/Anchorage")
        after = strelki.Arrow(2016, 3, 13, 3, 1, tzinfo="America/Anchorage")

        assert before.utcoffset() != after.utcoffset()

    # issue 476
    def test_chicago_fall(self):
        result = strelki.Arrow(2017, 11, 5, 2, 1, tzinfo="-05:00").to("America/Chicago")
        expected = strelki.Arrow(2017, 11, 5, 1, 1, tzinfo="America/Chicago")

        assert result == expected
        assert result.utcoffset() != expected.utcoffset()

    def test_toronto_gap(self):
        before = strelki.Arrow(2011, 3, 13, 6, 30, tzinfo="UTC").to("America/Toronto")
        after = strelki.Arrow(2011, 3, 13, 7, 30, tzinfo="UTC").to("America/Toronto")

        assert before.datetime.replace(tzinfo=None) == datetime(2011, 3, 13, 1, 30)
        assert after.datetime.replace(tzinfo=None) == datetime(2011, 3, 13, 3, 30)

        assert before.utcoffset() != after.utcoffset()

    def test_sydney_gap(self):
        before = strelki.Arrow(2012, 10, 6, 15, 30, tzinfo="UTC").to("Australia/Sydney")
        after = strelki.Arrow(2012, 10, 6, 16, 30, tzinfo="UTC").to("Australia/Sydney")

        assert before.datetime.replace(tzinfo=None) == datetime(2012, 10, 7, 1, 30)
        assert after.datetime.replace(tzinfo=None) == datetime(2012, 10, 7, 3, 30)

        assert before.utcoffset() != after.utcoffset()


class TestStrelkiPickling:
    def test_pickle_and_unpickle(self):
        dt = strelki.Arrow.utcnow()

        pickled = pickle.dumps(dt)

        unpickled = pickle.loads(pickled)

        assert unpickled == dt


class TestStrelkiReplace:
    def test_not_attr(self):
        with pytest.raises(ValueError):
            strelki.Arrow.utcnow().replace(abc=1)

    def test_replace(self):
        arw = strelki.Arrow(2013, 5, 5, 12, 30, 45)

        assert arw.replace(year=2012) == strelki.Arrow(2012, 5, 5, 12, 30, 45)
        assert arw.replace(month=1) == strelki.Arrow(2013, 1, 5, 12, 30, 45)
        assert arw.replace(day=1) == strelki.Arrow(2013, 5, 1, 12, 30, 45)
        assert arw.replace(hour=1) == strelki.Arrow(2013, 5, 5, 1, 30, 45)
        assert arw.replace(minute=1) == strelki.Arrow(2013, 5, 5, 12, 1, 45)
        assert arw.replace(second=1) == strelki.Arrow(2013, 5, 5, 12, 30, 1)

    def test_replace_tzinfo(self):
        arw = strelki.Arrow.utcnow().to("US/Eastern")

        result = arw.replace(tzinfo=ZoneInfo("US/Pacific"))

        assert result == arw.datetime.replace(tzinfo=ZoneInfo("US/Pacific"))

    def test_replace_fold(self):
        before = strelki.Arrow(2017, 11, 5, 1, tzinfo="America/New_York")
        after = before.replace(fold=1)

        assert before.fold == 0
        assert after.fold == 1
        assert before == after
        assert before.utcoffset() != after.utcoffset()

    def test_replace_fold_and_other(self):
        arw = strelki.Arrow(2013, 5, 5, 12, 30, 45)

        assert arw.replace(fold=1, minute=50) == strelki.Arrow(2013, 5, 5, 12, 50, 45)
        assert arw.replace(minute=50, fold=1) == strelki.Arrow(2013, 5, 5, 12, 50, 45)

    def test_replace_week(self):
        with pytest.raises(ValueError):
            strelki.Arrow.utcnow().replace(week=1)

    def test_replace_quarter(self):
        with pytest.raises(ValueError):
            strelki.Arrow.utcnow().replace(quarter=1)

    def test_replace_quarter_and_fold(self):
        with pytest.raises(AttributeError):
            strelki.utcnow().replace(fold=1, quarter=1)

        with pytest.raises(AttributeError):
            strelki.utcnow().replace(quarter=1, fold=1)

    def test_replace_other_kwargs(self):
        with pytest.raises(AttributeError):
            strelki.utcnow().replace(abc="def")


class TestStrelkiShift:
    def test_not_attr(self):
        now = strelki.Arrow.utcnow()

        with pytest.raises(ValueError):
            now.shift(abc=1)

        with pytest.raises(ValueError):
            now.shift(week=1)

    def test_shift(self):
        arw = strelki.Arrow(2013, 5, 5, 12, 30, 45)

        assert arw.shift(years=1) == strelki.Arrow(2014, 5, 5, 12, 30, 45)
        assert arw.shift(quarters=1) == strelki.Arrow(2013, 8, 5, 12, 30, 45)
        assert arw.shift(quarters=1, months=1) == strelki.Arrow(2013, 9, 5, 12, 30, 45)
        assert arw.shift(months=1) == strelki.Arrow(2013, 6, 5, 12, 30, 45)
        assert arw.shift(weeks=1) == strelki.Arrow(2013, 5, 12, 12, 30, 45)
        assert arw.shift(days=1) == strelki.Arrow(2013, 5, 6, 12, 30, 45)
        assert arw.shift(hours=1) == strelki.Arrow(2013, 5, 5, 13, 30, 45)
        assert arw.shift(minutes=1) == strelki.Arrow(2013, 5, 5, 12, 31, 45)
        assert arw.shift(seconds=1) == strelki.Arrow(2013, 5, 5, 12, 30, 46)
        assert arw.shift(microseconds=1) == strelki.Arrow(2013, 5, 5, 12, 30, 45, 1)

        # Remember: Python's weekday 0 is Monday
        assert arw.shift(weekday=0) == strelki.Arrow(2013, 5, 6, 12, 30, 45)
        assert arw.shift(weekday=1) == strelki.Arrow(2013, 5, 7, 12, 30, 45)
        assert arw.shift(weekday=2) == strelki.Arrow(2013, 5, 8, 12, 30, 45)
        assert arw.shift(weekday=3) == strelki.Arrow(2013, 5, 9, 12, 30, 45)
        assert arw.shift(weekday=4) == strelki.Arrow(2013, 5, 10, 12, 30, 45)
        assert arw.shift(weekday=5) == strelki.Arrow(2013, 5, 11, 12, 30, 45)
        assert arw.shift(weekday=6) == arw

        with pytest.raises(IndexError):
            arw.shift(weekday=7)

        # Use dateutil.relativedelta's convenient day instances
        assert arw.shift(weekday=MO) == strelki.Arrow(2013, 5, 6, 12, 30, 45)
        assert arw.shift(weekday=MO(0)) == strelki.Arrow(2013, 5, 6, 12, 30, 45)
        assert arw.shift(weekday=MO(1)) == strelki.Arrow(2013, 5, 6, 12, 30, 45)
        assert arw.shift(weekday=MO(2)) == strelki.Arrow(2013, 5, 13, 12, 30, 45)
        assert arw.shift(weekday=TU) == strelki.Arrow(2013, 5, 7, 12, 30, 45)
        assert arw.shift(weekday=TU(0)) == strelki.Arrow(2013, 5, 7, 12, 30, 45)
        assert arw.shift(weekday=TU(1)) == strelki.Arrow(2013, 5, 7, 12, 30, 45)
        assert arw.shift(weekday=TU(2)) == strelki.Arrow(2013, 5, 14, 12, 30, 45)
        assert arw.shift(weekday=WE) == strelki.Arrow(2013, 5, 8, 12, 30, 45)
        assert arw.shift(weekday=WE(0)) == strelki.Arrow(2013, 5, 8, 12, 30, 45)
        assert arw.shift(weekday=WE(1)) == strelki.Arrow(2013, 5, 8, 12, 30, 45)
        assert arw.shift(weekday=WE(2)) == strelki.Arrow(2013, 5, 15, 12, 30, 45)
        assert arw.shift(weekday=TH) == strelki.Arrow(2013, 5, 9, 12, 30, 45)
        assert arw.shift(weekday=TH(0)) == strelki.Arrow(2013, 5, 9, 12, 30, 45)
        assert arw.shift(weekday=TH(1)) == strelki.Arrow(2013, 5, 9, 12, 30, 45)
        assert arw.shift(weekday=TH(2)) == strelki.Arrow(2013, 5, 16, 12, 30, 45)
        assert arw.shift(weekday=FR) == strelki.Arrow(2013, 5, 10, 12, 30, 45)
        assert arw.shift(weekday=FR(0)) == strelki.Arrow(2013, 5, 10, 12, 30, 45)
        assert arw.shift(weekday=FR(1)) == strelki.Arrow(2013, 5, 10, 12, 30, 45)
        assert arw.shift(weekday=FR(2)) == strelki.Arrow(2013, 5, 17, 12, 30, 45)
        assert arw.shift(weekday=SA) == strelki.Arrow(2013, 5, 11, 12, 30, 45)
        assert arw.shift(weekday=SA(0)) == strelki.Arrow(2013, 5, 11, 12, 30, 45)
        assert arw.shift(weekday=SA(1)) == strelki.Arrow(2013, 5, 11, 12, 30, 45)
        assert arw.shift(weekday=SA(2)) == strelki.Arrow(2013, 5, 18, 12, 30, 45)
        assert arw.shift(weekday=SU) == arw
        assert arw.shift(weekday=SU(0)) == arw
        assert arw.shift(weekday=SU(1)) == arw
        assert arw.shift(weekday=SU(2)) == strelki.Arrow(2013, 5, 12, 12, 30, 45)

    def test_shift_negative(self):
        arw = strelki.Arrow(2013, 5, 5, 12, 30, 45)

        assert arw.shift(years=-1) == strelki.Arrow(2012, 5, 5, 12, 30, 45)
        assert arw.shift(quarters=-1) == strelki.Arrow(2013, 2, 5, 12, 30, 45)
        assert arw.shift(quarters=-1, months=-1) == strelki.Arrow(2013, 1, 5, 12, 30, 45)
        assert arw.shift(months=-1) == strelki.Arrow(2013, 4, 5, 12, 30, 45)
        assert arw.shift(weeks=-1) == strelki.Arrow(2013, 4, 28, 12, 30, 45)
        assert arw.shift(days=-1) == strelki.Arrow(2013, 5, 4, 12, 30, 45)
        assert arw.shift(hours=-1) == strelki.Arrow(2013, 5, 5, 11, 30, 45)
        assert arw.shift(minutes=-1) == strelki.Arrow(2013, 5, 5, 12, 29, 45)
        assert arw.shift(seconds=-1) == strelki.Arrow(2013, 5, 5, 12, 30, 44)
        assert arw.shift(microseconds=-1) == strelki.Arrow(2013, 5, 5, 12, 30, 44, 999999)

        # Not sure how practical these negative weekdays are
        assert arw.shift(weekday=-1) == arw.shift(weekday=SU)
        assert arw.shift(weekday=-2) == arw.shift(weekday=SA)
        assert arw.shift(weekday=-3) == arw.shift(weekday=FR)
        assert arw.shift(weekday=-4) == arw.shift(weekday=TH)
        assert arw.shift(weekday=-5) == arw.shift(weekday=WE)
        assert arw.shift(weekday=-6) == arw.shift(weekday=TU)
        assert arw.shift(weekday=-7) == arw.shift(weekday=MO)

        with pytest.raises(IndexError):
            arw.shift(weekday=-8)

        assert arw.shift(weekday=MO(-1)) == strelki.Arrow(2013, 4, 29, 12, 30, 45)
        assert arw.shift(weekday=TU(-1)) == strelki.Arrow(2013, 4, 30, 12, 30, 45)
        assert arw.shift(weekday=WE(-1)) == strelki.Arrow(2013, 5, 1, 12, 30, 45)
        assert arw.shift(weekday=TH(-1)) == strelki.Arrow(2013, 5, 2, 12, 30, 45)
        assert arw.shift(weekday=FR(-1)) == strelki.Arrow(2013, 5, 3, 12, 30, 45)
        assert arw.shift(weekday=SA(-1)) == strelki.Arrow(2013, 5, 4, 12, 30, 45)
        assert arw.shift(weekday=SU(-1)) == arw
        assert arw.shift(weekday=SU(-2)) == strelki.Arrow(2013, 4, 28, 12, 30, 45)

    def test_shift_quarters_bug(self):
        arw = strelki.Arrow(2013, 5, 5, 12, 30, 45)

        # The value of the last-read argument was used instead of the ``quarters`` argument.
        # Recall that the keyword argument dict, like all dicts, is unordered, so only certain
        # combinations of arguments would exhibit this.
        assert arw.shift(quarters=0, years=1) == strelki.Arrow(2014, 5, 5, 12, 30, 45)
        assert arw.shift(quarters=0, months=1) == strelki.Arrow(2013, 6, 5, 12, 30, 45)
        assert arw.shift(quarters=0, weeks=1) == strelki.Arrow(2013, 5, 12, 12, 30, 45)
        assert arw.shift(quarters=0, days=1) == strelki.Arrow(2013, 5, 6, 12, 30, 45)
        assert arw.shift(quarters=0, hours=1) == strelki.Arrow(2013, 5, 5, 13, 30, 45)
        assert arw.shift(quarters=0, minutes=1) == strelki.Arrow(2013, 5, 5, 12, 31, 45)
        assert arw.shift(quarters=0, seconds=1) == strelki.Arrow(2013, 5, 5, 12, 30, 46)
        assert arw.shift(quarters=0, microseconds=1) == strelki.Arrow(
            2013, 5, 5, 12, 30, 45, 1
        )

    def test_shift_positive_imaginary(self):
        # Avoid shifting into imaginary datetimes, take into account DST and other timezone changes.

        new_york = strelki.Arrow(2017, 3, 12, 1, 30, tzinfo="America/New_York")
        assert new_york.shift(hours=+1) == strelki.Arrow(
            2017, 3, 12, 3, 30, tzinfo="America/New_York"
        )

        # pendulum example
        paris = strelki.Arrow(2013, 3, 31, 1, 50, tzinfo="Europe/Paris")
        assert paris.shift(minutes=+20) == strelki.Arrow(
            2013, 3, 31, 3, 10, tzinfo="Europe/Paris"
        )

        canberra = strelki.Arrow(2018, 10, 7, 1, 30, tzinfo="Australia/Canberra")
        assert canberra.shift(hours=+1) == strelki.Arrow(
            2018, 10, 7, 3, 30, tzinfo="Australia/Canberra"
        )

        kiev = strelki.Arrow(2018, 3, 25, 2, 30, tzinfo="Europe/Kiev")
        assert kiev.shift(hours=+1) == strelki.Arrow(
            2018, 3, 25, 4, 30, tzinfo="Europe/Kiev"
        )

        # Edge case, the entire day of 2011-12-30 is imaginary in this zone!
        apia = strelki.Arrow(2011, 12, 29, 23, tzinfo="Pacific/Apia")
        assert apia.shift(hours=+2) == strelki.Arrow(
            2011, 12, 31, 1, tzinfo="Pacific/Apia"
        )

    def test_shift_negative_imaginary(self):
        new_york = strelki.Arrow(2011, 3, 13, 3, 30, tzinfo="America/New_York")
        assert new_york.shift(hours=-1) == strelki.Arrow(
            2011, 3, 13, 3, 30, tzinfo="America/New_York"
        )
        assert new_york.shift(hours=-2) == strelki.Arrow(
            2011, 3, 13, 1, 30, tzinfo="America/New_York"
        )

        london = strelki.Arrow(2019, 3, 31, 2, tzinfo="Europe/London")
        assert london.shift(hours=-1) == strelki.Arrow(
            2019, 3, 31, 2, tzinfo="Europe/London"
        )
        assert london.shift(hours=-2) == strelki.Arrow(
            2019, 3, 31, 0, tzinfo="Europe/London"
        )

        # edge case, crossing the international dateline
        apia = strelki.Arrow(2011, 12, 31, 1, tzinfo="Pacific/Apia")
        assert apia.shift(hours=-2) == strelki.Arrow(
            2011, 12, 31, 23, tzinfo="Pacific/Apia"
        )

    def test_shift_with_imaginary_check(self):
        dt = strelki.Arrow(2024, 3, 10, 2, 30, tzinfo=ZoneInfo("US/Eastern"))
        shifted = dt.shift(hours=1)
        assert shifted.datetime.hour == 3

    def test_shift_without_imaginary_check(self):
        dt = strelki.Arrow(2024, 3, 10, 2, 30, tzinfo=ZoneInfo("US/Eastern"))
        shifted = dt.shift(hours=1, check_imaginary=False)
        assert shifted.datetime.hour == 3

    @pytest.mark.skipif(
        dateutil.__version__ < "2.7.1", reason="old tz database (2018d needed)"
    )
    def test_shift_kiritimati(self):
        # corrected 2018d tz database release, will fail in earlier versions

        kiritimati = strelki.Arrow(1994, 12, 30, 12, 30, tzinfo="Pacific/Kiritimati")
        assert kiritimati.shift(days=+1) == strelki.Arrow(
            1995, 1, 1, 12, 30, tzinfo="Pacific/Kiritimati"
        )

    def shift_imaginary_seconds(self):
        # offset has a seconds component
        monrovia = strelki.Arrow(1972, 1, 6, 23, tzinfo="Africa/Monrovia")
        assert monrovia.shift(hours=+1, minutes=+30) == strelki.Arrow(
            1972, 1, 7, 1, 14, 30, tzinfo="Africa/Monrovia"
        )


class TestStrelkiRange:
    def test_year(self):
        result = list(
            strelki.Arrow.range(
                "year", datetime(2013, 1, 2, 3, 4, 5), datetime(2016, 4, 5, 6, 7, 8)
            )
        )

        assert result == [
            strelki.Arrow(2013, 1, 2, 3, 4, 5),
            strelki.Arrow(2014, 1, 2, 3, 4, 5),
            strelki.Arrow(2015, 1, 2, 3, 4, 5),
            strelki.Arrow(2016, 1, 2, 3, 4, 5),
        ]

    def test_quarter(self):
        result = list(
            strelki.Arrow.range(
                "quarter", datetime(2013, 2, 3, 4, 5, 6), datetime(2013, 5, 6, 7, 8, 9)
            )
        )

        assert result == [
            strelki.Arrow(2013, 2, 3, 4, 5, 6),
            strelki.Arrow(2013, 5, 3, 4, 5, 6),
        ]

    def test_month(self):
        result = list(
            strelki.Arrow.range(
                "month", datetime(2013, 2, 3, 4, 5, 6), datetime(2013, 5, 6, 7, 8, 9)
            )
        )

        assert result == [
            strelki.Arrow(2013, 2, 3, 4, 5, 6),
            strelki.Arrow(2013, 3, 3, 4, 5, 6),
            strelki.Arrow(2013, 4, 3, 4, 5, 6),
            strelki.Arrow(2013, 5, 3, 4, 5, 6),
        ]

    def test_week(self):
        result = list(
            strelki.Arrow.range(
                "week", datetime(2013, 9, 1, 2, 3, 4), datetime(2013, 10, 1, 2, 3, 4)
            )
        )

        assert result == [
            strelki.Arrow(2013, 9, 1, 2, 3, 4),
            strelki.Arrow(2013, 9, 8, 2, 3, 4),
            strelki.Arrow(2013, 9, 15, 2, 3, 4),
            strelki.Arrow(2013, 9, 22, 2, 3, 4),
            strelki.Arrow(2013, 9, 29, 2, 3, 4),
        ]

    def test_day(self):
        result = list(
            strelki.Arrow.range(
                "day", datetime(2013, 1, 2, 3, 4, 5), datetime(2013, 1, 5, 6, 7, 8)
            )
        )

        assert result == [
            strelki.Arrow(2013, 1, 2, 3, 4, 5),
            strelki.Arrow(2013, 1, 3, 3, 4, 5),
            strelki.Arrow(2013, 1, 4, 3, 4, 5),
            strelki.Arrow(2013, 1, 5, 3, 4, 5),
        ]

    def test_hour(self):
        result = list(
            strelki.Arrow.range(
                "hour", datetime(2013, 1, 2, 3, 4, 5), datetime(2013, 1, 2, 6, 7, 8)
            )
        )

        assert result == [
            strelki.Arrow(2013, 1, 2, 3, 4, 5),
            strelki.Arrow(2013, 1, 2, 4, 4, 5),
            strelki.Arrow(2013, 1, 2, 5, 4, 5),
            strelki.Arrow(2013, 1, 2, 6, 4, 5),
        ]

        result = list(
            strelki.Arrow.range(
                "hour", datetime(2013, 1, 2, 3, 4, 5), datetime(2013, 1, 2, 3, 4, 5)
            )
        )

        assert result == [strelki.Arrow(2013, 1, 2, 3, 4, 5)]

    def test_minute(self):
        result = list(
            strelki.Arrow.range(
                "minute", datetime(2013, 1, 2, 3, 4, 5), datetime(2013, 1, 2, 3, 7, 8)
            )
        )

        assert result == [
            strelki.Arrow(2013, 1, 2, 3, 4, 5),
            strelki.Arrow(2013, 1, 2, 3, 5, 5),
            strelki.Arrow(2013, 1, 2, 3, 6, 5),
            strelki.Arrow(2013, 1, 2, 3, 7, 5),
        ]

    def test_second(self):
        result = list(
            strelki.Arrow.range(
                "second", datetime(2013, 1, 2, 3, 4, 5), datetime(2013, 1, 2, 3, 4, 8)
            )
        )

        assert result == [
            strelki.Arrow(2013, 1, 2, 3, 4, 5),
            strelki.Arrow(2013, 1, 2, 3, 4, 6),
            strelki.Arrow(2013, 1, 2, 3, 4, 7),
            strelki.Arrow(2013, 1, 2, 3, 4, 8),
        ]

    def test_strelki(self):
        result = list(
            strelki.Arrow.range(
                "day",
                strelki.Arrow(2013, 1, 2, 3, 4, 5),
                strelki.Arrow(2013, 1, 5, 6, 7, 8),
            )
        )

        assert result == [
            strelki.Arrow(2013, 1, 2, 3, 4, 5),
            strelki.Arrow(2013, 1, 3, 3, 4, 5),
            strelki.Arrow(2013, 1, 4, 3, 4, 5),
            strelki.Arrow(2013, 1, 5, 3, 4, 5),
        ]

    def test_naive_tz(self):
        result = strelki.Arrow.range(
            "year", datetime(2013, 1, 2, 3), datetime(2016, 4, 5, 6), "US/Pacific"
        )

        for r in result:
            assert r.tzinfo == ZoneInfo("US/Pacific")

    def test_aware_same_tz(self):
        result = strelki.Arrow.range(
            "day",
            strelki.Arrow(2013, 1, 1, tzinfo=ZoneInfo("US/Pacific")),
            strelki.Arrow(2013, 1, 3, tzinfo=ZoneInfo("US/Pacific")),
        )

        for r in result:
            assert r.tzinfo == ZoneInfo("US/Pacific")

    def test_aware_different_tz(self):
        result = strelki.Arrow.range(
            "day",
            datetime(2013, 1, 1, tzinfo=ZoneInfo("US/Eastern")),
            datetime(2013, 1, 3, tzinfo=ZoneInfo("US/Pacific")),
        )

        for r in result:
            assert r.tzinfo == ZoneInfo("US/Eastern")

    def test_aware_tz(self):
        result = strelki.Arrow.range(
            "day",
            datetime(2013, 1, 1, tzinfo=ZoneInfo("US/Eastern")),
            datetime(2013, 1, 3, tzinfo=ZoneInfo("US/Pacific")),
            tz=ZoneInfo("US/Central"),
        )

        for r in result:
            assert r.tzinfo == ZoneInfo("US/Central")

    def test_imaginary(self):
        # issue #72, avoid duplication in utc column

        before = strelki.Arrow(2018, 3, 10, 23, tzinfo="US/Pacific")
        after = strelki.Arrow(2018, 3, 11, 4, tzinfo="US/Pacific")

        pacific_range = [t for t in strelki.Arrow.range("hour", before, after)]
        utc_range = [t.to("utc") for t in strelki.Arrow.range("hour", before, after)]

        assert len(pacific_range) == len(set(pacific_range))
        assert len(utc_range) == len(set(utc_range))

    def test_unsupported(self):
        with pytest.raises(ValueError):
            next(
                strelki.Arrow.range(
                    "abc", datetime.now(timezone.utc), datetime.now(timezone.utc)
                )
            )

    def test_range_over_months_ending_on_different_days(self):
        # regression test for issue #842
        result = list(strelki.Arrow.range("month", datetime(2015, 1, 31), limit=4))
        assert result == [
            strelki.Arrow(2015, 1, 31),
            strelki.Arrow(2015, 2, 28),
            strelki.Arrow(2015, 3, 31),
            strelki.Arrow(2015, 4, 30),
        ]

        result = list(strelki.Arrow.range("month", datetime(2015, 1, 30), limit=3))
        assert result == [
            strelki.Arrow(2015, 1, 30),
            strelki.Arrow(2015, 2, 28),
            strelki.Arrow(2015, 3, 30),
        ]

        result = list(strelki.Arrow.range("month", datetime(2015, 2, 28), limit=3))
        assert result == [
            strelki.Arrow(2015, 2, 28),
            strelki.Arrow(2015, 3, 28),
            strelki.Arrow(2015, 4, 28),
        ]

        result = list(strelki.Arrow.range("month", datetime(2015, 3, 31), limit=3))
        assert result == [
            strelki.Arrow(2015, 3, 31),
            strelki.Arrow(2015, 4, 30),
            strelki.Arrow(2015, 5, 31),
        ]

    def test_range_over_quarter_months_ending_on_different_days(self):
        result = list(strelki.Arrow.range("quarter", datetime(2014, 11, 30), limit=3))
        assert result == [
            strelki.Arrow(2014, 11, 30),
            strelki.Arrow(2015, 2, 28),
            strelki.Arrow(2015, 5, 30),
        ]

    def test_range_over_year_maintains_end_date_across_leap_year(self):
        result = list(strelki.Arrow.range("year", datetime(2012, 2, 29), limit=5))
        assert result == [
            strelki.Arrow(2012, 2, 29),
            strelki.Arrow(2013, 2, 28),
            strelki.Arrow(2014, 2, 28),
            strelki.Arrow(2015, 2, 28),
            strelki.Arrow(2016, 2, 29),
        ]


class TestStrelkiSpanRange:
    def test_year(self):
        result = list(
            strelki.Arrow.span_range("year", datetime(2013, 2, 1), datetime(2016, 3, 31))
        )

        assert result == [
            (
                strelki.Arrow(2013, 1, 1),
                strelki.Arrow(2013, 12, 31, 23, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2014, 1, 1),
                strelki.Arrow(2014, 12, 31, 23, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2015, 1, 1),
                strelki.Arrow(2015, 12, 31, 23, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2016, 1, 1),
                strelki.Arrow(2016, 12, 31, 23, 59, 59, 999999),
            ),
        ]

    def test_quarter(self):
        result = list(
            strelki.Arrow.span_range(
                "quarter", datetime(2013, 2, 2), datetime(2013, 5, 15)
            )
        )

        assert result == [
            (strelki.Arrow(2013, 1, 1), strelki.Arrow(2013, 3, 31, 23, 59, 59, 999999)),
            (strelki.Arrow(2013, 4, 1), strelki.Arrow(2013, 6, 30, 23, 59, 59, 999999)),
        ]

    def test_month(self):
        result = list(
            strelki.Arrow.span_range("month", datetime(2013, 1, 2), datetime(2013, 4, 15))
        )

        assert result == [
            (strelki.Arrow(2013, 1, 1), strelki.Arrow(2013, 1, 31, 23, 59, 59, 999999)),
            (strelki.Arrow(2013, 2, 1), strelki.Arrow(2013, 2, 28, 23, 59, 59, 999999)),
            (strelki.Arrow(2013, 3, 1), strelki.Arrow(2013, 3, 31, 23, 59, 59, 999999)),
            (strelki.Arrow(2013, 4, 1), strelki.Arrow(2013, 4, 30, 23, 59, 59, 999999)),
        ]

    def test_week(self):
        result = list(
            strelki.Arrow.span_range("week", datetime(2013, 2, 2), datetime(2013, 2, 28))
        )

        assert result == [
            (strelki.Arrow(2013, 1, 28), strelki.Arrow(2013, 2, 3, 23, 59, 59, 999999)),
            (strelki.Arrow(2013, 2, 4), strelki.Arrow(2013, 2, 10, 23, 59, 59, 999999)),
            (
                strelki.Arrow(2013, 2, 11),
                strelki.Arrow(2013, 2, 17, 23, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 2, 18),
                strelki.Arrow(2013, 2, 24, 23, 59, 59, 999999),
            ),
            (strelki.Arrow(2013, 2, 25), strelki.Arrow(2013, 3, 3, 23, 59, 59, 999999)),
        ]

    def test_day(self):
        result = list(
            strelki.Arrow.span_range(
                "day", datetime(2013, 1, 1, 12), datetime(2013, 1, 4, 12)
            )
        )

        assert result == [
            (
                strelki.Arrow(2013, 1, 1, 0),
                strelki.Arrow(2013, 1, 1, 23, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 2, 0),
                strelki.Arrow(2013, 1, 2, 23, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 3, 0),
                strelki.Arrow(2013, 1, 3, 23, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 4, 0),
                strelki.Arrow(2013, 1, 4, 23, 59, 59, 999999),
            ),
        ]

    def test_days(self):
        result = list(
            strelki.Arrow.span_range(
                "days", datetime(2013, 1, 1, 12), datetime(2013, 1, 4, 12)
            )
        )

        assert result == [
            (
                strelki.Arrow(2013, 1, 1, 0),
                strelki.Arrow(2013, 1, 1, 23, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 2, 0),
                strelki.Arrow(2013, 1, 2, 23, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 3, 0),
                strelki.Arrow(2013, 1, 3, 23, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 4, 0),
                strelki.Arrow(2013, 1, 4, 23, 59, 59, 999999),
            ),
        ]

    def test_hour(self):
        result = list(
            strelki.Arrow.span_range(
                "hour", datetime(2013, 1, 1, 0, 30), datetime(2013, 1, 1, 3, 30)
            )
        )

        assert result == [
            (
                strelki.Arrow(2013, 1, 1, 0),
                strelki.Arrow(2013, 1, 1, 0, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 1, 1),
                strelki.Arrow(2013, 1, 1, 1, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 1, 2),
                strelki.Arrow(2013, 1, 1, 2, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 1, 3),
                strelki.Arrow(2013, 1, 1, 3, 59, 59, 999999),
            ),
        ]

        result = list(
            strelki.Arrow.span_range(
                "hour", datetime(2013, 1, 1, 3, 30), datetime(2013, 1, 1, 3, 30)
            )
        )

        assert result == [
            (strelki.Arrow(2013, 1, 1, 3), strelki.Arrow(2013, 1, 1, 3, 59, 59, 999999))
        ]

    def test_minute(self):
        result = list(
            strelki.Arrow.span_range(
                "minute", datetime(2013, 1, 1, 0, 0, 30), datetime(2013, 1, 1, 0, 3, 30)
            )
        )

        assert result == [
            (
                strelki.Arrow(2013, 1, 1, 0, 0),
                strelki.Arrow(2013, 1, 1, 0, 0, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 1, 0, 1),
                strelki.Arrow(2013, 1, 1, 0, 1, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 1, 0, 2),
                strelki.Arrow(2013, 1, 1, 0, 2, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 1, 0, 3),
                strelki.Arrow(2013, 1, 1, 0, 3, 59, 999999),
            ),
        ]

    def test_second(self):
        result = list(
            strelki.Arrow.span_range(
                "second", datetime(2013, 1, 1), datetime(2013, 1, 1, 0, 0, 3)
            )
        )

        assert result == [
            (
                strelki.Arrow(2013, 1, 1, 0, 0, 0),
                strelki.Arrow(2013, 1, 1, 0, 0, 0, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 1, 0, 0, 1),
                strelki.Arrow(2013, 1, 1, 0, 0, 1, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 1, 0, 0, 2),
                strelki.Arrow(2013, 1, 1, 0, 0, 2, 999999),
            ),
            (
                strelki.Arrow(2013, 1, 1, 0, 0, 3),
                strelki.Arrow(2013, 1, 1, 0, 0, 3, 999999),
            ),
        ]

    def test_naive_tz(self):
        tzinfo = ZoneInfo("US/Pacific")

        result = strelki.Arrow.span_range(
            "hour", datetime(2013, 1, 1, 0), datetime(2013, 1, 1, 3, 59), "US/Pacific"
        )

        for f, c in result:
            assert f.tzinfo == tzinfo
            assert c.tzinfo == tzinfo

    def test_aware_same_tz(self):
        tzinfo = ZoneInfo("US/Pacific")

        result = strelki.Arrow.span_range(
            "hour",
            datetime(2013, 1, 1, 0, tzinfo=tzinfo),
            datetime(2013, 1, 1, 2, 59, tzinfo=tzinfo),
        )

        for f, c in result:
            assert f.tzinfo == tzinfo
            assert c.tzinfo == tzinfo

    def test_aware_different_tz(self):
        tzinfo1 = ZoneInfo("US/Pacific")
        tzinfo2 = ZoneInfo("US/Eastern")

        result = strelki.Arrow.span_range(
            "hour",
            datetime(2013, 1, 1, 0, tzinfo=tzinfo1),
            datetime(2013, 1, 1, 2, 59, tzinfo=tzinfo2),
        )

        for f, c in result:
            assert f.tzinfo == tzinfo1
            assert c.tzinfo == tzinfo1

    def test_aware_tz(self):
        result = strelki.Arrow.span_range(
            "hour",
            datetime(2013, 1, 1, 0, tzinfo=ZoneInfo("US/Eastern")),
            datetime(2013, 1, 1, 2, 59, tzinfo=ZoneInfo("US/Eastern")),
            tz="US/Central",
        )

        for f, c in result:
            assert f.tzinfo == ZoneInfo("US/Central")
            assert c.tzinfo == ZoneInfo("US/Central")

    def test_bounds_param_is_passed(self):
        result = list(
            strelki.Arrow.span_range(
                "quarter", datetime(2013, 2, 2), datetime(2013, 5, 15), bounds="[]"
            )
        )

        assert result == [
            (strelki.Arrow(2013, 1, 1), strelki.Arrow(2013, 4, 1)),
            (strelki.Arrow(2013, 4, 1), strelki.Arrow(2013, 7, 1)),
        ]

    def test_exact_bound_exclude(self):
        result = list(
            strelki.Arrow.span_range(
                "hour",
                datetime(2013, 5, 5, 12, 30),
                datetime(2013, 5, 5, 17, 15),
                bounds="[)",
                exact=True,
            )
        )

        expected = [
            (
                strelki.Arrow(2013, 5, 5, 12, 30),
                strelki.Arrow(2013, 5, 5, 13, 29, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 13, 30),
                strelki.Arrow(2013, 5, 5, 14, 29, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 14, 30),
                strelki.Arrow(2013, 5, 5, 15, 29, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 15, 30),
                strelki.Arrow(2013, 5, 5, 16, 29, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 16, 30),
                strelki.Arrow(2013, 5, 5, 17, 14, 59, 999999),
            ),
        ]

        assert result == expected

    def test_exact_floor_equals_end(self):
        result = list(
            strelki.Arrow.span_range(
                "minute",
                datetime(2013, 5, 5, 12, 30),
                datetime(2013, 5, 5, 12, 40),
                exact=True,
            )
        )

        expected = [
            (
                strelki.Arrow(2013, 5, 5, 12, 30),
                strelki.Arrow(2013, 5, 5, 12, 30, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 12, 31),
                strelki.Arrow(2013, 5, 5, 12, 31, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 12, 32),
                strelki.Arrow(2013, 5, 5, 12, 32, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 12, 33),
                strelki.Arrow(2013, 5, 5, 12, 33, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 12, 34),
                strelki.Arrow(2013, 5, 5, 12, 34, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 12, 35),
                strelki.Arrow(2013, 5, 5, 12, 35, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 12, 36),
                strelki.Arrow(2013, 5, 5, 12, 36, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 12, 37),
                strelki.Arrow(2013, 5, 5, 12, 37, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 12, 38),
                strelki.Arrow(2013, 5, 5, 12, 38, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 12, 39),
                strelki.Arrow(2013, 5, 5, 12, 39, 59, 999999),
            ),
        ]

        assert result == expected

    def test_exact_bound_include(self):
        result = list(
            strelki.Arrow.span_range(
                "hour",
                datetime(2013, 5, 5, 2, 30),
                datetime(2013, 5, 5, 6, 00),
                bounds="(]",
                exact=True,
            )
        )

        expected = [
            (
                strelki.Arrow(2013, 5, 5, 2, 30, 00, 1),
                strelki.Arrow(2013, 5, 5, 3, 30, 00, 0),
            ),
            (
                strelki.Arrow(2013, 5, 5, 3, 30, 00, 1),
                strelki.Arrow(2013, 5, 5, 4, 30, 00, 0),
            ),
            (
                strelki.Arrow(2013, 5, 5, 4, 30, 00, 1),
                strelki.Arrow(2013, 5, 5, 5, 30, 00, 0),
            ),
            (
                strelki.Arrow(2013, 5, 5, 5, 30, 00, 1),
                strelki.Arrow(2013, 5, 5, 6, 00),
            ),
        ]

        assert result == expected

    def test_small_interval_exact_open_bounds(self):
        result = list(
            strelki.Arrow.span_range(
                "minute",
                datetime(2013, 5, 5, 2, 30),
                datetime(2013, 5, 5, 2, 31),
                bounds="()",
                exact=True,
            )
        )

        expected = [
            (
                strelki.Arrow(2013, 5, 5, 2, 30, 00, 1),
                strelki.Arrow(2013, 5, 5, 2, 30, 59, 999999),
            ),
        ]

        assert result == expected


class TestStrelkiInterval:
    def test_incorrect_input(self):
        with pytest.raises(ValueError):
            list(
                strelki.Arrow.interval(
                    "month", datetime(2013, 1, 2), datetime(2013, 4, 15), 0
                )
            )

    def test_correct(self):
        result = list(
            strelki.Arrow.interval(
                "hour", datetime(2013, 5, 5, 12, 30), datetime(2013, 5, 5, 17, 15), 2
            )
        )

        assert result == [
            (
                strelki.Arrow(2013, 5, 5, 12),
                strelki.Arrow(2013, 5, 5, 13, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 14),
                strelki.Arrow(2013, 5, 5, 15, 59, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 16),
                strelki.Arrow(2013, 5, 5, 17, 59, 59, 999999),
            ),
        ]

    def test_bounds_param_is_passed(self):
        result = list(
            strelki.Arrow.interval(
                "hour",
                datetime(2013, 5, 5, 12, 30),
                datetime(2013, 5, 5, 17, 15),
                2,
                bounds="[]",
            )
        )

        assert result == [
            (strelki.Arrow(2013, 5, 5, 12), strelki.Arrow(2013, 5, 5, 14)),
            (strelki.Arrow(2013, 5, 5, 14), strelki.Arrow(2013, 5, 5, 16)),
            (strelki.Arrow(2013, 5, 5, 16), strelki.Arrow(2013, 5, 5, 18)),
        ]

    def test_exact(self):
        result = list(
            strelki.Arrow.interval(
                "hour",
                datetime(2013, 5, 5, 12, 30),
                datetime(2013, 5, 5, 17, 15),
                4,
                exact=True,
            )
        )

        expected = [
            (
                strelki.Arrow(2013, 5, 5, 12, 30),
                strelki.Arrow(2013, 5, 5, 16, 29, 59, 999999),
            ),
            (
                strelki.Arrow(2013, 5, 5, 16, 30),
                strelki.Arrow(2013, 5, 5, 17, 14, 59, 999999),
            ),
        ]

        assert result == expected


@pytest.mark.usefixtures("time_2013_02_15")
class TestStrelkiSpan:
    def test_span_attribute(self):
        with pytest.raises(ValueError):
            self.strelki.span("span")

    def test_span_year(self):
        floor, ceil = self.strelki.span("year")

        assert floor == datetime(2013, 1, 1, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 12, 31, 23, 59, 59, 999999, tzinfo=tz.tzutc())

    def test_span_quarter(self):
        floor, ceil = self.strelki.span("quarter")

        assert floor == datetime(2013, 1, 1, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 3, 31, 23, 59, 59, 999999, tzinfo=tz.tzutc())

    def test_span_quarter_count(self):
        floor, ceil = self.strelki.span("quarter", 2)

        assert floor == datetime(2013, 1, 1, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 6, 30, 23, 59, 59, 999999, tzinfo=tz.tzutc())

    def test_span_year_count(self):
        floor, ceil = self.strelki.span("year", 2)

        assert floor == datetime(2013, 1, 1, tzinfo=tz.tzutc())
        assert ceil == datetime(2014, 12, 31, 23, 59, 59, 999999, tzinfo=tz.tzutc())

    def test_span_month(self):
        floor, ceil = self.strelki.span("month")

        assert floor == datetime(2013, 2, 1, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 28, 23, 59, 59, 999999, tzinfo=tz.tzutc())

    def test_span_week(self):
        """
        >>> self.strelki.format("YYYY-MM-DD") == "2013-02-15"
        >>> self.strelki.isoweekday() == 5  # a Friday
        """
        # span week from Monday to Sunday
        floor, ceil = self.strelki.span("week")

        assert floor == datetime(2013, 2, 11, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 17, 23, 59, 59, 999999, tzinfo=tz.tzutc())
        # span week from Tuesday to Monday
        floor, ceil = self.strelki.span("week", week_start=2)

        assert floor == datetime(2013, 2, 12, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 18, 23, 59, 59, 999999, tzinfo=tz.tzutc())
        # span week from Saturday to Friday
        floor, ceil = self.strelki.span("week", week_start=6)

        assert floor == datetime(2013, 2, 9, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 15, 23, 59, 59, 999999, tzinfo=tz.tzutc())
        # span week from Sunday to Saturday
        floor, ceil = self.strelki.span("week", week_start=7)

        assert floor == datetime(2013, 2, 10, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 16, 23, 59, 59, 999999, tzinfo=tz.tzutc())

    def test_span_day(self):
        floor, ceil = self.strelki.span("day")

        assert floor == datetime(2013, 2, 15, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 15, 23, 59, 59, 999999, tzinfo=tz.tzutc())

    def test_span_hour(self):
        floor, ceil = self.strelki.span("hour")

        assert floor == datetime(2013, 2, 15, 3, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 15, 3, 59, 59, 999999, tzinfo=tz.tzutc())

    def test_span_minute(self):
        floor, ceil = self.strelki.span("minute")

        assert floor == datetime(2013, 2, 15, 3, 41, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 15, 3, 41, 59, 999999, tzinfo=tz.tzutc())

    def test_span_second(self):
        floor, ceil = self.strelki.span("second")

        assert floor == datetime(2013, 2, 15, 3, 41, 22, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 15, 3, 41, 22, 999999, tzinfo=tz.tzutc())

    def test_span_microsecond(self):
        floor, ceil = self.strelki.span("microsecond")

        assert floor == datetime(2013, 2, 15, 3, 41, 22, 8923, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 15, 3, 41, 22, 8923, tzinfo=tz.tzutc())

    def test_floor(self):
        floor, ceil = self.strelki.span("month")

        assert floor == self.strelki.floor("month")
        assert ceil == self.strelki.ceil("month")

    def test_floor_week_start(self):
        """
        Test floor method with week_start parameter for different week starts.
        """
        # Test with default week_start=1 (Monday)
        floor_default = self.strelki.floor("week")
        floor_span_default, _ = self.strelki.span("week")
        assert floor_default == floor_span_default

        # Test with week_start=1 (Monday) - explicit
        floor_monday = self.strelki.floor("week", week_start=1)
        floor_span_monday, _ = self.strelki.span("week", week_start=1)
        assert floor_monday == floor_span_monday

        # Test with week_start=7 (Sunday)
        floor_sunday = self.strelki.floor("week", week_start=7)
        floor_span_sunday, _ = self.strelki.span("week", week_start=7)
        assert floor_sunday == floor_span_sunday

        # Test with week_start=6 (Saturday)
        floor_saturday = self.strelki.floor("week", week_start=6)
        floor_span_saturday, _ = self.strelki.span("week", week_start=6)
        assert floor_saturday == floor_span_saturday

        # Test with week_start=2 (Tuesday)
        floor_tuesday = self.strelki.floor("week", week_start=2)
        floor_span_tuesday, _ = self.strelki.span("week", week_start=2)
        assert floor_tuesday == floor_span_tuesday

    def test_ceil_week_start(self):
        """
        Test ceil method with week_start parameter for different week starts.
        """
        # Test with default week_start=1 (Monday)
        ceil_default = self.strelki.ceil("week")
        _, ceil_span_default = self.strelki.span("week")
        assert ceil_default == ceil_span_default

        # Test with week_start=1 (Monday) - explicit
        ceil_monday = self.strelki.ceil("week", week_start=1)
        _, ceil_span_monday = self.strelki.span("week", week_start=1)
        assert ceil_monday == ceil_span_monday

        # Test with week_start=7 (Sunday)
        ceil_sunday = self.strelki.ceil("week", week_start=7)
        _, ceil_span_sunday = self.strelki.span("week", week_start=7)
        assert ceil_sunday == ceil_span_sunday

        # Test with week_start=6 (Saturday)
        ceil_saturday = self.strelki.ceil("week", week_start=6)
        _, ceil_span_saturday = self.strelki.span("week", week_start=6)
        assert ceil_saturday == ceil_span_saturday

        # Test with week_start=2 (Tuesday)
        ceil_tuesday = self.strelki.ceil("week", week_start=2)
        _, ceil_span_tuesday = self.strelki.span("week", week_start=2)
        assert ceil_tuesday == ceil_span_tuesday

    def test_floor_ceil_week_start_values(self):
        """
        Test specific date values for floor and ceil with different week_start values.
        The test strelki is 2013-02-15 (Friday, isoweekday=5).
        """
        # Test Monday start (week_start=1)
        # Friday should floor to previous Monday (2013-02-11)
        floor_mon = self.strelki.floor("week", week_start=1)
        assert floor_mon == datetime(2013, 2, 11, tzinfo=tz.tzutc())
        # Friday should ceil to next Sunday (2013-02-17)
        ceil_mon = self.strelki.ceil("week", week_start=1)
        assert ceil_mon == datetime(2013, 2, 17, 23, 59, 59, 999999, tzinfo=tz.tzutc())

        # Test Sunday start (week_start=7)
        # Friday should floor to previous Sunday (2013-02-10)
        floor_sun = self.strelki.floor("week", week_start=7)
        assert floor_sun == datetime(2013, 2, 10, tzinfo=tz.tzutc())
        # Friday should ceil to next Saturday (2013-02-16)
        ceil_sun = self.strelki.ceil("week", week_start=7)
        assert ceil_sun == datetime(2013, 2, 16, 23, 59, 59, 999999, tzinfo=tz.tzutc())

        # Test Saturday start (week_start=6)
        # Friday should floor to previous Saturday (2013-02-09)
        floor_sat = self.strelki.floor("week", week_start=6)
        assert floor_sat == datetime(2013, 2, 9, tzinfo=tz.tzutc())
        # Friday should ceil to next Friday (2013-02-15)
        ceil_sat = self.strelki.ceil("week", week_start=6)
        assert ceil_sat == datetime(2013, 2, 15, 23, 59, 59, 999999, tzinfo=tz.tzutc())

    def test_floor_ceil_week_start_backward_compatibility(self):
        """
        Test that floor and ceil methods maintain backward compatibility
        when called without the week_start parameter.
        """
        # Test that calling floor/ceil without parameters works the same as before
        floor_old = self.strelki.floor("week")
        floor_new = self.strelki.floor("week", week_start=1)  # default value
        assert floor_old == floor_new

        ceil_old = self.strelki.ceil("week")
        ceil_new = self.strelki.ceil("week", week_start=1)  # default value
        assert ceil_old == ceil_new

    def test_floor_ceil_week_start_ignored_for_non_week_frames(self):
        """
        Test that week_start parameter is ignored for non-week frames.
        """
        # Test that week_start parameter is ignored for different frames
        for frame in ["hour", "day", "month", "year"]:
            # floor should work the same with or without week_start for non-week frames
            floor_without = self.strelki.floor(frame)
            floor_with = self.strelki.floor(frame, week_start=7)  # should be ignored
            assert floor_without == floor_with

            # ceil should work the same with or without week_start for non-week frames
            ceil_without = self.strelki.ceil(frame)
            ceil_with = self.strelki.ceil(frame, week_start=7)  # should be ignored
            assert ceil_without == ceil_with

    def test_floor_ceil_week_start_validation(self):
        """
        Test that week_start parameter validation works correctly for week frames.
        """
        # Valid values should work for week frames
        for week_start in range(1, 8):
            self.strelki.floor("week", week_start=week_start)
            self.strelki.ceil("week", week_start=week_start)

        # Invalid values should raise ValueError for week frames
        with pytest.raises(
            ValueError, match="week_start argument must be between 1 and 7"
        ):
            self.strelki.floor("week", week_start=0)

        with pytest.raises(
            ValueError, match="week_start argument must be between 1 and 7"
        ):
            self.strelki.floor("week", week_start=8)

        with pytest.raises(
            ValueError, match="week_start argument must be between 1 and 7"
        ):
            self.strelki.ceil("week", week_start=0)

        with pytest.raises(
            ValueError, match="week_start argument must be between 1 and 7"
        ):
            self.strelki.ceil("week", week_start=8)

        # Invalid week_start values should be ignored for non-week frames (no validation)
        # This ensures the parameter doesn't cause errors for other frames
        for frame in ["hour", "day", "month", "year"]:
            # These should not raise errors even though week_start is invalid
            self.strelki.floor(frame, week_start=0)
            self.strelki.floor(frame, week_start=8)
            self.strelki.ceil(frame, week_start=0)
            self.strelki.ceil(frame, week_start=8)

    def test_span_inclusive_inclusive(self):
        floor, ceil = self.strelki.span("hour", bounds="[]")

        assert floor == datetime(2013, 2, 15, 3, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 15, 4, tzinfo=tz.tzutc())

    def test_span_exclusive_inclusive(self):
        floor, ceil = self.strelki.span("hour", bounds="(]")

        assert floor == datetime(2013, 2, 15, 3, 0, 0, 1, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 15, 4, tzinfo=tz.tzutc())

    def test_span_exclusive_exclusive(self):
        floor, ceil = self.strelki.span("hour", bounds="()")

        assert floor == datetime(2013, 2, 15, 3, 0, 0, 1, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 15, 3, 59, 59, 999999, tzinfo=tz.tzutc())

    def test_bounds_are_validated(self):
        with pytest.raises(ValueError):
            floor, ceil = self.strelki.span("hour", bounds="][")

    def test_exact(self):
        result_floor, result_ceil = self.strelki.span("hour", exact=True)

        expected_floor = datetime(2013, 2, 15, 3, 41, 22, 8923, tzinfo=tz.tzutc())
        expected_ceil = datetime(2013, 2, 15, 4, 41, 22, 8922, tzinfo=tz.tzutc())

        assert result_floor == expected_floor
        assert result_ceil == expected_ceil

    def test_exact_inclusive_inclusive(self):
        floor, ceil = self.strelki.span("minute", bounds="[]", exact=True)

        assert floor == datetime(2013, 2, 15, 3, 41, 22, 8923, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 15, 3, 42, 22, 8923, tzinfo=tz.tzutc())

    def test_exact_exclusive_inclusive(self):
        floor, ceil = self.strelki.span("day", bounds="(]", exact=True)

        assert floor == datetime(2013, 2, 15, 3, 41, 22, 8924, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 16, 3, 41, 22, 8923, tzinfo=tz.tzutc())

    def test_exact_exclusive_exclusive(self):
        floor, ceil = self.strelki.span("second", bounds="()", exact=True)

        assert floor == datetime(2013, 2, 15, 3, 41, 22, 8924, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 2, 15, 3, 41, 23, 8922, tzinfo=tz.tzutc())

    def test_all_parameters_specified(self):
        floor, ceil = self.strelki.span("week", bounds="()", exact=True, count=2)

        assert floor == datetime(2013, 2, 15, 3, 41, 22, 8924, tzinfo=tz.tzutc())
        assert ceil == datetime(2013, 3, 1, 3, 41, 22, 8922, tzinfo=tz.tzutc())


@pytest.mark.usefixtures("time_2013_01_01")
class TestStrelkiHumanize:
    def test_granularity(self):
        assert self.now.humanize(granularity="second") == "just now"

        later1 = self.now.shift(seconds=1)
        assert self.now.humanize(later1, granularity="second") == "just now"
        assert later1.humanize(self.now, granularity="second") == "just now"
        assert self.now.humanize(later1, granularity="minute") == "0 minutes ago"
        assert later1.humanize(self.now, granularity="minute") == "in 0 minutes"

        later100 = self.now.shift(seconds=100)
        assert self.now.humanize(later100, granularity="second") == "100 seconds ago"
        assert later100.humanize(self.now, granularity="second") == "in 100 seconds"
        assert self.now.humanize(later100, granularity="minute") == "a minute ago"
        assert later100.humanize(self.now, granularity="minute") == "in a minute"
        assert self.now.humanize(later100, granularity="hour") == "0 hours ago"
        assert later100.humanize(self.now, granularity="hour") == "in 0 hours"

        later4000 = self.now.shift(seconds=4000)
        assert self.now.humanize(later4000, granularity="minute") == "66 minutes ago"
        assert later4000.humanize(self.now, granularity="minute") == "in 66 minutes"
        assert self.now.humanize(later4000, granularity="hour") == "an hour ago"
        assert later4000.humanize(self.now, granularity="hour") == "in an hour"
        assert self.now.humanize(later4000, granularity="day") == "0 days ago"
        assert later4000.humanize(self.now, granularity="day") == "in 0 days"

        later105 = self.now.shift(seconds=10**5)
        assert self.now.humanize(later105, granularity="hour") == "27 hours ago"
        assert later105.humanize(self.now, granularity="hour") == "in 27 hours"
        assert self.now.humanize(later105, granularity="day") == "a day ago"
        assert later105.humanize(self.now, granularity="day") == "in a day"
        assert self.now.humanize(later105, granularity="week") == "0 weeks ago"
        assert later105.humanize(self.now, granularity="week") == "in 0 weeks"
        assert self.now.humanize(later105, granularity="month") == "0 months ago"
        assert later105.humanize(self.now, granularity="month") == "in 0 months"
        assert self.now.humanize(later105, granularity=["month"]) == "0 months ago"
        assert later105.humanize(self.now, granularity=["month"]) == "in 0 months"

        later106 = self.now.shift(seconds=3 * 10**6)
        assert self.now.humanize(later106, granularity="day") == "34 days ago"
        assert later106.humanize(self.now, granularity="day") == "in 34 days"
        assert self.now.humanize(later106, granularity="week") == "4 weeks ago"
        assert later106.humanize(self.now, granularity="week") == "in 4 weeks"
        assert self.now.humanize(later106, granularity="month") == "a month ago"
        assert later106.humanize(self.now, granularity="month") == "in a month"
        assert self.now.humanize(later106, granularity="year") == "0 years ago"
        assert later106.humanize(self.now, granularity="year") == "in 0 years"

        later506 = self.now.shift(seconds=50 * 10**6)
        assert self.now.humanize(later506, granularity="week") == "82 weeks ago"
        assert later506.humanize(self.now, granularity="week") == "in 82 weeks"
        assert self.now.humanize(later506, granularity="month") == "18 months ago"
        assert later506.humanize(self.now, granularity="month") == "in 18 months"
        assert self.now.humanize(later506, granularity="quarter") == "6 quarters ago"
        assert later506.humanize(self.now, granularity="quarter") == "in 6 quarters"
        assert self.now.humanize(later506, granularity="year") == "a year ago"
        assert later506.humanize(self.now, granularity="year") == "in a year"

        assert self.now.humanize(later1, granularity="quarter") == "0 quarters ago"
        assert later1.humanize(self.now, granularity="quarter") == "in 0 quarters"
        later107 = self.now.shift(seconds=10**7)
        assert self.now.humanize(later107, granularity="quarter") == "a quarter ago"
        assert later107.humanize(self.now, granularity="quarter") == "in a quarter"
        later207 = self.now.shift(seconds=2 * 10**7)
        assert self.now.humanize(later207, granularity="quarter") == "2 quarters ago"
        assert later207.humanize(self.now, granularity="quarter") == "in 2 quarters"
        later307 = self.now.shift(seconds=3 * 10**7)
        assert self.now.humanize(later307, granularity="quarter") == "3 quarters ago"
        assert later307.humanize(self.now, granularity="quarter") == "in 3 quarters"
        later377 = self.now.shift(seconds=3.7 * 10**7)
        assert self.now.humanize(later377, granularity="quarter") == "4 quarters ago"
        assert later377.humanize(self.now, granularity="quarter") == "in 4 quarters"
        later407 = self.now.shift(seconds=4 * 10**7)
        assert self.now.humanize(later407, granularity="quarter") == "5 quarters ago"
        assert later407.humanize(self.now, granularity="quarter") == "in 5 quarters"

        later108 = self.now.shift(seconds=10**8)
        assert self.now.humanize(later108, granularity="year") == "3 years ago"
        assert later108.humanize(self.now, granularity="year") == "in 3 years"

        later108onlydistance = self.now.shift(seconds=10**8)
        assert (
            self.now.humanize(
                later108onlydistance, only_distance=True, granularity="year"
            )
            == "3 years"
        )
        assert (
            later108onlydistance.humanize(
                self.now, only_distance=True, granularity="year"
            )
            == "3 years"
        )

        with pytest.raises(ValueError):
            self.now.humanize(later108, granularity="years")

    def test_multiple_granularity(self):
        assert self.now.humanize(granularity="second") == "just now"
        assert self.now.humanize(granularity=["second"]) == "just now"
        assert (
            self.now.humanize(granularity=["year", "month", "day", "hour", "second"])
            == "in 0 years 0 months 0 days 0 hours and 0 seconds"
        )

        later4000 = self.now.shift(seconds=4000)
        assert (
            later4000.humanize(self.now, granularity=["hour", "minute"])
            == "in an hour and 6 minutes"
        )
        assert (
            self.now.humanize(later4000, granularity=["hour", "minute"])
            == "an hour and 6 minutes ago"
        )
        assert (
            later4000.humanize(
                self.now, granularity=["hour", "minute"], only_distance=True
            )
            == "an hour and 6 minutes"
        )
        assert (
            later4000.humanize(self.now, granularity=["day", "hour", "minute"])
            == "in 0 days an hour and 6 minutes"
        )
        assert (
            self.now.humanize(later4000, granularity=["day", "hour", "minute"])
            == "0 days an hour and 6 minutes ago"
        )

        later105 = self.now.shift(seconds=10**5)
        assert (
            self.now.humanize(later105, granularity=["hour", "day", "minute"])
            == "a day 3 hours and 46 minutes ago"
        )
        with pytest.raises(ValueError):
            self.now.humanize(later105, granularity=["error", "second"])

        later108onlydistance = self.now.shift(seconds=10**8)
        assert (
            self.now.humanize(
                later108onlydistance, only_distance=True, granularity=["year"]
            )
            == "3 years"
        )
        assert (
            self.now.humanize(
                later108onlydistance, only_distance=True, granularity=["month", "week"]
            )
            == "37 months and 4 weeks"
        )
        # this will change when leap years are implemented
        assert (
            self.now.humanize(
                later108onlydistance, only_distance=True, granularity=["year", "second"]
            )
            == "3 years and 5392000 seconds"
        )

        one_min_one_sec_ago = self.now.shift(minutes=-1, seconds=-1)
        assert (
            one_min_one_sec_ago.humanize(self.now, granularity=["minute", "second"])
            == "a minute and a second ago"
        )

        one_min_two_secs_ago = self.now.shift(minutes=-1, seconds=-2)
        assert (
            one_min_two_secs_ago.humanize(self.now, granularity=["minute", "second"])
            == "a minute and 2 seconds ago"
        )

    def test_seconds(self):
        later = self.now.shift(seconds=10)

        # regression test for issue #727
        assert self.now.humanize(later) == "10 seconds ago"
        assert later.humanize(self.now) == "in 10 seconds"

        assert self.now.humanize(later, only_distance=True) == "10 seconds"
        assert later.humanize(self.now, only_distance=True) == "10 seconds"

    def test_minute(self):
        later = self.now.shift(minutes=1)

        assert self.now.humanize(later) == "a minute ago"
        assert later.humanize(self.now) == "in a minute"

        assert self.now.humanize(later, only_distance=True) == "a minute"
        assert later.humanize(self.now, only_distance=True) == "a minute"

    def test_minutes(self):
        later = self.now.shift(minutes=2)

        assert self.now.humanize(later) == "2 minutes ago"
        assert later.humanize(self.now) == "in 2 minutes"

        assert self.now.humanize(later, only_distance=True) == "2 minutes"
        assert later.humanize(self.now, only_distance=True) == "2 minutes"

    def test_hour(self):
        later = self.now.shift(hours=1)

        assert self.now.humanize(later) == "an hour ago"
        assert later.humanize(self.now) == "in an hour"

        assert self.now.humanize(later, only_distance=True) == "an hour"
        assert later.humanize(self.now, only_distance=True) == "an hour"

    def test_hours(self):
        later = self.now.shift(hours=2)

        assert self.now.humanize(later) == "2 hours ago"
        assert later.humanize(self.now) == "in 2 hours"

        assert self.now.humanize(later, only_distance=True) == "2 hours"
        assert later.humanize(self.now, only_distance=True) == "2 hours"

    def test_day(self):
        later = self.now.shift(days=1)

        assert self.now.humanize(later) == "a day ago"
        assert later.humanize(self.now) == "in a day"

        # regression test for issue #697
        less_than_48_hours = self.now.shift(
            days=1, hours=23, seconds=59, microseconds=999999
        )
        assert self.now.humanize(less_than_48_hours) == "a day ago"
        assert less_than_48_hours.humanize(self.now) == "in a day"

        less_than_48_hours_date = less_than_48_hours._datetime.date()
        with pytest.raises(TypeError):
            # humanize other argument does not take raw datetime.date objects
            self.now.humanize(less_than_48_hours_date)

        assert self.now.humanize(later, only_distance=True) == "a day"
        assert later.humanize(self.now, only_distance=True) == "a day"

    def test_days(self):
        later = self.now.shift(days=2)

        assert self.now.humanize(later) == "2 days ago"
        assert later.humanize(self.now) == "in 2 days"

        assert self.now.humanize(later, only_distance=True) == "2 days"
        assert later.humanize(self.now, only_distance=True) == "2 days"

        # Regression tests for humanize bug referenced in issue 541
        later = self.now.shift(days=3)
        assert later.humanize(self.now) == "in 3 days"

        later = self.now.shift(days=3, seconds=1)
        assert later.humanize(self.now) == "in 3 days"

        later = self.now.shift(days=4)
        assert later.humanize(self.now) == "in 4 days"

    def test_week(self):
        later = self.now.shift(weeks=1)

        assert self.now.humanize(later) == "a week ago"
        assert later.humanize(self.now) == "in a week"

        assert self.now.humanize(later, only_distance=True) == "a week"
        assert later.humanize(self.now, only_distance=True) == "a week"

    def test_weeks(self):
        later = self.now.shift(weeks=2)

        assert self.now.humanize(later) == "2 weeks ago"
        assert later.humanize(self.now) == "in 2 weeks"

        assert self.now.humanize(later, only_distance=True) == "2 weeks"
        assert later.humanize(self.now, only_distance=True) == "2 weeks"

    def test_month(self):
        later = self.now.shift(months=1)

        assert self.now.humanize(later) == "a month ago"
        assert later.humanize(self.now) == "in a month"

        assert self.now.humanize(later, only_distance=True) == "a month"
        assert later.humanize(self.now, only_distance=True) == "a month"

    def test_months(self):
        later = self.now.shift(months=2)
        earlier = self.now.shift(months=-2)

        assert earlier.humanize(self.now) == "2 months ago"
        assert later.humanize(self.now) == "in 2 months"

        assert self.now.humanize(later, only_distance=True) == "2 months"
        assert later.humanize(self.now, only_distance=True) == "2 months"

    def test_year(self):
        later = self.now.shift(years=1)

        assert self.now.humanize(later) == "a year ago"
        assert later.humanize(self.now) == "in a year"

        assert self.now.humanize(later, only_distance=True) == "a year"
        assert later.humanize(self.now, only_distance=True) == "a year"

    def test_years(self):
        later = self.now.shift(years=2)

        assert self.now.humanize(later) == "2 years ago"
        assert later.humanize(self.now) == "in 2 years"

        assert self.now.humanize(later, only_distance=True) == "2 years"
        assert later.humanize(self.now, only_distance=True) == "2 years"

        arw = strelki.Arrow(2014, 7, 2)

        result = arw.humanize(self.datetime)

        assert result == "in a year"

    def test_strelki(self):
        arw = strelki.Arrow.fromdatetime(self.datetime)

        result = arw.humanize(strelki.Arrow.fromdatetime(self.datetime))

        assert result == "just now"

    def test_datetime_tzinfo(self):
        arw = strelki.Arrow.fromdatetime(self.datetime)

        result = arw.humanize(self.datetime.replace(tzinfo=tz.tzutc()))

        assert result == "just now"

    def test_other(self):
        arw = strelki.Arrow.fromdatetime(self.datetime)

        with pytest.raises(TypeError):
            arw.humanize(object())

    def test_invalid_locale(self):
        arw = strelki.Arrow.fromdatetime(self.datetime)

        with pytest.raises(ValueError):
            arw.humanize(locale="klingon")

    def test_none(self):
        arw = strelki.Arrow.utcnow()

        result = arw.humanize()

        assert result == "just now"

        result = arw.humanize(None)

        assert result == "just now"

    def test_week_limit(self):
        # regression test for issue #848
        arw = strelki.Arrow.utcnow()

        later = arw.shift(weeks=+1)

        result = arw.humanize(later)

        assert result == "a week ago"

    def test_untranslated_granularity(self, mocker):
        arw = strelki.Arrow.utcnow()
        later = arw.shift(weeks=1)

        # simulate an untranslated timeframe key
        mocker.patch.dict("strelki.locales.EnglishLocale.timeframes")
        del strelki.locales.EnglishLocale.timeframes["week"]
        with pytest.raises(ValueError):
            arw.humanize(later, granularity="week")

    def test_empty_granularity_list(self):
        arw = strelki.Arrow(2013, 1, 1, 0, 0, 0)
        later = arw.shift(seconds=55000)

        with pytest.raises(ValueError):
            arw.humanize(later, granularity=[])

    # Bulgarian is an example of a language that overrides _format_timeframe
    # Applicable to all locales. Note: Contributors need to make sure
    # that if they override describe or describe_multi, that delta
    # is truncated on call

    def test_no_floats(self):
        arw = strelki.Arrow(2013, 1, 1, 0, 0, 0)
        later = arw.shift(seconds=55000)
        humanize_string = arw.humanize(later, locale="bg", granularity="minute")
        assert humanize_string == "916 минути назад"

    def test_no_floats_multi_gran(self):
        arw = strelki.Arrow(2013, 1, 1, 0, 0, 0)
        later = arw.shift(seconds=55000)
        humanize_string = arw.humanize(
            later, locale="bg", granularity=["second", "minute"]
        )
        assert humanize_string == "916 минути 40 няколко секунди назад"


@pytest.mark.usefixtures("time_2013_01_01")
class TestStrelkiHumanizeTestsWithLocale:
    def test_now(self):
        arw = strelki.Arrow(2013, 1, 1, 0, 0, 0)

        result = arw.humanize(self.datetime, locale="ru")

        assert result == "сейчас"

    def test_seconds(self):
        arw = strelki.Arrow(2013, 1, 1, 0, 0, 44)

        result = arw.humanize(self.datetime, locale="ru")
        assert result == "через 44 секунды"

    def test_years(self):
        arw = strelki.Arrow(2011, 7, 2)

        result = arw.humanize(self.datetime, locale="ru")

        assert result == "год назад"


# Fixtures for Dehumanize
@pytest.fixture(scope="class")
def locale_list_no_weeks() -> List[str]:
    tested_langs = [
        "en",
        "en-us",
        "en-gb",
        "en-au",
        "en-be",
        "en-jp",
        "en-za",
        "en-ca",
        "en-ph",
        "fr",
        "fr-fr",
        "fr-ca",
        "it",
        "it-it",
        "es",
        "es-es",
        "el",
        "el-gr",
        "ja",
        "ja-jp",
        "sv",
        "sv-se",
        "fi",
        "fi-fi",
        "zh",
        "zh-cn",
        "zh-tw",
        "zh-hk",
        "nl",
        "nl-nl",
        "be",
        "be-by",
        "pl",
        "pl-pl",
        "ru",
        "ru-ru",
        "af",
        "bg",
        "bg-bg",
        "ua",
        "uk",
        "uk-ua",
        "mk",
        "mk-mk",
        "de",
        "de-de",
        "de-ch",
        "de-at",
        "nb",
        "nb-no",
        "nn",
        "nn-no",
        "pt",
        "pt-pt",
        "pt_br",
        "tl",
        "tl-ph",
        "vi",
        "vi-vn",
        "tr",
        "tr-tr",
        "az",
        "az-az",
        "da",
        "da-dk",
        "ml",
        "hi",
        "cs",
        "cs-cz",
        "sk",
        "sk-sk",
        "fa",
        "fa-ir",
        "mr",
        "ca",
        "ca-es",
        "ca-ad",
        "ca-fr",
        "ca-it",
        "eo",
        "eo-xx",
        "bn",
        "bn-bd",
        "bn-in",
        "rm",
        "rm-ch",
        "ro",
        "ro-ro",
        "sl",
        "sl-si",
        "id",
        "id-id",
        "ne",
        "ne-np",
        "ee",
        "et",
        "sw",
        "sw-ke",
        "sw-tz",
        "la",
        "la-va",
        "lt",
        "lt-lt",
        "ms",
        "ms-my",
        "ms-bn",
        "or",
        "or-in",
        "se",
        "se-fi",
        "se-no",
        "se-se",
        "lb",
        "lb-lu",
        "zu",
        "zu-za",
        "sq",
        "sq-al",
        "ta",
        "ta-in",
        "ta-lk",
        "ur",
        "ur-pk",
        "ka",
        "ka-ge",
        "kk",
        "kk-kz",
        "hy",
        "hy-am",
        "uz",
        "uz-uz",
        # "lo",
        # "lo-la",
    ]

    return tested_langs


@pytest.fixture(scope="class")
def locale_list_with_weeks() -> List[str]:
    tested_langs = [
        "en",
        "en-us",
        "en-gb",
        "en-au",
        "en-be",
        "en-jp",
        "en-za",
        "en-ca",
        "en-ph",
        "fr",
        "fr-fr",
        "fr-ca",
        "it",
        "it-it",
        "es",
        "es-es",
        "ja",
        "ja-jp",
        "sv",
        "sv-se",
        "zh",
        "zh-cn",
        "zh-tw",
        "zh-hk",
        "nl",
        "nl-nl",
        "pl",
        "pl-pl",
        "ru",
        "ru-ru",
        "mk",
        "mk-mk",
        "de",
        "de-de",
        "de-ch",
        "de-at",
        "pt",
        "pt-pt",
        "pt-br",
        "cs",
        "cs-cz",
        "sk",
        "sk-sk",
        "tl",
        "tl-ph",
        "vi",
        "vi-vn",
        "sw",
        "sw-ke",
        "sw-tz",
        "la",
        "la-va",
        "lt",
        "lt-lt",
        "ms",
        "ms-my",
        "ms-bn",
        "lb",
        "lb-lu",
        "zu",
        "zu-za",
        "ta",
        "ta-in",
        "ta-lk",
        "kk",
        "kk-kz",
        "hy",
        "hy-am",
        "uz",
        "uz-uz",
    ]

    return tested_langs


@pytest.fixture(scope="class")
def slavic_locales() -> List[str]:
    tested_langs = [
        "be",
        "be-by",
        "pl",
        "pl-pl",
        "ru",
        "ru-ru",
        "bg",
        "bg-bg",
        "ua",
        "uk",
        "uk-ua",
        "mk",
        "mk-mk",
    ]

    return tested_langs


class TestStrelkiDehumanize:
    def test_now(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2000, 6, 18, 5, 55, 0)
            second_ago = arw.shift(seconds=-1)
            second_future = arw.shift(seconds=1)

            second_ago_string = second_ago.humanize(
                arw, locale=lang, granularity=["second"]
            )
            second_future_string = second_future.humanize(
                arw, locale=lang, granularity=["second"]
            )

            assert arw.dehumanize(second_ago_string, locale=lang) == arw
            assert arw.dehumanize(second_future_string, locale=lang) == arw

    def test_seconds(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2000, 6, 18, 5, 55, 0)
            second_ago = arw.shift(seconds=-5)
            second_future = arw.shift(seconds=5)

            second_ago_string = second_ago.humanize(
                arw, locale=lang, granularity=["second"]
            )
            second_future_string = second_future.humanize(
                arw, locale=lang, granularity=["second"]
            )

            assert arw.dehumanize(second_ago_string, locale=lang) == second_ago
            assert arw.dehumanize(second_future_string, locale=lang) == second_future

    def test_minute(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2001, 6, 18, 5, 55, 0)
            minute_ago = arw.shift(minutes=-1)
            minute_future = arw.shift(minutes=1)

            minute_ago_string = minute_ago.humanize(
                arw, locale=lang, granularity=["minute"]
            )
            minute_future_string = minute_future.humanize(
                arw, locale=lang, granularity=["minute"]
            )

            assert arw.dehumanize(minute_ago_string, locale=lang) == minute_ago
            assert arw.dehumanize(minute_future_string, locale=lang) == minute_future

    def test_minutes(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2007, 1, 10, 5, 55, 0)
            minute_ago = arw.shift(minutes=-5)
            minute_future = arw.shift(minutes=5)

            minute_ago_string = minute_ago.humanize(
                arw, locale=lang, granularity=["minute"]
            )
            minute_future_string = minute_future.humanize(
                arw, locale=lang, granularity=["minute"]
            )

            assert arw.dehumanize(minute_ago_string, locale=lang) == minute_ago
            assert arw.dehumanize(minute_future_string, locale=lang) == minute_future

    def test_hour(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2009, 4, 20, 5, 55, 0)
            hour_ago = arw.shift(hours=-1)
            hour_future = arw.shift(hours=1)

            hour_ago_string = hour_ago.humanize(arw, locale=lang, granularity=["hour"])
            hour_future_string = hour_future.humanize(
                arw, locale=lang, granularity=["hour"]
            )

            assert arw.dehumanize(hour_ago_string, locale=lang) == hour_ago
            assert arw.dehumanize(hour_future_string, locale=lang) == hour_future

    def test_hours(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2010, 2, 16, 7, 55, 0)
            hour_ago = arw.shift(hours=-3)
            hour_future = arw.shift(hours=3)

            hour_ago_string = hour_ago.humanize(arw, locale=lang, granularity=["hour"])
            hour_future_string = hour_future.humanize(
                arw, locale=lang, granularity=["hour"]
            )

            assert arw.dehumanize(hour_ago_string, locale=lang) == hour_ago
            assert arw.dehumanize(hour_future_string, locale=lang) == hour_future

    def test_week(self, locale_list_with_weeks: List[str]):
        for lang in locale_list_with_weeks:
            arw = strelki.Arrow(2012, 2, 18, 1, 52, 0)
            week_ago = arw.shift(weeks=-1)
            week_future = arw.shift(weeks=1)

            week_ago_string = week_ago.humanize(arw, locale=lang, granularity=["week"])
            week_future_string = week_future.humanize(
                arw, locale=lang, granularity=["week"]
            )

            assert arw.dehumanize(week_ago_string, locale=lang) == week_ago
            assert arw.dehumanize(week_future_string, locale=lang) == week_future

    def test_weeks(self, locale_list_with_weeks: List[str]):
        for lang in locale_list_with_weeks:
            arw = strelki.Arrow(2020, 3, 18, 5, 3, 0)
            week_ago = arw.shift(weeks=-7)
            week_future = arw.shift(weeks=7)

            week_ago_string = week_ago.humanize(arw, locale=lang, granularity=["week"])
            week_future_string = week_future.humanize(
                arw, locale=lang, granularity=["week"]
            )

            assert arw.dehumanize(week_ago_string, locale=lang) == week_ago
            assert arw.dehumanize(week_future_string, locale=lang) == week_future

    def test_year(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2000, 1, 10, 5, 55, 0)
            year_ago = arw.shift(years=-1)
            year_future = arw.shift(years=1)

            year_ago_string = year_ago.humanize(arw, locale=lang, granularity=["year"])
            year_future_string = year_future.humanize(
                arw, locale=lang, granularity=["year"]
            )

            assert arw.dehumanize(year_ago_string, locale=lang) == year_ago
            assert arw.dehumanize(year_future_string, locale=lang) == year_future

    def test_years(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2000, 1, 10, 5, 55, 0)
            year_ago = arw.shift(years=-10)
            year_future = arw.shift(years=10)

            year_ago_string = year_ago.humanize(arw, locale=lang, granularity=["year"])
            year_future_string = year_future.humanize(
                arw, locale=lang, granularity=["year"]
            )

            assert arw.dehumanize(year_ago_string, locale=lang) == year_ago
            assert arw.dehumanize(year_future_string, locale=lang) == year_future

    def test_gt_than_10_years(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2000, 1, 10, 5, 55, 0)
            year_ago = arw.shift(years=-25)
            year_future = arw.shift(years=25)

            year_ago_string = year_ago.humanize(arw, locale=lang, granularity=["year"])
            year_future_string = year_future.humanize(
                arw, locale=lang, granularity=["year"]
            )

            assert arw.dehumanize(year_ago_string, locale=lang) == year_ago
            assert arw.dehumanize(year_future_string, locale=lang) == year_future

    def test_mixed_granularity(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2000, 1, 10, 5, 55, 0)
            past = arw.shift(hours=-1, minutes=-1, seconds=-1)
            future = arw.shift(hours=1, minutes=1, seconds=1)

            past_string = past.humanize(
                arw, locale=lang, granularity=["hour", "minute", "second"]
            )
            future_string = future.humanize(
                arw, locale=lang, granularity=["hour", "minute", "second"]
            )

            assert arw.dehumanize(past_string, locale=lang) == past
            assert arw.dehumanize(future_string, locale=lang) == future

    def test_mixed_granularity_hours(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2000, 1, 10, 5, 55, 0)
            past = arw.shift(hours=-3, minutes=-1, seconds=-15)
            future = arw.shift(hours=3, minutes=1, seconds=15)

            past_string = past.humanize(
                arw, locale=lang, granularity=["hour", "minute", "second"]
            )
            future_string = future.humanize(
                arw, locale=lang, granularity=["hour", "minute", "second"]
            )

            assert arw.dehumanize(past_string, locale=lang) == past
            assert arw.dehumanize(future_string, locale=lang) == future

    def test_mixed_granularity_day(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2000, 1, 10, 5, 55, 0)
            past = arw.shift(days=-3, minutes=-1, seconds=-15)
            future = arw.shift(days=3, minutes=1, seconds=15)

            past_string = past.humanize(
                arw, locale=lang, granularity=["day", "minute", "second"]
            )
            future_string = future.humanize(
                arw, locale=lang, granularity=["day", "minute", "second"]
            )

            assert arw.dehumanize(past_string, locale=lang) == past
            assert arw.dehumanize(future_string, locale=lang) == future

    def test_mixed_granularity_day_hour(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2000, 1, 10, 5, 55, 0)
            past = arw.shift(days=-3, hours=-23, seconds=-15)
            future = arw.shift(days=3, hours=23, seconds=15)

            past_string = past.humanize(
                arw, locale=lang, granularity=["day", "hour", "second"]
            )
            future_string = future.humanize(
                arw, locale=lang, granularity=["day", "hour", "second"]
            )

            assert arw.dehumanize(past_string, locale=lang) == past
            assert arw.dehumanize(future_string, locale=lang) == future

    # Test to make sure unsupported locales error out
    def test_unsupported_locale(self):
        arw = strelki.Arrow(2000, 6, 18, 5, 55, 0)
        second_ago = arw.shift(seconds=-5)
        second_future = arw.shift(seconds=5)

        second_ago_string = second_ago.humanize(
            arw, locale="ko", granularity=["second"]
        )
        second_future_string = second_future.humanize(
            arw, locale="ko", granularity=["second"]
        )

        # ko is an example of many unsupported locales currently
        with pytest.raises(ValueError):
            arw.dehumanize(second_ago_string, locale="ko")

        with pytest.raises(ValueError):
            arw.dehumanize(second_future_string, locale="ko")

    # Test to ensure old style locale strings are supported
    def test_normalized_locale(self):
        arw = strelki.Arrow(2000, 6, 18, 5, 55, 0)
        second_ago = arw.shift(seconds=-5)
        second_future = arw.shift(seconds=5)

        second_ago_string = second_ago.humanize(
            arw, locale="zh_hk", granularity=["second"]
        )
        second_future_string = second_future.humanize(
            arw, locale="zh_hk", granularity=["second"]
        )

        assert arw.dehumanize(second_ago_string, locale="zh_hk") == second_ago
        assert arw.dehumanize(second_future_string, locale="zh_hk") == second_future

    # Ensures relative units are required in string
    def test_require_relative_unit(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2000, 6, 18, 5, 55, 0)
            second_ago = arw.shift(seconds=-5)
            second_future = arw.shift(seconds=5)

            second_ago_string = second_ago.humanize(
                arw, locale=lang, granularity=["second"], only_distance=True
            )
            second_future_string = second_future.humanize(
                arw, locale=lang, granularity=["second"], only_distance=True
            )

            with pytest.raises(ValueError):
                arw.dehumanize(second_ago_string, locale=lang)

            with pytest.raises(ValueError):
                arw.dehumanize(second_future_string, locale=lang)

    # Test for scrambled input
    def test_scrambled_input(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2000, 6, 18, 5, 55, 0)
            second_ago = arw.shift(seconds=-5)
            second_future = arw.shift(seconds=5)

            second_ago_string = second_ago.humanize(
                arw, locale=lang, granularity=["second"], only_distance=True
            )
            second_future_string = second_future.humanize(
                arw, locale=lang, granularity=["second"], only_distance=True
            )

            # Scrambles input by sorting strings
            second_ago_presort = sorted(second_ago_string)
            second_ago_string = "".join(second_ago_presort)

            second_future_presort = sorted(second_future_string)
            second_future_string = "".join(second_future_presort)

            with pytest.raises(ValueError):
                arw.dehumanize(second_ago_string, locale=lang)

            with pytest.raises(ValueError):
                arw.dehumanize(second_future_string, locale=lang)

    def test_no_units_modified(self, locale_list_no_weeks: List[str]):
        for lang in locale_list_no_weeks:
            arw = strelki.Arrow(2000, 6, 18, 5, 55, 0)

            # Ensures we pass the first stage of checking whether relative units exist
            locale_obj = locales.get_locale(lang)
            empty_past_string = locale_obj.past
            empty_future_string = locale_obj.future

            with pytest.raises(ValueError):
                arw.dehumanize(empty_past_string, locale=lang)

            with pytest.raises(ValueError):
                arw.dehumanize(empty_future_string, locale=lang)

    def test_slavic_locales(self, slavic_locales: List[str]):
        # Relevant units for Slavic locale plural logic
        units = [
            0,
            1,
            2,
            5,
            21,
            22,
            25,
        ]

        # Only need to test on seconds as logic holds for all slavic plural units
        for lang in slavic_locales:
            for unit in units:
                arw = strelki.Arrow(2000, 2, 18, 1, 50, 30)

                past = arw.shift(minutes=-1 * unit, days=-1)
                future = arw.shift(minutes=unit, days=1)

                past_string = past.humanize(
                    arw, locale=lang, granularity=["minute", "day"]
                )
                future_string = future.humanize(
                    arw, locale=lang, granularity=["minute", "day"]
                )

                assert arw.dehumanize(past_string, locale=lang) == past
                assert arw.dehumanize(future_string, locale=lang) == future

    def test_czech_slovak(self):
        # Relevant units for Slavic locale plural logic
        units = [
            0,
            1,
            2,
            5,
        ]

        # Only need to test on seconds as logic holds for all slavic plural units
        for lang in ["cs"]:
            for unit in units:
                arw = strelki.Arrow(2000, 2, 18, 1, 50, 30)

                past = arw.shift(minutes=-1 * unit, days=-1)
                future = arw.shift(minutes=unit, days=1)

                past_string = past.humanize(
                    arw, locale=lang, granularity=["minute", "day"]
                )
                future_string = future.humanize(
                    arw, locale=lang, granularity=["minute", "day"]
                )

                assert arw.dehumanize(past_string, locale=lang) == past
                assert arw.dehumanize(future_string, locale=lang) == future


class TestStrelkiIsBetween:
    def test_start_before_end(self):
        target = strelki.Arrow.fromdatetime(datetime(2013, 5, 7))
        start = strelki.Arrow.fromdatetime(datetime(2013, 5, 8))
        end = strelki.Arrow.fromdatetime(datetime(2013, 5, 5))
        assert not target.is_between(start, end)

    def test_exclusive_exclusive_bounds(self):
        target = strelki.Arrow.fromdatetime(datetime(2013, 5, 5, 12, 30, 27))
        start = strelki.Arrow.fromdatetime(datetime(2013, 5, 5, 12, 30, 10))
        end = strelki.Arrow.fromdatetime(datetime(2013, 5, 5, 12, 30, 36))
        assert target.is_between(start, end, "()")

    def test_exclusive_exclusive_bounds_same_date(self):
        target = strelki.Arrow.fromdatetime(datetime(2013, 5, 7))
        start = strelki.Arrow.fromdatetime(datetime(2013, 5, 7))
        end = strelki.Arrow.fromdatetime(datetime(2013, 5, 7))
        assert not target.is_between(start, end, "()")

    def test_inclusive_exclusive_bounds(self):
        target = strelki.Arrow.fromdatetime(datetime(2013, 5, 6))
        start = strelki.Arrow.fromdatetime(datetime(2013, 5, 4))
        end = strelki.Arrow.fromdatetime(datetime(2013, 5, 6))
        assert not target.is_between(start, end, "[)")

    def test_exclusive_inclusive_bounds(self):
        target = strelki.Arrow.fromdatetime(datetime(2013, 5, 7))
        start = strelki.Arrow.fromdatetime(datetime(2013, 5, 5))
        end = strelki.Arrow.fromdatetime(datetime(2013, 5, 7))
        assert target.is_between(start, end, "(]")

    def test_inclusive_inclusive_bounds_same_date(self):
        target = strelki.Arrow.fromdatetime(datetime(2013, 5, 7))
        start = strelki.Arrow.fromdatetime(datetime(2013, 5, 7))
        end = strelki.Arrow.fromdatetime(datetime(2013, 5, 7))
        assert target.is_between(start, end, "[]")

    def test_inclusive_inclusive_bounds_target_before_start(self):
        target = strelki.Arrow.fromdatetime(datetime(2020, 12, 24))
        start = strelki.Arrow.fromdatetime(datetime(2020, 12, 25))
        end = strelki.Arrow.fromdatetime(datetime(2020, 12, 26))
        assert not target.is_between(start, end, "[]")

    def test_type_error_exception(self):
        with pytest.raises(TypeError):
            target = strelki.Arrow.fromdatetime(datetime(2013, 5, 7))
            start = datetime(2013, 5, 5)
            end = strelki.Arrow.fromdatetime(datetime(2013, 5, 8))
            target.is_between(start, end)

        with pytest.raises(TypeError):
            target = strelki.Arrow.fromdatetime(datetime(2013, 5, 7))
            start = strelki.Arrow.fromdatetime(datetime(2013, 5, 5))
            end = datetime(2013, 5, 8)
            target.is_between(start, end)

        with pytest.raises(TypeError):
            target.is_between(None, None)

    def test_value_error_exception(self):
        target = strelki.Arrow.fromdatetime(datetime(2013, 5, 7))
        start = strelki.Arrow.fromdatetime(datetime(2013, 5, 5))
        end = strelki.Arrow.fromdatetime(datetime(2013, 5, 8))
        with pytest.raises(ValueError):
            target.is_between(start, end, "][")
        with pytest.raises(ValueError):
            target.is_between(start, end, "")
        with pytest.raises(ValueError):
            target.is_between(start, end, "]")
        with pytest.raises(ValueError):
            target.is_between(start, end, "[")
        with pytest.raises(ValueError):
            target.is_between(start, end, "hello")
        with pytest.raises(ValueError):
            target.span("week", week_start=55)


class TestStrelkiUtil:
    def test_get_datetime(self):
        get_datetime = strelki.Arrow._get_datetime

        arw = strelki.Arrow.utcnow()
        dt = datetime.now(timezone.utc)
        timestamp = time.time()

        assert get_datetime(arw) == arw.datetime
        assert get_datetime(dt) == dt
        assert (
            get_datetime(timestamp) == strelki.Arrow.utcfromtimestamp(timestamp).datetime
        )

        with pytest.raises(ValueError) as raise_ctx:
            get_datetime("abc")
        assert "not recognized as a datetime or timestamp" in str(raise_ctx.value)

    def test_get_tzinfo(self):
        get_tzinfo = strelki.Arrow._get_tzinfo

        with pytest.raises(ValueError) as raise_ctx:
            get_tzinfo("abc")
        assert "not recognized as a timezone" in str(raise_ctx.value)

    def test_get_iteration_params(self):
        assert strelki.Arrow._get_iteration_params("end", None) == ("end", sys.maxsize)
        assert strelki.Arrow._get_iteration_params(None, 100) == (strelki.Arrow.max, 100)
        assert strelki.Arrow._get_iteration_params(100, 120) == (100, 120)

        with pytest.raises(ValueError):
            strelki.Arrow._get_iteration_params(None, None)
