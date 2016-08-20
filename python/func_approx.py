from NN_Approximator import NN_Approximator
import os
import config
from utility import *
import tensorflow as tf
import time
import numpy as np
from sklearn.metrics import mean_squared_error
import sys


def load_data(train_dir, batch_n, b_sample_size, b_bound, dim):
	NB = []
	Dnb = []
	for n in batch_n:
		with open(train_dir + "{}.txt".format(n)) as fin:
			line = fin.readline()
			line = line[:len(line) - 1].split("\t")
			line = line[1:]
			b_list = [i for i in range(b_bound, len(line))]
			np.random.shuffle(b_list)
			if b_sample_size > 0:
				b_list = b_list[:b_sample_size]

			for b in b_list:
				nb = [n, b]
				if dim == 3:
					nb.append(b / n)
				dnb = float(line[b])
				NB.append(nb)
				Dnb.append([dnb])
	NB = np.array(NB)
	Dnb = np.array(Dnb)
	return NB, Dnb


def evaluate_rmse(train_dir, n_list, b_sample_size, batch_size, b_bound, dim, model, echo=False):
	preds = []
	labels = []

	square_error = 0
	cnt = 0
	buf_x_vecs = []
	buf_value_labels = []
	for n in n_list:
		x_vecs, value_labels = load_data(train_dir, [n], b_sample_size, b_bound, dim)

		buf_x_vecs.extend(x_vecs)
		buf_value_labels.extend(value_labels.flatten())
		while len(buf_x_vecs) >= batch_size:
			batch_x_vecs = buf_x_vecs[0: batch_size]
			batch_value_labels = buf_value_labels[0: batch_size]
			feed_dict = {
				model.batch_x_vecs: batch_x_vecs
			}
			batch_predictions = model.batch_value_predictions.eval(feed_dict=feed_dict)
			batch_predictions = batch_predictions.flatten().tolist()
			for _i in range(batch_size):
				if batch_value_labels[_i] == 0:
					continue
				square_error += (batch_value_labels[_i] - batch_predictions[_i]) ** 2
				cnt += 1
			buf_x_vecs = buf_x_vecs[batch_size:]
			buf_value_labels = buf_value_labels[batch_size:]
		if echo:
			print("{}\t{}\t{}".format(n, np.sqrt(square_error / cnt), getTime()))

	for _i in range(len(buf_x_vecs)):
		x_vec = buf_x_vecs[_i: (_i + 1)]
		value_label = buf_value_labels[_i]
		if value_label == 0:
			continue
		feed_dict = {
			model.x_vec: x_vec
		}
		pred = model.value_prediction.eval(feed_dict=feed_dict)
		pred = pred.flatten()
		pred = pred[0]
		square_error += (value_label - pred) ** 2
		cnt += 1

	return np.sqrt(square_error / cnt)


seeds = [0x0123, 0x4567, 0x3210, 0x7654, 0x89AB, 0xCDEF, 0xBA98, 0xFEDC,
	     0x0123, 0x4567, 0x3210, 0x7654, 0x89AB, 0xCDEF, 0xBA98, 0xFEDC]

model = "dnb"
_argv = sys.argv

if model == "dnb":
	dim = 2
	net_type = "nn"
	src = "ipinyou"

	camp = "1458"
	if len(_argv) == 2:
		camp = _argv[1]

	obj_type = "clk"
	clk_vp = 1
	N = 5000
	tag = src + "_" + camp + "_" + model + "_" + net_type + "_N={}_{}".format(N, obj_type) + "_" + getTime()
	if src == "ipinyou":
		data_path = config.ipinyouPath
		camp_info = config.get_camp_info(camp, src)
	elif src == 'vlion':
		data_path = config.vlionPath
		camp_info = config.get_camp_info(camp, src)
	elif src == "yoyi":
		data_path = config.yoyiPath
		camp_info = config.get_camp_info(camp, src)

	opt_obj = Opt_Obj(obj_type, int(clk_vp * camp_info["cost_train"] / camp_info["clk_train"]))
	avg_theta = camp_info["clk_train"] / camp_info["imp_train"]
	if obj_type == "profit":
		avg_theta *= opt_obj.clk_v

	b_bound = 800
	n_bound = 50
	max_train_round = 500
	final_model_path = data_path + camp + "/bid-model/fa_dnb_{}.pickle".format(obj_type)

	n_sample_size = 50
	b_sample_size = 200
	eval_n_sample_size = 500
	eval_b_sample_size = 1000
	batch_size = n_sample_size * b_sample_size

	net_argv = [4, [dim, 30, 15, 1], "tanh"]
	init_rag = avg_theta
	nn_approx = NN_Approximator(net_type, net_argv,
	                                          # data_path + camp + "/bid-model/fa_dnb_{}.pickle".format(obj_type)
	                                          None
	                                          ,
	                                          [('uniform', -0.001, 0.001, seeds[4]),
	                                           ('zero', None),
	                                           ('uniform', -0.001, 0.001, seeds[5]),
	                                           ('zero', None),
	                                           ('uniform', -init_rag, init_rag, seeds[6]),
	                                           ('zero', None)
	                                           ],
	                                          [dim], batch_size,
	                                          ['adam', 3e-5, 1e-8, 'sum']
	                                          # ["ftrl", 1e-2, "mean"]
	                                          # ['sgd', 2e-2, 'mean']
	                                          )

	train_dir = data_path + camp + "/fa-train/rlb_dnb_gamma=1_N={}_{}_1/".format(N, obj_type)
	n_list = [i for i in range(n_bound + 1, N)]

	# train, eval
	mode = "train"
	save_model = True
	model_path = config.projectPath + "fa-model/" + tag + "/"
	log_path = config.projectPath + "fa-log/" + tag + ".txt"
	if save_model and mode == "train":
		os.mkdir(model_path)

	print(tag)
	print(nn_approx.log)

	if mode == "train":
		if save_model:
			write_log(log_path, nn_approx.log)

		with tf.Session(graph=nn_approx.graph) as sess:
			tf.initialize_all_variables().run()
			print("model initialized")

			_iter = 0
			perf = 1e5
			start_time = time.time()
			while True:
				_iter += 1
				print("iteration {0} start".format(_iter))
				np.random.shuffle(n_list)

				buf_loss = []
				buf_predictions = []
				buf_labels = []

				_round = int(len(n_list) / n_sample_size)
				for _i in range(_round):
					batch_n = n_list[_i * n_sample_size: (_i + 1) * n_sample_size]
					batch_x_vecs, batch_value_labels = load_data(train_dir, batch_n, b_sample_size, b_bound, dim)

					feed_dict = {
						nn_approx.batch_x_vecs: batch_x_vecs,
						nn_approx.batch_value_labels: batch_value_labels
					}

					_, loss, batch_predictions = sess.run([nn_approx.opt_value, nn_approx.loss_value,
					                                       nn_approx.batch_value_predictions], feed_dict=feed_dict)
					buf_loss.append(np.sqrt(loss) / avg_theta)
					buf_labels.extend(batch_value_labels.flatten())
					buf_predictions.extend(batch_predictions.flatten())
				buf_loss = np.array(buf_loss)
				buf_rmse = np.sqrt(mean_squared_error(buf_labels, buf_predictions))
				buf_log = "buf loss, max={:.6f}\tmin={:.6f}\tmean={:.6f}\tbuf rmse={}\ttime={}".format(
					buf_loss.max(), buf_loss.min(), buf_loss.mean(), buf_rmse / avg_theta, getTime())
				print(buf_log)

				np.random.shuffle(n_list)
				eval_rmse = evaluate_rmse(train_dir, n_list[:eval_n_sample_size], eval_b_sample_size, batch_size,
				                          b_bound, dim, nn_approx)
				eval_log = "iteration={}\ttime={}\teval rmse={}\tbuf rmse={}" \
					.format(_iter, time.time() - start_time, eval_rmse / avg_theta, buf_rmse / avg_theta)
				print(eval_log)
				if save_model:
					write_log(log_path, eval_log)
					nn_approx.dump(model_path + "{}_{}.pickle".format(tag, _iter), net_type, net_argv)
					n_perf = (buf_rmse + eval_rmse) / avg_theta
					if n_perf < perf:
						perf = n_perf
						nn_approx.dump(final_model_path, net_type, net_argv)
				start_time = time.time()
				if _iter >= max_train_round:
					break

	elif mode == "eval":
		with tf.Session(graph=nn_approx.graph) as sess:
			tf.initialize_all_variables().run()
			eval_rmse = evaluate_rmse(train_dir, n_list, -1, batch_size, b_bound, dim, nn_approx, echo=True)

			print("campaign={}\tfull eval rmse={}".format(camp, eval_rmse / avg_theta))
