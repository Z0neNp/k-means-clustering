class QuickSort:
	def __init__(self, elements):
		try:
			self.elements = elements
		except Exception as err:
			err_msg = f"Failed to initialize the QuickSort object. The reason:\n\t{str(err)}"
			raise RuntimeError(err_msg)

	@property
	def elements(self):
		return self._elements

	@elements.setter
	def elements(self, elements):
		if type(elements) is list:
			self._elements = elements
		else:
			raise RuntimeError("Elements for quick sort should be of the type list.")

	def sort(self):
		low = 0
		high = len(self.elements) - 1
		try:
			self._sort_helper(low, high)
		except Exception as err:
			err_msg = f"QuickSort has failed to sort the elements. The reason:\n\t{str(err)}"
			raise RuntimeError(err_msg)

	# private methods

	def _partition(self, low, high):
		pivot = self.elements[high]
		index_for_smallest = low - 1
		for i in range(low, high):
			if self.elements[i] < pivot:
				index_for_smallest += 1
				self._swap(index_for_smallest, i)
		index_for_smallest += 1
		self._swap(index_for_smallest, high)
		return index_for_smallest

	def _sort_helper(self, low, high):
		if low < high:
			try:
				partition_index = self._partition(low, high)
			except Exception as err:
				err_msg = "Failed to get the partition index with"
				err_msg += f"\n\tlow:\t{low}\n\thigh:\t{high}. The reason:\n\t{str(err)}"
				raise RuntimeError(err_msg)
			try:
				self._sort_helper(low, partition_index - 1)
			except Exception as err:
				err_msg = "Failed at the recursive sort_helper with"
				err_msg += f"\n\tlow:\t{low}\n\tfollowed by partition index:\t{partition_index - 1}"
				err_msg += f"The reason:\n\t{str(err)}"
				raise RuntimeError(err_msg)
			try:
				self._sort_helper(partition_index + 1, high)
			except Exception as err:
				err_msg = "Failed at the recursive sort_helper with"
				err_msg += f"\n\tfollowing the partition index:\t#{partition_index + 1}\n\thigh:\t{high}"
				err_msg += f"The reason:\n\t{str(err)}"
				raise RuntimeError(err_msg)

	def _swap(self, a, b):
		temp_element = self.elements[a]
		self.elements[a] = self.elements[b]
		self.elements[b] = temp_element


if __name__ == '__main__':
	import unittest


	class TestQuickSort(unittest.TestCase):
		def test_initialization(self):
			with self.assertRaises(RuntimeError):
				QuickSort(None)
			QuickSort([])

		def test_empty_list_sort(self):
			a = QuickSort([])
			a.sort()
			self.assertEqual(a.elements, [])

		def test_list_with_one_element_sort(self):
			a = QuickSort([1])
			a.sort()
			self.assertEqual(a.elements, [1])

		def test_list_with_two_elements_sort(self):
			a = QuickSort([2, 1])
			a.sort()
			self.assertEqual(a.elements[0], 1)
			self.assertEqual(a.elements[1], 2)

		def test_list_with_three_elements_sort(self):
			a = QuickSort([2, 1, 3])
			a.sort()
			self.assertEqual(a.elements[0], 1)
			self.assertEqual(a.elements[1], 2)
			self.assertEqual(a.elements[2], 3)

		def test_list_with_four_elements_sort(self):
			a = QuickSort([2, 1, 3, 4])
			a.sort()
			self.assertEqual(a.elements[0], 1)
			self.assertEqual(a.elements[1], 2)
			self.assertEqual(a.elements[2], 3)
			self.assertEqual(a.elements[3], 4)

		def test_list_with_eight_elements_sort(self):
			a = QuickSort([2, 1, 3, 4, 8, 7, 6, 5])
			a.sort()
			self.assertEqual(a.elements[0], 1)
			self.assertEqual(a.elements[1], 2)
			self.assertEqual(a.elements[2], 3)
			self.assertEqual(a.elements[3], 4)
			self.assertEqual(a.elements[4], 5)
			self.assertEqual(a.elements[5], 6)
			self.assertEqual(a.elements[6], 7)
			self.assertEqual(a.elements[7], 8)


	unittest.main()
