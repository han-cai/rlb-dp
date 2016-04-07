import time


print("import the settings from config file")

T = 1000
c0 = 1/32

data_path = "../data/{0}/".format(T)
result_path = "../results/"
log_path = "../log/"

max_market_price = 300
laplace = 1

campaign_list = ("1458", "2259", "2261", "2821", "2997", "3358", "3386", "3427", "3476")
campaign_info = {}

# load campaign train info
for campaign in campaign_list:
	CPC = 0
	CPM = 0
	avg_ctr = 0
	m_counter = []
	with open(data_path + campaign + ".train-info.txt") as fin:
		line = fin.readline()
		line = line[:len(line) - 1].split("\t")
		CPC = float(line[1])
		# set CPM
		line = fin.readline()
		line = line[:len(line) - 1].split("\t")
		CPM = float(line[1])
		# set avg ctr
		line = fin.readline()
		line = line[:len(line) - 1].split("\t")
		avg_ctr = float(line[1])
		# set market price counter
		line = fin.readline()
		line = line[:len(line) - 1].split("\t")[1].split("_")
		max_market_price = len(line) - 1
		for item in line:
			m_counter.append(int(item))
	campaign_info[campaign] = (CPC, CPM, avg_ctr, m_counter)


def getTime():
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
