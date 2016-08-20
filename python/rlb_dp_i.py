from utility import *
import config


class RLB_DP_I:
	up_precision = 1e-10
	zero_precision = 1e-12

	def __init__(self, camp_info, opt_obj, gamma):
		self.cpm = camp_info["cost_train"] / camp_info["imp_train"]
		self.theta_avg = camp_info["clk_train"] / camp_info["imp_train"]
		self.opt_obj = opt_obj
		self.gamma = gamma
		self.v1 = self.opt_obj.v1
		self.v0 = self.opt_obj.v0
		self.V = []
		self.D = []

	def calc_optimal_value_function_with_approximation_i(self, N, B, max_bid, m_pdf, save_path):
		#print(getTime() + "\tvalue function with approx_i, N={}, B={}, save in {}".format(N, B, save_path))
		V_out = open(save_path, "w")
		V = [0] * (B + 1)
		nV = [0] * (B + 1)
		V_max = 0
		V_inc = 0
		if self.v0 != 0:
			a_max = min(int(self.v1 * self.theta_avg / self.v0), max_bid)
		else:
			a_max = max_bid
		for b in range(0, a_max + 1):
			V_inc += m_pdf[b] * (self.v1 * self.theta_avg - self.v0 * b)
		for n in range(1, N):
			a = [0] * (B + 1)
			bb = B - 1
			for b in range(B, 0, -1):
				while bb >= 0 and self.gamma * (V[bb] - V[b]) + self.v1 * self.theta_avg - self.v0 * (b - bb) >= 0:
					bb -= 1
				if bb < 0:
					a[b] = min(max_bid, b)
				else:
					a[b] = min(max_bid, b - bb - 1)

			for b in range(0, B):
				V_out.write("{}\t".format(V[b]))
			V_out.write("{}\n".format(V[B]))

			V_max = self.gamma * V_max + V_inc
			flag = False
			for b in range(1, B + 1):
				nV[b] = self.gamma * V[b]
				for delta in range(0, a[b] + 1):
					nV[b] += m_pdf[delta] * (self.v1 * self.theta_avg + self.gamma * (V[b - delta] - V[b]) - self.v0 * delta)
				if abs(nV[b] - V_max) < self.up_precision:
					for bb in range(b + 1, B + 1):
						nV[bb] = V_max
					flag = True
					break
			V = nV[:]
			# if flag:
			# 	print(getTime() + "\tround {} end with early stop.".format(n))
			# else:
			# 	print(getTime() + "\tround {} end.".format(n))
		for b in range(0, B):
			V_out.write("{0}\t".format(V[b]))
		V_out.write("{0}\n".format(V[B]))
		V_out.flush()
		V_out.close()

	def calc_Dnb(self, N, B, max_bid, m_pdf, save_path):
		print(getTime() + "\tD(n, b), N={}, B={}, save in {}".format(N, B, save_path))
		D_out = open(save_path, "w")
		V = [0] * (B + 1)
		nV = [0] * (B + 1)
		V_max = 0
		V_inc = 0
		if self.v0 != 0:
			a_max = min(int(self.v1 * self.theta_avg / self.v0), max_bid)
		else:
			a_max = max_bid
		for b in range(0, a_max + 1):
			V_inc += m_pdf[b] * (self.v1 * self.theta_avg - self.v0 * b)
		for n in range(1, N):
			a = [0] * (B + 1)
			bb = B - 1
			for b in range(B, 0, -1):
				while bb >= 0 and self.gamma * (V[bb] - V[b]) + self.v1 * self.theta_avg - self.v0 * (b - bb) >= 0:
					bb -= 1
				if bb < 0:
					a[b] = min(max_bid, b)
				else:
					a[b] = min(max_bid, b - bb - 1)

			for b in range(0, B):
				dtb = V[b + 1] - V[b]
				if abs(dtb) < self.zero_precision:
					dtb = 0
				if b == B - 1:
					D_out.write("{}\n".format(dtb))
				else:
					D_out.write("{}\t".format(dtb))

			V_max = self.gamma * V_max + V_inc
			flag = False
			for b in range(1, B + 1):
				nV[b] = self.gamma * V[b]
				for delta in range(0, a[b] + 1):
					nV[b] += m_pdf[delta] * (self.v1 * self.theta_avg + self.gamma * (V[b - delta] - V[b]) - self.v0 * delta)
				if abs(nV[b] - V_max) < self.up_precision:
					for bb in range(b + 1, B + 1):
						nV[bb] = V_max
					flag = True
					break
			V = nV[:]
			if flag:
				print(getTime() + "\tround {} end with early stop.".format(n))
			else:
				print(getTime() + "\tround {} end.".format(n))
		for b in range(0, B):
			dtb = V[b + 1] - V[b]
			if abs(dtb) < self.zero_precision:
				dtb = 0
			if b == B - 1:
				D_out.write("{}\n".format(dtb))
			else:
				D_out.write("{}\t".format(dtb))
		D_out.flush()
		D_out.close()

	def Vnb2Dnb(self, v_path, d_path):
		with open(v_path, "r") as fin:
			with open(d_path, "w") as fout:
				for line in fin:
					line = line[:len(line) - 1].split("\t")
					nl = ""
					for b in range(len(line) - 1):
						d = float(line[b + 1]) - float(line[b])
						if abs(d) < RLB_DP_I.zero_precision:
							d = 0
						if b == len(line) - 2:
							nl += "{}\n".format(d)
						else:
							nl += "{}\t".format(d)
					fout.write(nl)

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

	def load_Dnb(self, N, B, model_path):
		self.D = [[0 for i in range(B)] for j in range(N)]
		with open(model_path, "r") as fin:
			n = 0
			for line in fin:
				line = line[:len(line) - 1].split("\t")
				for b in range(B):
					self.D[n][b] = float(line[b])
				n += 1
				if n >= N:
					break

	def bid(self, n, b, theta, max_bid):
		a = 0
		if len(self.V) > 0:
			for delta in range(1, min(b, max_bid) + 1):
				if self.v1 * theta + self.gamma * (self.V[n - 1][b - delta] - self.V[n - 1][b]) - self.v0 * delta >= 0:
					a = delta
				else:
					break
		elif len(self.D) > 0:
			value = self.v1 * theta
			for delta in range(1, min(b, max_bid) + 1):
				value -= self.gamma * self.D[n - 1][b - delta] + self.v0
				if value >= 0:
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
				theta = float(line[2])
			else:
				(click, price, theta) = line
			a = self.bid(n, b, theta, max_bid)
			a = min(int(a), min(b, max_bid))

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

	@staticmethod
	def Dnb_save_points(d_path, out_path, b_bound, n_bound):
		N_bound = 0
		B_bound = 0
		with open(d_path, "r") as fin:
			for line in fin:
				N_bound += 1
				if B_bound == 0:
					line = line[:len(line) - 1].split("\t")
					B_bound = len(line)
		with open(d_path, "r") as fin:
			with open(out_path, "w") as fout:
				fout.write("{}_{}_{}\n".format(N_bound, B_bound, config.vlion_max_market_price))
				n = 0
				for line in fin:
					line = line[:len(line) - 1].split("\t")
					bb = -1
					for b in range(len(line)):
						dnb = float(line[b])
						if abs(dnb) < RLB_DP_I.zero_precision:
							bb = b
							break
					if bb >= 0:
						if n <= n_bound:
							s_ids = bb
						else:
							s_ids = min(bb, b_bound)
						out = "{}_{}_{}\t".format(n, bb, s_ids)
						out += "\t".join(line[:s_ids]) + "\n"
						fout.write(out)
					else:
						if n <= n_bound:
							s_ids = len(line)
						else:
							s_ids = min(b_bound, len(line))
						out = "{}_{}_{}\t".format(n, bb, s_ids)
						out += "\t".join(line[:s_ids]) + "\n"
						fout.write(out)
					n += 1


