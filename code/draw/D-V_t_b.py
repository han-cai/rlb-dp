from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as pl
import numpy as np
from matplotlib import cm

B = np.arange(1000, 100000, 3000)
T = np.arange(0, 5000, 200)
#load data


pl.rc('text', usetex=True)
fig = pl.figure(figsize=(10,4))

ax = fig.add_subplot(1, 2, 1, projection='3d')
Dtb = []
for t in T:
	Db = []
	data = open("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/3427/D_t_b_train/{0}.txt".format(t))
	line = data.readline()
	line = line[:len(line)-1].split("\t")
	for b in B:
		Db.append(float(line[b]) * 100000)
	Dtb.append(Db)
	data.close()

D = np.array(Dtb)
for i in range(len(B)):
	B[i] /= 1000.0

B, T = np.meshgrid(B, T)

ax.plot_surface(B, T, D, rstride=1, cstride=1, cmap='rainbow')
pl.xlabel(r"$b$ ($\times 10^3$)", fontsize=15)
pl.ylabel(r"$t$", fontsize=15)
ax.set_zlim(0)
ax.set_xlim(1)
ax.set_zlabel(r'$D(t, b)$ ($\times 10^{-5}$)', fontsize=15)
pl.title("D(t, b) on campaign 3427 as example")
Dtb = []

ax = fig.add_subplot(1, 2, 2, projection='3d')
Vtb = []
B = np.arange(1000, 100000, 3000)
T = np.arange(0, 5000, 200)
for t in T:
	Vb = []
	data = open("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/3427/V_t_b/{0}.txt".format(t))
	line = data.readline()
	line = line[:len(line)-1].split("\t")
	for b in B:
		Vb.append(float(line[b]))
	Vtb.append(Vb)
	data.close()

V = np.array(Vtb)
for i in range(len(B)):
	B[i] /= 1000.0

B, T = np.meshgrid(B, T)
ax.plot_surface(B, T, V, rstride=1, cstride=1, cmap='rainbow')
pl.xlabel(r"$b$ ($\times 10^3$)", fontsize=15)
pl.ylabel(r"$t$", fontsize=15)
ax.set_zlim(0)
ax.set_xlim(1)
ax.set_zlabel(r'$V(t, b)$', fontsize=15)
pl.title("V(t, b) on campaign 3427 as example")

pl.tight_layout()

#pl.show()
pl.savefig('/home/hm/Project/reinforce-bid/tex/figures/DV_3d.pdf', dpi=300)

