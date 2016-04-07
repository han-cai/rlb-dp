import os

import DataPath


def get_Db(campaign, t):
	path = DataPath.rtb_mdp_path + campaign + "/derivative_value_function.txt"
	with open(path) as fin:
		i = 0
		count = len(t)
		for line in fin:
			if i in t:
				with open("/home/hm/Documents/derivative_value_function/" + campaign + "/D({0}, b).txt".format(i), "w") as fout:
					fout.write(line)
				count -= 1
				if count == 0:
					break
			i += 1


def get_Dt(campaign, b):
	#path = DataPath.rtb_mdp_path + campaign + "/derivative_value_function.txt"
	path = "/media/hm/Seagate Backup Plus Drive/data-hcai/" + campaign + "/derivative_value_function.txt"
	with open(path) as fin:
		fout = [0] * len(b)
		for i in range(0, len(b)):
			fout[i] = open("/home/hm/Documents/derivative_value_function/" + campaign + "/D(t, {0}).txt".format(b[i]), "w")
		for line in fin:
			tokens = line[:len(line) - 1].split("\t")
			for i in range(0, len(b)):
				fout[i].write(tokens[b[i]] + "\n")
		for i in range(0, len(b)):
			fout[i].close()


def get_sub_Dtb(campaign, t, b):
	path = DataPath.rtb_mdp_path + campaign + "/derivative_value_function.txt"
	fout = open("/home/hm/Documents/derivative_value_function/" + campaign + "/sub.txt", "w")
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


def get_stationary_points(campaign):
	path = DataPath.rtb_mdp_path + campaign + "/derivative_value_function.txt"
	stationary_points = open(DataPath.rtb_mdp_path + campaign + "/stationary_points.txt", "w")
	with open(path, "r") as fin:
		t = 0
		last_b = 0
		for line in fin:
			line = line[:len(line) - 1]
			tokens = line.split("\t")
			flag = False
			for b in range(last_b, len(tokens)):
				tokens[b] = float(tokens[b])
				if tokens[b] == 0:
					last_b = b
					stationary_points.write("{0}\n".format(b))
					flag = True
					break
			if not flag:
				break
			t += 1
	stationary_points.close()


def get_value_function(campaign):
	T = 10000
	with open("/media/hm/Seagate Backup Plus Drive/data-hcai/" + campaign + "/value_function.txt", "w") as fout:
		for i in range(T):
			with open(DataPath.rtb_mdp_path + campaign + "/D_t_b_train/" + "{0}.txt".format(i)) as fin:
				line = fin.readline()
				line = line[:len(line) - 1].split("\t")
				value_function = [0] * (len(line) + 1)
				fout.write(str(value_function[0]))
				for i in range(len(line)):
					value_function[i + 1] = value_function[i] + float(line[i])
					fout.write("\t{0}".format(value_function[i + 1]))
				fout.write("\n")


if __name__ == "__main__":
	campaign = "2259"
	path = "/home/hm/Documents/derivative_value_function/" + campaign
	if not os.path.exists(path):
		os.mkdir(path)
	#get_sub_Dtb(campaign, 1000, 15000)
	#get_Db(campaign, range(1000, 10000, 500))
	#get_Dt(campaign, range(5000, 60000, 5000))
	#get_stationary_points(campaign)
	#get_value_function(campaign)
