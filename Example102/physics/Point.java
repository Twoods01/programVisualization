package physics;
public class Point
{
   private int x;
   private int y;
   
   public Point(int x, int y)
   {
      this.x = x;
      this.y = y;
   }
   
   public int xCoord()
   {
      return x;
   }
   
   public void setX(int x)
   {
      this.x = x;
   }
   
   public int yCoord()
   {
      return y;
   }
   
   public void setY(int y)
   {
      this.y = y;
   }
   
   public double distanceSq(Point pt2)
   {
      return ((x - pt2.xCoord()) * (x - pt2.xCoord())+(y - pt2.yCoord()) * (y - pt2.yCoord()));
   }
   
   public boolean adjacent(Point pt2)
   {
      return ((x == pt2.xCoord() && Math.abs(y - pt2.yCoord()) == 1) || (y == pt2.yCoord() && Math.abs(x - pt2.xCoord()) == 1));
   }
   
   public Point nextPosition(WorldModel world, Point destPt)
   {
      int horiz = sign(destPt.xCoord() - x);
      Point newPt = new Point(x + horiz, y);
      
      if (horiz == 0 || world.isOccupied(newPt))
      {
         int vert = sign(destPt.yCoord() - y);
         newPt.setX(x);
         newPt.setY(y + vert);
         
         if (vert == 0 || world.isOccupied(newPt))
         {
            newPt.setY(y);
         }
      }
      
      return newPt;
   }
   
   public int sign(int x)
   {
      if (x < 0)
      {
         return -1;
      }
      else if (x > 0)
      {
         return 1;
      }
      else
      {
         return 0;
      }
   }
   
   public boolean equals(Object o)
   {
      return (o instanceof Point && this.xCoord() == ((Point) o).xCoord() && this.yCoord() == ((Point) o).yCoord());
   }
}
