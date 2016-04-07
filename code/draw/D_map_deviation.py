import matplotlib.pyplot as pl
import re
import numpy as np

avg_ctr = {"1458": 0.0007959634856, "2259": 0.0003351062047, "2261": 0.0003010396776, "2821": 0.0006373997116,
           "2997": 0.004436094317, "3358": 0.0007795171815, "3386": 0.000728983265, "3427": 0.0007425499226,
           "3476": 0.0005212245478}

pl.rc('text', usetex=True)
pl.figure(figsize=(12,4))

pl.subplot(1, 3, 1)

data = open("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/3427/D_t_b_map_7000_5000.txt")
B = []
Dev = []
for line in data:
	line = line[:len(line) - 1].split("\t")
	b = int(line[0].split("_")[1])
	B.append(b / 10000.0)
	dev = float(line[2].split("_")[1])
	Dev.append(dev / avg_ctr["3427"] * 10000)
pl.plot(B, Dev)
pl.xlabel(r"$b$ ($\times 10^4$)", fontsize=15)
pl.ylabel(r"$Dev(7000, 5000, b) / \theta_{avg}$ ($\times 10^{-4}$)", fontsize=15)

data.close()

pl.subplot(1, 3, 2)

data = open("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/3427/D_t_b_map_8000_5000.txt")
B = []
Dev = []
for line in data:
	line = line[:len(line) - 1].split("\t")
	b = int(line[0].split("_")[1])
	B.append(b / 10000.0)
	dev = float(line[2].split("_")[1])
	Dev.append(dev / avg_ctr["3427"] * 10000)
pl.plot(B, Dev)
pl.xlabel(r"$b$ ($\times 10^4$)", fontsize=15)
pl.ylabel(r"$Dev(8000, 5000, b) / \theta_{avg}$ ($\times 10^{-4}$)", fontsize=15)

data.close()

pl.subplot(1, 3, 3)

data = open("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/3427/D_t_b_map_9000_5000.txt")
B = []
Dev = []
for line in data:
	line = line[:len(line) - 1].split("\t")
	b = int(line[0].split("_")[1])
	B.append(b / 10000.0)
	dev = float(line[2].split("_")[1])
	Dev.append(dev / avg_ctr["3427"] * 10000)
pl.plot(B, Dev)
pl.xlabel(r"$b$ ($\times 10^4$)", fontsize=15)
pl.ylabel(r"$Dev(9000, 5000, b) / \theta_{avg}$ ($\times 10^{-4}$)", fontsize=15)

data.close()
pl.tight_layout()
#pl.show()
pl.savefig('/home/hm/Project/reinforce-bid/tex/figures/Dev.pdf', dpi=300)
