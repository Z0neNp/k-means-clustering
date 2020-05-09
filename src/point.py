from math import fabs, pow, sqrt


# noinspection PyMethodMayBeStatic
class Point:
	###
	# The class represents the XY points.
	def __init__(self, x, y):
		try:
			self.x = x
			self.y = y
		except Exception as err:
			err_msg = f"Failed to initialize the Point object. The reason:\n\t{str(err)}"
			raise RuntimeError(err_msg)

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@x.setter
	def x(self, x):
		if self._is_coordinate(x):
			self._x = x
		else:
			raise RuntimeError("The x value is not a proper coordinate")

	@y.setter
	def y(self, y):
		if self._is_coordinate(y):
			self._y = y
		else:
			raise RuntimeError("The y value is not a proper coordinate")

	def distance_to_start(self):
		return fabs(sqrt(pow(self.x, 2) + pow(self.y, 2)))

	def distance(self, other):
		if type(other) is Point:
			return fabs(sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2)))
		else:
			raise RuntimeError("Can not measure distance against a non Point object.")

	# overloaded methods

	def __eq__(self, other):
		if type(other) is Point:
			return self.x == other.x and self.y == other.y
		else:
			return False

	def __gt__(self, other):
		if self.__eq__(other):
			return False
		else:
			return self.distance_to_start() > other.distance_to_start()

	def __lt__(self, other):
		if self.__eq__(other):
			return False
		elif self.__gt__(other):
			return False
		else:
			return self.distance_to_start() < other.distance_to_start()

	def __str__(self):
		return f"[{str(self.x)},{str(self.y)}]"

	# private methods

	def _is_coordinate(self, obj):
		if type(obj) is int:
			return True
		else:
			return False


if __name__ == '__main__':
	import unittest


	class TestPoint(unittest.TestCase):
		def test_initialization(self):
			with self.assertRaises(RuntimeError):
				Point(None, 2)
			with self.assertRaises(RuntimeError):
				Point(2, None)
			with self.assertRaises(RuntimeError):
				Point("1", 2)
			with self.assertRaises(RuntimeError):
				Point(1, "2")
			Point(1, 2)

		def test_str(self):
			self.assertEqual(str(Point(1, 2)), "[1,2]")

		def test_distance(self):
			self.assertEqual(Point(4, 3).distance(Point(0, 0)), 5)

		def test_distance_to_start(self):
			self.assertEqual(Point(4, 3).distance_to_start(), 5)

		def test_equality(self):
			self.assertEqual(Point(4, 3), Point(4, 3))
			self.assertNotEqual(Point(4, 3), Point(3, 4))

		def test_greater_than(self):
			self.assertGreater(Point(4, 4), Point(4, 3))
			self.assertGreater(Point(5, 3), Point(4, 3))
			self.assertGreater(Point(-4, -4), Point(4, 3))
			self.assertGreater(Point(-5, -3), Point(4, 3))

		def test_less_than(self):
			self.assertLess(Point(4, 3), Point(4, 4))
			self.assertLess(Point(4, 3), Point(5, 3))
			self.assertLess(Point(4, 3), Point(-4, -4))
			self.assertLess(Point(4, 3), Point(-5, -3))

	unittest.main()
