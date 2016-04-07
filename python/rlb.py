import config


def get_market_price_distribution(m_counter):
	m_pdf = [0] * len(m_counter)
	sum = 0
	for i in range(0, len(m_counter)):
		sum += m_counter[i]
	for i in range(0, len(m_counter)):
		m_pdf[i] = (m_counter[i] + config.laplace) / (
		sum + len(m_counter) * config.laplace)
	return m_pdf


def update_value_function(m_pdf, avg_ctr, T, B):
	V = [[0 for i in range(B + 1)] for j in range(T)]
	for t in range(1, T):
		action = [0] * (B + 1)
		end = B - 1
		for start in range(B, 0, -1):
			while end >= 0 and V[t - 1][end] - V[t - 1][start] + avg_ctr > 0:
				end -= 1
			if end < 0:
				action[start] = min(config.max_market_price, start)
			else:
				action[start] = min(config.max_market_price, start - end - 1)
		for b in range(1, B + 1):
			V[t][b] = V[t - 1][b]
			for i in range(0, action[b] + 1):
				V[t][b] += m_pdf[i] * (avg_ctr + V[t - 1][b - i] - V[t - 1][b])
	return V


def take_action(theta_c, V, t, b):
	a = 0
	for delta in range(1, min(b, config.max_market_price)):
		if theta_c + V[t - 1][b - delta] - V[t - 1][b] >= 0:
			a = delta
		else:
			break
	return a


def rlb(campaign, c0):
	auction = 0
	imp = 0
	clk = 0
	cost = 0
	# load parameters
	CPM = config.campaign_info[campaign][1]
	avg_ctr = config.campaign_info[campaign][2]
	m_pdf = get_market_price_distribution(config.campaign_info[campaign][3])
	# run bidding on test data
	log = open(config.log_path + campaign + ".rlb.log", "w")
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
		# update value function
		V = update_value_function(m_pdf, avg_ctr, T, B)
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
				a = take_action(pCTR, V, t, b)
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