from unittest import TestCase

from main import solution_part_1


class Test(TestCase):
    def test_solution_part_1(self):
        self.assertEqual(solution_part_1("testData.txt"), 2)
