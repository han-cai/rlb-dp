import matplotlib.pyplot as pl
import numpy as np

avg_ctr = {"1458": 0.0007959634856, "2259": 0.0003351062047, "2261": 0.0003010396776, "2821": 0.0006373997116,
           "2997": 0.004436094317, "3358": 0.0007795171815, "3386": 0.000728983265, "3427": 0.0007425499226,
           "3476": 0.0005212245478}

delta_max = 300
campaign = "2821"
# load data
#load data
T1 = 5000
T2 = 10000
V1 = []
V2 = []
data = open("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/V_t_b/{0}.txt".format(T1-1))
line = data.readline()
line = line[:len(line) - 1].split("\t")
for item in line:
	V1.append(float(item))
data.close()

data = open("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/V_t_b/{0}.txt".format(T2-1))
line = data.readline()
line = line[:len(line) - 1].split("\t")
for item in line:
	V2.append(float(item))
data.close()

# draw graph
pl.rc('text', usetex=True)
pl.figure(figsize=(12,4))

paras = [1.0/2, 1, 2.0]
pl.subplot(1, 3, 1)
a = [0, 0, 0]
for j in range(len(paras)):
	para = paras[j]
	g_delta = [avg_ctr[campaign] * para] * (delta_max + 1)
	x = []
	for i in range(delta_max + 1):
		g_delta[i] += V1[20000 - i] - V1[20000]
		if g_delta[i] >= 0:
			a[j] = i
		g_delta[i] *= 1000
		x.append(i)
	pl.plot(x, g_delta)
pl.plot(np.arange(0, delta_max + 1), [0] * (delta_max + 1), 'y--')
pl.grid(True)
pl.xlabel(r'$\delta$', fontsize=15)
pl.ylabel(r'$g(\delta)$ ($\times 10^{-3}$)',fontsize=15)
pl.ylim(-11.5)
pl.title('$g(\delta)$ on campaign 2821 \n under t = 5000 and b = 20000')
pl.legend([r"$\theta(x)=\frac{1}{2}\theta_{avg}$, $a = " + str(a[0]) + "$",
           r"$\theta(x)=\theta_{avg}$, $a = " + str(a[1]) + "$",
           r"$\theta(x)=2\theta_{avg}$, $a = " + str(a[2]) + "$"], loc="lower left", prop={'size':15})

pl.subplot(1, 3, 2)
a = [0, 0, 0]
for j in range(len(paras)):
	para = paras[j]
	g_delta = [avg_ctr[campaign] * para] * (delta_max + 1)
	x = []
	for i in range(delta_max + 1):
		g_delta[i] += V1[100000 - i] - V1[100000]
		if g_delta[i] >= 0:
			a[j] = i
		g_delta[i] *= 1000
		x.append(i)
	pl.plot(x, g_delta)
pl.plot(np.arange(0, delta_max + 1), [0] * (delta_max + 1), 'y--')
pl.grid(True)
pl.xlabel(r'$\delta$', fontsize=15)
pl.ylabel(r'$g(\delta)$ ($\times 10^{-3}$)',fontsize=15)
pl.ylim(-5)
pl.title('$g(\delta)$ on campaign 2821 \n under t = 5000 and b = 100000')
pl.legend([r"$\theta(x)=\frac{1}{2}\theta_{avg}$, $a = " + str(a[0]) + "$",
           r"$\theta(x)=\theta_{avg}$, $a = " + str(a[1]) + "$",
           r"$\theta(x)=2\theta_{avg}$, $a = " + str(a[2]) + "$"], loc="lower left", prop={'size':15})
'''
pl.subplot(1, 4, 3)
for para in paras:
	g_delta = [avg_ctr[campaign] * para] * (delta_max + 1)
	x = []
	for i in range(delta_max + 1):
		g_delta[i] += V2[20000 - i] - V2[20000]
		g_delta[i] *= 1000
		x.append(i)
	pl.plot(x, g_delta)
pl.plot(np.arange(0, delta_max + 1), [0] * (delta_max + 1), 'y--')
pl.grid(True)
pl.xlabel(r'$\delta$', fontsize=15)
pl.ylabel(r'$g(\delta)$ ($\times 10^{-3}$)',fontsize=15)
pl.ylim(-13)
pl.title('$g(\delta)$ on campaign 2821 \n under t = 10000 and b = 20000')
pl.legend([r"$\theta(x)=\frac{1}{2}\theta_{avg}$", r"$\theta(x)=\theta_{avg}$", r"$\theta(x)=2\theta_{avg}$"], loc="lower left", prop={'size':15})
'''
pl.subplot(1, 3, 3)
a = [0, 0, 0]
for j in range(len(paras)):
	para = paras[j]
	g_delta = [avg_ctr[campaign] * para] * (delta_max + 1)
	x = []
	for i in range(delta_max + 1):
		g_delta[i] += V2[100000 - i] - V2[100000]
		if g_delta[i] >= 0:
			a[j] = i
		g_delta[i] *= 1000
		x.append(i)
	pl.plot(x, g_delta)
pl.plot(np.arange(0, delta_max + 1), [0] * (delta_max + 1), 'y--')
pl.grid(True)
pl.xlabel(r'$\delta$', fontsize=15)
pl.ylabel(r'$g(\delta)$ ($\times 10^{-3}$)',fontsize=15)
pl.ylim(-9)
pl.title('$g(\delta)$ on campaign 2821 \n under t = 10000 and b = 100000')
pl.legend([r"$\theta(x)=\frac{1}{2}\theta_{avg}$, $a = " + str(a[0]) + "$",
           r"$\theta(x)=\theta_{avg}$, $a = " + str(a[1]) + "$",
           r"$\theta(x)=2\theta_{avg}$, $a = " + str(a[2]) + "$"], loc="lower left", prop={'size':15})

pl.tight_layout()
#pl.show()
pl.savefig('/home/hm/Project/reinforce-bid/tex/figures/g_delta.pdf', dpi=300)
