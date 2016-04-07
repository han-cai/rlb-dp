package FunctionLibrary;

import java.text.SimpleDateFormat;
import java.util.Date;

public class StringOperation {

	public static String[] keyboard_neighbor = {
			"qwsxz", "vfghn", "xsdfv", "werfvcxs", "wsdfr", "edcvbgtr", "rfvbnhyt", "tgbnmjuy", "ujklo", "yhnmkiu",
			"ujmloi", "ikpo", "hnkj", "gbmjh", "iklp", "ol", "aw", "edfgt", "qazxcdew", "rfghy", "yhjki", "dcbgf",
			"qasde", "azcds", "tghju", "axs"
	};
	public static String[] number_neighbor = {
			"op", "qw", "qwe", "wer", "ert", "rty", "tyu", "yui", "uio", "iop"
	};

	public static String getTime(){
		SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		return df.format(new Date());
	}

	public static int editDistance(String str1, String str2){
		int m = str1.length(), n = str2.length();
		int[][] L = new int[m + 1][n + 1];

		for (int i = 0; i <= m; ++i){
			L[i][0] = i;
		}

		for (int j = 0; j <= n; ++j){
			L[0][j] = j;
		}

		for (int i = 1; i <= m; ++i){
			for (int j = 1; j <= n; ++j){
				if (str1.charAt(i - 1) == str2.charAt(j - 1)){
					L[i][j] = L[i - 1][j - 1];
				} else {
					L[i][j] = Math.min(Math.min(L[i - 1][j - 1], L[i - 1][j]), L[i][j - 1]) + 1;
				}
			}
		}

		if (L[m][n] < Math.abs(m - n)){
			L[m][n] = Math.abs(m - n);
		}

		return L[m][n];
	}

	public static int keyboardDistance(String s1, String s2){
		int m = s1.length(), n = s2.length();
		int INFINITE = (m + n);

		int[][] keyboardDist = new int[26][26];
		for (int i = 0; i < 26; ++i){
			for (int j = 0; j < 26; ++j){
				keyboardDist[i][j] = INFINITE;
			}
			keyboardDist[i][i] = 0;
			for (char c : keyboard_neighbor[i].toCharArray()){
				int j = c - 'a';
				keyboardDist[i][j] = 1;
			}
		}
		int[][] L = new int[m + 1][n + 1];
		for (int i = 0; i <= m; ++i){
			L[i][0] = i;
		}

		for (int j = 0; j <= n; ++j){
			L[0][j] = j;
		}

		for (int i = 1; i <= m; ++i){
			for (int j = 1; j <= n; ++j){
				if (s1.charAt(i - 1) == s2.charAt(j - 1)){
					L[i][j] = L[i - 1][j - 1];
				} else {
					int c1 = s1.charAt(i - 1) - 'a';
					int c2 = s2.charAt(j - 1) - 'a';
					int keyboard;
					if (c1 < 0 || c1 >= 26 || c2 < 0 || c2 >= 26) keyboard = INFINITE;
					else {
						keyboard = keyboardDist[c1][c2];
					}
					L[i][j] = Math.min(Math.min(L[i - 1][j - 1] + keyboard, L[i - 1][j] + 1), L[i][j - 1] + 1);
				}
			}
		}

		if (L[m][n] < Math.abs(m - n)){
			L[m][n] = Math.abs(m - n);
		}

		return L[m][n];
	}

	//not-finished
	public static int hmDistance(String s1, String s2){
		int m = s1.length(), n = s2.length();
		int INFINITE = (m + n);

		int[][] keyboardDist = new int[26][26];
		for (int i = 0; i < 26; ++i){
			for (int j = 0; j < 26; ++j){
				keyboardDist[i][j] = INFINITE;
			}
			for (char c : keyboard_neighbor[i].toCharArray()){
				int j = c - 'a';
				keyboardDist[i][j] = 1;
			}
			keyboardDist[i][i] = 0;
		}
		int[][] L = new int[m + 1][n + 1];
		for (int i = 0; i <= m; ++i){
			L[i][0] = i;
		}

		for (int j = 0; j <= n; ++j){
			L[0][j] = j;
		}

		for (int i = 1; i <= m; ++i){
			for (int j = 1; j <= n; ++j){
				if (i == j){

				}
			}
		}

		return L[m][n];
	}
}
