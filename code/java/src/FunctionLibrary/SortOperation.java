package FunctionLibrary;

import javafx.util.Pair;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class SortOperation {

	//true for descend & false for ascend
	public enum Direction {
		ASCEND, DESCEND
	}
	public static Direction direction = Direction.DESCEND;

	public static void setDirection(Direction nd){
		direction = nd;
	}

	public static void guibing(List<Pair<String, Integer>> list, int op, int ed){
		if (op >= ed - 1) return;
		int mid = (op + ed) / 2;

		guibing(list, op, mid);
		guibing(list, mid, ed);

		List<Pair<String, Integer>> tlist = new LinkedList<Pair<String, Integer>>();
		int p1 = op, p2 = mid;
		while (p1 < mid && p2 < ed){
			if ((list.get(p1).getValue() < list.get(p2).getValue()) ^ (direction == Direction.ASCEND)){
				tlist.add(list.get(p2++));
			} else{
				tlist.add(list.get(p1++));
			}
		}

		while (p1 < mid){
			tlist.add(list.get(p1++));
		}

		while (p2 < ed){
			tlist.add(list.get(p2++));
		}

		for (int i = op; i < ed; ++i){
			list.set(i, tlist.get(i - op));
		}
	}

}
