import unittest
from src.point import Point
from src.quicksort_parallel import QuickSortParallel


class TestQuickSortParallel(unittest.TestCase):
	def test_initialization(self):
		with self.assertRaises(RuntimeError):
			QuickSortParallel(23, 1)
		with self.assertRaises(RuntimeError):
			QuickSortParallel([], 0)
		with self.assertRaises(RuntimeError):
			QuickSortParallel([], 1)
		QuickSortParallel([], 2)

	def test_empty_elements_sort(self):
		qsp = QuickSortParallel([], 2)
		self.assertEqual(qsp.sort(), [])

	def test_single_element_sort(self):
		qsp = QuickSortParallel([Point(1, 1)], 2)
		self.assertEqual(qsp.sort(), [Point(1, 1)])

	def test_two_elements_sort(self):
		qsp = QuickSortParallel([Point(1, 1), Point(1, 2)], 2)
		self.assertEqual(qsp.sort(), [Point(1, 1), Point(1, 2)])
		qsp = QuickSortParallel([Point(1, 1), Point(2, 1)], 2)
		self.assertEqual(qsp.sort(), [Point(1, 1), Point(2, 1)])
		qsp = QuickSortParallel([Point(2, 1), Point(1, 1)], 2)
		self.assertEqual(qsp.sort(), [Point(1, 1), Point(2, 1)])
		qsp = QuickSortParallel([Point(1, 2), Point(1, 1)], 2)
		self.assertEqual(qsp.sort(), [Point(1, 1), Point(1, 2)])

	def test_three_elements_sort(self):
		qsp = QuickSortParallel([Point(1, 1), Point(-3, -3), Point(1, 2)], 2)
		self.assertEqual(qsp.sort(), [Point(1, 1), Point(1, 2), Point(-3, -3)])
		qsp = QuickSortParallel([Point(-3, -3), Point(1, 1), Point(1, 2)], 4)
		self.assertEqual(qsp.sort(), [Point(1, 1), Point(1, 2), Point(-3, -3)])
		qsp = QuickSortParallel([Point(1, 2), Point(-3, -3), Point(1, 1)], 6)
		self.assertEqual(qsp.sort(), [Point(1, 1), Point(1, 2), Point(-3, -3)])

	def test_four_elements(self):
		qsp = QuickSortParallel([Point(1, 1), Point(-3, -3), Point(1, 2), Point(4, 4)], 2)
		self.assertEqual(qsp.sort(), [Point(1, 1), Point(1, 2), Point(-3, -3), Point(4, 4)])
		qsp = QuickSortParallel([Point(4, 4), Point(-3, -3), Point(1, 2), Point(1, 1)], 4)
		self.assertEqual(qsp.sort(), [Point(1, 1), Point(1, 2), Point(-3, -3), Point(4, 4)])
		qsp = QuickSortParallel([Point(1, 2), Point(4, 4), Point(-3, -3), Point(1, 1)], 6)
		self.assertEqual(qsp.sort(), [Point(1, 1), Point(1, 2), Point(-3, -3), Point(4, 4)])

	def test_five_elements(self):
		qsp = QuickSortParallel([Point(5, 5), Point(1, 1), Point(-3, -3), Point(1, 2), Point(4, 4)], 2)
		self.assertEqual(qsp.sort(), [Point(1, 1), Point(1, 2), Point(-3, -3), Point(4, 4), Point(5, 5)])
		qsp = QuickSortParallel([Point(1, 1), Point(-3, -3), Point(5, 5), Point(1, 2), Point(4, 4)], 4)
		self.assertEqual(qsp.sort(), [Point(1, 1), Point(1, 2), Point(-3, -3), Point(4, 4), Point(5, 5)])
		qsp = QuickSortParallel([Point(1, 1), Point(-3, -3), Point(5, 5), Point(4, 4), Point(1, 2)], 1000)
		self.assertEqual(qsp.sort(), [Point(1, 1), Point(1, 2), Point(-3, -3), Point(4, 4), Point(5, 5)])
