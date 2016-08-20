from utility import *
from NN_Approximator import NN_Approximator
import time


class RLB_DP_FA:
	def __init__(self, camp_info, opt_obj, gamma):
		self.cpm = camp_info["cost_train"] / camp_info["imp_train"]
		self.theta_avg = camp_info["clk_train"] / camp_info["imp_train"]
		self.opt_obj = opt_obj
		self.gamma = gamma
		self.v1 = self.opt_obj.v1
		self.v0 = self.opt_obj.v0

		self.D_info = []
		self.D_point = []
		self.N_bound = 0
		self.B_bound = 0

		self.nn_approx = None
		self.sess = None
		self.dim = 0

		self.net_type = None
		self.net_argv = None
		self.params = []

	def load_save_points(self, in_path):
		self.D_info = []
		self.D_point = []
		with open(in_path, "r") as fin:
			line = fin.readline()
			line = line[:len(line) - 1].split("_")
			self.N_bound = int(line[0])
			self.B_bound = int(line[1])
			for line in fin:
				line = line[:len(line) - 1].split("\t")
				info = line[0].split("_")
				for i in range(len(info)):
					info[i] = int(info[i])
				points = [0] * info[2]
				for i in range(info[2]):
					points[i] = float(line[1 + i])
				self.D_info.append(info)
				self.D_point.append(points)

	def load_nn_approximator(self, input_type, model_path):
		if input_type == "txt":
			self.params = []
			with open(model_path, "r") as fin:
				line = fin.readline()
				line = line[:len(line) - 1].split("\t")
				self.net_type = line[0]
				if self.net_type == "nn":
					depth = int(line[1])
					h_dims = line[2].split("_")
					for i in range(len(h_dims)):
						h_dims[i] = int(h_dims[i])
					act_func = line[3]
					self.net_argv = [depth, h_dims, act_func]
					self.dim = h_dims[0]
					for i in range(depth - 1):
						line = fin.readline()
						line = line[:len(line) - 1].split("\t")
						Wi = []
						for item in line[1:]:
							item = item.split("_")
							item = str_list2float_list(item)
							Wi.append(item)
						line = fin.readline()
						line = line[:len(line) - 1].split("\t")
						bi = str_list2float_list(line[1:])
						self.params.append((Wi, bi))
		elif input_type == "pickle":
			var_map = pickle.load(open(model_path, "rb"))
			self.net_type = var_map["net_type"]
			if self.net_type == "nn":
				depth = var_map["depth"]
				h_dims = var_map["h_dims"]
				act_func = var_map["act_func"]
				self.net_argv = [depth, h_dims, act_func]
				self.dim = h_dims[0]
				batch_size = 100
				self.nn_approx = NN_Approximator(self.net_type, self.net_argv, model_path, None, [self.dim],
				                            batch_size, ['adam', 1e-4, 1e-8, 'mean'])
				self.sess = tf.Session(graph=self.nn_approx.graph)
				self.sess.run(self.nn_approx.init)

	def forward(self, x_vec):
		if self.sess:
			x_vec = np.array(x_vec).reshape(1, len(x_vec))
			feed_dict = {
				self.nn_approx.x_vec: x_vec
			}
			pred = self.sess.run(self.nn_approx.value_prediction, feed_dict=feed_dict)
			pred = pred.flatten()
			pred = pred[0]
		elif len(self.params) > 0:
			if self.net_type == "nn":
				depth, h_dims, act_func = self.net_argv
				z = x_vec
				for _i in range(depth - 2):
					Wi, bi = self.params[_i]
					a = [0] * h_dims[_i + 1]
					for _j in range(h_dims[_i + 1]):
						for _k in range(h_dims[_i]):
							a[_j] += Wi[_j][_k] * z[_k]
						a[_j] += bi[_j]
					z = [0] * len(a)
					for _j in range(h_dims[_i + 1]):
						z[_j] = activate_calc(act_func, a[_j])
				W, b = self.params[depth - 2]
				pred = 0
				for _j in range(len(z)):
					pred += W[0][_j] * z[_j]
				pred += b[0]
		return pred

	def get_Dnb(self, n, b):
		if n < len(self.D_info):
			if 0 <= self.D_info[n][1] <= b:
				return 0
			if b < len(self.D_point[n]):
				return self.D_point[n][b]
		x_vec = [n, b]
		if self.dim == 3:
			x_vec.append(b / n)
		dnb = self.forward(x_vec)
		dnb = max(dnb, 0)
		return dnb

	def bid(self, n, b, theta, max_bid):
		if n > self.N_bound:
			return self.bid(self.N_bound, int(b / n * self.N_bound), theta, max_bid)
		if b > self.B_bound:
			return self.bid(int(n / b * self.B_bound), self.B_bound, theta, max_bid)
		a = 0
		value = self.v1 * theta
		for delta in range(1, min(b, max_bid) + 1):
			dnb = self.get_Dnb(n - 1, b - delta)
			value -= self.gamma * dnb + self.v0
			if value >= 0:
				a = delta
			else:
				break
		return a

	def run(self, auction_in, bid_log_path, N, c0, max_bid, input_type="file reader", delimiter=" ", save_log=False, bid_factor=1):
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
			t0 = time.time()
			a = self.bid(n, b, theta, max_bid) * bid_factor
			a = min(int(a), min(b, max_bid))
			
			t1 = time.time()
			log = str(t1 - t0) + "\t{}\t{}_{}\t{}_{}_{}\t{}_{}\t".format(
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
