import unittest
from src.k_means_clustering_parallel import KmeansClusteringMaster


class TestKmeansClusteringParallel(unittest.TestCase):
	def test_initialization(self):
		KmeansClusteringMaster(3, 5.9, [], 4, 5)
		with self.assertRaises(RuntimeError):
			KmeansClusteringMaster(0, 5.9, [], 4, 5)
		with self.assertRaises(RuntimeError):
			KmeansClusteringMaster(3, 2, [], 4, 5)
		with self.assertRaises(RuntimeError):
			KmeansClusteringMaster(0, 0, [], 4, 5)
		with self.assertRaises(RuntimeError):
			KmeansClusteringMaster(0, 5.9, None, 4, 5)
		with self.assertRaises(RuntimeError):
			KmeansClusteringMaster(0, 5.9, [], 0, 5)
		with self.assertRaises(RuntimeError):
			KmeansClusteringMaster(0, 5.9, [], 4, 0)
