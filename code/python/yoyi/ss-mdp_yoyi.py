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

market_price_counter = [0] * (max_market_price + 1)
market_price_distribution = [1 / (max_market_price + 1)] * (max_market_price + 1)

hidden_click_num = 0

value_function = []

dimension = 0
weights = []
w = 0.01

Dt_b_points = []
St = []
T0 = 10000

update_frequency = 10000000


def sigmoid(p):
	if p <= -700:
		return 0
	return 1.0 / (1.0 + math.exp(-p))


def update_market_price_distribution_counter():
	global market_price_distribution, market_price_counter, laplace, win_num, max_market_price
	counter = 0
	for i in range(0, max_market_price + 1):
		counter += market_price_counter[i]
	for i in range(0, max_market_price + 1):
		market_price_distribution[i] = (market_price_counter[i] + laplace) / (counter + (max_market_price + 1) * laplace)


def update_click_rate():
	global click_num, win_num, ctr, w

	if win_num > 0 and click_num > 0:
		ctr = click_num / win_num
		ctr /= (ctr + (1 - ctr) / w)
	else:
		ctr = 0.001


# KPI prediction function
def theta(x):
	global weights
	res = 0
	for index in x:
		res += weights[index]
	p = sigmoid(res)
	q = p / (p + (1 - p) / w)
	return q


def load_derivative_value_function(campaign, tc, bc):
	global Dt_b_points, St

	Dt_b_points = []
	St = []
	with open(rtb_yoyi + campaign + "/D_t_b_points.txt") as fin:
		t = 0
		for line in fin:
			if t >= tc:
				break
			t += 1
			line = line[:len(line) - 1].split("\t")
			num = int(line[1])
			st = int(line[2])
			points = []
			for i in range(min(num, bc)):
				points.append(float(line[3 + i]))
			Dt_b_points.append(points)
			St.append(st)


def get_D_t_b(t, b):
	global Dt_b_points, St

	if b < len(Dt_b_points[t]):
		return Dt_b_points[t][b]
	elif b >= St[t]:
		return 0


def bid(bc, tc, x):
	global max_market_price, ctr

	take_action = 0
	theta_x = ctr
	for delta in range(0, min(bc, max_market_price) + 1):
		if delta == bc:
			take_action = bc
			break
		elif delta == max_market_price:
			take_action = max_market_price
			break
		else:
			theta_x -= get_D_t_b(tc - 1, bc - delta - 1)
			if theta_x < 0:
				take_action = delta
				break
	return take_action


def rtb_mdp(campaign):
	global win_num, click_num, market_price_counter, \
		dimension, weights, budget_parameter, hidden_click_num, update_frequency
	# load history data
	cost = 0
	with open(rtb_yoyi + campaign + "/" + rtb_history_name) as fin:
		fin.readline()
		for line in fin:
			line = line[:len(line) - 1].split("\t")
			click = int(line[0])
			price = int(line[1])

			win_num += 1
			cost += price
			if price <= max_market_price:
				market_price_counter[price] += 1
			if click == 1:
				click_num += 1
	hidden_click_num = click_num
	update_market_price_distribution_counter()
	update_click_rate()
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
		#update_frequency = int(T / 10)
		period = 0

		t = 0
		b = 0
		for line in fin:
			if t == 0:
				line = line[:len(line) - 1].split("\t")
				period = int(line[0])
				b = int(budget * T)
				t = T
				if period == 1:
					load_derivative_value_function(campaign, t, b)
			else:
				line = line[0:len(line) - 1].split("\t")
				click = int(line[0])
				price = int(line[1])
				x = []
				for i in range(2, len(line)):
					x.append(int(line[i].split(":")[0]))
				action = bid(b, t, x)

				record = FunctionLibrary.StringOperation.getTime() + "\t{0}\t{1}_{2}\t{3}_{4}_{5}\t{6}_{7}_{8}\t".format(
						period, b, t, action, price, click, hidden_click_num, click_num, win_num)
				print(record)
				log.write(record + "\n")

				if action >= price:
					win_num += 1
					market_price_counter[price] += 1

					if click == 1:
						click_num += 1
					b -= price
				else:
					take_this_place = 1
				t -= 1
				if click == 1:
					hidden_click_num += 1


if __name__ == "__main__":
	log = open(projectPath + "log/" + campaign + "-baseline.log", "w")
	print(FunctionLibrary.StringOperation.getTime() + "\t" + campaign + "\tstart")
	log.write(FunctionLibrary.StringOperation.getTime() + "\t" + campaign + "\tstart\n")
	rtb_mdp(campaign)
	log.close()