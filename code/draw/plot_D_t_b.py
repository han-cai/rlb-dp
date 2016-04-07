import matplotlib.pyplot as pl
import numpy as np
from matplotlib.ticker import OldScalarFormatter, ScalarFormatter
from matplotlib import rc

pl.rc('text', usetex=True)
pl.figure(figsize=(12,4))
# plot D({3000, 4000, 5000, 6000, 7000}, b)
# ipinyou 3386, load data
T = [1000, 3000, 5000, 7000, 9000]
B = [10000, 20000, 30000, 40000, 50000]
Dt_b = {}
Db_t = {}
for t in T:
	fin = open("/home/hm/Documents/derivative_value_function/3386/D({0}, b).txt".format(t))
	line = fin.readline()
	line = line[:len(line) - 1].split("\t")
	points = []
	bs = []
	for b in range(len(line)):
		bs.append(b)
		points.append(float(line[b]))
	Dt_b[t] = (bs, points)
	fin.close()
for b in B:
	fin = open("/home/hm/Documents/derivative_value_function/3386/D(t, {0}).txt".format(b))
	points = []
	ts = []
	t = 0
	for line in fin:
		line = line[:len(line) - 1]
		ts.append(t)
		points.append(float(line))
		t += 1
	Db_t[b] = (ts, points)
# plot D(5000, 0 - B0)
pl.subplot(1, 3, 1)
(bs, points) = Dt_b[5000]
x = []
y = []
x_scalar = 1
y_scalar = 1E5
for i in range(300):
	x.append(bs[i] * x_scalar)
	y.append(points[i] * y_scalar)
pl.plot(x, y)
pl.grid(True)
pl.xlabel(r'$b$', fontsize=15)
pl.ylabel(r'$D(5000, b)$ ($\times 10^{-5}$)',fontsize=15)
pl.title(r'$D(5000, b)$ of campaign 3386')

# plot D({3000, 5000, 7000}, B0 -)
pl.subplot(1, 3, 2)
x_scalar = 1E-4
y_scalar = 1E5
for t in T:
	(bs, points) = Dt_b[t]
	x = []
	y = []
	for i in range(1000, len(bs)):
		x.append(bs[i] * x_scalar)
		y.append(points[i] * y_scalar)
	pl.plot(x, y)

pl.grid(True)
pl.xlabel(r'$b$ ($\times 10^{4}$)', fontsize=15)
pl.ylabel(r'$D_t(b)$ ($\times 10^{-5}$)', fontsize=15)
pl.title(r'$D_t(b)$ of campaign 3386')
pl.xlim(0.1)
legend = []
for t in T:
	legend.append("D({0}, b)".format(t))
pl.legend(legend, prop={'size':10})

# plot D(t, b = {})
pl.subplot(1, 3, 3)
x_scalar = 1
y_scalar = 1E6
for b in B:
	(ts, points) = Db_t[b]
	x = []
	y = []
	for i in range(0, len(ts)):
		x.append(ts[i] * x_scalar)
		y.append(points[i] * y_scalar)
	pl.plot(x, y)

pl.grid(True)
pl.xlabel(r'$t$', fontsize=15)
pl.ylabel(r'$D_b(t)$ ($\times 10^{-6}$)', fontsize=15)
pl.title(r'$D_b(t)$ of campaign 3386')
legend = []
for b in B:
	legend.append("D(t, {0})".format(b))
pl.legend(legend, loc = 'lower right', prop={'size':10})

pl.tight_layout()
#pl.show()
pl.savefig('/home/hm/Project/reinforce-bid/tex/figures/D_t_b_analysis.pdf', dpi=300)