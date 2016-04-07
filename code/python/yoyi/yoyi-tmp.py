rtb_yoyi = "/home/hm/Project/data/reinforce-bid/yoyi-rtb/"
rtb_history_name = "history.txt"
lg_weight_name = "lg_weights.txt"
rtb_validation_name = "validation.txt"
rtb_test_name = "test.rtb.txt"
projectPath = "/home/hm/Project/reinforce-bid/code/Python/"
yoyiPath = "/home/hm/Project/data/reinforce-bid/yoyi-data/"
testOriginName = "cross_lr_15.txt.50302020.7"


def get_stationary_points(campaign):
	path = rtb_yoyi + campaign + "/derivative_value_function.txt"
	stationary_points = open(rtb_yoyi + campaign + "/stationary_points.txt", "w")
	with open(path, "r") as fin:
		t = 0
		last_b = 0
		for line in fin:
			line = line[:len(line) - 1]
			tokens = line.split("\t")
			flag = False
			for b in range(last_b, len(tokens)):
				tokens[b] = float(tokens[b])
				if abs(tokens[b]) <= 1E-26:
					last_b = b
					stationary_points.write("{0}\n".format(b))
					flag = True
					break
			if not flag:
				break
			t += 1
	stationary_points.close()


def click_path(campaign):
	with open(yoyiPath + campaign + "/" + testOriginName) as fin:
		auc = 0
		clk = 0
		for line in fin:
			line = line[:len(line) - 1].split("\t")
			auc += 1
			if line[0] == '1':
				clk += 1
			print("{0}\t{1}".format(auc, clk))


if __name__ == "__main__":
	campaign = "0130"
	get_stationary_points(campaign)