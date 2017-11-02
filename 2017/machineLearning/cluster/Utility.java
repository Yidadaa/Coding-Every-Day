package cn.uestc.util;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

import cn.uestc.clustering.*;

public class Utility {
	public static double getDistance(Point p, Point q)
	{

		double dx = p.getX() - q.getX();

		double dy = p.getY() - q.getY();

		double distance = Math.sqrt(dx * dx + dy * dy);

		return distance;

	}

	public static List<Point> isKeyPoint(List<Point> lst, Point p, int e,
			int minp)
	{

		int count = 0;

		List<Point> tmpLst = new ArrayList<Point>();

		for (Iterator<Point> it = lst.iterator(); it.hasNext();)
		{

			Point q = it.next();

			if (getDistance(p, q) <= e)
			{

				++count;

				if (!tmpLst.contains(q))
				{

					tmpLst.add(q);

				}

			}

		}

		if (count >= minp)
		{

			p.setKey(true);

			return tmpLst;

		}

		return null;

	}

	public static void setListClassed(List<Point> lst)
	{

		for (Iterator<Point> it = lst.iterator(); it.hasNext();)
		{

			Point p = it.next();

			if (!p.isClassed())
			{

				p.setClassed(true);

			}

		}

	}


	public static boolean mergeList(List<Point> a, List<Point> b)
	{

		boolean merge = false;

		for (int index = 0; index < b.size(); ++index)
		{

			if (a.contains(b.get(index)))
			{

				merge = true;

				break;

			}

		}

		if (merge)
		{

			for (int index = 0; index < b.size(); ++index)
			{

				if (!a.contains(b.get(index)))
				{

					a.add(b.get(index));

				}

			}

		}

		return merge;

	}


	public static List<Point> getPointsList() throws IOException
	{

		List<Point> lst = new ArrayList<Point>();

		String txtPath = "data/data";

		BufferedReader br = new BufferedReader(new FileReader(txtPath));

		String str = "";

		while ((str = br.readLine()) != null && str != "")
		{

			lst.add(new Point(str));

		}

		br.close();

		return lst;

	}

}
