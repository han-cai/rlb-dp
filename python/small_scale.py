import config
import ss_mdp
import mcpc
import linear
import rlb

print("{7:<50}\t{0:>8}\t{1:>10}\t{2:>8}\t{3:>8}\t{4:>9}\t{5:>8}\t{6:>8}".format("auction", "impression", "click", "cost", "win-rate", "CPM", "eCPC", "setting"))
result = open(config.result_path + "result.txt", "w")
result.write("{7:<50}\t{0:>8}\t{1:>10}\t{2:>8}\t{3:>8}\t{4:>9}\t{5:>8}\t{6:>8}".format("auction", "impression", "click", "cost", "win-rate", "CPM", "eCPC", "setting"))
for campaign in config.campaign_list:

	(auction, imp, clk, cost) = ss_mdp.ss_mdp(campaign, config.c0)
	win_rate = imp / auction * 100
	cpm = (cost / 1000) / imp * 1000
	ecpc = (cost / 1000) / clk
	setting = "SS-MDP on " + campaign + " under T = {0} and c0 = {1}".format(config.T, config.c0)
	record = "{7:<50}\t{0:>8}\t{1:>10}\t{2:>8}\t{3:>8}\t{4:>8.2f}%\t{5:>8.2f}\t{6:>8.2f}".format(auction, imp, clk, cost, win_rate, cpm, ecpc, setting)
	print(record)
	result.write(record + "\n")

	(auction, imp, clk, cost) = mcpc.mcpc(campaign, config.c0)
	win_rate = imp / auction * 100
	cpm = (cost / 1000) / imp * 1000
	ecpc = (cost / 1000) / clk
	setting = "Mcpc on " + campaign + " under T = {0} and c0 = {1}".format(config.T, config.c0)
	record = "{7:<50}\t{0:>8}\t{1:>10}\t{2:>8}\t{3:>8}\t{4:>8.2f}%\t{5:>8.2f}\t{6:>8.2f}".format(auction, imp, clk, cost, win_rate, cpm, ecpc, setting)
	print(record)
	result.write(record + "\n")

	(auction, imp, clk, cost) = linear.linear(campaign, config.c0)
	win_rate = imp / auction * 100
	cpm = (cost / 1000) / imp * 1000
	ecpc = (cost / 1000) / clk
	setting = "Lin on " + campaign + " under T = {0} and c0 = {1}".format(config.T, config.c0)
	record = "{7:<50}\t{0:>8}\t{1:>10}\t{2:>8}\t{3:>8}\t{4:>8.2f}%\t{5:>8.2f}\t{6:>8.2f}".format(auction, imp, clk, cost, win_rate, cpm, ecpc, setting)
	print(record)
	result.write(record + "\n")

	(auction, imp, clk, cost) = rlb.rlb(campaign, config.c0)
	win_rate = imp / auction * 100
	cpm = (cost / 1000) / imp * 1000
	ecpc = (cost / 1000) / clk
	setting = "RLB on " + campaign + " under T = {0} and c0 = {1}".format(config.T, config.c0)
	record = "{7:<50}\t{0:>8}\t{1:>10}\t{2:>8}\t{3:>8}\t{4:>8.2f}%\t{5:>8.2f}\t{6:>8.2f}".format(auction, imp, clk, cost, win_rate, cpm, ecpc, setting)
	print(record)
	result.write(record + "\n")

result.flush()
result.close()




