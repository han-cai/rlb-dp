import os
import FunctionLibrary.StringOperation
import random
import datetime
yoyiPath = "/home/hm/Project/data/reinforce-bid/yoyi-data/"
#campaign_list = {"0106", "0107", "0108", "0109", "0110", "0111", "0112", "0113", "0117", "0123", "0124", "0125", "0126","0127", "0130", "0201", "0202", "1224"}
campaign_list = {"0123", "0124", "0125", "0127", "0130"}
feature_index_name = "featindex_lr_15.txt.50302020.7"
testSequenceName = "test.sequence.txt"
trainOriginName = "train_lr_15.txt.50302020.7"
testOriginName = "cross_lr_15.txt.50302020.7"
rtb_yoyi = "/home/hm/Project/data/reinforce-bid/yoyi-rtb/"
rtb_history_name = "history.txt"
rtb_train_name = "train.rtb.txt"
rtb_test_name = "test.rtb.txt"
rtb_validation_name = "validation.txt"

sec = datetime.datetime.now()
random.seed(sec.hour * 3600000 + sec.minute * 60000 + sec.second * 1000 + sec.microsecond)


def prepare_train_data_from_ipinyou(inPath, historyPath, trainPath, dimension, T, ratio, test_num):
	history = open(historyPath, "w")
	train = open(trainPath, "w")
	history.write("{0}\t{1}\n".format(dimension, T))
	train.write("{0}\t{1}\n".format(dimension, T))
	train_num = int(test_num * ratio) * T

	total_num = 0
	with open(inPath, "r") as fin:
		total_num = len(fin.readlines())
	history_num = total_num - train_num

	period = 1
	cost = 0
	t = 0
	store = [0] * T
	counter = 0
	with open(inPath, "r") as fin:
		for line in fin:
			counter += 1
			if counter <= history_num:
				history.write(line)
			else:
				store[t] = line
				line = line[0:len(line) - 1].split("\t")
				cost += int(line[1])
				t += 1
				if t == T:
					train.write("{0}\t{1}\n".format(period, cost))
					for record in store:
						train.write(record)
					cost = 0
					t = 0
					period += 1
	history.flush()
	train.flush()
	history.close()
	train.close()
	if train_num == 0:
		os.remove(trainPath)


def prepare_test_data_from_ipinyou(inPath, outPath, dimension, T):
	period = 1
	cost = 0
	t = 0
	fout = open(outPath, "w")
	fout.write("{0}\t{1}\n".format(dimension, T))
	store = [0] * T
	with open(inPath, "r") as fin:
		for line in fin:
			store[t] = line
			line = line[0:len(line) - 1].split("\t")
			cost += int(line[1])
			t += 1
			if t == T:
				fout.write("{0}\t{1}\n".format(period, cost))
				for record in store:
					fout.write(record)
				cost = 0
				t = 0
				period += 1
	fout.write("{0}\t{1}\n".format(period, cost))
	for i in range(0, t):
		fout.write(store[i])
	fout.flush()
	fout.close()
	return period - 1


def prepare_data(T, ratio):
	global campaign_list, yoyiPath
	for campaign in campaign_list:
		dimension = 0
		with open(yoyiPath + campaign + "/" + feature_index_name, "r") as fin:
			dimension = len(fin.readlines())
		inPath = yoyiPath + campaign + "/" + testOriginName
		outPath = rtb_yoyi + campaign
		if not os.path.exists(outPath):
			os.mkdir(outPath)
		outPath += "/" + rtb_test_name
		test_num = prepare_test_data_from_ipinyou(inPath, outPath, dimension, T)

		inPath = yoyiPath + campaign + "/" + trainOriginName
		historyPath = rtb_yoyi + campaign + "/" + rtb_history_name
		outPath = rtb_yoyi + campaign + "/" + rtb_train_name
		prepare_train_data_from_ipinyou(inPath, historyPath, outPath, dimension, T, ratio, test_num)


def tmp():
	for campaign in campaign_list:
		max_price = 0
		lines = []
		with open(yoyiPath + campaign + "/" + testOriginName) as fin:
			for line in fin:
				line = line[:len(line) - 1].split("\t")
				price = int(line[1])
				price = int(price / 1000)
				max_price = max(max_price, price)
				line[1] = str(price)
				lines.append("\t".join(line) + "\n")
		with open(yoyiPath + campaign + "/" + testOriginName, "w") as fout:
			for line in lines:
				fout.write(line)
		lines = []
		with open(yoyiPath + campaign + "/" + trainOriginName) as fin:
			for line in fin:
				line = line[:len(line) - 1].split("\t")
				price = int(line[1])
				price = int(price / 1000)
				max_price = max(max_price, price)
				line[1] = str(price)
				lines.append("\t".join(line) + "\n")
		random.shuffle(lines)
		with open(yoyiPath + campaign + "/" + trainOriginName, "w") as fout:
			for line in lines:
				fout.write(line)
		print(campaign + "\t{0}".format(max_price))


def get_max_price():
	for campaign in campaign_list:
		max_price = 300
		total_num = 0
		num = 0
		with open(yoyiPath + campaign + "/" + testOriginName) as fin:
			for line in fin:
				line = line[:len(line) - 1].split("\t")
				price = int(line[1])
				if line[0] == '1':
					total_num += 1
					if price <= max_price:
						num += 1
		print(campaign + "\t{0}".format(num / total_num))


def clean():
	for campaign in campaign_list:
		lines = []
		with open(yoyiPath + campaign + "/" + testOriginName) as fin:
			for line in fin:
				line = line[:len(line) - 1].split("\t")
				if line[0] == '0' or line[0] == '1':
					lines.append("\t".join(line) + "\n")
		'''
		with open(yoyiPath + campaign + "/" + testOriginName, "w") as fout:
			for line in lines:
				fout.write(line)
		'''
		lines = []
		with open(yoyiPath + campaign + "/" + trainOriginName) as fin:
			for line in fin:
				line = line[:len(line) - 1].split("\t")
				if line[0] == '0' or line[0] == '1':
					lines.append("\t".join(line) + "\n")
		'''
		with open(yoyiPath + campaign + "/" + trainOriginName, "w") as fout:
			for line in lines:
				fout.write(line)
		print(campaign + "\t{0}".format(max_price))
		'''


if __name__ == "__main__":
	prepare_data(1000, 0)