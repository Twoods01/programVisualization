package astar;

import java.util.Comparator;

public class AStarCompare
   implements Comparator<AStarNode>
{
   public int compare(AStarNode a, AStarNode b)
   {
      return (int) (a.getF() - b.getF());
   }
}
