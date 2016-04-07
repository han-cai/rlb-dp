import FunctionApproximation.D_t_b_nn;
import FunctionLibrary.StringOperation;

import java.io.File;

public class Interface {

	public static void D_t_b_nn(String campaign) throws Exception{
		// train stationary points
		/*String[] lines = FileOperation.File2String("/home/hm/Project/data/reinforce-bid/yoyi-rtb/" + campaign + "/stationary_points.txt").split("\n");
		double[][] points = new double[lines.length - 500][2];
		int index = 0;
		for (String line : lines){
			if (index >= 500) {
				points[index - 500][0] = index;
				points[index - 500][1] = Double.parseDouble(line);
			}
			index += 1;
		}
		Stationary_Point.stationary_point_train_basic(points);*/
		// prepare train
		D_t_b_nn nn = new D_t_b_nn(campaign);
		File for_train = new File("/home/hm/Project/data/reinforce-bid/ipinyou-rtb/" + campaign + "/D_t_b_train/");
		if (! for_train.exists()){
			for_train.mkdir();
			nn.prepareData();
		}
		// start train
		System.out.println(StringOperation.getTime() + "\t" + campaign + " train start");
		//nn.train();

		//nn.points();
		//nn.chooseModel("D_t_b_nn_50");
		//nn.evaluate();
	}

    public static void main(String[] args) throws Exception{
	    String campaign = "3427";
	    D_t_b_nn(campaign);
    }
}
