import matplotlib.pyplot as pl
import numpy as np
from matplotlib.ticker import OldScalarFormatter, ScalarFormatter
import matplotlib.ticker as mtick

pl.figure(figsize=(16, 4))
T = np.arange(200, 1200, 200)

Lin_click = [1782, 1782, 1809, 1800, 1803]
MDPx_click = [1915, 1938, 1952, 1950, 1947]

Lin_win_rate = [0.276454365, 0.2769478358, 0.2749982884, 0.2817146743, 0.2781177294]
MDPx_win_rate = [0.3453394583, 0.3469187518, 0.3476368552, 0.3480490786, 0.3482550763]
for i in range(len(Lin_win_rate)):
	Lin_win_rate[i] *= 100
	MDPx_win_rate[i] *= 100

Lin_cpm = [47.92264778, 48.77912143, 49.56991052, 49.94669036, 48.86970461]
MDPx_cpm = [50.36961933, 50.82350713, 50.99984204, 51.08676151, 51.11750404]

Lin_ecpc = [60.77136942, 66.64475004, 62.66183658, 66.73493034, 65.48271284]
MDPx_ecpc = [61.2344705, 62.9034603, 61.41130129, 64.45750469, 61.23610893]

legend = ["Lin", "RLB"]

pl.subplot(1, 4, 1)
pl.bar(T - 50, Lin_click, 50)
pl.bar(T, MDPx_click, 50, color='r')
pl.xlabel(r'$T$', fontsize=15)
pl.ylabel('Total Clicks', fontsize=15)
pl.ylim(0, 2500)
pl.grid(True)
pl.legend(legend, loc='upper right', prop={'size':12})

pl.subplot(1, 4, 2)
pl.bar(T - 50, Lin_win_rate, 50)
pl.bar(T, MDPx_win_rate, 50, color='r')
pl.xlabel(r'$T$', fontsize=15)
pl.ylabel('Win Rate', fontsize=15)
pl.ylim(0, 45)
pl.grid(True)
ax = pl.gca()
fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(xticks)
pl.legend(legend, loc='upper right', prop={'size':12})

pl.subplot(1, 4, 3)
pl.bar(T - 50, Lin_cpm, 50)
pl.bar(T, MDPx_cpm, 50, color='r')
pl.ylim(0, 65)
pl.xlabel(r'$T$', fontsize=15)
pl.ylabel('CPM', fontsize=15)
pl.grid(True)
pl.legend(legend, loc='upper right', prop={'size':12})

pl.subplot(1, 4, 4)
pl.bar(T - 50, Lin_ecpc, 50)
pl.bar(T, MDPx_ecpc, 50, color='r')
pl.ylim(0, 85)
pl.xlabel(r'$T$', fontsize=15)
pl.ylabel('eCPC', fontsize=15)
pl.grid(True)
pl.legend(legend, loc='upper right', prop={'size':12})

pl.tight_layout()
pl.savefig('/home/hm/Project/reinforce-bid/tex/figures/s_perf_Ts_ipinyou.pdf', dpi=300)
#lgd = pl.legend(["Lin", "RLB"], bbox_to_anchor=(1.01,0.8),loc='center left', prop={'size':14})
#pl.show()
#pl.savefig('/home/hm/Project/reinforce-bid/tex/figures/s_perf_Ts_ipinyou.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight', dpi=300)