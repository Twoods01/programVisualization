package actions;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

import physics.Point;
import physics.WorldModel;
import processing.core.PImage;
import entities.*;

public class SickVeinAction
   implements Action
{
   final static int MITE_CORRUPT_MIN = 20000;
   final static int MITE_CORRUPT_MAX = 30000;
   
   final static int VEIN_RATE_MIN =  8000;
   final static int VEIN_RATE_MAX = 17000;
   
   private SickVein sickvein;
   private HashMap<String, ArrayList<PImage>> iStore;
   
   public SickVeinAction(SickVein sickvein,
            HashMap<String, ArrayList<PImage>> iStore)
   {
      this.sickvein = sickvein;
      this.iStore = iStore;
   }
   
   public void entAction(WorldModel world)
   {
      if (world.withinBounds(sickvein.getPosition()))
      {
         Point openPt = findOpenAround(world, sickvein.getResourceDistance());
   
         if (!openPt.equals(sickvein.getPosition()))
         {
            Mite newMite = createMite(world, openPt);
            world.addEntity(newMite);
            scheduleMiteAnimation(world, newMite);
            scheduleMiteDecay(world, newMite);
         }
         
         Random rand = new Random();      
         world.scheduleAction(this, VEIN_RATE_MAX - rand.nextInt(VEIN_RATE_MIN));
      }
      return; 
   }
   
   public Point findOpenAround(WorldModel world, int dist)
   {
      Point pt = sickvein.getPosition();
      
      for(int dy = -dist; dy <= dist; dy++)
      {
         for (int dx = -dist; dx <= dist; dx++)
         {
            Point newPt = new Point(pt.xCoord() + dx, pt.yCoord() + dy);
            
            if (world.withinBounds(newPt) && !world.isOccupied(newPt))
            {
               return newPt;
            }
         }
      }
      
      return pt;
   }
   
   public Mite createMite(WorldModel world, Point openPt)
   {
      Random rand = new Random();
      return new Mite("mite", iStore.get("mite"), openPt, MITE_CORRUPT_MIN + rand.nextInt(MITE_CORRUPT_MAX + 1),(4 - rand.nextInt(2)) * 75);
   }
   
   public void scheduleMiteAnimation(WorldModel world, Mite mite)
   {
      world.scheduleAction(new AnimationAction(mite, 0),mite.getAnimationRate());
   }
   
   public void scheduleMiteDecay(WorldModel world, Mite mite)
   {
      world.scheduleAction(new MiteTransformAction(mite, iStore),
                           mite.getRate());
      return; 
   }
}
