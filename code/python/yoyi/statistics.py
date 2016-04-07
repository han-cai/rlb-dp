
yoyiPath = "/home/hm/Project/data/reinforce-bid/yoyi-data/"
campaign_list = ["0123", "0124", "0125", "0127", "0130"]
feature_index_name = "featindex_lr_15.txt.50302020.7"
testSequenceName = "test.sequence.txt"
trainOriginName = "train_lr_15.txt.50302020.7"
testOriginName = "cross_lr_15.txt.50302020.7"
rtb_yoyi = "/home/hm/Project/data/reinforce-bid/yoyi-rtb/"
rtb_history_name = "history.txt"
rtb_train_name = "train.rtb.txt"
rtb_test_name = "test.rtb.txt"
rtb_validation_name = "validation.txt"

for campaign in campaign_list:
	imp = 0
	clk = 0
	cost = 0
	with open(yoyiPath + campaign + "/" + trainOriginName) as fin:
		ip1 = 0
		ip2 = 0
		c1 = 0
		c2 = 0
		for line in fin:
			line = line[:len(line) - 1].split("\t")
			click = int(line[0])
			price = int(line[1])

			if click == 1:
				clk += 1
				ip1 += 1
				c1 += price
			else:
				ip2 += 1
				c2 += price
		cost = c1 + c2 * 100
		imp = ip1 + ip2 * 100
	with open(yoyiPath + campaign + "/" + testOriginName) as fin:
		for line in fin:
			line = line[:len(line) - 1].split("\t")
			click = int(line[0])
			price = int(line[1])

			imp += 1
			if click == 1:
				clk += 1
			cost += price

	print(campaign + "\t{0}\t{1}\t{2}".format(imp, clk, cost))