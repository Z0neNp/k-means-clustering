from unittest import TestLoader, TextTestRunner, TestSuite
from test.quicksort_points import TestQuickSortPoints

if __name__ == '__main__':
	loader = TestLoader()
	suite = TestSuite([
		loader.loadTestsFromTestCase(TestQuickSortPoints)
	])
	runner = TextTestRunner(verbosity=2)
	runner.run(suite)
