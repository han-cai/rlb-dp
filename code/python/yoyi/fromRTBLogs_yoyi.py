campaign_list = ["0125", "0130"]
projectPath = "/home/hm/Project/reinforce-bid/code/Python/"

def campaign_click(campaign):
	total_click_num = 0
	cost = [0, 0, 0, 0]
	click_num = [0, 0, 0, 0]

	with open(projectPath + "log/" + campaign + "-ttb.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				cost[1] += market_price
				if click == 1:
					click_num[1] += 1

	with open(projectPath + "log/" + campaign + "-baseline.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				cost[0] += market_price
				if click == 1:
					click_num[0] += 1
			if click == 1:
				total_click_num += 1

	with open(projectPath + "log/" + campaign + "-rtb.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				cost[3] += market_price
				if click == 1:
					click_num[3] += 1

	with open(projectPath + "log/" + campaign + "-linear.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				cost[2] += market_price
				if click == 1:
					click_num[2] += 1

	print(campaign + "\t{0}\t {1} \t {2} \t {3} \t {4}".format(total_click_num, click_num[0], click_num[1],
		click_num[2], click_num[3]))


def campaign_cost(campaign):
	total_click_num = 0
	cost = [0, 0, 0, 0]
	click_num = [0, 0, 0, 0]

	with open(projectPath + "log/" + campaign + "-ttb.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				cost[1] += market_price
				if click == 1:
					click_num[1] += 1

	with open(projectPath + "log/" + campaign + "-baseline.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				cost[0] += market_price
				if click == 1:
					click_num[0] += 1
			if click == 1:
				total_click_num += 1

	with open(projectPath + "log/" + campaign + "-rtb.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				cost[3] += market_price
				if click == 1:
					click_num[3] += 1

	with open(projectPath + "log/" + campaign + "-linear.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				cost[2] += market_price
				if click == 1:
					click_num[2] += 1

	print(campaign + "\t{0}\t {1} \t {2} \t {3}".format(cost[0], cost[1], cost[2], cost[3]))


def campaign_win_rate(campaign):
	total_auction_num = 0
	win_num = [0, 0, 0, 0]

	with open(projectPath + "log/" + campaign + "-ttb.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			total_auction_num += 1
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				win_num[1] += 1

	with open(projectPath + "log/" + campaign + "-baseline.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				win_num[0] += 1

	with open(projectPath + "log/" + campaign + "-rtb.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				win_num[3] += 1

	with open(projectPath + "log/" + campaign + "-linear.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				win_num[2] += 1

	print(campaign + "\t{0}\t {1} \t {2} \t {3}".format(win_num[0] / total_auction_num, win_num[1] / total_auction_num,
		win_num[2] / total_auction_num, win_num[3] / total_auction_num))


def campaign_ctr(campaign):
	total_auction_num = 0
	win_num = [0, 0, 0, 0]
	click_num = [0, 0, 0, 0]

	with open(projectPath + "log/" + campaign + "-ttb.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			total_auction_num += 1
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				win_num[1] += 1
				if click == 1:
					click_num[1] += 1

	with open(projectPath + "log/" + campaign + "-baseline.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				win_num[0] += 1
				if click == 1:
					click_num[0] += 1

	with open(projectPath + "log/" + campaign + "-rtb.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				win_num[3] += 1
				if click == 1:
					click_num[3] += 1

	with open(projectPath + "log/" + campaign + "-linear.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				win_num[2] += 1
				if click == 1:
					click_num[2] += 1

	print(campaign + "\t{0}\t {1} \t {2} \t {3}".format(click_num[0] / win_num[0], click_num[1] / win_num[1],
		click_num[2] / win_num[2], click_num[3] / win_num[3]))


def campaign_cpm(campaign):
	total_click_num = 0
	cost = [0, 0, 0, 0]
	win_num = [0, 0, 0, 0]

	with open(projectPath + "log/" + campaign + "-ttb.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				cost[1] += market_price
				win_num[1] += 1

	with open(projectPath + "log/" + campaign + "-baseline.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				cost[0] += market_price
				win_num[0] += 1

	with open(projectPath + "log/" + campaign + "-rtb.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				cost[3] += market_price
				win_num[3] += 1

	with open(projectPath + "log/" + campaign + "-linear.log") as fin:
		fin.readline()
		line = fin.readline()

		for line in fin:
			line = line[:len(line) - 1].split("\t")
			consider = line[3].split("_")
			bid = int(consider[0])
			market_price = int(consider[1])
			click = int(consider[2])
			if bid >= market_price:
				cost[2] += market_price
				win_num[2] += 1

	print(campaign + "\t{0}\t {1} \t {2} \t {3}".format(cost[0] / win_num[0], cost[1] / win_num[1],
		cost[2] / win_num[2], cost[3] / win_num[3]))


def campaign_bt(campaign):
	with open(projectPath + "log/" + campaign + "-rtb.log") as fin:
		fin.readline()

		line = fin.readline()
		line = line[:len(line) - 1].split("\t")
		line = line[2].split("_")
		T = int(line[1])
		B = int(line[0])

		print(campaign + "\t{0}\t{1}".format(T, B))


if __name__ == "__main__":
	for campaign in campaign_list:
		campaign_bt(campaign)
	print("___________________________________________________")
	for campaign in campaign_list:
		campaign_click(campaign)
	print("___________________________________________________")
	for campaign in campaign_list:
		campaign_cost(campaign)
	print("___________________________________________________")
	for campaign in campaign_list:
		campaign_win_rate(campaign)
	print("___________________________________________________")
	for campaign in campaign_list:
		campaign_ctr(campaign)
	print("___________________________________________________")
	for campaign in campaign_list:
		campaign_cpm(campaign)