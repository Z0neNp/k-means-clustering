import threading
from src.quicksort import QuickSort


# noinspection PyMethodMayBeStatic
class QuickSortParallelWorker(threading.Thread):
	###
	# An object of the QuickSortParallelWorker is a thread object that knows to execute
	# the QuickSort object.
	def __init__(self, thread_id, elements):
		threading.Thread.__init__(self)
		try:
			self.thread_id = thread_id
			self.qs = QuickSort(elements)
		except RuntimeError as err:
			err_msg = f"Failed to initialize QuickSortParallelWorker object. Reason:\n\t{str(err)}"
			raise RuntimeError(err_msg)
		self._error = None

	@property
	def error(self):
		return self._error

	@property
	def qs(self):
		return self._qs

	@property
	def thread_id(self):
		return self._thread_id

	@error.setter
	def error(self, err):
		if type(err) is str:
			self._error = err
		else:
			self._error = f"Tried to set error message with non string object:\n\t{str(err)}"

	@qs.setter
	def qs(self, quick_sort):
		if type(quick_sort) is QuickSort:
			self._qs = quick_sort
		else:
			raise RuntimeError("Expected sorting algorithm to be of type QuickSort.")

	@thread_id.setter
	def thread_id(self, thread_id):
		if type(thread_id) is int and thread_id >= 0:
			self._thread_id = thread_id
		else:
			raise RuntimeError("Expected thread_id must be a non negative integer.")

	# override methods

	def run(self):
		try:
			self.qs.sort()
		except RuntimeError as err:
			self.error = f"Thread {str(self._thread_id)} has failed to run. Reason:\n\t{str(err)}"


class QuickSortParallel:
	###
	# The object performs a parallel sorting of the other objects by breaking the sorting
	# tasks into smaller tasks, executed by the QuickSortParallelWorker objects
	def __init__(self, elements, threads_count):
		try:
			self.elements = elements
		except Exception as err:
			err_msg = "Failed to initialize the QuickSortParallel object"
			err_msg += f" with the elements value. Reason:\n\t{str(err)}"
			raise RuntimeError(err_msg)
		try:
			if threads_count > 0:
				self.threads_count = threads_count
			else:
				raise RuntimeError("threads_count must be greater than 0.")
		except Exception as err:
			err_msg = "Failed to initialize the QuickSortParallel object"
			err_msg += f" with the threads_count value. Reason:\n\t{str(err)}"
			raise RuntimeError(err_msg)
		self._workers = []
		self._partition_values = []

	@property
	def elements(self):
		return self._elements

	@property
	def threads_count(self):
		return self._threads_count

	@property
	def workers(self):
		return self._workers

	@elements.setter
	def elements(self, elements):
		if type(elements) is list:
			self._elements = elements
		else:
			raise RuntimeError("Expected the elements to be a list.")

	@threads_count.setter
	def threads_count(self, threads_count):
		if type(threads_count) is int:
			if threads_count % 2 != 0 and threads_count > 2:
				threads_count -= 1
			if threads_count % 2 == 0:
				if threads_count > len(self.elements) > 0:
					threads_count = len(self.elements)
					if threads_count % 2 != 0:
						threads_count += 1
			self._threads_count = threads_count
		else:
			raise RuntimeError("Expected the threads_count to be an even integer.")

	def sort(self):
		low = 0
		high = len(self.elements) - 1
		if low == high:
			return self.elements
		try:
			self.threads_count -= 2
			self._sort_helper(low, high)
			for worker in self.workers:
				worker.start()
			for worker in self.workers:
				worker.join()
			for worker in self.workers:
				if worker.error:
					err_msg = f"QuickSortParallelWorker {worker.thread_id} has failed."
					err_msg += f" The Reason:\n\t{worker.error}"
					raise RuntimeError(err_msg)
		except Exception as err:
			err_msg = "QuickSortParallel has failed to sort the elements."
			err_msg = f" The reason:\n\t{str(err)}"
			raise RuntimeError(err_msg)
		result = []
		for worker in self.workers:
			for element in worker.qs.elements:
				result.append(element)
		return result

	# private

	def _add_worker(self, worker):
		self._workers.append(worker)

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
		if self.threads_count < 0 or self.threads_count % 2 != 0:
			err_msg = "Failed during the recursive calls."
			err_msg += " The threads_count was not even while expected to be so."
			raise RuntimeError(err_msg)
		if low < high:
			try:
				partition_index = self._partition(low, high)
			except Exception as err:
				err_msg = "Failed to get the partition index with"
				err_msg += f"\n\tlow:\t{low}\n\thigh:\t{high}. The reason:\n\t{str(err)}"
				raise RuntimeError(err_msg)
			self._partition_values.append(self.elements[partition_index])
			if self.threads_count > 4:
				self.threads_count -= 4
				try:
					self._sort_helper(low, partition_index)
				except Exception as err:
					err_msg = "Failed at the recursive sort_helper with"
					err_msg += f"\n\tlow:\t{low}\n\tfollowed by partition index:\t{partition_index - 1}"
					err_msg += f"The reason:\n\t{str(err)}"
					raise RuntimeError(err_msg)
				try:
					self._sort_helper(partition_index + 1, high)
				except Exception as err:
					err_msg = "Failed at the recursive sort_helper with"
					err_msg += f"\n\tfollowing the partition index:\t#{partition_index + 1}\n\t"
					err_msg += "high:\t{high}"
					err_msg += f"The reason:\n\t{str(err)}"
					raise RuntimeError(err_msg)
			else:
				self._add_worker(
					QuickSortParallelWorker(self.threads_count, self.elements[low:partition_index])
				)
				self._add_worker(
					QuickSortParallelWorker(self.threads_count, self.elements[partition_index:high + 1])
				)
		elif low == high:
			self._add_worker(
				QuickSortParallelWorker(self.threads_count, [self.elements[low]])
			)
			self._add_worker(
				QuickSortParallelWorker(self.threads_count, [self.elements[high]])
			)

	def _swap(self, a, b):
		temp_element = self.elements[a]
		self.elements[a] = self.elements[b]
		self.elements[b] = temp_element
