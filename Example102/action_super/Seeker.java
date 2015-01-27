package action_super;

import java.lang.ref.Reference;
import java.util.ArrayList;

import entities.*;
import entity_super.*;
import physics.*;

public class Seeker
{
   protected ArrayList<Point> path;
   
   public Seeker()
   {
      this.path = new ArrayList<Point>();
   }
   
   public EntityPosn findNearestItem(WorldModel world, String typeName,
         EntityPosn seeker)
   {
      ArrayList<Point> objPosLst = new ArrayList<Point>();
      
      for (int yi = 0; yi < world.getRows(); yi++)
      {
         for (int xi = 0; xi < world.getCols(); xi++)
         {
            Point objPt = new Point(xi, yi);
            if (world.getOccupant(objPt) != null &&
                world.getOccupant(objPt).getName() == typeName)
            {
               objPosLst.add(objPt);
            }
         }
      }
      
      return world.getOccupant(nearestObj(world, objPosLst, seeker));
   }
   
   public Point nearestObj(WorldModel world, ArrayList<Point> objPosLst,
         EntityPosn seeker)
   {
      Point seekerPt = seeker.getPosition();
      
      if (objPosLst.size() > 0)
      {
         double dist = seekerPt.distanceSq(objPosLst.get(0));
         Point nearest = objPosLst.get(0);
         
         for (int i = 0; i < objPosLst.size(); i++)
         {
            double newDist = seekerPt.distanceSq(objPosLst.get(i));
            if (newDist < dist)
            {
               dist = newDist;
               nearest = objPosLst.get(i);
            }
         }
         
         return nearest;
      }
      
      return seekerPt;
   }
}
