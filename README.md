## Real-time Bidding with Reinforcement Learning in Display Advertising

This is a repository of the experiment code supporting the paper Real-time Bidding with Reinforcement Learning in Display Advertising in ECML PKDD 2016.

## Small-scale Evaluation Demo
For the demo of the small-scale evaluation, please run:
```bash
$ bash small-scale.sh
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
```
