import unittest


class ImportsTestCase(unittest.TestCase):

    def test_root_import(self):
        import resort
        self.assertIsNotNone(resort)

    def test_packages(self):
        from resort import etalons
        self.assertIsNotNone(etalons.BaseComparator)
        self.assertIsNotNone(etalons.BaseEtalon)
        self.assertIsNotNone(etalons.BasicHTTPResponseEtalon)
        self.assertIsNotNone(etalons.EtalonIO)

    def test_modules(self):
        from resort import engine
        self.assertIsNotNone(engine.ResortEngine)

        from resort import project
        self.assertIsNotNone(project.ResortProject)


if __name__ == '__main__':
    unittest.main()
