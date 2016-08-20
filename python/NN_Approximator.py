from utility import *
import tensorflow as tf
import os
import numpy as np


class NN_Approximator:
	def __init__(self, net_type, net_argv, init_path, init_argv, dim_argv, batch_size, opt_argv):
		if net_type == "nn":
			self.graph = tf.Graph()
			nb_dim = dim_argv[0]
			depth, h_dims, act_func = net_argv
			with self.graph.as_default():
				var_init = []
				if not init_path:
					_j = 0
					for _i in range(depth - 1):
						var_init.extend([("W{}".format(_i), [h_dims[_i], h_dims[_i + 1]], init_argv[_j][0], init_argv[_j][1:]),
						                 ("b{}".format(_i), [1, h_dims[_i + 1]], init_argv[_j + 1][0], init_argv[_j + 1][1:])
						                 ])
						_j += 2
				var_map = init_var_map(init_path, var_init)
				self.W = [0] * (depth - 1)
				self.b = [0] * (depth - 1)
				for _i in range(depth - 1):
					self.W[_i] = tf.Variable(var_map["W{}".format(_i)])
					self.b[_i] = tf.Variable(var_map["b{}".format(_i)])

				self.x_vec = tf.placeholder(tf.float32, shape=[1, nb_dim])
				self.batch_x_vecs = tf.placeholder(tf.float32, shape=[batch_size, nb_dim])
				self.batch_value_labels = tf.placeholder(tf.float32, shape=[batch_size, 1])

				self.value_prediction = self.forward(net_type, depth, act_func, self.x_vec, [self.W, self.b])
				self.batch_value_predictions = self.forward(net_type, depth, act_func, self.batch_x_vecs, [self.W, self.b])

				square_loss_value = tf.square(self.batch_value_labels - self.batch_value_predictions)
				if opt_argv[-1] == "sum":
					self.loss_value = tf.reduce_sum(square_loss_value)
				elif opt_argv[-1] == "mean":
					self.loss_value = tf.reduce_mean(square_loss_value)

				self.opt_value = build_optimizer(opt_argv, self.loss_value)

				self.init = tf.initialize_all_variables()
		self.log = "net_type={}\tnet_argv={}\tinit_path={}\tinit_argv={}\tdim_argv={}\tbatch_size={}\topt_argv={}"\
			.format(net_type, net_argv, init_path, init_argv, dim_argv, batch_size, opt_argv)

	@staticmethod
	def forward(net_type, depth, act_func, x_vec, _vars):
		if net_type == "nn":
			W, b = _vars
			a = [0] * (depth - 1)
			z = [0] * (depth - 1)
			z[0] = x_vec
			for _i in range(depth - 2):
				a[_i + 1] = tf.matmul(z[_i], W[_i]) + b[_i]
				z[_i + 1] = activate(act_func, a[_i + 1])
			y_hat = tf.matmul(z[depth - 2], W[depth - 2]) + b[depth - 2]
		return y_hat

	@staticmethod
	def separate_value_table(in_path, out_dir, option="n", list=[]):
		if not os.path.exists(out_dir):
			os.mkdir(out_dir)
		if option == "n":
			n = 0
			with open(in_path, "r") as fin:
				for line in fin:
					with open(out_dir + "/{}.txt".format(n), "w") as fout:
						fout.write("n={}\t".format(n) + line)
					n += 1
		if option == "b":
			with open(in_path, "r") as fin:
				num = len(list)
				fouts = [0] * num
				for i in range(num):
					fouts[i] = open(out_dir + "/{}.txt".format(list[i]), "w")
				for line in fin:
					line = line[:len(line) - 1].split("\t")
					for i in range(num):
						fouts[i].write(line[list[i]] + "\n")
				for i in range(num):
					fouts[i].close()
				
	def dump(self, model_path, net_type, net_argv):
		var_map = {}
		if net_type == "nn":
			depth, h_dims, act_func = net_argv
			for _i in range(depth - 1):
				var_map["W{}".format(_i)] = self.W[_i].eval()
				var_map["b{}".format(_i)] = self.b[_i].eval()
			var_map["depth"] = depth
			var_map["h_dims"] = h_dims
			var_map["act_func"] = act_func
		var_map["net_type"] = net_type
		pickle.dump(var_map, open(model_path, 'wb'))
		print("NN_Approximator model dumped at {0}".format(model_path))

	@staticmethod
	def pickle2txt(pickle_path, txt_path):
		var_map = pickle.load(open(pickle_path, "rb"))
		net_type = var_map["net_type"]
		if net_type == "nn":
			depth = var_map["depth"]
			h_dims = var_map["h_dims"]
			act_func = var_map["act_func"]

			str_h_dims = []
			for item in h_dims:
				str_h_dims.append(str(item))
			with open(txt_path, "w") as fout:
				out = "{}\t{}\t{}\t{}\n".format(net_type, depth, "_".join(str_h_dims), act_func)
				fout.write(out)
				for i in range(depth - 1):
					Wi = var_map["W{}".format(i)]
					bi = var_map["b{}".format(i)]
					_is = h_dims[i]
					_os = h_dims[i + 1]
					str_W = []
					str_b = []
					for j in range(_os):
						seg_W = []
						for k in range(_is):
							seg_W.append(str(Wi[k][j]))
						str_W.append("_".join(seg_W))
						str_b.append(str(bi[0][j]))
					str_W = "\t".join(str_W)
					str_b = "\t".join(str_b)
					fout.write("W{}".format(i) + "\t" + str_W + "\n")
					fout.write("b{}".format(i) + "\t" + str_b + "\n")
