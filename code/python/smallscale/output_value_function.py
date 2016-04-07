import DataPath
import FunctionLibrary.StringOperation

budget_parameter = 0.2
laplace = 1
max_market_price = 300

click_num = 0
win_num = 0
ctr = 0.001

market_price_counter = [0] * (max_market_price + 1)
market_price_distribution = [1 / (max_market_price + 1)] * (max_market_price + 1)

market_price_counter_click = [0] * (max_market_price + 1)
market_price_distribution_click = [1 / (max_market_price + 1)] * (max_market_price + 1)

hidden_click_num = 0


def update_market_price_distribution_counter():
	global market_price_distribution, market_price_counter, laplace, win_num, max_market_price
	for i in range(0, max_market_price + 1):
		market_price_distribution[i] = (market_price_counter[i] + laplace) / (win_num + (max_market_price + 1) * laplace)


def update_market_price_distribution_click_counter():
	global market_price_distribution_click, market_price_counter_click, laplace, click_num, max_market_price
	for i in range(1, max_market_price + 1):
		market_price_distribution_click[i] = \
			(market_price_counter_click[i] + laplace) / (click_num + max_market_price * laplace)


def update_click_rate():
	global click_num, win_num, ctr

	if win_num > 0 and click_num > 0:
		ctr = click_num / win_num
	else:
		ctr = 0.001


def out_value_function(bc, tc, out):
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

		for b in range(0, bc):
			out.write("{0}\t".format(value_function[b]))
		out.write("{0}\n".format(value_function[bc]))

		for b in range(1, bc + 1):
			for i in range(0, action[b] + 1):
				t_value_function[b] += market_price_distribution[i] * (ctr + value_function[b - i] - value_function[b])

			if abs(t_value_function[b] - t * ctr) < 1E-13:
				print("{0}\t{1}".format(b, t_value_function[b]))
				for bb in range(b + 1, bc + 1):
					t_value_function[bb] = t * ctr
				break
		value_function = t_value_function[:]
	for b in range(0, bc):
		out.write("{0}\t".format(value_function[b]))
	out.write("{0}\n".format(value_function[bc]))


if __name__ == "__main__":
	campaign = "3427"
	B = 100000
	T = 5000

	# load history data
	cost = 0
	with open(DataPath.rtb_mdp_path + campaign + "/" + DataPath.rtb_history_name) as fin:
		fin.readline()
		for line in fin:
			line = line[:len(line) - 1].split(" ")
			click = int(line[0])
			price = int(line[1])

			win_num += 1
			cost += price
			market_price_counter[price] += 1
			if click == 1:
				click_num += 1
				market_price_counter_click[price] += 1
	hidden_click_num = click_num
	update_market_price_distribution_counter()
	update_market_price_distribution_click_counter()
	update_click_rate()
	budget = cost / win_num * budget_parameter

	B = 100000 + 100
	print("campaign: " + campaign + "\tT: {0} , B: {1}".format(T, B))
	# write value function
	with open(DataPath.rtb_mdp_path + campaign + "/value_function.txt", "w") as fout:
		out_value_function(B, T, fout)
