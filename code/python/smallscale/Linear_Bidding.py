import math
import FunctionLibrary.StringOperation
import DataPath

budget_parameter = 1 / 32
campaign = "3476"
laplace = 1
max_market_price = 300

click_num = 0
win_num = 0
ctr = 0.001

hidden_click_num = 0
linear_para = 300

dimension = 0
weights = []


def sigmoid(p):
	if p < -700:
		return 0
	return 1.0 / (1.0 + math.exp(-p))


def update_click_rate():
	global click_num, win_num, ctr

	if win_num > 0 and click_num > 0:
		ctr = click_num / win_num
	else:
		ctr = 0.001


# KPI prediction function
def theta(x):
	global weights
	res = 0
	for index in x:
		res += weights[index]
	return sigmoid(res)


def rtb_mdp(campaign):
	global win_num, click_num, dimension, weights, budget_parameter, hidden_click_num, linear_para, ctr
	# load history data
	cost = 0
	with open(DataPath.rtb_mdp_path + campaign + "/" + DataPath.rtb_history_name) as fin:
		fin.readline()
		for line in fin:
			line = line[:len(line) - 1].split(" ")
			click = int(line[0])
			price = int(line[1])
			cost += price

			win_num += 1
			if click == 1:
				click_num += 1
	update_click_rate()
	hidden_click_num = click_num
	budget = cost / win_num * budget_parameter

	# load logistic regression weights
	with open(DataPath.rtb_mdp_path + campaign + "/" + DataPath.lg_weight_name) as fin:
		line = fin.readline()
		line = line[:len(line) - 1].split("\t")
		dimension = len(line)
		for item in line:
			weights.append(float(item))

	# compute linear para
	candidates = range(2, 300, 6)
	best_pref = 0
	for candidate in candidates:
		clk = 0
		with open(DataPath.rtb_mdp_path + campaign + "/" + DataPath.rtb_validation_name) as fin:
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
					line = line[0:len(line) - 1].split(" ")
					click = int(line[0])
					price = int(line[1])
					x = []
					for i in range(2, len(line)):
						x.append(int(line[i].split(":")[0]))
					action = min(int(theta(x) * candidate / ctr), max_market_price)
					action = min(action, b)

					if action >= price:
						if click == 1:
							clk += 1
						b -= price
					else:
						take_this_place = 1
					t -= 1
		if clk > best_pref:
			best_pref = clk
			linear_para = candidate
	print("linear para:\t{0}\t{1}".format(linear_para, best_pref))

	# start test
	print(FunctionLibrary.StringOperation.getTime() + "\ttest start")
	with open(DataPath.rtb_mdp_path + campaign + "/" + DataPath.rtb_test_name) as fin:
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
				line = line[0:len(line) - 1].split(" ")
				click = int(line[0])
				price = int(line[1])
				x = []
				for i in range(2, len(line)):
					x.append(int(line[i].split(":")[0]))
				action = min(int(theta(x) * linear_para / ctr), max_market_price)
				action = min(action, b)

				record = FunctionLibrary.StringOperation.getTime() + "\t{0}\t{1}_{2}\t{3}_{4}_{5}\t{6}_{7}_{8}\t".format(
						period, b, t, action, price, click, hidden_click_num, click_num, win_num)
				#print(record)
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
				update_click_rate()


if __name__ == "__main__":
	log = open(DataPath.projectPath + "log/" + campaign + "-linear.log", "w")
	print(FunctionLibrary.StringOperation.getTime() + "\t" + campaign + "\tstart")
	log.write(FunctionLibrary.StringOperation.getTime() + "\t" + campaign + "\tstart\n")
	rtb_mdp(campaign)
	log.close()