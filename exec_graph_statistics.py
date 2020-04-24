import os
import pandas as pd
import matplotlib.pyplot as plt

li = []
with os.scandir(f"assets/") as files:
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