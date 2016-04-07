import datetime
import math
import random
import FunctionLibrary.StringOperation

rtb_yoyi = "/home/hm/Project/data/reinforce-bid/yoyi-rtb/"
yoyiPath = "/home/hm/Project/data/reinforce-bid/yoyi-data/"
testOriginName = "cross_lr_15.txt.50302020.7"
rtb_history_name = "history.txt"
lg_weight_name = "lg_weights.txt"

min_trainRound = 20
max_trainRound = 50
stopBound = 1E-10
lamb = 0

sec = datetime.datetime.now()
random.seed(sec.hour * 3600000 + sec.minute * 60000 + sec.second * 1000 + sec.microsecond)
initWeight = 0.05

dimension = 0
weights = []

train_data = []


def sigmoid(p):
	if p <= -700:
		return 0
	return 1.0 / (1.0 + math.exp(-p))


# feature expressed with non-zero terms
def train_predict(x):
	global weights
	res = 0
	for index in x:
		res += weights[index]
	p = sigmoid(res)
	return p


def get_train_error():
	global train_data
	error = 0
	for (click, x) in train_data:
		h = train_predict(x)
		error += click * math.log(h) + (1 - click) * math.log(1 - h)
	error *= (-1 / len(train_data))
	return error


def round_function():
	global dimension, train_data, weights
	delta = [0] * dimension
	for (click, x) in train_data:
		h = train_predict(x)
		for index in x:
			delta[index] += (h - click)
	for i in range(0, dimension):
		delta[i] /= len(train_data)
		weights[i] -= lamb * delta[i]


if __name__ == "__main__":
	campaign = "0130"
	print("campaign:\t" + campaign)
	with open(rtb_yoyi + campaign + "/" + rtb_history_name) as fin:
		line = fin.readline()
		# set dimension
		dimension = int(line.split("\t")[0])
		weights = [0] * dimension
		print("dimension:\t{0}".format(dimension))

		# load train data
		for line in fin:
			line = line[0:len(line) - 1].split("\t")
			click = int(line[0])
			x = []
			for i in range(2, len(line)):
				x.append(int(line[i].split(":")[0]))
			train_data.append((click, x))
		print("train size:\t{0}".format(len(train_data)))

		# randomly initiate weights
		for i in range(0, dimension):
			weights[i] = (random.random() - 0.5) * initWeight

	# train
	last_error = get_train_error()
	lamb = last_error
	inc = 0
	for round in range(1, max_trainRound + 1):
		random.shuffle(train_data)
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
		if inc == 5:
			lamb *= 2
			inc = 0
		last_error = error
		with open(rtb_yoyi + campaign + "/" + lg_weight_name, "w") as fout:
			fout.write("\t".join(FunctionLibrary.StringOperation.getStringList(weights)) + "\n")

	# output weights
	with open(rtb_yoyi + campaign + "/" + lg_weight_name, "w") as fout:
		fout.write("\t".join(FunctionLibrary.StringOperation.getStringList(weights)) + "\n")