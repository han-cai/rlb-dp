stationary_w = []
dimension = 0


def stationary_point_train_basic(points):
	global stationary_w, dimension

	dimension = 2
	stationary_w = [0] * dimension

	X = 0
	XX = 0
	Y = 0
	XY = 0
	N = len(points)

	for i in range(0, N):
		X += points[i][0]
		XX += points[i][0] ** 2
		Y += points[i][1]
		XY += points[i][0] * points[i][1]

	stationary_w[1] = (XY / X - Y / N) / (XX / X - X / N)
	stationary_w[0] = (Y - X * stationary_w[1]) / N
	print("{0} * t + {1}".format(stationary_w[1], stationary_w[0]))


def stationary_point_predict_basic(t):
	global stationary_w, dimension

	return stationary_w[1] * t + stationary_w[0]


def write_stationary_points():
	points = []
	t = 0
	with open("/home/hm/Documents/stationary_points.txt", "r") as fin:
		for line in fin:
			line = line[: len(line) - 1]
			points.append((t, int(line)))
			t += 1
	stationary_point_train_basic(points[500:])
	with open("/home/hm/Documents/stationary_points_predict.txt", "w") as fout:
		for i in range(0, len(points)):
			fout.write("{0}\n".format(stationary_point_predict_basic(i)))


if __name__ == "__main__":
	write_stationary_points()