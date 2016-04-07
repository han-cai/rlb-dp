import math
import FunctionLibrary.StringOperation
import DataPath

from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error

ctr = 0
click_num = 0
counter = 0

test_data = []
train_data = []
dimension = 0
weights = []


def sigmoid(p):
	return 1.0 / (1.0 + math.exp(-p))


def predict(x):
	global weights
	res = 0
	for index in x:
		res += weights[index]
	return sigmoid(res)

if __name__ == "__main__":
	campaign = "3476"
	# calculation ctr
	with open(DataPath.ipinyouPath + campaign + "/" + DataPath.trainOriginName) as fin:
		for line in fin:
			counter += 1
			line = line[:len(line) - 1].split(" ")
			if int(line[0]) == 1:
				click_num += 1
		ctr = click_num / counter

	# load train data
	with open(DataPath.rtb_mdp_path + campaign + "/" + DataPath.rtb_history_name) as fin:
		fin.readline()
		for line in fin:
			line = line[0:len(line) - 1].split(" ")
			click = int(line[0])
			x = []
			for i in range(2, len(line)):
				x.append(int(line[i].split(":")[0]))
			train_data.append((click, x))

	# load test data
	with open(DataPath.ipinyouPath + campaign + "/" + DataPath.testOriginName) as fin:
		for line in fin:
			line = line[0:len(line) - 1].split(" ")
			click = int(line[0])
			x = []
			for i in range(2, len(line)):
				x.append(int(line[i].split(":")[0]))
			test_data.append((click, x))

	# load weight
	with open(DataPath.rtb_mdp_path + campaign + "/" + DataPath.lg_weight_name) as fin:
		line = fin.readline()
		line = line[:len(line) - 1].split("\t")
		dimension = len(line)
		for item in line:
			weights.append(float(item))

	# calc error
	lg_error = 0
	ctr_error = 0
	t1 = 0
	t2 = 0
	t3 = 0
	t4 = 0
	y = []
	y_avg = []
	y_lr = []
	for (click, x) in test_data:
		y.append(click)
		y_avg.append(ctr)

		h = predict(x)
		y_lr.append(h)
		lg_error += click * math.log(h) + (1 - click) * math.log(1 - h)
		ctr_error += click * math.log(ctr) + (1 - click) * math.log(1 - ctr)
		counter += 1
		if click == 1:
			t1 += 1
			click_num += 1
			print("{0}\t{1}".format(ctr, h))
			if h > ctr:
				t2 += 1
		else:
			t3 += 1
			if h < ctr:
				t4 += 1

	lg_error *= (-1 / len(test_data))
	ctr_error *= (-1 / len(test_data))

	print("average ctr:\t{0}".format(ctr_error))
	print("logistic regression:\t{0}".format(lg_error))
	print("{0}\t{1}".format(t2, t1))
	print("{0}\t{1}".format(t4, t3))

	auc = roc_auc_score(y, y_avg)
	print("average ctr auc:\t{0}".format(auc))
	auc = roc_auc_score(y, y_lr)
	print("lr auc:\t{0}".format(auc))

