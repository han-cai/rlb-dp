import matplotlib.pyplot as pl
import numpy as np
from matplotlib.ticker import OldScalarFormatter, ScalarFormatter
import matplotlib.ticker as mtick

c0 = [1.0/32, 1.0/16, 1.0/8, 1.0/4, 1.0/2]

SSMDP_click = [202, 333, 539, 913, 1667]
Mcpc_click = [591, 1029, 1492, 1931, 2129]
Lin_click = [1265, 1415, 1583, 1912, 2351]
MDPx_click = [1340, 1536, 1763, 2064, 2468]

SSMDP_win_rate = [0.171539704, 0.2554823867, 0.3667761645, 0.5227110349, 0.733756186]
Mcpc_win_rate = [0.06192552176, 0.1153133941, 0.2042406819, 0.3242106137, 0.3783758461]
Lin_win_rate = [0.08222902696, 0.1373219538, 0.2079765679, 0.3252516714, 0.5573397202]
MDPx_win_rate = [0.1114200754, 0.172627219, 0.2614743264, 0.399513015, 0.6148297107]
for i in range(len(SSMDP_win_rate)):
	SSMDP_win_rate[i] *= 100
	Mcpc_win_rate[i] *= 100
	Lin_win_rate[i] *= 100
	MDPx_win_rate[i] *= 100

SSMDP_cpm = [15.7690323, 21.09742941, 29.00061374, 39.97568122, 55.89974641]
Mcpc_cpm = [44.71373847, 46.72558185, 48.1837887, 49.75599585, 50.59084907]
Lin_cpm = [29.14507047, 34.13130387, 41.0054285, 52.26984646, 66.13411477]
MDPx_cpm = [30.58393944, 36.31371877, 44.54436457, 54.59711835, 66.9700898]

SSMDP_ecpc = [95.74649013, 97.17627636, 112.136423, 124.8376227, 137.4522651]
Mcpc_ecpc = [52.77288198, 65.55674625, 62.56634964, 66.66969539, 66.05547627]
Lin_ecpc = [39.15378694, 39.93776417, 49.56992256, 71.47120716, 98.07418796]
MDPx_ecpc = [29.14881339, 37.36275179, 51.07421334, 67.63782787, 96.73062853]

legend = ["SS-MDP", "Mcpc", "Lin", "RLB"]
pl.figure(figsize=(16, 4))

pl.subplot(1,4,1)
pl.plot(c0, SSMDP_click, '*b--')
pl.plot(c0, Mcpc_click, 'cx--')
pl.plot(c0, Lin_click, 'kp-')
pl.plot(c0, MDPx_click, 'or-')
pl.xlim(0.01, 0.6)
pl.xlabel(r'Budget Parameter $c_0$', fontsize=15)
pl.ylabel('Total Clicks', fontsize=15)
pl.grid(True)
pl.legend(legend, loc='lower right', prop={'size':12})

pl.subplot(1,4,2)
pl.plot(c0, SSMDP_win_rate, '*b--')
pl.plot(c0, Mcpc_win_rate, 'cx--')
pl.plot(c0, Lin_win_rate, 'kp-')
pl.plot(c0, MDPx_win_rate, 'or-')
pl.xlim(0.01, 0.6)
pl.xlabel(r'Budget Parameter $c_0$', fontsize=15)
pl.ylabel('Win Rate', fontsize=15)
pl.grid(True)
ax = pl.gca()
fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(xticks)
pl.legend(legend, loc='lower right', prop={'size':12})

pl.subplot(1,4,3)
pl.plot(c0, SSMDP_cpm, '*b--')
pl.plot(c0, Mcpc_cpm, 'cx--')
pl.plot(c0, Lin_cpm, 'kp-')
pl.plot(c0, MDPx_cpm, 'or-')
pl.xlim(0.01, 0.6)
pl.xlabel(r'Budget Parameter $c_0$', fontsize=15)
pl.ylabel('CPM', fontsize=15)
pl.grid(True)
pl.legend(legend, loc='lower right', prop={'size':12})

pl.subplot(1,4,4)
pl.plot(c0, SSMDP_ecpc, '*b--')
pl.plot(c0, Mcpc_ecpc, 'cx--')
pl.plot(c0, Lin_ecpc, 'kp-')
pl.plot(c0, MDPx_ecpc, 'or-')
pl.xlim(0.01, 0.6)
pl.ylim(10)
pl.xlabel(r'Budget Parameter $c_0$', fontsize=15)
pl.ylabel('eCPC', fontsize=15)
pl.grid(True)
pl.legend(legend, loc='lower right', prop={'size':12})

pl.tight_layout()
pl.savefig('/home/hm/Project/reinforce-bid/tex/figures/s_perf_overall_ipinyou.pdf', dpi=300)
#lgd = pl.legend(legend, bbox_to_anchor=(1.01,0.8),loc='center left', prop={'size':14})
#pl.tight_layout()
#pl.savefig('/home/hm/Project/reinforce-bid/tex/figures/s_perf_overall_ipinyou.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight', dpi=300)
#pl.show()
