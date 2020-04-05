import unittest
from src.quicksort_parallel import QuickSortParallelWorker


class TestQuickSortParallelWorker(unittest.TestCase):
	def test_initialization(self):
		with self.assertRaises(RuntimeError):
			QuickSortParallelWorker(-1, [])
		with self.assertRaises(RuntimeError):
			QuickSortParallelWorker(0, 23)
		QuickSortParallelWorker(0, [])
