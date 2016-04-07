package FunctionApproximation;

import FunctionLibrary.FileOperation;
import FunctionLibrary.StringOperation;
import FunctionLibrary.UltraFile;
import javafx.util.Pair;

import java.io.File;
import java.util.*;
import java.util.concurrent.CountDownLatch;
import java.util.function.Function;

public class D_t_b_nn{
	String campaign;
	HashMap<String, Double> avg_ctr;
	int b0 = 1000;
	int t0 = 1000;
	int T0 = 10000;
	int K = 50;
	double alpha = 2E-2;
	double init_para = 0.001;
	double t_para = 0.04;
	double b_para = 0.5;
	double rmse_para = 0.01;

	double[] w_1_t = new double[K];
	double[] w_1_b = new double[K];
	double[] w_1_1 = new double[K];
	double[] w_2 = new double[K + 1];

	int T;

	Random rand = new Random(0);

	public D_t_b_nn(String campaign){
		this.campaign = campaign;

		avg_ctr = new HashMap<>();
		avg_ctr.put("1458", 0.0007959634856);
		avg_ctr.put("2259", 0.0003351062047);
		avg_ctr.put("2261", 0.0003010396776);
		avg_ctr.put("2821", 0.0006373997116);
		avg_ctr.put("2997", 0.004436094317);
		avg_ctr.put("3358", 0.0007795171815);
		avg_ctr.put("3386", 0.000728983265);
		avg_ctr.put("3427", 0.0007425499226);
		avg_ctr.put("3476", 0.0005212245478);

		avg_ctr.put("0123", 0.0009569721743);
		avg_ctr.put("0124", 0.0009087415179);
		avg_ctr.put("0125", 0.0008747838329);
		avg_ctr.put("0127", 0.0007907649161);
		avg_ctr.put("0130", 0.001246433547);
	}

	public double sigmoid(double x){
		if (x <= -700){
			return 0;
		}
		return 1.0 / (1.0 + Math.exp(-x));
	}

	public String getCurrentWeights(){
		String res = "";
		for (int i = 0; i < K; ++i){
			res += w_1_t[i] + "\t";
		}
		for (int i = 0; i < K; ++i){
			res += w_1_b[i] + "\t";
		}
		for (int i = 0; i < K; ++i){
			res += w_1_1[i] + "\t";
		}
		for (int i = 0; i < K; ++i){
			res += w_2[i] + "\t";
		}
		res += w_2[K];
		return res;
	}

	public void prepareData(){
		class data_thread extends Thread{
			UltraFile fin;
			CountDownLatch threadSignal;
			int[] t;
			int current;

			public data_thread(UltraFile fin, CountDownLatch threadSignal, int[] t){
				this.fin = fin;
				this.threadSignal = threadSignal;
				this.t = t;
			}

			public String read_data() throws Exception{
				synchronized (data_thread.class){
					String line = fin.readLine();
					current = t[0];
					t[0] += 1;
					return line;
				}
			}
			public void run(){
				String line = null;
				try {
					while ((line = read_data()) != null){
						File out = new File("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_train/" + current + ".txt");
						if (out.exists()){
							System.out.println(current + "\texist");
						} else{
							FileOperation.String2File(out, line + "\n");
							System.out.println(current + "\twrite finish");
						}
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
				threadSignal.countDown();
			}
		}

		UltraFile uf = new UltraFile("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/derivative_value_function.txt");
		int[] t = {0};
		int threadNum = 20;
		CountDownLatch threadSignal = new CountDownLatch(threadNum);
		for (int i = 0; i < threadNum; ++i){
			data_thread dt = new data_thread(uf, threadSignal, t);
			dt.start();
		}
		try {
			threadSignal.await();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public class nn_train extends Thread{
		List<Integer> t_index;
		CountDownLatch threadSignal;

		int[] t;
		int current;
		List<Pair<Double, Double>> points;

		public nn_train(List<Integer> t_index, int[] t, CountDownLatch threadSignal){
			this.t_index = t_index;
			this.t = t;
			this.threadSignal = threadSignal;

			points = new ArrayList<>();
		}

		public boolean read_data(){
			synchronized (nn_train.class){
				current = t[0];
				if (current >= t_index.size()){
					return false;
				} else{
					t[0] += 1;
					int index = t_index.get(current);
					int St = (int)Stationary_Point.stationary_point_predict_basic(index) + 1;
					String line = FileOperation.File2String("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_train/" + index + ".txt");
					line = line.substring(0, line.length() - 1);
					String[] items = line.split("\t");
					points.clear();
					for (int b = b0; b < items.length; ++b){
						points.add(new Pair(b + 0.0, Double.parseDouble(items[b])));
					}
					return true;
				}
			}
		}

		public void run(){
			while (read_data()){
				List<Integer> b_index = new ArrayList<>();
				for (int i = 0; i < points.size(); ++i){
					b_index.add(i);
				}
				Collections.shuffle(b_index, rand);
				int ts = t_index.get(current);
				for (int i = 0; i < (int)(b_index.size() * b_para); ++i){
					int index = b_index.get(i);
					double bs = points.get(index).getKey();
					double D_t_b = points.get(index).getValue();
					// forward
					double[] z1 = new double[K + 1];
					double y = 0;
					//synchronized (nn_train.class){
						for (int j = 0; j < K; ++j){
							z1[j] = 0;
							z1[j] = sigmoid(w_1_t[j] * ts + w_1_b[j] * bs + w_1_1[j] * 1);
						}
						z1[K] = 1;
						for (int j = 0; j < K + 1; ++j){
							y += w_2[j] * z1[j];
						}
					//}
					// back propagation
					double[] patial_w_1_t = new double[K];
					double[] patial_w_1_b = new double[K];
					double[] patial_w_1_1 = new double[K];
					double[] patial_w_2 = new double[K + 1];
					for (int j = 0; j < K; ++j){
						patial_w_1_t[j] = patial_w_1_b[j] = patial_w_1_1[j] = 0;
						patial_w_2[j] = 0;
					}
					patial_w_2[K] = 0;

					double delta_2 = y - D_t_b;
					for (int j = 0; j < K; ++j){
						patial_w_2[j] = delta_2 * z1[j];
					}
					patial_w_2[K] = delta_2;
					double[] delta_1 = new double[K];
					for (int j = 0; j < K; ++j){
						delta_1[j] = (1 - z1[j]) * z1[j] * w_2[j] * delta_2;
					}
					for (int j = 0; j < K; ++j){
						patial_w_1_t[j] = delta_1[j] * ts;
						patial_w_1_b[j] = delta_1[j] * bs;
						patial_w_1_1[j] = delta_1[j] * 1;
					}
					// update parameter
					//synchronized (nn_train.class){
						for (int j = 0; j < K + 1; ++j){
							w_2[j] -= alpha * patial_w_2[j];
						}
						for (int j = 0; j < K; ++j){
							w_1_t[j] -= alpha * patial_w_1_t[j];
							w_1_b[j] -= alpha * patial_w_1_b[j];
							w_1_1[j] -= alpha * patial_w_1_1[j];
						}
					//}
				}
			}
			threadSignal.countDown();
		}
	}

	public class RMSE_Thread extends Thread{
		List<Integer> t_index;
		int[] t;
		double[] rmse;
		CountDownLatch threadSignal;
		int current;

		public RMSE_Thread(List<Integer> t_index, int[] t, CountDownLatch threadSignal, double[] rmse){
			this.t_index = t_index;
			this.t = t;
			this.threadSignal = threadSignal;
			this.rmse = rmse;
		}

		public boolean get_data(){
			synchronized (RMSE_Thread.class){
				current = t[0];
				if (current >= t_index.size()){
					return false;
				} else{
					t[0] += 1;
					return true;
				}
			}
		}

		public void run(){
			while (get_data()){
				int index = t_index.get(current);
				String line = FileOperation.File2String("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_train/" + index + ".txt");
				line = line.substring(0, line.length() - 1);
				String[] items = line.split("\t");
				for (int b = b0; b < items.length; ++b){
					double D_t_b = Double.parseDouble(items[b]);
					// forward
					double[] z1 = new double[K + 1];
					for (int j = 0; j < K; ++j){
						z1[j] = 0;
						z1[j] = sigmoid(w_1_t[j] * index + w_1_b[j] * b + w_1_1[j] * 1);
					}
					z1[K] = 1;
					double y = 0;
					for (int j = 0; j < K + 1; ++j){
						y += w_2[j] * z1[j];
					}

					rmse[0] += (y - D_t_b) * (y - D_t_b);
					rmse[1] += 1;
				}
			}
			threadSignal.countDown();
		}
	}

	public double getRMSE(){
		int threadNum = 8;
		int[] t = {0};
		List<Integer> t_index = new ArrayList<>();
		for (int i = t0; i < T; ++i){
			t_index.add(i);
		}
		Collections.shuffle(t_index, rand);
		double[] rmse = {0, 0};
		CountDownLatch threadSignal = new CountDownLatch(threadNum);
		for (int i = 0; i < threadNum; ++i){
			RMSE_Thread rmse_thread = new RMSE_Thread(t_index.subList(0, (int)(rmse_para * t_index.size())), t, threadSignal, rmse);
			rmse_thread.start();
		}
		try {
			threadSignal.await();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return Math.sqrt(rmse[0] / rmse[1]);
	}

	public double getSampleEvaluation(){
		int threadNum = 8;
		int[] t = {0};
		List<Integer> t_index = new ArrayList<>();
		for (int i = 4000; i < T; i += 500){
			t_index.add(i);
		}
		double[] rmse = {0, 0};
		CountDownLatch threadSignal = new CountDownLatch(threadNum);
		for (int i = 0; i < threadNum; ++i){
			RMSE_Thread rmse_thread = new RMSE_Thread(t_index, t, threadSignal, rmse);
			rmse_thread.start();
		}
		try {
			threadSignal.await();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return Math.sqrt(rmse[0] / rmse[1]);
	}

	public double getFullEvaluation(){
		int threadNum = 50;
		int[] t = {0};
		List<Integer> t_index = new ArrayList<>();
		for (int i = t0; i < T; ++i){
			t_index.add(i);
		}
		double[] rmse = {0, 0};
		CountDownLatch threadSignal = new CountDownLatch(threadNum);
		for (int i = 0; i < threadNum; ++i){
			RMSE_Thread rmse_thread = new RMSE_Thread(t_index, t, threadSignal, rmse);
			rmse_thread.start();
		}
		try {
			threadSignal.await();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return Math.sqrt(rmse[0] / rmse[1]);
	}

	public void train(){
		T = new File("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_train/").listFiles().length;
		List<Integer> t_index = new ArrayList<>();
		for (int i = t0; i < T; ++i){
			t_index.add(i);
		}
		// initialize parameter
		for (int i = 0; i < K; ++i){
			w_2[i] = avg_ctr.get(campaign) / K * (1 + (rand.nextDouble() - 0.5) * init_para * 0.1);
		}
		w_2[K] = 0;
		for (int i = 0; i < K; ++i){
			w_1_t[i] = rand.nextDouble() * init_para;
			w_1_b[i] = - rand.nextDouble() * init_para;
			w_1_1[i] = (rand.nextDouble() - 0.5) * init_para;
		}

		double best_rmse = getRMSE();
		double last_rmse = best_rmse;
		int count = 0;
		String weights = getCurrentWeights();
		FileOperation.Add2File("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_nn_" + K, best_rmse + " $$ " + weights + "\n");
		System.out.println(StringOperation.getTime() + "\tInit rmse:\t" + last_rmse + "\trmse / avg_ctr:\t" + (last_rmse / avg_ctr.get(campaign)) + "\t" + getSampleEvaluation());
		for (int round = 0; round < 1000000; ++round) {
			Collections.shuffle(t_index, rand);

			// start train
			int threadNum = 8;
			int[] t = {0};
			CountDownLatch threadSignal = new CountDownLatch(threadNum);
			for (int i = 0; i < threadNum; ++i){
				nn_train nn_thread = new nn_train(t_index.subList(0, (int)(t_index.size() * t_para)), t, threadSignal);
				nn_thread.start();
			}
			try {
				threadSignal.await();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

			// calculate RMSE
			double rmse = getRMSE();
			FileOperation.Add2File("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_nn_" + K, rmse + " $$ " + getCurrentWeights() + "\n");
			if (best_rmse > rmse){
				best_rmse = rmse;
				weights = getCurrentWeights();
			}
			if (rmse < last_rmse){
				count += 1;
				if (count == 2){
					count = 0;
					//alpha *= 2;
				}
			} else{
				//alpha /= 2;
			}
			last_rmse = rmse;
			System.out.println(StringOperation.getTime() + "\tround " + round + " finish with rmse:\t" + rmse + "\trmse / avg_ctr:\t" + (rmse / avg_ctr.get(campaign)) + "\t" + getSampleEvaluation());
		}
		System.out.println(StringOperation.getTime() + "\ttrain finish with rmse:\t" + best_rmse + "\tbest_rmse / avg_ctr:\t" + (best_rmse / avg_ctr.get(campaign)));
		FileOperation.Add2File("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_nn_" + K, best_rmse + " $$ " + weights + "\n");
	}

	public void loadWeights(String weights){
		String[] items = weights.split("\t");
		K = (items.length - 1) / 4;
		w_1_t = new double[K];
		w_1_b = new double[K];
		w_1_1 = new double[K];
		w_2 = new double[K + 1];
		for (int i = 0; i < K; ++i){
			w_1_t[i] = Double.parseDouble(items[i]);
			w_1_b[i] = Double.parseDouble(items[i + K]);
			w_1_1[i] = Double.parseDouble(items[i + 2 * K]);
		}
		for (int i = 0; i < K + 1; ++i){
			w_2[i] = Double.parseDouble(items[i + 3 * K]);
		}
	}

	public void chooseModel(String file) throws Exception {
		T = new File("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_train/").listFiles().length;

		UltraFile uf = new UltraFile("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/" + file);
		List<Double> rmses = new ArrayList<>();
		List<String> weights = new ArrayList<>();

		String line = null;
		while ((line = uf.readLine()) != null){
			String[] parts = line.split(" \\$\\$ ");
			rmses.add(Double.parseDouble(parts[0]));
			weights.add(parts[1]);
		}

		// choose the last one
		String res = weights.get(weights.size() - 1);
		FileOperation.String2File("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_weights.txt", res);

		// get performance of the chosen model
		System.out.println(StringOperation.getTime() + "\tModel Out Finish");
		loadWeights(res);
		double rmse = getSampleEvaluation();
		System.out.println(StringOperation.getTime() + "\tsample rmse: " + rmse + "\t sample rmse / avg_ctr: " + (rmse / avg_ctr.get(campaign)));
		//rmse = getFullEvaluation();
		//System.out.println(StringOperation.getTime() + "\trmse: " + rmse + "\t rmse / avg_ctr: " + (rmse / avg_ctr.get(campaign)));

	}

	public void points() throws Exception {
		class points_thread extends Thread{
			int[] t;
			int current;
			CountDownLatch threadSignal;

			public points_thread(int[] t, CountDownLatch threadSignal){
				this.t = t;
				this.threadSignal = threadSignal;
			}

			public String read_data(){
				synchronized (points_thread.class){
					current = t[0];
					if (current >= T){
						return null;
					}
					t[0] += 1;
				}
				String res = FileOperation.File2String("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_train/" + current + ".txt");
				return res.substring(0, res.length() - 1);
			}

			public void run(){
				String line = null;
				try {
					while ((line = read_data()) != null) {
						UltraFile fout = new UltraFile("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_points/" + current + ".txt");
						fout.initWriter(UltraFile.WriteOption.WRITE);
						String[] items = line.split("\t");
						if (current < t0 || current == T0) {
							int St = -1;
							for (int i = 0; i < items.length; ++i) {
								double value = Double.parseDouble(items[i]);
								if (Math.abs(value) < 1E-16) {
									St = i;
									break;
								}
							}
							if (St >= 0) {
								fout.write(current + "\t" + (St + 1) + "\t" + St + "\t");
								for (int b = 0; b < St + 1; ++b) {
									fout.write(items[b] + "\t");
								}
								fout.write("\n");
							} else {
								St = (int)(Stationary_Point.stationary_point_predict_basic(current)) + 1;
								fout.write(current + "\t" + items.length + "\t" + St + "\t");
								for (int b = 0; b < items.length; ++b) {
									fout.write(items[b] + "\t");
								}
								fout.write("\n");
							}
							fout.close();
						} else {
							int St = (int)Stationary_Point.stationary_point_predict_basic(current) + 1;
							for (int b = 0; b < items.length; ++b){
								double value = Double.parseDouble(items[b]);
								if (Math.abs(value) < 1E-16){
									St = b;
									break;
								}
							}
							fout.write(current + "\t" + b0 + "\t" + St + "\t");
							for (int b = 0; b < b0; ++b) {
								fout.write(items[b] + "\t");
							}
							fout.write("\n");
						}
					}
				} catch (Exception e){
					e.printStackTrace();
				}
				threadSignal.countDown();
			}
		}

		T = new File("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_train/").listFiles().length;
		File point_path = new File("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_points/");
		if (! point_path.exists()){
			point_path.mkdir();
		}

		int[] t = {0};
		int threadNum = 8;
		CountDownLatch threadSignal = new CountDownLatch(threadNum);
		for (int i = 0; i < threadNum; ++i){
			points_thread p_thread = new points_thread(t, threadSignal);
			p_thread.start();
		}
		try {
			threadSignal.await();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		File dtb = new File("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_points/");
		File[] files = dtb.listFiles();
		int T = files.length;
		UltraFile uf = new UltraFile("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_points.txt");
		uf.initWriter(UltraFile.WriteOption.WRITE);
		for (int i = 0; i < T; ++i){
			String line = FileOperation.File2String("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_points/" + i + ".txt");
			uf.write(line);
		}
		uf.close();
	}

	public void evaluate(){
		T = new File("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_train/").listFiles().length;
		String weights = FileOperation.File2String("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_weights.txt");
		loadWeights(weights);
		double rmse = getFullEvaluation();
		System.out.println(StringOperation.getTime() + "\t" + rmse + "\t" + (rmse / avg_ctr.get(campaign)));
	}
}
