import DataPath
import FunctionLibrary.StringOperation


def from_logs():
	graph1 = open("/home/hm/Documents/graph1.txt", "w")
	graph2 = open("/home/hm/Documents/graph2.txt", "w")
	graph3 = open("/home/hm/Documents/graph3.txt", "w")
	graph4 = open("/home/hm/Documents/graph4.txt", "w")

	current_period = 0
	first_record = None
	last_record = None
	total_auction_num = 0
	total_paying = 0
	with open("/home/hm/Documents/log.txt", "r") as fin:
		for line in fin:
			line = line[:len(line) - 1]
			items = line.split("\t")
			if len(items) != 6:
				continue
			period = int(items[1])
			if period != current_period:
				if first_record != None:
					items = first_record.split("\t")
					tokens = items[2].split("_")
					B = int(tokens[0])
					T = int(tokens[1])

					items = last_record.split("\t")
					tokens = items[2].split("_")
					b = int(tokens[0])

					tokens = items[3].split("_")
					action = int(tokens[0])
					market_price = int(tokens[1])
					if action >= market_price:
						b -= market_price

					item = line.split("\t")
					tokens = items[4].split("_")
					hidden_win_click = int(tokens[0])
					win_click = int(tokens[1])
					win_auction = int(tokens[2])

					total_auction_num += T
					total_paying += (B - b)

					graph1.write("{0}\t{1}\n".format(current_period, win_auction / total_auction_num))
					graph2.write("{0}\t{1}\n".format(current_period, b / B))
					graph3.write("{0}\t{1}\t{2}\n".format(current_period, win_click, hidden_win_click))
					graph4.write("{0}\t{1}\n".format(current_period, win_click / total_paying))
				first_record = line
				current_period = period
			else:
				last_record = line
	graph1.close()
	graph2.close()
	graph3.close()
	graph4.close()


def get_distribution_click_rate(path):
	laplace = 1
	max_market_price = 300
	counter = 0
	click_num = 0
	win_num = 0
	market_price_counter = [0] * (max_market_price + 1)
	market_price_distribution = [1 / (max_market_price + 1)] * (max_market_price + 1)
	with open(path, 'r') as fin:
		for line in fin:
			line = line[:len(line) - 1]
			items = line.split("\t")
			for i in range(1, len(items)):
				tokens = items[i].split("_")
				price = int(tokens[0])
				click = int(tokens[1])
				counter += 1
				market_price_counter[price] += 1

				win_num += 1
				if click == 1:
					click_num += 1


	for i in range(0, max_market_price + 1):
		market_price_distribution[i] = (market_price_counter[i] + laplace) / (counter + (max_market_price + 1) * laplace)
	return market_price_distribution, click_num / win_num

if __name__ == "__main__":
	(market_price_distribution, click_rate) = get_distribution_click_rate(
		DataPath.sequencePath + "2259/" + DataPath.trainSequenceName)
	print("_".join(FunctionLibrary.StringOperation.getStringList(market_price_distribution)))
	print(click_rate)
