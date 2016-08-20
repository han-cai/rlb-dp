import _pickle as pickle
import numpy as np

dataPath = "../data/"
projectPath = dataPath + "rlb-dp/"

ipinyouPath = dataPath + "ipinyou-data/"
vlionPath = dataPath + "vlion-data/"
yoyiPath = dataPath + "yoyi-data/"

ipinyou_camps = ["1458", "2259", "2261", "2821", "2997", "3358", "3386", "3427", "3476"]
vlion_camps = ["20160727"]
yoyi_camps = ["121"]

ipinyou_max_market_price = 300
vlion_max_market_price = 300
yoyi_max_market_price = 300

info_keys = ["imp_test", "cost_test", "clk_test", "imp_train", "cost_train", "clk_train", "field", "dim", "price_counter_train"]


# info_keys:imp_test   cost_test   clk_test    clk_train   imp_train   field   cost_train  dim  price_counter_train
def get_camp_info(camp, src="ipinyou"):
	if src == "ipinyou":
		info = pickle.load(open(ipinyouPath + camp + "/info.txt", "rb"))
	elif src == "vlion":
		info = pickle.load(open(vlionPath + camp + "/info.txt", "rb"))
	elif src == "yoyi":
		info = pickle.load(open(yoyiPath + camp + "/info.txt", "rb"))
	return info

