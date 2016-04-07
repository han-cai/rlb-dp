## Real-time Bidding with Reinforcement Learning in Display Advertising

This is a repository of the experiment code supporting the paper **Real-time Bidding with Reinforcement Learning in Display Advertising** in ECML PKDD 2016.

## Small-scale Evaluation Demo
For the demo of the small-scale evaluation, please run under the folder of **scripts**:
```bash
$ bash small-scale.sh
```
or run under the folder of **python**:
```bash
$ python3 small_scale.py
```
After running, you could get the performance table printed in the console like:
```
setting                                           	 auction	impression	   click	    cost	 win-rate	     CPM	    eCPC
SS-MDP on 1458 under T = 1000 and c0 = 0.03125    	  300000	     45482	       9	  641446	   15.16%	   14.10	   71.27
Mcpc on 1458 under T = 1000 and c0 = 0.03125      	  300000	     25437	     108	  644498	    8.48%	   25.34	    5.97
Lin on 1458 under T = 1000 and c0 = 0.03125       	  300000	     26170	     218	  485537	    8.72%	   18.55	    2.23
RLB on 1458 under T = 1000 and c0 = 0.03125       	  300000	     22851	     242	  588777	    7.62%	   25.77	    2.43
SS-MDP on 2259 under T = 1000 and c0 = 0.03125    	  300000	     54315	       6	  864478	   18.11%	   15.92	  144.08
Mcpc on 2259 under T = 1000 and c0 = 0.03125      	  300000	     16985	       7	  872223	    5.66%	   51.35	  124.60
Lin on 2259 under T = 1000 and c0 = 0.03125       	  300000	     34427	       4	  869013	   11.48%	   25.24	  217.25
RLB on 2259 under T = 1000 and c0 = 0.03125       	  300000	     39753	      10	  858412	   13.25%	   21.59	   85.84
SS-MDP on 2261 under T = 1000 and c0 = 0.03125    	  300000	     71388	       8	  837633	   23.80%	   11.73	  104.70
Mcpc on 2261 under T = 1000 and c0 = 0.03125      	  300000	     22001	       5	  839970	    7.33%	   38.18	  167.99
Lin on 2261 under T = 1000 and c0 = 0.03125       	  300000	     46262	       7	  789395	   15.42%	   17.06	  112.77
RLB on 2261 under T = 1000 and c0 = 0.03125       	  300000	     51525	       9	  838026	   17.18%	   16.26	   93.11
SS-MDP on 2821 under T = 1000 and c0 = 0.03125    	  300000	     56061	      17	  829955	   18.69%	   14.80	   48.82
Mcpc on 2821 under T = 1000 and c0 = 0.03125      	  300000	     18819	       9	  836986	    6.27%	   44.48	   93.00
Lin on 2821 under T = 1000 and c0 = 0.03125       	  300000	     33650	      12	  538669	   11.22%	   16.01	   44.89
RLB on 2821 under T = 1000 and c0 = 0.03125       	  300000	     42202	      19	  825077	   14.07%	   19.55	   43.43
SS-MDP on 2997 under T = 1000 and c0 = 0.03125    	  156063	     40369	      80	  306444	   25.87%	    7.59	    3.83
Mcpc on 2997 under T = 1000 and c0 = 0.03125      	  156063	     14752	      48	  307751	    9.45%	   20.86	    6.41
Lin on 2997 under T = 1000 and c0 = 0.03125       	  156063	     26743	      63	  163300	   17.14%	    6.11	    2.59
RLB on 2997 under T = 1000 and c0 = 0.03125       	  156063	     39658	      78	  304227	   25.41%	    7.67	    3.90
SS-MDP on 3358 under T = 1000 and c0 = 0.03125    	  300000	     34208	       9	  854699	   11.40%	   24.99	   94.97
Mcpc on 3358 under T = 1000 and c0 = 0.03125      	  300000	     12382	      80	  864251	    4.13%	   69.80	   10.80
Lin on 3358 under T = 1000 and c0 = 0.03125       	  300000	     12792	      96	  860009	    4.26%	   67.23	    8.96
RLB on 3358 under T = 1000 and c0 = 0.03125       	  300000	     12924	     210	  833398	    4.31%	   64.48	    3.97
SS-MDP on 3386 under T = 1000 and c0 = 0.03125    	  300000	     44090	       6	  715156	   14.70%	   16.22	  119.19
Mcpc on 3386 under T = 1000 and c0 = 0.03125      	  300000	     15532	      14	  720391	    5.18%	   46.38	   51.46
Lin on 3386 under T = 1000 and c0 = 0.03125       	  300000	     12332	      31	  286043	    4.11%	   23.20	    9.23
RLB on 3386 under T = 1000 and c0 = 0.03125       	  300000	     25214	      34	  711798	    8.40%	   28.23	   20.94
SS-MDP on 3427 under T = 1000 and c0 = 0.03125    	  300000	     45003	       3	  753911	   15.00%	   16.75	  251.30
Mcpc on 3427 under T = 1000 and c0 = 0.03125      	  300000	     16888	      43	  758919	    5.63%	   44.94	   17.65
Lin on 3427 under T = 1000 and c0 = 0.03125       	  300000	     17588	     113	  674679	    5.86%	   38.36	    5.97
RLB on 3427 under T = 1000 and c0 = 0.03125       	  300000	     18410	     143	  729305	    6.14%	   39.61	    5.10
SS-MDP on 3476 under T = 1000 and c0 = 0.03125    	  300000	     44001	      14	  736048	   14.67%	   16.73	   52.57
Mcpc on 3476 under T = 1000 and c0 = 0.03125      	  300000	     13730	      29	  742121	    4.58%	   54.05	   25.59
Lin on 3476 under T = 1000 and c0 = 0.03125       	  300000	     14940	      54	  736830	    4.98%	   49.32	   13.65
RLB on 3476 under T = 1000 and c0 = 0.03125       	  300000	     15633	      98	  733211	    5.21%	   46.90	    7.48
```
Note these results are produced from a subset (the first 300,000 lines of each campaign in iPinYou) under T = 1000 and c0 = 1/32.
For the full small-scale evaluation and large-scale evaluation, please first check our GitHub project [make-ipinyou-data](https://github.com/wnzhang/make-ipinyou-data "make-ipinyou-data") for pre-processing the [iPinYou data](http://data.computational-advertising.org "iPinYou data"). 
After downloading the dataset, by simplying make all you can generate the standardised data.

