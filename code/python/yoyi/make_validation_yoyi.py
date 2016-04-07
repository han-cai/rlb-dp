campaign_list = {"0123", "0124", "0125", "0127", "0130"}
rtb_yoyi = "/home/hm/Project/data/reinforce-bid/yoyi-rtb/"
rtb_validation_name = "validation.txt"
rtb_history_name = "history.txt"

if __name__ == "__main__":
	for campaign in campaign_list:
		p0 = 0
		validation = open(rtb_yoyi + campaign + "/" + rtb_validation_name, "w")
		with open(rtb_yoyi + campaign + "/" + rtb_history_name) as fin:
			line = fin.readline()
			line = line[:len(line) - 1].split("\t")
			dimension = int(line[0])
			T = int(line[1])
			p0 = int(100000 / T)
			validation.write("{0}\t{1}\n".format(dimension, T))
			store = [0] * T
			click_num = 0
			period = 1
			t = 0
			cost = 0
			for line in fin:
				store[t] = line
				line = line[0:len(line) - 1].split("\t")
				cost += int(line[1])
				click = int(line[0])
				if click == 1:
					click_num += 1
				t += 1
				if t == T:
					if click_num > 0:
						validation.write("{0}\t{1}\n".format(period, cost))
						for record in store:
							validation.write(record)
						period += 1
						if period >= p0:
							break
					t = 0
					cost = 0
					click_num = 0
			if click_num > 0:
				validation.write("{0}\t{1}\n".format(period, cost))
				for i in range(0, t):
					validation.write(store[i])

		validation.flush()
		validation.close()
