package astar;

import physics.*;

public class AStarNode
{
   private Point entPos;
   private double gScore;
   private double fScore;
   
   public AStarNode(Point entPos)
   {
      this.entPos = entPos;
      this.gScore = 0.0;
      this.fScore = 0.0;
   }
   
   public Point getPos()
   {
      return entPos;
   }
   
   public double getG()
   {
      return gScore;
   }
   
   public void setG(double g)
   {
      gScore = g;
      return;
   }
   
   public double getF()
   {
      return fScore;
   }
   
   public void setF(double f)
   {
      fScore = f;
      return;
   }
   
   public boolean equals(Object o)
   {
      return (o instanceof AStarNode && entPos.xCoord() == ((AStarNode) o).getPos().xCoord() && entPos.yCoord() == ((AStarNode) o).getPos().yCoord());
   }
   
   public int hashCode()
   {
      // get code xxyy
      return (entPos.xCoord() * 1000) + entPos.yCoord();
   }
}
