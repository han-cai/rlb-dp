import os
import FunctionLibrary.StringOperation
import DataPath


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
				line = line[0:len(line) - 1].split(" ")
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
			line = line[0:len(line) - 1].split(" ")
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
	for campaign in DataPath.campaign_list:
		dimension = 0
		with open(DataPath.ipinyouPath + campaign + "/" + DataPath.feature_index_name, "r") as fin:
			dimension = len(fin.readlines())
		inPath = DataPath.ipinyouPath + campaign + "/" + DataPath.testOriginName
		outPath = DataPath.rtb_mdp_path + campaign
		if not os.path.exists(outPath):
			os.mkdir(outPath)
		outPath += "/" + DataPath.rtb_test_name
		test_num = prepare_test_data_from_ipinyou(inPath, outPath, dimension, T)

		inPath = DataPath.ipinyouPath + campaign + "/" + DataPath.trainOriginName
		historyPath = DataPath.rtb_mdp_path + campaign + "/" + DataPath.rtb_history_name
		outPath = DataPath.rtb_mdp_path + campaign + "/" + DataPath.rtb_train_name
		prepare_train_data_from_ipinyou(inPath, historyPath, outPath, dimension, T, ratio, test_num)

if __name__ == "__main__":
	prepare_data(100000, 0)