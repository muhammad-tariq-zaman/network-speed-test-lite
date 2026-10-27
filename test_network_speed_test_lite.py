import io
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import main


class FakeResp:
    def __init__(self):
        self._data = io.BytesIO(b"x" * 10000)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self, n=-1):
        return self._data.read(n)


class TestSpeed(unittest.TestCase):
    def test_measured_bytes_only(self):
        with mock.patch("main.urllib.request.urlopen", return_value=FakeResp()):
            r = main.measure("https://example.test/file.bin")
        self.assertEqual(r["status"], "OK")
        self.assertEqual(r["bytes"], 10000)
        self.assertIsNotNone(r["kb_per_sec"])

    def test_error_reported(self):
        with mock.patch("main.urllib.request.urlopen", side_effect=OSError("fail")):
            r = main.measure("https://bad.test")
        self.assertEqual(r["status"], "ERROR")
        self.assertIsNone(r["kb_per_sec"])


if __name__ == "__main__":
    unittest.main()
