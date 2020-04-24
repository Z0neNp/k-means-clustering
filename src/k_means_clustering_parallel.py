import multiprocessing
from math import floor, pi
from src.quicksort_parallel import QuickSortParallel
from src.quicksort import QuickSort


class KmeansClusteringSlave(multiprocessing.Process):
	def __init__(self, tasks_queue, results_queue):
		multiprocessing.Process.__init__(self)
		try:
			self.tasks_queue = tasks_queue
			self.results_queue = results_queue
		except RuntimeError as err:
			err_msg = f"Failed to initialize the KmeansClusteringSlave object. Reason:\n\t{str(err)}"
			raise RuntimeError(err_msg)

	@property
	def results_queue(self):
		return self._results_queue

	@property
	def tasks_queue(self):
		return self._tasks_queue

	@results_queue.setter
	def results_queue(self, results_queue):
		if type(results_queue) is multiprocessing.queues.Queue:
			self._results_queue = results_queue
		else:
			raise RuntimeError("results_queue expected to be of type multiprocessing.queues.Queue")

	@tasks_queue.setter
	def tasks_queue(self, tasks_queue):
		if type(tasks_queue) is multiprocessing.queues.JoinableQueue:
			self._tasks_queue = tasks_queue
		else:
			print(f"Actual type is {type(tasks_queue)}")
			raise RuntimeError("tasks_queue expected to be of type multiprocessing.queues.JoinableQueue")

	def run(self):
		while True:
			next_task = self.tasks_queue.get()
			if next_task is None:
				self.tasks_queue.task_done()
				break
			else:
				cluster_center = None
				radius = None
				if len(next_task) < 1:
					pass
				elif len(next_task) < 2:
					cluster_center = next_task[0]
					radius = 0
				else:
					for point in next_task:
						potential_center = point
						potential_radius = None
						for point_ref in next_task:
							if potential_center != point_ref:
								distance = point.distance(point_ref)
								if potential_radius is None or potential_radius < distance:
									potential_radius = distance
						if cluster_center is None and radius is None or radius > potential_radius:
							cluster_center = potential_center
							radius = potential_radius
				if cluster_center is not None and radius is not None:
					self.results_queue.put((cluster_center, 2 * pi * radius))
				self.tasks_queue.task_done()


class KmeansClusteringMaster:
	def __init__(self, clusters_count, points, threads_count, processes_count):
		try:
			self.clusters_count = clusters_count
			self.points = points
			self.threads_count = threads_count
			self.processes_count = processes_count
			self._results = multiprocessing.Queue()
			self._tasks = multiprocessing.JoinableQueue()
			self._centers = []
			self._diameters = []
			self._precision = 0
		except RuntimeError as err:
			err_msg = f"Failed to initialize the KmeansClusteringMaster. Reason:\n\t{str(err)}"
			raise RuntimeError(err_msg)

	@property
	def clusters_count(self):
		return self._clusters_count

	@property
	def points(self):
		return self._points

	@property
	def processes_count(self):
		return self._processes_count

	@property
	def threads_count(self):
		return self._threads_count

	@clusters_count.setter
	def clusters_count(self, clusters_count):
		if type(clusters_count) is int and clusters_count > 0:
			self._clusters_count = clusters_count
		else:
			raise RuntimeError("Expected clusters_count to be a positive integer.")

	@points.setter
	def points(self, points):
		if type(points) is list:
			self._points = points
		else:
			raise RuntimeError("Expected points to be a list")

	@processes_count.setter
	def processes_count(self, processes_count):
		if type(processes_count) is int and processes_count > 0:
			self._processes_count = processes_count
		else:
			raise RuntimeError("Expected the processes_count to be a positive integer.")

	@threads_count.setter
	def threads_count(self, threads_count):
		if type(threads_count) is int:
			self._threads_count = threads_count
		else:
			raise RuntimeError("Expected the threads_count to be an integer.")

	def run(self):
		try:
			self._quick_sort()
			print("===>\tpoints have been sorted\t<===")
			print(f"\tsorting method:\tquick_sort paralleled with {self.threads_count} threads")
			print("\tsorting order:\tascending")
			print("\tsorted by:\tdistance from the [0, 0] coordinate")
			self._init_slaves()
			print("===>\tKMeansClusteringSlaves have been initiated\t<===")
			print(f"\tamount of slaves:\t{len(self._slaves)}")
			print(f"\tprocesses per slave:\t1")
			self._start_slaves()
			print("===>\tKMeansClusteringSlaves have started their execution\t<===")
			self._init_tasks()
			print("===>\ttasks have been enqueued for the KMeansClusteringSlaves\t<===")
			print(f"\tamount of tasks:\t{self._tasks.qsize()}")
			self._kill_slaves()
			print("===>\tpoison pills have been enqueued for the KMeansClusteringSlaves\t<===")
			self._tasks.join()
			self._tasks.close()
			self._stop_slaves()
			print("===>\tKMeansClusteringSlaves have stopped their execution\t<===")
			self._update_centers_and_diameters()
			self._update_precision()
			print("\t{0:20}|{1:^20}".format("cluster center", "cluster diameter"))
			for i in range(0, len(self._centers)):
				print("\t{0:20}|{1:^20.2f}".format(str(self._centers[i]), self._diameters[i]))
			print("\tprecision is {0:.2f}".format(self._precision))
		except RuntimeError as err:
			print(f"KmeansClusteringMaster failed to run. Reason:\n\t{str(err)}")

	# private

	def _init_slaves(self):
		self._slaves = []
		for n in range(0, self.processes_count):
			self._slaves.append(KmeansClusteringSlave(self._tasks, self._results))

	def _init_tasks(self):
		points_per_cluster = self._points_per_cluster()
		for n in range(0, self.clusters_count):
			next_low = points_per_cluster * n
			next_high = next_low + points_per_cluster
			self._tasks.put(self.points[next_low:next_high])

	def _kill_slaves(self):
		for n in range(0, self.processes_count):
			self._tasks.put(None)

	def _points_per_cluster(self):
		return floor(len(self.points) / self.clusters_count)

	def _quick_sort(self):
		if self.threads_count > 1:
			qsp = QuickSortParallel(self.points, self.threads_count)
			result = qsp.sort()
		else:
			qs = QuickSort(self.points)
			qs.sort()
			result = qs.elements
		if len(result) != len(self.points):
			err_msg = "the sorted points returned by QuickSortParallel object do not"
			err_msg += " contain all the original points."
			raise RuntimeError(err_msg)
		self.points = result

	def _start_slaves(self):
		for s in self._slaves:
			s.start()

	def _stop_slaves(self):
		for s in self._slaves:
			s.join()
			s.close()

	def _update_centers_and_diameters(self):
		while not self._results.empty():
			result = self._results.get()
			self._centers.append(result[0])
			self._diameters.append(result[1])

	def _update_precision(self):
		for i in range(0, len(self._centers)):
			point = self._centers[i]
			diameter = self._diameters[i]
			point_precision = 0
			for point_ref in self._centers:
				if point != point_ref:
					point_precision += diameter / point.distance(point_ref)
			self._precision += point_precision
