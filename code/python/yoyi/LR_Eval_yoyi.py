import datetime
import math
import random
import FunctionLibrary.StringOperation
from sklearn.metrics import roc_auc_score

rtb_yoyi = "/home/hm/Project/data/reinforce-bid/yoyi-rtb/"
yoyiPath = "/home/hm/Project/data/reinforce-bid/yoyi-data/"
testOriginName = "cross_lr_15.txt.50302020.7"
rtb_history_name = "history.txt"
lg_weight_name = "lg_weights.txt"

ctr = 0
click_num = 0
counter = 0
w = 0.01

sec = datetime.datetime.now()
random.seed(sec.hour * 3600000 + sec.minute * 60000 + sec.second * 1000 + sec.microsecond)
initWeight = 0.05

dimension = 0
weights = []

train_data = []
test_data = []


def sigmoid(p):
	if p <= -700:
		return 0
	return 1.0 / (1.0 + math.exp(-p))


# feature expressed with non-zero terms
def test_predict(x):
	global weights, w
	res = 0
	for index in x:
		res += weights[index]
	p = sigmoid(res)
	q = p / (p + (1 - p) / w)
	return q


if __name__ == "__main__":
	campaign = "0130"

	# calculation ctr
	with open(rtb_yoyi + campaign + "/" + rtb_history_name) as fin:
		for line in fin:
			counter += 1
			line = line[:len(line) - 1].split("\t")
			if int(line[0]) == 1:
				click_num += 1
		ctr = click_num / counter
		ctr /= (ctr + (1 - ctr) / w)

	# load test data
	with open(yoyiPath + campaign + "/" + testOriginName) as fin:
		for line in fin:
			line = line[0:len(line) - 1].split("\t")
			click = int(line[0])
			x = []
			for i in range(2, len(line)):
				x.append(int(line[i].split(":")[0]))
			test_data.append((click, x))

	# load weight
	with open(rtb_yoyi + campaign + "/" + lg_weight_name) as fin:
		line = fin.readline()
		line = line[:len(line) - 1].split("\t")
		dimension = len(line)
		for item in line:
			weights.append(float(item))
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

		h = test_predict(x)
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