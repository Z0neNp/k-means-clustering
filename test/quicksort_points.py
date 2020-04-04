import unittest
from src.point import Point
from src.quicksort import QuickSort


class TestQuickSortPoints(unittest.TestCase):
	def test_quick_sort_points(self):
		points = [
			Point(2, 2),
			Point(10, 10),
			Point(1, 1),
			Point(-9, -9),
			Point(3, 3),
			Point(4, 4)
		]
		qs = QuickSort(points)
		qs.sort()
		self.assertEqual(qs.elements[0], Point(1, 1))
		self.assertEqual(qs.elements[1], Point(2, 2))
		self.assertEqual(qs.elements[2], Point(3, 3))
		self.assertEqual(qs.elements[3], Point(4, 4))
		self.assertEqual(qs.elements[4], Point(-9, -9))
		self.assertEqual(qs.elements[5], Point(10, 10))

	def test_quick_sort_single_point(self):
		points = [
			Point(2, 2),
			Point(1, 1)
		]
		qs = QuickSort(points)
		qs.sort()
		self.assertEqual(qs.elements[0], Point(1, 1))
		self.assertEqual(qs.elements[1], Point(2, 2))

	def test_quick_sort_single_point(self):
		points = [
			Point(2, 2),
			Point(1, 1)
		]
		qs = QuickSort(points)
		qs.sort()
		self.assertEqual(qs.elements[0], Point(1, 1))
		self.assertEqual(qs.elements[1], Point(2, 2))

	def test_quick_sort_three_points(self):
		points = [
			Point(2, 2),
			Point(1, 1),
			Point(0, 0)
		]
		qs = QuickSort(points)
		qs.sort()
		self.assertEqual(qs.elements[0], Point(0, 0))
		self.assertEqual(qs.elements[1], Point(1, 1))
		self.assertEqual(qs.elements[2], Point(2, 2))

	def test_quick_sort_four_points(self):
		points = [
			Point(2, 2),
			Point(1, 1),
			Point(0, 0),
			Point(-3, -3)
		]
		qs = QuickSort(points)
		qs.sort()
		self.assertEqual(qs.elements[0], Point(0, 0))
		self.assertEqual(qs.elements[1], Point(1, 1))
		self.assertEqual(qs.elements[2], Point(2, 2))
		self.assertEqual(qs.elements[3], Point(-3, -3))


if __name__ == '__main__':
	unittest.main()
