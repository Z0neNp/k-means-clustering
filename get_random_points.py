import sys
import random


legal_command_example = "An example of legal run:\nget_random_points.py 10000 points"
if len(sys.argv) < 3:
	print(legal_command_example)
	exit(1)
amount = int(sys.argv[1])
if type(amount) is not int or not amount > 0:
	print("Expected amount of points to be a positive integer")
	print(legal_command_example)
	exit(1)
filename = sys.argv[2]
if type(filename) is not str or not len(filename) > 0:
	print("Expected the filename to be a string with at least one character")
	print(legal_command_example)
	exit(1)

output = open(f"assets/{filename}.txt", 'w')
output.write(f"{amount}\n")
for count in range(1, amount + 1):
	output.write(f"{random.randrange(-1000, 1000)} {random.randrange(-1000, 10000)}\n")
output.close()
