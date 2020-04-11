from unittest import TestLoader, TextTestRunner, TestSuite
from test.quicksort_points import TestQuickSortPoints
from test.quick_sort_parallel import TestQuickSortParallel
from test.quick_sort_parallel_worker import TestQuickSortParallelWorker
from test.k_means_clustering import TestKmeansClusteringParallel

if __name__ == '__main__':
	loader = TestLoader()
	suite = TestSuite([
		loader.loadTestsFromTestCase(TestQuickSortPoints),
		loader.loadTestsFromTestCase(TestQuickSortParallel),
		loader.loadTestsFromTestCase(TestQuickSortParallelWorker),
		loader.loadTestsFromTestCase(TestKmeansClusteringParallel)
	])
	runner = TextTestRunner(verbosity=2)
	runner.run(suite)
