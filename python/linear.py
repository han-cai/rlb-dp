import config


def linear(campaign, c0):
	auction = 0
	imp = 0
	clk = 0
	cost = 0
	# load parameters
	CPM = config.campaign_info[campaign][1]
	avg_ctr = config.campaign_info[campaign][2]

	# tune b0 on validation data
	b0 = 0
	best_clk = 0
	for bs in range(2, 300, 6):
		with open(config.data_path + campaign + ".validation.txt") as fin:
			clk = 0
			# set T & B
			line = fin.readline()
			line = line[:len(line) - 1].split("\t")
			T = int(line[1])
			B = int(CPM * T * c0 * 1E-3)
			# start
			period = 0
			t = 0
			b = 0
			for line in fin:
				if t == 0:
					line = line[:len(line) - 1].split("\t")
					period = int(line[0])
					t = T
					b = B
				else:
					line = line[0:len(line) - 1].split("\t")
					click = int(line[0])
					price = int(line[1])
					pCTR = float(line[2])
					a = min(int(pCTR * bs / avg_ctr), config.max_market_price)
					a = min(b, a)

					if a >= price:
						if click == 1:
							clk += 1
						b -= price
					t -= 1
			if clk > best_clk:
				best_clk = clk
				b0 = bs

	# run bidding on test data
	log = open(config.log_path + campaign + ".lin.log", "w")
	with open(config.data_path + campaign + ".test.txt") as fin:
		auction = 0
		imp = 0
		clk = 0
		cost = 0
		# set T & B
		line = fin.readline()
		line = line[:len(line) - 1].split("\t")
		T = int(line[1])
		B = int(CPM * T * c0 * 1E-3)
		# start
		period = 0
		t = 0
		b = 0
		for line in fin:
			if t == 0:
				line = line[:len(line) - 1].split("\t")
				period = int(line[0])
				t = T
				b = B
			else:
				line = line[0:len(line) - 1].split("\t")
				click = int(line[0])
				price = int(line[1])
				pCTR = float(line[2])
				a = min(int(pCTR * b0 / avg_ctr), config.max_market_price)
				a = min(b, a)
				record = config.getTime() + "\t{0}\t{1}_{2}\t{3}_{4}_{5}\t{6}_{7}\t".format(
					period, b, t, a, price, click, clk, imp)
				log.write(record + "\n")

				if a >= price:
					imp += 1

					if click == 1:
						clk += 1
					b -= price
					cost += price
				t -= 1
				auction += 1
	log.flush()
	log.close()
	return auction, imp, clk, cost