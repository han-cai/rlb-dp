import matplotlib.pyplot as pl
import numpy as np
from matplotlib.ticker import OldScalarFormatter, ScalarFormatter
import matplotlib.ticker as mtick

c0 = [1.0/32, 1.0/16, 1.0/8, 1.0/4, 1.0/2]

Mcpc_click = [617, 1094, 1595, 2006, 2131]
Lin_click = [1308, 1477, 1661, 2029, 2460]
LMDP_NN_click = [1404, 1577, 1769, 2029, 2362]
LMDP_NN_Seg_click = [1379, 1574, 1806, 2090, 2500]
LMDP_NN_MapD_click = [1405, 1599, 1806, 2112, 2498]
LMDP_NN_MapA_click = [1409, 1597, 1803, 2111, 2501]
for i in range(len(c0)):
	Mcpc_click[i] = (Mcpc_click[i] - Lin_click[i] + 0.0) / Lin_click[i] * 100
	LMDP_NN_click[i] = (LMDP_NN_click[i] - Lin_click[i] + 0.0) / Lin_click[i] * 100
	LMDP_NN_Seg_click[i] = (LMDP_NN_Seg_click[i] - Lin_click[i] + 0.0) / Lin_click[i] * 100
	LMDP_NN_MapD_click[i] = (LMDP_NN_MapD_click[i] - Lin_click[i] + 0.0) / Lin_click[i] * 100
	LMDP_NN_MapA_click[i] = (LMDP_NN_MapA_click[i] - Lin_click[i] + 0.0) / Lin_click[i] * 100
	Lin_click[i] = (Lin_click[i] - Lin_click[i] + 0.0) / Lin_click[i] * 100

Mcpc_win_rate = [0.03275755273, 0.06257683202, 0.1121500966, 0.1686865998, 0.1893407772]
Lin_win_rate = [0.0500504729, 0.07572838231, 0.1135898733, 0.1881421236, 0.3017615079]
LMDP_NN_win_rate = [0.05673661646, 0.08761435644, 0.129927222, 0.1971865857, 0.2925190981]
LMDP_NN_Seg_win_rate = [0.05564423871, 0.08639043306, 0.1312631665, 0.2020359723, 0.3128059871]
LMDP_NN_MapD_win_rate = [0.05655508537, 0.08672048244, 0.1309857838, 0.2024370434, 0.3114504123]
LMDP_NN_MapA_win_rate = [0.05664011225, 0.08695220413, 0.1309317611, 0.2020374251, 0.3115168612]
for i in range(len(c0)):
	Mcpc_win_rate[i] *= 100
	Lin_win_rate[i] *= 100
	LMDP_NN_win_rate[i] *= 100
	LMDP_NN_Seg_win_rate[i] *= 100
	LMDP_NN_MapD_win_rate[i] *= 100
	LMDP_NN_MapA_win_rate[i] *= 100

Mcpc_cpm = [49.40812757, 49.51268142, 49.78442351, 50.42546626, 50.61035386]
Lin_cpm = [31.7286652, 36.94494262, 43.21544331, 55.42472718, 67.34550438]
LMDP_NN_cpm = [32.09428123, 36.93753207, 46.13279041, 56.37145038, 66.89935165]
LMDP_NN_Seg_cpm = [31.90089619, 37.17274118, 45.10584968, 54.88676337, 67.25215849]
LMDP_NN_MapD_cpm = [31.76804547, 36.99570112, 44.8325732, 54.28466141, 66.88559141]
LMDP_NN_MapA_cpm = [31.7150943, 36.8993512, 44.82306013, 54.33548025, 66.90916852]

Mcpc_ecpc = [79.54902779, 83.84305422, 75.50968564, 65.47307791, 66.06823079]
Lin_ecpc = [59.09697311, 43.76473468, 50.34751834, 74.68891601, 97.18499928]
LMDP_NN_ecpc = [28.20200689, 41.69433642, 49.35009243, 67.28604108, 93.95548806]
LMDP_NN_Seg_ecpc = [28.72508967, 37.11868585, 48.95337986, 69.13768784, 96.96258847]
LMDP_NN_MapD_ecpc = [30.95715779, 41.10366189, 47.76219206, 65.94314745, 96.21773646]
LMDP_NN_MapA_ecpc = [27.86758698, 41.30045177, 48.78306749, 65.74918755, 96.13247051]

legend = ["Mcpc", "Lin", "RLB-NN", "RLB-NN-Seg", "RLB-NN-MapD", "RLB-NN-MapA"]
pl.figure(figsize=(16, 4))

pl.subplot(1,4,1)
pl.plot(c0, Mcpc_click, 'cx--')
pl.plot(c0, Lin_click, 'yp-')
pl.plot(c0, LMDP_NN_click, 'ok-')
pl.plot(c0, LMDP_NN_Seg_click, '^-')
pl.plot(c0, LMDP_NN_MapD_click, 's-')
pl.plot(c0, LMDP_NN_MapA_click, 'r+-')
pl.xlim(0.01, 0.6)
pl.xlabel('Budget Parameter $c_0$', fontsize=15)
pl.ylabel('Total Clicks \n Improvement over Lin', fontsize=15)
pl.grid(True)
ax = pl.gca()
fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(xticks)
pl.legend(legend, loc='lower right', prop={'size':12})

pl.subplot(1,4,2)
pl.plot(c0, Mcpc_win_rate, 'cx--')
pl.plot(c0, Lin_win_rate, 'yp-')
pl.plot(c0, LMDP_NN_win_rate, 'ok-')
pl.plot(c0, LMDP_NN_Seg_win_rate, '^-')
pl.plot(c0, LMDP_NN_MapD_win_rate, 's-')
pl.plot(c0, LMDP_NN_MapA_win_rate, 'r+-')
pl.xlim(0.01, 0.6)
pl.ylim(-10)
pl.xlabel(r'Budget Parameter $c_0$', fontsize=15)
pl.ylabel('Win Rate', fontsize=15)
pl.grid(True)
ax = pl.gca()
fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(xticks)
pl.legend(legend, loc='lower right', prop={'size':12})

pl.subplot(1,4,3)
pl.plot(c0, Mcpc_cpm, 'cx--')
pl.plot(c0, Lin_cpm, 'yp-')
pl.plot(c0, LMDP_NN_cpm, 'ok-')
pl.plot(c0, LMDP_NN_Seg_cpm, '^-')
pl.plot(c0, LMDP_NN_MapD_cpm, 's-')
pl.plot(c0, LMDP_NN_MapA_cpm, 'r+-')
pl.xlim(0.01, 0.6)
pl.ylim(15)
pl.xlabel(r'Budget Parameter $c_0$', fontsize=15)
pl.ylabel('CPM', fontsize=15)
pl.grid(True)
pl.legend(legend, loc='lower right', prop={'size':12})

pl.subplot(1,4,4)
pl.plot(c0, Mcpc_ecpc, 'cx--')
pl.plot(c0, Lin_ecpc, 'yp-')
pl.plot(c0, LMDP_NN_ecpc, 'ok-')
pl.plot(c0, LMDP_NN_Seg_ecpc, '^-')
pl.plot(c0, LMDP_NN_MapD_ecpc, 's-')
pl.plot(c0, LMDP_NN_MapA_ecpc, 'r+-')
pl.xlim(0.01, 0.6)
pl.ylim(10)
pl.xlabel(r'Budget Parameter $c_0$', fontsize=15)
pl.ylabel('eCPC', fontsize=15)
pl.grid(True)
pl.legend(legend, loc='lower right', prop={'size':12})

pl.tight_layout()
pl.savefig('/home/hm/Project/reinforce-bid/tex/figures/l_perf_overall_ipinyou.pdf', dpi=300)
#lgd = pl.legend(legend, bbox_to_anchor=(1.01,0.8),loc='center left', prop={'size':14})
#pl.show()
#pl.savefig('/home/hm/Project/reinforce-bid/tex/figures/l_perf_overall_ipinyou.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight', dpi=300)