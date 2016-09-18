from sklearn.metrics import roc_auc_score
from sklearn.metrics import log_loss
import numpy as np
from LR import LR
import tensorflow as tf
import time
import config
import utility
import os


def collect(fin, size=100000, shuf=True):
	buf = []
	for i in range(size):
		try:
			line = next(fin)
			buf.append(line)
		except StopIteration as e:
			break
	if shuf:
		np.random.shuffle(buf)
	return buf


def load_data(fin, size, X_dim, X_field, shuf=True):
	X_ind = []
	Y = []
	Wt = []
	buf = collect(fin, size, shuf)
	if len(buf) < 1:
		return None, None, None

	for line in buf:
		fields = line.strip().split()
		Y.append(int(fields[0]))
		x_ind = [int(x.split(b':')[0]) for x in fields[2:]]
		l = len(x_ind)
		wt = [1] * l
		X_ind.append(x_ind)
		Wt.append(wt)
		X_ind[-1].extend([X_dim] * (X_field - l))
		Wt[-1].extend([0] * (X_field - l))

	X_ind = np.array(X_ind)
	Wt = np.array(Wt)
	Y = np.array(Y)

	return X_ind, Wt, Y


def evaluate(eval_path, buf_size, batch_size, X_dim, X_field, model):
	eval_data_set = open(eval_path, 'rb')

	preds = []
	labels = []

	while True:
		buf_x_ids, buf_wts, buf_labels = load_data(eval_data_set, buf_size, X_dim, X_field, shuf=False)

		if buf_x_ids is None:
			break

		_round = int(len(buf_labels) / batch_size)
		for _i in range(_round):
			batch_x_ids = buf_x_ids[_i * batch_size: (_i + 1) * batch_size]
			batch_wts = buf_wts[_i * batch_size: (_i + 1) * batch_size]
			if 'LR' in algo:
				feed_dict = {model.batch_x_ids: batch_x_ids,
				             model.batch_wts: batch_wts}

			batch_predictions = model.batch_predictions.eval(feed_dict=feed_dict)
			preds.extend(batch_predictions)

		op = _round * batch_size
		for _i in range(op, len(buf_labels)):
			x_id = buf_x_ids[_i: (_i + 1)]
			wt = buf_wts[_i: (_i + 1)]
			if 'LR' in algo:
				feed_dict = {model.x_id: x_id,
				             model.wt: wt}
			pred = model.prediction.eval(feed_dict=feed_dict)[0][0]
			preds.append(pred)
		labels.extend(buf_labels)

	return np.array(labels), np.array(preds)


if __name__ == '__main__':
	src = "vlion"
	camp = "231"
	algo = "LR"
	tag = src + "_" + camp + "_" + algo + "_" + utility.getTime()
	if src == "ipinyou":
		data_path = config.ipinyouPath
		camp_info = config.get_camp_info(camp, src)
	elif src == 'vlion':
		data_path = config.vlionPath
		camp_info = config.get_camp_info(camp, src)
	elif src == "yoyi":
		data_path = config.yoyiPath
		camp_info = config.get_camp_info(camp, src)
		
	train_path = data_path + camp + "/urp-train/train.yzx.shuf.txt"
	test_path = data_path + camp + "/urp-train/test.yzx.shuf.txt"
	eval_path = data_path + camp + "/urp-train/test.yzx.eval.txt"

	# mode options: train, test, write prediction
	mode = "write prediction"
	save_model = True
	model_path = config.projectPath + "urp-model/" + tag + "/"
	log_path = config.projectPath + "urp-log/" + tag + ".txt"
	if save_model and mode == "train":
		os.mkdir(model_path)

	print(tag)

	X_dim = camp_info["dim"]
	X_field = camp_info["field"]

	seeds = [0x0123, 0x4567, 0x3210, 0x7654, 0x89AB, 0xCDEF, 0xBA98, 0xFEDC,
	         0x0123, 0x4567, 0x3210, 0x7654, 0x89AB, 0xCDEF, 0xBA98, 0xFEDC]

	if "LR" in algo:
		batch_size = 10000
		buf_size = 1000000
		model = LR([X_dim, X_field], batch_size,
		           data_path + camp + "/urp-model/lr.pickle"
		           # None
		           , [('uniform', -0.001, 0.001, seeds[4])], ['sgd', 1e-3, 'sum'], 0)  # 1e-3

	print("batch size={0}, buf size={1}".format(batch_size, buf_size))
	print(model.log)

	if mode == "train":
		if save_model:
			utility.write_log(log_path, model.log)

		# gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.9)
		# sess_config = tf.ConfigProto(gpu_options=gpu_options)
		# with tf.Session(graph=model.graph, config=sess_config) as sess:
		with tf.Session(graph=model.graph) as sess:
			tf.initialize_all_variables().run()
			print("model initialized")

			_iter = 0
			while True:
				_iter += 1
				print("iteration {0} start".format(_iter))

				train_data_set = open(train_path, 'rb')
				start_time = time.time()
				step = 0
				batch_auc = -1

				while True:
					buf_x_ids, buf_wts, buf_labels = load_data(train_data_set, buf_size, X_dim, X_field)

					buf_predictions = []
					buf_loss = []

					if buf_x_ids is None:
						eval_labels, eval_preds = evaluate(eval_path, buf_size, batch_size, X_dim, X_field, model)
						eval_auc = roc_auc_score(eval_labels, eval_preds)
						eval_log_loss = log_loss(eval_labels, eval_preds)
						base_log_loss = log_loss(eval_labels,
						                         [camp_info["clk_train"] / camp_info["imp_train"]] * len(eval_labels))

						eval_log = "iteration={}\tstep={}\ttime={}\teval auc={}\teval log loss={}" \
							.format(_iter, step, time.time() - start_time, eval_auc, eval_log_loss / base_log_loss)
						print(eval_log)
						if save_model:
							utility.write_log(log_path, eval_log)
							model.dump(model_path + "{}_{}_{}.pickle".format(tag, _iter, step))
						start_time = time.time()
						break

					_round = int(len(buf_labels) / batch_size)
					for _i in range(_round):
						batch_x_ids = buf_x_ids[_i * batch_size: (_i + 1) * batch_size]
						batch_wts = buf_wts[_i * batch_size: (_i + 1) * batch_size]
						batch_labels = buf_labels[_i * batch_size: (_i + 1) * batch_size]

						if 'LR' in algo:
							feed_dict = {model.batch_labels: batch_labels,
							             model.batch_x_ids: batch_x_ids,
							             model.batch_wts: batch_wts}

						_, loss, batch_predictions = sess.run([model.opt, model.loss, model.batch_predictions],
						                                      feed_dict=feed_dict)
						buf_loss.append(loss)
						buf_predictions.extend(batch_predictions)
						step += batch_size

					buf_loss = np.array(buf_loss)
					buf_auc = roc_auc_score(buf_labels[:len(buf_predictions)], buf_predictions)
					print("buf loss, max={:.3f}\tmin={:.3f}\tmean={:.3f}\tbuf auc={:.3f}\ttime={}".format(
						buf_loss.max(), buf_loss.min(), buf_loss.mean(), buf_auc, utility.getTime()))

					if step % (5 * buf_size) == 0:
						eval_labels, eval_preds = evaluate(eval_path, buf_size, batch_size, X_dim, X_field, model)
						eval_auc = roc_auc_score(eval_labels, eval_preds)
						eval_log_loss = log_loss(eval_labels, eval_preds)
						base_log_loss = log_loss(eval_labels, [camp_info["clk_train"] / camp_info["imp_train"]] * len(eval_labels))

						eval_log = "iteration={}\tstep={}\ttime={}\teval auc={}\teval log loss={}" \
							.format(_iter, step, time.time() - start_time, eval_auc, eval_log_loss/base_log_loss)
						print(eval_log)
						if save_model:
							utility.write_log(log_path, eval_log)
							model.dump(model_path + "{}_{}_{}.pickle".format(tag, _iter, step))
						start_time = time.time()

	elif mode == "test":
		with tf.Session(graph=model.graph) as sess:
			tf.initialize_all_variables().run()
			test_labels, test_preds = evaluate(test_path, buf_size, batch_size, X_dim, X_field, model)

			test_auc = roc_auc_score(test_labels, test_preds)
			test_log_loss = log_loss(test_labels, test_preds)
			base_log_loss = log_loss(test_labels, [camp_info["clk_train"] / camp_info["imp_train"]] * len(test_labels))
			print("campaign={}\talgorithm={}\ttest auc={}\ttest log loss".format(camp, algo, test_auc, test_log_loss / base_log_loss))

	elif mode == "write prediction":
		train_yzx = data_path + camp + "/train.yzx.txt"
		test_yzx = data_path + camp + "/test.yzx.txt"
		train_theta = data_path + camp + "/train.theta.txt"
		test_theta = data_path + camp + "/test.theta.txt"
		with tf.Session(graph=model.graph) as sess:
			tf.initialize_all_variables().run()

			labels, preds = evaluate(test_yzx, buf_size, batch_size, X_dim, X_field, model)
			with open(test_yzx, "r") as fin:
				with open(test_theta, "w") as fout:
					_i = 0
					for line in fin:
						line = line[:len(line) - 1].split(" ")
						fout.write("{} {} {}\n".format(line[0], line[1], preds[_i]))
						_i += 1

			labels, preds = evaluate(train_yzx, buf_size, batch_size, X_dim, X_field, model)
			with open(train_yzx, "r") as fin:
				with open(train_theta, "w") as fout:
					_i = 0
					for line in fin:
						line = line[:len(line) - 1].split(" ")
						fout.write("{} {} {}\n".format(line[0], line[1], preds[_i]))
						_i += 1
