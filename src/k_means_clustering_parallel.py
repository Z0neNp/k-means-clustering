import multiprocessing
import threading
from math import floor, pi
from src.point import Point
from src.quicksort_parallel import QuickSortParallel
from src.quicksort import QuickSort


def find_local_center_with_greatest_radius(cluster_center, radius, potential_centers, points):
	###
	# The method receives points and finds a center among them.
	# The center point has the largest possible radius among all the points.
	###
	for point in potential_centers:
		potential_center = point
		potential_radius = None
		for point_ref in points:
			if potential_center != point_ref:
				distance = point.distance(point_ref)
				if potential_radius is None:
					potential_radius = distance
				elif potential_radius < distance:
					potential_radius = distance
		if cluster_center is None and radius is None:
			cluster_center = potential_center
			radius = potential_radius
		elif cluster_center is None or radius is None:
			raise RuntimeError("Corrupted cluster_center and radius")
		elif radius < potential_radius:
			cluster_center = potential_center
			radius = potential_radius
	return cluster_center, radius


class KmeansClusteringSlaveWorker(threading.Thread):
	###
	# This is a thread object that receives a collection of points
	# and possible centers for a cluster that will include all of the points.
	#
	# The run method will calculate the largest radius from the possible centers
	# and store it, along with the center for the KmeansClusteringSlave to retrieve
	# the values.
	###
	def __init__(self, thread_id, potential_centers, points):
		threading.Thread.__init__(self)
		try:
			self.thread_id = thread_id
			self._potential_centers = potential_centers
			self._points = points
		except RuntimeError as err:
			err_msg = f"Failed to initialize KmeansClusteringSlaveWorker object."
			err_msg += " The Reason:\n\t{str(err)}"
			raise RuntimeError(err_msg)
		self._center = None
		self._error = None
		self._radius = None

	@property
	def center(self):
		return self._center

	@property
	def error(self):
		return self._error

	@property
	def radius(self):
		return self._radius

	@property
	def thread_id(self):
		return self._thread_id

	@center.setter
	def center(self, center):
		if type(center) is Point:
			self._center = center
		else:
			raise RuntimeError("Expected center to be of type Point.")

	@error.setter
	def error(self, err):
		if type(err) is str:
			self._error = err
		else:
			self._error = f"Tried to set error message with non string object:\n\t{str(err)}"

	@radius.setter
	def radius(self, radius):
		if type(radius) is int or type(radius) is float:
			self._radius = radius
		else:
			raise RuntimeError("Expected the radius to be a number.")

	@thread_id.setter
	def thread_id(self, thread_id):
		if type(thread_id) is int and thread_id >= 0:
			self._thread_id = thread_id
		else:
			raise RuntimeError("Expected thread_id must be a non negative integer.")

	# override methods

	def run(self):
		try:
			cluster_center = None
			radius = None
			cluster_center, radius = find_local_center_with_greatest_radius(
				cluster_center,
				radius,
				self._potential_centers,
				self._points
			)
			self.center = cluster_center
			self.radius = radius
		except Exception as err:
			err_msg = "KmeansClusteringSlaveWorker has failed to find potential center and radius."
			err_msg += f" The Reason:\n\t{str(err)}"
			self.error = err_msg


class KmeansClusteringSlave(multiprocessing.Process):
	###
	# This is a process object that receives amount of the threads it is allowed to use,
	# a two queues shared among the process.
	# The first queue will hold the result of the processes' calculations,
	# the second queue holds the tasks for the processes' to calculate.
	#
	# The run method will pull the tasks from the tasks queue until there are none.
	# Each task contains a collection of points that represent a cluster.
	# One of the points should be chosen as a center that covers all the points.
	#
	# The task will divided among the KmeansClusteringSlaveWorker objects.
	# The amount of objects is limited by the amount of threads available.
	# Each object receives a part of the points to iterate that part and find
	# a potential center.
	# Once all the objects conclude their execution, KmeansClusteringSlave chooses
	# the optimal center and radius among all the potential data.
	###
	def __init__(self, tasks_queue, results_queue, threads_count):
		multiprocessing.Process.__init__(self)
		try:
			self.tasks_queue = tasks_queue
			self.results_queue = results_queue
			self.threads_count = threads_count
			self._workers = []
			self.used_threads = False
		except Exception as err:
			err_msg = f"Failed to initialize the KmeansClusteringSlave object."
			err_msg += " The Reason:\n\t{str(err)}"
			raise RuntimeError(err_msg)

	@property
	def results_queue(self):
		return self._results_queue

	@property
	def tasks_queue(self):
		return self._tasks_queue

	@property
	def threads_count(self):
		return self._threads_count

	@property
	def workers(self):
		return self._workers

	@results_queue.setter
	def results_queue(self, results_queue):
		if type(results_queue) is multiprocessing.queues.Queue:
			self._results_queue = results_queue
		else:
			err_msg = "results_queue expected to be of type multiprocessing.queues.Queue"
			raise RuntimeError(err_msg)

	@tasks_queue.setter
	def tasks_queue(self, tasks_queue):
		if type(tasks_queue) is multiprocessing.queues.JoinableQueue:
			self._tasks_queue = tasks_queue
		else:
			err_msg = "tasks_queue expected to be of type multiprocessing.queues.JoinableQueue"
			raise RuntimeError(err_msg)

	@threads_count.setter
	def threads_count(self, threads_count):
		if type(threads_count) is int and threads_count > 0:
			self._threads_count = threads_count
		else:
			raise RuntimeError("Expected the threads_count to a positive integer.")

	def run(self):
		while True:
			next_task = self.tasks_queue.get()
			if next_task is None:
				self.tasks_queue.task_done()
				break
			elif len(next_task) < 1:
				self.tasks_queue.task_done()
				continue
			elif len(next_task) < 2:
				self.results_queue.put((next_task[0], 0))
				self.tasks_queue.task_done()
				continue
			else:
				try:
					cluster_center = None
					radius = None
					if self.used_threads:
						cluster_center, radius = find_local_center_with_greatest_radius(
							cluster_center,
							radius,
							next_task,
							next_task
						)
					else:
						self.used_threads = True
						self._init_workers(next_task)
						for worker in self.workers:
							worker.start()
						for worker in self.workers:
							worker.join()
						cluster_center, radius = self._process_worker_results()
					self.results_queue.put((cluster_center, 2 * pi * radius))
				except Exception as err:
					err_msg = f"KmeansClusteringSlave has failed. The Reason:\n\t{str(err)}"
					self.results_queue.put(RuntimeError(err_msg))
				finally:
					self.tasks_queue.task_done()

	# private

	def _add_worker(self, worker):
		self._workers.append(worker)

	def _init_workers(self, task):
		points_per_thread = floor(len(task) / self.threads_count)
		counter = 0
		low = 0
		high = points_per_thread + 1
		while counter < self.threads_count - 1:
			self._add_worker(KmeansClusteringSlaveWorker(counter, task[low:high], task))
			low = high
			high = low + points_per_thread
			counter += 1
		self._add_worker(KmeansClusteringSlaveWorker(counter, task[low:len(task)], task))

	def _process_worker_results(self):
		cluster_center = None
		radius = None
		for worker in self.workers:
			if worker.error:
				err_msg = f"KmeansClusteringSlave has failed. The Reason:\n\t{worker.error}"
				self.results_queue.put(RuntimeError(err_msg))
				return None, None
			else:
				if cluster_center is None and radius is None:
					cluster_center = worker.center
					radius = worker.radius
				elif cluster_center is None or radius is None:
					err_msg = "KmeansClusteringSlave has failed"
					err_msg += " because the KmeansClusteringSlaveWorker"
					err_msg += f" {worker.thread_id} has reported corrupted data."
					self.results_queue.put(RuntimeError(err_msg))
					return None, None
				elif radius < worker.radius:
					cluster_center = worker.center
					radius = worker.radius
		return cluster_center, radius


class KmeansClusteringMaster:
	###
	# The object receives the points for which clusters are to be found.
	# It assumes that the points are ordered in the ascending order.
	#
	# The order assumption is used during the dividing of the points into smaller
	# tasks that are executed by the KmeansClusteringSlave objects.
	#
	# During the run method KmeansClusteringSlave objects are initiated according to the
	# processes_count value. It passes the tasks into the queue shared among the slaves
	# and retrieves their results from another shared queue.
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
	def centers(self):
		return self._centers

	@property
	def clusters_count(self):
		return self._clusters_count

	@property
	def diameters(self):
		return self._diameters

	@property
	def points(self):
		return self._points

	@property
	def precision(self):
		return self._precision

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
		if type(threads_count) is int and threads_count > 0:
			self._threads_count = threads_count
		else:
			raise RuntimeError("Expected the threads_count to be a positive integer.")

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
			print(f"\tprocesses per slave:\t{self.threads_count}")
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
		except RuntimeError as err:
			raise RuntimeError(f"KmeansClusteringMaster failed to run. The Reason:\n\t{str(err)}")

	# private

	def _init_slaves(self):
		self._slaves = []
		for n in range(0, self.processes_count):
			self._slaves.append(KmeansClusteringSlave(self._tasks, self._results, self.threads_count))

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
			if type(result) is RuntimeError:
				raise result
			else:
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
