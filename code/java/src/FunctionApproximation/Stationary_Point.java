package FunctionApproximation;

import FunctionLibrary.FileOperation;
import FunctionLibrary.UltraFile;

public class Stationary_Point {
    public static double[] stationary_w;
    public static int dimension = 0;

    public static void stationary_point_train_basic(double[][] points) {
        dimension = 2;
        stationary_w = new double[dimension];

        double X = 0;
        double XX = 0;
        double Y = 0;
        double XY = 0;
        int N = points.length;

        for (int i = 0; i < N; ++i) {
            X += points[i][0];
            XX += points[i][0] * points[i][0];
            Y += points[i][1];
            XY += points[i][0] * points[i][1];
        }

        stationary_w[1] = (XY / X - Y / N) / (XX / X - X / N);
        stationary_w[0] = (Y - X * stationary_w[1]) / N;
        System.out.println(String.format("%f * t + %f", stationary_w[1], stationary_w[0]));
    }

    public static double stationary_point_predict_basic(double t){
        return stationary_w[1] * t + stationary_w[0];
    }


}
