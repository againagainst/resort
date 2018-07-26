import unittest
import pathlib
import sys

from resort.engine import ResortEngine
from resort.project import ResortProject


class TestBasicRESTServer(unittest.TestCase):

    def test_resort_all(self):
        curdir = pathlib.Path(__file__)
        self.assertTrue(curdir.is_file)
        # rp = ResortProject()
        # ResortEngine.check()


if __name__ == '__main__':
    unittest.main()
