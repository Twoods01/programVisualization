package actions;
import entities.*;
import physics.*;

import java.util.ArrayList;
import java.util.HashMap;

import processing.core.*;

import java.util.Random;

public class VeinAction
   implements Action
{
   final static int ORE_CORRUPT_MIN = 20000;
   final static int ORE_CORRUPT_MAX = 30000;
   
   final static int VEIN_RATE_MIN =  8000;
   final static int VEIN_RATE_MAX = 17000;
   
   protected Vein vein;
   protected HashMap<String, ArrayList<PImage>> iStore;
   
   public VeinAction(Vein vein, HashMap<String, ArrayList<PImage>> iStore)
   {
      this.vein = vein;
      this.iStore = iStore;
   }
   
   public void entAction(WorldModel world)
   {
      if (world.withinBounds(vein.getPosition()))
      {
         Point openPt = findOpenAround(world, vein.getResourceDistance());
   
         if (openPt.xCoord() != vein.getPosition().xCoord() ||
             openPt.yCoord() != vein.getPosition().yCoord())
         {
            Ore newOre = createOre(world, openPt);
            world.addEntity(newOre);
            scheduleOreDecay(world, newOre);
         }
         
         Random rand = new Random();      
         world.scheduleAction(this, VEIN_RATE_MAX - rand.nextInt(VEIN_RATE_MIN));
      }
      return; 
   }
   
   public Point findOpenAround(WorldModel world, int dist)
   {
      Point pt = vein.getPosition();
      
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
   
   public Ore createOre(WorldModel world, Point openPt)
   {
      Random rand = new Random();
      return new Ore("ore", iStore.get("ore"), openPt, ORE_CORRUPT_MIN + rand.nextInt(ORE_CORRUPT_MAX + 1));
   }
   
   public void scheduleOreDecay(WorldModel world, Ore ore)
   {
      world.scheduleAction(new OreTransformAction(ore, iStore),
                           ore.getRate());
      return; 
   }

}
