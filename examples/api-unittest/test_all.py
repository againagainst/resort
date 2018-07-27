import unittest
import pathlib

from resort.engine import ResortEngine
from resort.project import ResortProject


class TestBasicRESTServer(unittest.TestCase):

    def test_resort_all(self):
        project_dir = pathlib.Path(__file__).parent
        rp = ResortProject.read(project_dir)
        self.assertIsNotNone(rp)
        check_result = ResortEngine.check(rp)
        self.assertEqual(check_result['changes'], 0,
                         'There are differences in the response')


if __name__ == '__main__':
    unittest.main()
