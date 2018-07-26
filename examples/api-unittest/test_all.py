import unittest
import pathlib

from resort.engine import ResortEngine
from resort.project import ResortProject


class TestBasicRESTServer(unittest.TestCase):

    def test_resort_all(self):
        curfile = pathlib.Path(__file__)
        self.assertTrue(curfile.is_file())

        project_dir = curfile.parent
        self.assertTrue(project_dir.is_dir())

        rp = ResortProject(project_dir)
        self.assertIsNotNone(rp)
        ResortEngine.check(rp)


if __name__ == '__main__':
    unittest.main()
