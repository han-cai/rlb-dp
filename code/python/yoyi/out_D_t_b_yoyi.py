import FunctionLibrary.StringOperation

rtb_yoyi = "/home/hm/Project/data/reinforce-bid/yoyi-rtb/"
rtb_history_name = "history.txt"
lg_weight_name = "lg_weights.txt"
rtb_validation_name = "validation.txt"
rtb_test_name = "test.rtb.txt"
projectPath = "/home/hm/Project/reinforce-bid/code/Python/"

budget_parameter = 1 / 2
campaign = "0124"

laplace = 1
max_market_price = 300

click_num = 0
win_num = 0
ctr = 0.001
w = 0.01

market_price_counter = [0] * (max_market_price + 1)
market_price_distribution = [1 / (max_market_price + 1)] * (max_market_price + 1)

hidden_click_num = 0


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


def out_derivative_value_function(bc, tc, out):
	global ctr, market_price_distribution

	value_function = [0] * (bc + 1)
	for t in range(1, tc):
		print(FunctionLibrary.StringOperation.getTime() + "\t{0} start".format(t))
		action = [0] * (bc + 1)
		end = bc - 1
		for start in range(bc, 0, -1):
			while end >= 0 and value_function[end] - value_function[start] + ctr > 0:
				end -= 1
			if end < 0:
				action[start] = min(max_market_price, start)
			else:
				action[start] = min(max_market_price, start - end - 1)
		t_value_function = value_function[:]

		for b in range(0, bc - 1):
			derivative = value_function[b + 1] - value_function[b]
			sp = "\t"
			if b == bc - 2:
				sp = "\n"
			if abs(value_function[b] - (t - 1) * ctr) < 1E-10:
				out.write("0" + sp)
			else:
				out.write("{0}".format(derivative) + sp)

		for b in range(1, bc + 1):
			for i in range(0, action[b] + 1):
				t_value_function[b] += market_price_distribution[i] * (ctr + value_function[b - i] - value_function[b])

			if abs(t_value_function[b] - t * ctr) < 1E-10:
				print("{0}\t{1}".format(b, t_value_function[b]))
				for bb in range(b + 1, bc + 1):
					t_value_function[bb] = t * ctr
				break
		value_function = t_value_function[:]
	for b in range(0, bc - 1):
		derivative = value_function[b + 1] - value_function[b]
		sp = "\t"
		if b == bc - 2:
			sp = "\n"
		if abs(value_function[b] - (tc - 1) * ctr) < 1E-10:
			out.write("0" + sp)
		else:
			out.write("{0}".format(derivative) + sp)


if __name__ == "__main__":
	B = 100000
	T = 100

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

	B = int(budget * T)
	print("campaign: " + campaign + "\tT: {0} , B: {1}".format(T, B))
	# write derivative value function
	with open(rtb_yoyi + campaign + "/derivative_value_function.txt", "w") as fout:
		out_derivative_value_function(B, T, fout)
