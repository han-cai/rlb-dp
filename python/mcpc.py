from utility import *


class Mcpc:
	def __init__(self, camp_info):
		self.cpc = camp_info["cost_train"] / camp_info["clk_train"]
		self.cpm = camp_info["cost_train"] / camp_info["imp_train"]

	def run(self, auction_in, bid_log_path, N, c0, max_bid, input_type="file reader", delimiter=" ", save_log=False):
		auction = 0
		imp = 0
		clk = 0
		cost = 0

		if save_log:
			log_in = open(bid_log_path, "w")
		B = int(self.cpm * c0 * N)

		episode = 1
		n = N
		b = B
		for line in auction_in:
			if input_type == "file reader":
				line = line[:len(line) - 1].split(delimiter)
				click = int(line[0])
				price = int(line[1])
				theta = float(line[2])
			else:
				(click, price, theta) = line
			a = min(int(theta * self.cpc), max_bid)
			a = min(b, a)

			log = getTime() + "\t{}\t{}_{}\t{}_{}_{}\t{}_{}\t".format(
				episode, b, n, a, price, click, clk, imp)
			if save_log:
				log_in.write(log + "\n")

			if a >= price:
				imp += 1
				if click == 1:
					clk += 1
				b -= price
				cost += price
			n -= 1
			auction += 1

			if n == 0:
				episode += 1
				n = N
				b = B
		if save_log:
			log_in.flush()
			log_in.close()

		return auction, imp, clk, cost

