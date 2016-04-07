import math


def matrix_norm_column(m1, m2):
	rows = len(m1)
	columns = len(m1[0])

	norm = 0
	for j in range(0, columns):
		rs = 0
		for i in range(0, rows):
			rs += abs(m1[i][j] - m2[i][j])
		norm = max(norm, rs)
	return norm / rows


def matrix_norm_row(m1, m2):
	rows = len(m1)
	columns = len(m1[0])

	norm = 0
	for i in range(0, rows):
		rs = 0
		for j in range(0, columns):
			rs += abs(m1[i][j] - m2[i][j])
		norm = max(norm, rs)
	return norm / columns


def matrix_norm_f(m1, m2):
	rows = len(m1)
	columns = len(m1[0])

	norm = 0
	for i in range(0, rows):
		for j in range(0, columns):
			norm += (m1[i][j] - m2[i][j]) * (m1[i][j] - m2[i][j])
	norm = math.sqrt(norm)
	return norm / math.sqrt(rows * columns)