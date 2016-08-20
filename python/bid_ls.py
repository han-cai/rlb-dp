import os
import config
from utility import *
from mcpc import Mcpc
from rlb_dp_fa import RLB_DP_FA
from lin_bid import Lin_Bid
import tensorflow as tf
import time
import numpy as np


obj_type = "clk"
clk_vp = 1
N = 1000
c0 = 1 / 8
gamma = 1

src = "ipinyou"

log_in = open(config.projectPath + "bid-performance/{}_N={}_c0={}_obj={}_clkvp={}.txt"
              .format(src, N, c0, obj_type, clk_vp), "w")
print("logs in {}".format(log_in.name))
log = "{:<80}\t{:>10}\t{:>8}\t{:>10}\t{:>8}\t{:>8}\t{:>9}\t{:>8}\t{:>8}"\
	.format("setting", "objective", "auction", "impression", "click", "cost", "win-rate", "CPM", "eCPC")
print(log)
log_in.write(log + "\n")

if src == "ipinyou":
	camps = config.ipinyou_camps
	data_path = config.ipinyouPath
	max_market_price = config.ipinyou_max_market_price
elif src == "vlion":
	camps = config.vlion_camps
	data_path = config.vlionPath
	max_market_price = config.vlion_max_market_price
elif src == "yoyi":
	camps = config.yoyi_camps
	data_path = config.yoyiPath
	max_market_price = config.yoyi_max_market_price

for camp in camps:
	camp_info = config.get_camp_info(camp, src)
	auction_in = open(data_path + camp + "/test.theta.txt", "r")
	opt_obj = Opt_Obj(obj_type, int(clk_vp * camp_info["cost_train"] / camp_info["clk_train"]))
	B = int(camp_info["cost_train"] / camp_info["imp_train"] * c0 * N)

	# Mcpc
	auction_in = open(data_path + camp + "/test.theta.txt", "r")
	mcpc = Mcpc(camp_info)
	setting = "{}, camp={}, algo={}, N={}, c0={}, obj={}, clk_v={}"\
		.format(src, camp, "mcpc", N, c0, obj_type, opt_obj.clk_v)
	bid_log_path = config.projectPath + "bid-log/{}.txt".format(setting)
	(auction, imp, clk, cost) = mcpc.run(auction_in, bid_log_path, N, c0,
	                                     max_market_price, delimiter=" ", save_log=True)
	win_rate = imp / auction * 100
	cpm = (cost / 1000) / imp * 1000
	ecpc = (cost / 1000) / clk
	obj = opt_obj.get_obj(imp, clk, cost)
	log = "{:<80}\t{:>10}\t{:>8}\t{:>10}\t{:>8}\t{:>8}\t{:>8.2f}%\t{:>8.2f}\t{:>8.2f}" \
		.format(setting, obj, auction, imp, clk, cost, win_rate, cpm, ecpc)
	print(log)
	log_in.write(log + "\n")

	# # Lin-Bid
	# auction_in = open(data_path + camp + "/test.theta.txt", "r")
	# lin_bid = Lin_Bid(camp_info)
	# setting = "{}, camp={}, algo={}, N={}, c0={}, obj={}, clk_v={}" \
	# 	.format(src, camp, "lin_bid", N, c0, obj_type, opt_obj.clk_v)
	# bid_log_path = config.projectPath + "bid-log/{}.txt".format(setting)
	# model_path = data_path + camp + "/bid-model/{}_{}_{}_{}_{}.pickle".format("lin-bid", N, c0, obj_type, opt_obj.clk_v)
	# valid_path = data_path + camp + "/train.theta.txt"
	# lin_bid.parameter_tune(opt_obj, valid_path, model_path, N, c0, max_market_price,
	#                        max_market_price, delimiter=" ", load=True)
	# (auction, imp, clk, cost) = lin_bid.run(auction_in, bid_log_path, N, c0,
	#                                         max_market_price, delimiter=" ", save_log=True)
	#
	# win_rate = imp / auction * 100
	# cpm = (cost / 1000) / imp * 1000
	# ecpc = (cost / 1000) / clk
	# obj = opt_obj.get_obj(imp, clk, cost)
	# log = "{:<80}\t{:>10}\t{:>8}\t{:>10}\t{:>8}\t{:>8}\t{:>8.2f}%\t{:>8.2f}\t{:>8.2f}" \
	# 	.format(setting, obj, auction, imp, clk, cost, win_rate, cpm, ecpc)
	# print(log)
	# log_in.write(log + "\n")

	# RLB-DP-FA
	auction_in = open(data_path + camp + "/test.theta.txt", "r")
	rlb_dp_fa = RLB_DP_FA(camp_info, opt_obj, gamma)
	setting = "{}, camp={}, algo={}, N={}, c0={}, obj={}, clk_v={}" \
		.format(src, camp, "rlb_dp_fa", N, c0, obj_type, opt_obj.clk_v)
	bid_log_path = config.projectPath + "bid-log/{}.txt".format(setting)

	save_point_path = data_path + camp + "/bid-model/rlb_dnb_save_points_{}.txt".format(obj_type)
	rlb_dp_fa.load_save_points(save_point_path)

	# model_path = data_path + camp + "/bid-model/fa_dnb_{}.pickle".format(obj_type)
	# rlb_dp_fa.load_nn_approximator("pickle", model_path)

	model_path = data_path + camp + "/bid-model/fa_dnb_{}.txt".format(obj_type)
	rlb_dp_fa.load_nn_approximator("txt", model_path)

	bid_factor_file = data_path + camp + "/bid-model/{}_{}_{}_{}_{}.pickle".format("rlb_bid_factor", N, c0, obj_type, opt_obj.clk_v)
	if os.path.isfile(bid_factor_file):
		bf = pickle.load(open(bid_factor_file, "rb"))["bid-factor"]
	else:
		bf = 1

	(auction, imp, clk, cost) = rlb_dp_fa.run(auction_in, bid_log_path, N, c0,
	                                         max_market_price, delimiter=" ", save_log=True, bid_factor=bf)

	win_rate = imp / auction * 100
	cpm = (cost / 1000) / imp * 1000
	ecpc = (cost / 1000) / clk
	obj = opt_obj.get_obj(imp, clk, cost)
	log = "{:<80}\t{:>10}\t{:>8}\t{:>10}\t{:>8}\t{:>8}\t{:>8.2f}%\t{:>8.2f}\t{:>8.2f}" \
		.format(setting, obj, auction, imp, clk, cost, win_rate, cpm, ecpc)
	print(log)
	log_in.write(log + "\n")

log_in.flush()
log_in.close()
