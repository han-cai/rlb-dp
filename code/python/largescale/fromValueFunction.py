import os

import DataPath

avg_ctr = {"1458": 0.0007959634856, "2259": 0.0003351062047, "2261": 0.0003010396776, "2821": 0.0006373997116,
           "2997": 0.004436094317, "3358": 0.0007795171815, "3386": 0.000728983265, "3427": 0.0007425499226,
           "3476": 0.0005212245478}


def get_stationary_points(campaign):
	ctr = avg_ctr[campaign]
	path = DataPath.rtb_mdp_path + campaign + "/value_function.txt"
	stationary_points = open("/home/hm/Documents/value_function/" + campaign + "/stationary_points.txt", "w")
	with open(path, "r") as fin:
		t = 0
		last_b = 0
		for line in fin:
			line = line[:len(line) - 1]
			tokens = line.split("\t")
			flag = False
			for b in range(last_b, len(tokens)):
				tokens[b] = float(tokens[b])
				if abs(tokens[b] - t * ctr) <= 0.0000000001:
					last_b = b
					stationary_points.write("{0}\n".format(b))
					flag = True
					break
			if not flag:
				break
			t += 1
	stationary_points.close()


def get_Vb(campaign, t):
	path = DataPath.rtb_mdp_path + campaign + "/value_function.txt"
	with open(path) as fin:
		i = 0
		for line in fin:
			if i in t:
				with open("/home/hm/Documents/value_function/" + campaign + "/V({0}, b).txt".format(i), "w") as fout:
					fout.write(line)
			i += 1


def get_Vt(campaign, b):
	path = DataPath.rtb_mdp_path + campaign + "/value_function.txt"
	with open(path) as fin:
		fout = [0] * len(b)
		for i in range(0, len(b)):
			fout[i] = open("/home/hm/Documents/value_function/" + campaign + "/V(t, {0}).txt".format(b[i]), "w")
		for line in fin:
			tokens = line[:len(line) - 1].split("\t")
			for i in range(0, len(b)):
				fout[i].write(tokens[b[i]] + "\n")
		for i in range(0, len(b)):
			fout[i].close()


def get_sub_Vtb(campaign, t, b):
	path = DataPath.rtb_mdp_path + campaign + "/value_function.txt"
	fout = open("/home/hm/Documents/value_function/" + campaign + "/sub.txt", "w")
	with open(path) as fin:
		for i in range(0, t + 1):
			line = fin.readline()
			line = line[:len(line) - 1].split("\t")
			sub = line[0]
			for j in range(0, b):
				sub += "\t" + line[j + 1]
			sub += "\n"
			fout.write(sub)
	fout.flush()
	fout.close()


def get_Dtb(campaign):
	fout = open(DataPath.rtb_mdp_path + campaign + "/derivative_value_function.txt", "w")
	with open(DataPath.rtb_mdp_path + campaign + "/value_function.txt", "r") as fin:
		for line in fin:
			line = line[:len(line) - 1].split("\t")
			line[0] = float(line[0])
			Db = []
			for i in range(0, len(line) - 1):
				line[i + 1] = float(line[i + 1])
				value = line[i + 1] - line[i]
				if value == 0:
					Db.append(0)
				else:
					Db.append(value)
			for i in range(len(Db) - 1):
				fout.write("{0}\t".format(Db[i]))
			fout.write("{0}\n".format(Db[len(Db) - 1]))
	fout.flush()
	fout.close()


if __name__ == "__main__":
	campaign = "3358"
	path = "/home/hm/Documents/value_function/" + campaign
	if not os.path.exists(path):
		os.mkdir(path)
	#get_sub_Vtb(campaign, 1000, 15000)
	get_Vb(campaign, range(1000, 10000, 500))
	#get_Vt(campaign, range(20000, 120000, 20000))
	#get_stationary_points(campaign)
