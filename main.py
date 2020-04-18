import json
import multiprocessing
from timeit import default_timer as timer
from src.point import Point
from src.k_means_clustering_parallel import KmeansClusteringMaster

if __name__ == '__main__':
	multiprocessing.freeze_support()
	print("\n\n===========================================================")
	print(f"==========Started the K Means Parallel Clustering==========")
	try:
		with open("config.json", "r") as f:
			config = json.load(f)
	except RuntimeError as err:
		print(f"Failed to read the configuration file. Reason:\n\t{str(err)}")
		exit(1)
	print("\n===>\tThe configurations have been successfully loaded\t<===")
	print(f"\tfile with the points:\t./assets/{config['file_with_points']}")
	print(f"\t# of clusters:\t{config['clusters']}")
	print(f"\tminimal precision per cluster:\t{config['min_precision']}")
	print(f"\t# of processes:\t{config['processes']}")
	print(f"\t# of threads per process:\t{config['threads']}")

	try:
		input_file = open(f"assets/{config['file_with_points']}.txt")
		expected_points_count = int(input_file.readline())
		points = []
		for line in input_file:
			line = line.partition(' ')
			points.append(Point(int(line[0]), int(line[2])))
		if expected_points_count != len(points):
			raise RuntimeError("Expected points count is different from the actually loaded points count.")
	except RuntimeError as err:
		print(f"Failed to load the points. Reason:\n\t{str(err)}")
		exit(1)
	print("\n==>\tXY points have been successfully loaded\t<===")
	print(f"\tamount of points:\t{len(points)}")

	start = timer()
	kmc = KmeansClusteringMaster(
		config["clusters"],
		config["min_precision"],
		points,
		config["threads"],
		config["processes"]
	)
	kmc.run()
	end = timer()

	filename = f"assets/stats_{config['processes']}_processes"
	filename += f"_{config['threads']}_threads_per_process.txt"
	output = open(filename, 'w')
	data = f"%d %d %.2f" % (config['processes'], config['threads'], end - start)
	output.write(data)
	output.close()
	print("\n===>\tstatistical data has been stored\t<===")
	print(f"\tlocation:\t{filename}")
	msg = f"\t{config['processes']} processes"
	msg += f" - {config['threads']} threads per process"
	msg += " - %.2f execution time in seconds" % (end-start)
	print(msg)

	print("\n\n==========Ended the K Means Parallel Clustering==========")
	print("=========================================================")


	print('#########################_DON_MARCHELLO_##################################')

	import os
	import pandas as pd
	import matplotlib.pyplot as plt

	li = []
	with os.scandir('C:/Users/marat/k-means-clustering/assets/') as files:
		for file in files:
			print(str(file))
			if str(file) != "<DirEntry 'points.txt'>":
				df = pd.read_csv(file, delim_whitespace=True, header=None, names=['N of processes', 'N of threads', 'Time in seconds'])
				li.append(df)

	frame = pd.concat(li, axis=0, ignore_index=True)

	print(frame)
	ax = frame.plot(kind='bar', grid=True, title='Processes, threads, time - graph')
	ax.set_xlabel("N of try")
	ax.set_ylabel("")
	plt.show()

