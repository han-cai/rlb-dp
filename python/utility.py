import _pickle as pickle

import time
import numpy as np
import tensorflow as tf
import math


def sigmoid(x):
  return 1 / (1 + math.exp(-x))


def getTime():
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def write_log(log_path, line, echo=False):
	with open(log_path, "a") as log_in:
		log_in.write(line + "\n")
		if echo:
			print(line)


def activate(act_func, x):
	if act_func == 'tanh':
		return tf.tanh(x)
	elif act_func == 'relu':
		return tf.nn.relu(x)
	else:
		return tf.sigmoid(x)


def activate_calc(act_func, x):
	if act_func == "tanh":
		return np.tanh(x)
	elif act_func == "relu":
		return max(0, x)
	else:
		return sigmoid(x)


def init_var_map(init_path, _vars):
	if init_path:
		var_map = pickle.load(open(init_path, "rb"))
	else:
		var_map = {}

	for i in range(len(_vars)):
		key, shape, init_method, init_argv = _vars[i]
		if key not in var_map.keys():
			if init_method == "normal":
				mean, dev, seed = init_argv
				var_map[key] = tf.random_normal(shape, mean, dev, seed=seed)
			elif init_method == "uniform":
				min_val, max_val, seed = init_argv
				var_map[key] = tf.random_uniform(shape, min_val, max_val, seed=seed)
			else:
				var_map[key] = tf.zeros(shape)

	return var_map


def build_optimizer(opt_argv, loss):
	opt_method = opt_argv[0]
	if opt_method == 'adam':
		_learning_rate, _epsilon = opt_argv[1:3]
		opt = tf.train.AdamOptimizer(learning_rate=_learning_rate, epsilon=_epsilon).minimize(loss)
	elif opt_method == 'ftrl':
		_learning_rate = opt_argv[1]
		opt = tf.train.FtrlOptimizer(learning_rate=_learning_rate).minimize(loss)
	else:
		_learning_rate = opt_argv[1]
		opt = tf.train.GradientDescentOptimizer(learning_rate=_learning_rate).minimize(loss)
	return opt


# obj_type: clk, profit, imp
class Opt_Obj:
	def __init__(self, obj_type="clk", clk_v=500):
		self.obj_type = obj_type
		self.clk_v = clk_v
		if obj_type == "clk":
			self.v1 = 1
			self.v0 = 0
			self.w = 0
		elif obj_type == "profit":
			self.v1 = clk_v
			self.v0 = 1
			self.w = 0
		else:
			self.v1 = 0
			self.v0 = 0
			self.w = 1

	def get_obj(self, imp, clk, cost):
		return self.v1 * clk - self.v0 * cost + self.w * imp


def calc_m_pdf(m_counter, laplace=1):
	m_pdf = [0] * len(m_counter)
	sum = 0
	for i in range(0, len(m_counter)):
		sum += m_counter[i]
	for i in range(0, len(m_counter)):
		m_pdf[i] = (m_counter[i] + laplace) / (
			sum + len(m_counter) * laplace)
	return m_pdf


def str_list2float_list(str_list):
	res = []
	for _str in str_list:
		res.append(float(_str))
	return res
