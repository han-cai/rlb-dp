from utility import *


class SS_MDP:
	def __init__(self, camp_info):
		self.cpm = camp_info["cost_train"] / camp_info["imp_train"]
		self.theta_avg = camp_info["clk_train"] / camp_info["imp_train"]
		self.V = []

	def load_value_function(self, N, B, model_path):
		self.V = [[0 for i in range(B + 1)] for j in range(N)]
		with open(model_path, "r") as fin:
			n = 0
			for line in fin:
				line = line[:len(line) - 1].split("\t")
				for b in range(B + 1):
					self.V[n][b] = float(line[b])
				n += 1
				if n >= N:
					break

	def bid(self, n, b, theta, max_bid):
		a = 0
		for delta in range(1, min(b, max_bid) + 1):
			if theta + (self.V[n - 1][b - delta] - self.V[n - 1][b]) >= 0:
				a = delta
			else:
				break
		return a

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
			else:
				(click, price, theta) = line
			a = self.bid(n, b, self.theta_avg, max_bid)

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
