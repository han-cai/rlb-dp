from utility import *


class LR:
	def __init__(self, dim_argv, batch_size, init_path, init_argv, opt_argv, _lambda):
		self.graph = tf.Graph()
		dim, field = dim_argv
		with self.graph.as_default():
			var_map = init_var_map(init_path, [("W", [dim + 1, 1], init_argv[0][0], init_argv[0][1:])])
			self.W = tf.Variable(var_map["W"])

			# single prediction channel
			self.x_id = tf.placeholder(tf.int32, shape=[1, field])
			self.wt = tf.placeholder(tf.float32, shape=[1, field])
			regression = self.regression(self.x_id, self.wt, self.W)
			self.prediction = tf.sigmoid(regression)

			# batch prediction channel
			self.batch_x_ids = tf.placeholder(tf.int32, shape=[batch_size, field])
			self.batch_wts = tf.placeholder(tf.float32, shape=[batch_size, field])
			batch_regressions = tf.reshape(self.regression(self.batch_x_ids, self.batch_wts, self.W), [-1])
			self.batch_predictions = tf.sigmoid(batch_regressions)

			# batch train channel
			self.batch_labels = tf.placeholder(tf.float32, shape=[batch_size])
			log_loss = tf.nn.sigmoid_cross_entropy_with_logits(batch_regressions, self.batch_labels)
			if opt_argv[-1] == 'sum':
				self.loss = tf.reduce_sum(log_loss)
			else:
				self.loss = tf.reduce_mean(log_loss)
			self.loss += _lambda * tf.nn.l2_loss(self.W)

			self.opt = build_optimizer(opt_argv, self.loss)
		self.log = "dim_argv={}\tbatch_size={}\tinit_path={}\tinit_argv={}\topt_argv={}\t_lambda={}"\
			.format(dim_argv, batch_size, init_path, init_argv, opt_argv, _lambda)

	@staticmethod
	def regression(x_id, x_wt, W_lr):
		theta_gather_weights = tf.gather(W_lr, x_id)
		wt_shape = x_wt.get_shape().as_list()
		wt_shape.append(1)
		theta_weighted_gather_weights = tf.mul(theta_gather_weights, tf.reshape(x_wt, wt_shape))
		theta_regression = tf.reduce_sum(theta_weighted_gather_weights, 1)
		return theta_regression

	def dump(self, model_path):
		var_map = {'W': self.W.eval()}
		pickle.dump(var_map, open(model_path, 'wb'))
		print("LR model dumped at {0}".format(model_path))
