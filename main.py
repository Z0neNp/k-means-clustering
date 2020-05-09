import multiprocessing
import os
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import random
from timeit import default_timer as timer
from src.point import Point
from src.k_means_clustering_parallel import KmeansClusteringMaster

###
# This is the main script that needs to be executed.
# At the beginning of the main you can set different configurations, i.e.
# amount of points to work with, amount of clusters to calculate.
#
# The script execution starts with generating random XY points to work with.
#
# Later the configuration runs are created, iterated and sent as agurments to the
# execute_clustering method which calculates the clusters.
# Each configuration differs in the amount of processes and threads used.
# The points that are used for clustering are the same for each configuration.
#
# The data about each run is stored in a dedicated file in the assets directory.
# The data includes amount of processes, threads per process, execution time,
# found clusters, their diameter and the quality of the clustering.
# ###


def execute_clustering(configuration):
	input_file = open(f"assets/{configuration['file_with_points']}.txt")
	expected_points_count = int(input_file.readline())
	points = []
	for line in input_file:
		line = line.partition(' ')
		points.append(Point(int(line[0]), int(line[2])))
	if expected_points_count != len(points):
		err_msg = "Expected points count is different from the actually loaded points count."
		raise RuntimeError(err_msg)
	print("==>\tXY points have been successfully loaded\t<===")
	print(f"\t\tamount of points:\t{len(points)}")
	kmc = KmeansClusteringMaster(
		configuration["clusters"],
		points,
		configuration["threads_per_process"],
		configuration["processes"]
	)
	kmc.run()
	return kmc.centers, kmc.diameters, kmc.precision


def generate_random_points(destination, amount, min_coord=-1000, max_coord=1000):
	output_file = open(f"assets/{destination}.txt", 'w')
	output_file.write(f"{amount}\n")
	for count in range(1, amount + 1):
		output_file.write(
			f"{random.randrange(min_coord, max_coord)} {random.randrange(min_coord, max_coord)}\n"
		)
	output_file.close()


def render_graphical_stats(points_filename):
	li = []
	with os.scandir(f"assets/") as files:
		for file in files:
			print(f"Revealed the file:\t{str(file)}")
			if str(file) != f"<DirEntry '{points_filename}.txt'>":
				input_file = open(file)
				data = input_file.readline()
				input_file.close()
				df = pd.read_csv(
					StringIO(data),
					delim_whitespace=True,
					header=None,
					names=['N of processes', 'N of threads', 'Time in seconds']
				)
				li.append(df)
	frame = pd.concat(li, axis=0, ignore_index=True)
	print(frame)
	ax = frame.plot(kind='bar', grid=True, title='Processes, threads, time - graph')
	ax.set_xlabel("N of try")
	ax.set_ylabel("")
	plt.show()


if __name__ == '__main__':
	multiprocessing.freeze_support()
	print(f"==========Started the K Means Parallel Clustering==========")
	points_amount = 10000
	clusters = 3
	file_with_points_to_cluster = "points"
	pc_physical_cores = multiprocessing.cpu_count()
	generate_random_points(file_with_points_to_cluster, points_amount)
	configurations = [
		{
			"clusters": clusters,
			"file_with_points": file_with_points_to_cluster,
			"processes": 1,
			"threads_per_process": 1
		}
	]
	for i in range(0, multiprocessing.cpu_count() * 2):
		configurations.append(
			{
				"clusters": clusters,
				"file_with_points": file_with_points_to_cluster,
				"processes": pc_physical_cores,
				"threads_per_process": i + 1
			}
		)
	try:
		for config in configurations:
			start = timer()
			centers, diameters, precision = execute_clustering(config)
			end = timer()
			filename = f"assets/stats_{config['processes']}_processes"
			filename += f"_{config['threads_per_process']}_threads_per_process.txt"
			output = open(filename, 'w')
			log = f"%d %d %.2f\n" % (
				config['processes'],
				config['threads_per_process'],
				end - start
			)
			log += "\t{0:20}|{1:^20}\n".format("cluster center", "cluster diameter")
			for i in range(0, len(centers)):
				log += "\t{0:20}|{1:^20.2f}\n".format(str(centers[i]), diameters[i])
			log += "\tprecision is {0:.2f}\n".format(precision)
			output.write(log)
			output.close()
			print("===>\tstatistical data has been stored\t<===")
			print(f"\t\tThe destination filename:\t{filename}")
			print("=========================================================")
		render_graphical_stats(file_with_points_to_cluster)
	except RuntimeError as err:
		print(f"K Means Parallel Clustering has failed.\n\t{str(err)}")
		exit(1)
	finally:
		print("==========Ended the K Means Parallel Clustering==========")
		print("=========================================================")
