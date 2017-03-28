import unittest
from raspi.read import get_vals, get_means, get_clusters


LINE = b'S:1023|983|834|234|324|456|363|1023|1045|\n'
TEST_DATA = [1023, 983, 834, 234, 324, 456, 363, 1023, 1045]


class ReadRaspiTestCase(unittest.TestCase):
    def setUp(self):
        self.a = TEST_DATA

    def tearDown(self):
        pass

    def test_get_vals(self):
        res = get_vals(LINE)
        expected = [1023, 983, 834, 234, 324, 456, 363, 1023, 1045]
        self.assertEqual(expected, res)

    def test_get_means(self):
        res = get_means(self.a, 4)

    def test_integration(self):
        row = b'S:1023|983|834|675|698|456|234|324|456|363|1023|1045|982|763|674|743\n'
        arr = get_vals(row)
        print(arr)
        print()
        clusters = get_clusters(arr, range_end=500)
        print(clusters)

        # for c in clusters:
        #     print(c)

