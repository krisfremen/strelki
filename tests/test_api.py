import strelki


class TestModule:
    def test_get(self, mocker):
        mocker.patch("strelki.api._factory.get", return_value="result")

        assert strelki.api.get() == "result"

    def test_utcnow(self, mocker):
        mocker.patch("strelki.api._factory.utcnow", return_value="utcnow")

        assert strelki.api.utcnow() == "utcnow"

    def test_now(self, mocker):
        mocker.patch("strelki.api._factory.now", tz="tz", return_value="now")

        assert strelki.api.now("tz") == "now"

    def test_factory(self):
        class MockCustomArrowClass(strelki.Arrow):
            pass

        result = strelki.api.factory(MockCustomArrowClass)

        assert isinstance(result, strelki.factory.ArrowFactory)
        assert isinstance(result.utcnow(), MockCustomArrowClass)
