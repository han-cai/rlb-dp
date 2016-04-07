import math
import FunctionLibrary.StringOperation

rtb_yoyi = "/home/hm/Project/data/reinforce-bid/yoyi-rtb/"
rtb_history_name = "history.txt"
lg_weight_name = "lg_weights.txt"
rtb_validation_name = "validation.txt"
rtb_test_name = "test.rtb.txt"
projectPath = "/home/hm/Project/reinforce-bid/code/Python/"

budget_parameter = 1 / 2
campaign = "0130"
laplace = 1
max_market_price = 300

click_num = 0
win_num = 0
ctr = 0.001
truth_telling_para = 0
w = 0.01

hidden_click_num = 0

dimension = 0
weights = []


def sigmoid(p):
	return 1.0 / (1.0 + math.exp(-p))


# KPI prediction function
def theta(x):
	global weights, w
	res = 0
	for index in x:
		res += weights[index]
	p = sigmoid(res)
	q = p / (p + (1 - p) / w)
	return q


def rtb_mdp(campaign):
	global win_num, click_num, dimension, weights, budget_parameter, hidden_click_num, truth_telling_para, w
	# load history data
	cost1 = 0
	cost2 = 0
	cost = 0
	with open(rtb_yoyi + campaign + "/" + rtb_history_name) as fin:
		fin.readline()
		for line in fin:
			line = line[:len(line) - 1].split("\t")
			click = int(line[0])
			price = int(line[1])
			cost += price
			win_num += 1
			if click == 1:
				click_num += 1
				cost1 += price
			else:
				cost2 += price
	hidden_click_num = click_num
	truth_telling_para = (cost1 + cost2 / w) / click_num
	budget = cost / win_num * budget_parameter

	# load logistic regression weights
	with open(rtb_yoyi + campaign + "/" + lg_weight_name) as fin:
		line = fin.readline()
		line = line[:len(line) - 1].split("\t")
		dimension = len(line)
		for item in line:
			weights.append(float(item))

	# start test
	print(FunctionLibrary.StringOperation.getTime() + "\ttest start")
	with open(rtb_yoyi + campaign + "/test.rtb.txt") as fin:
		line = fin.readline()
		line = line[:len(line) - 1].split("\t")
		T = int(line[1])
		period = 0

		t = 0
		b = 0
		for line in fin:
			if t == 0:
				line = line[:len(line) - 1].split("\t")
				period = int(line[0])
				b = int(budget * T)
				t = T
			else:
				line = line[0:len(line) - 1].split("\t")
				click = int(line[0])
				price = int(line[1])
				x = []
				for i in range(2, len(line)):
					x.append(int(line[i].split(":")[0]))
				action = min(int(theta(x) * truth_telling_para), max_market_price)
				action = min(action, b)

				record = FunctionLibrary.StringOperation.getTime() + "\t{0}\t{1}_{2}\t{3}_{4}_{5}\t{6}_{7}_{8}\t".format(
						period, b, t, action, price, click, hidden_click_num, click_num, win_num)
				print(record)
				log.write(record + "\n")

				if action >= price:
					win_num += 1

					if click == 1:
						click_num += 1
					b -= price
				else:
					take_this_place = 1
				t -= 1
				if click == 1:
					hidden_click_num += 1


if __name__ == "__main__":
	log = open(projectPath + "log/" + campaign + "-ttb.log", "w")
	print(FunctionLibrary.StringOperation.getTime() + "\t" + campaign + "\tstart")
	log.write(FunctionLibrary.StringOperation.getTime() + "\t" + campaign + "\tstart\n")
	rtb_mdp(campaign)
	log.close()