import datetime
import math
import random
import FunctionLibrary.StringOperation
import DataPath

min_trainRound = 20
max_trainRound = 2000
stopBound = 1E-10
lamb = 0

sec = datetime.datetime.now()
random.seed(sec.hour * 3600000 + sec.minute * 60000 + sec.second * 1000 + sec.microsecond)
initWeight = 0.05

dimension = 0
weights = []

train_data = []


def sigmoid(p):
	return 1.0 / (1.0 + math.exp(-p))


# feature expressed with non-zero terms
def predict(x):
	global weights
	res = 0
	for index in x:
		res += weights[index]
	return sigmoid(res)


def get_train_error():
	global train_data
	error = 0
	for (click, x) in train_data:
		h = predict(x)
		error += click * math.log(h) + (1 - click) * math.log(1 - h)
	error *= -1
	return error


def round_function():
	global dimension, train_data, weights
	delta = [0] * dimension
	for (click, x) in train_data:
		h = predict(x)
		for index in x:
			delta[index] += (h - click)
	for i in range(0, dimension):
		delta[i] /= len(train_data)
		weights[i] -= lamb * delta[i]


if __name__ == "__main__":
	with open(DataPath.rtb_mdp_path + "2259/" + DataPath.rtb_history_name) as fin:
		line = fin.readline()
		# set dimension
		dimension = int(line.split("\t")[0])
		weights = [0] * dimension
		print("dimension:\t{0}".format(dimension))
		# randomly initiate weights
		for i in range(0, dimension):
			weights[i] = (random.random() - 0.5) * initWeight

		# load train data
		for line in fin:
			line = line[0:len(line) - 1].split(" ")
			click = int(line[0])
			x = []
			for i in range(2, len(line)):
				x.append(int(line[i].split(":")[0]))
			train_data.append((click, x))
		print("train size:\t{0}".format(len(train_data)))

	# train
	last_error = get_train_error()
	lamb = last_error
	inc = 0
	for round in range(1, max_trainRound + 1):
		round_function()
		error = get_train_error()
		print(FunctionLibrary.StringOperation.getTime() + "\t{0}.\t{1}".format(round, error))
		if abs(error - last_error) < stopBound and round > min_trainRound:
			break
		if error > last_error:
			lamb = max(lamb / 5, 1E-5)
			inc = 0
		else:
			inc += 1
		if inc == 10:
			lamb *= 2
			inc = 0
		last_error = error
		with open(DataPath.rtb_mdp_path + "2259/" + DataPath.lg_weight_name, "w") as fout:
			fout.write("\t".join(FunctionLibrary.StringOperation.getStringList(weights)) + "\n")

	# output weights
	with open(DataPath.rtb_mdp_path + "2259/" + DataPath.lg_weight_name, "w") as fout:
		fout.write("\t".join(FunctionLibrary.StringOperation.getStringList(weights)) + "\n")