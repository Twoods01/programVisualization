package actions;

import entities.*;
import physics.*;

import java.util.HashMap;
import java.util.ArrayList;
import java.util.Random;

import processing.core.*;

public class WyvernSpawnAction
   implements Action
{
   final static int WVRN_RATE_MIN = 200;
   final static int WVRN_RATE_MAX = 600;
   final static int WVRN_ANIM_RATE = 100;
   
   private Blacksmith smith;
   private HashMap<String, ArrayList<PImage>> iStore;   
   
   public WyvernSpawnAction(Blacksmith smith,
                            HashMap<String, ArrayList<PImage>> iStore)
   {
      this.smith = smith;
      this.iStore = iStore;
   }
   
   public void entAction(WorldModel world)
   {
      Point openPt = findOpenAround(world, smith.getResourceDistance());
      
      if (openPt.xCoord() != smith.getPosition().xCoord() &&
          openPt.yCoord() != smith.getPosition().yCoord())
      {
         Wyvern wyvern = createWyvern(world, openPt);
         scheduleWyvern(world, wyvern);
         world.addEntity(wyvern);
      }
      else
      {
         world.scheduleAction(this, smith.getRate());
      }
      return; 
   }
   
   public Point findOpenAround(WorldModel world, int dist)
   {
      Point pt = smith.getPosition();
      
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
   
   public Wyvern createWyvern(WorldModel world, Point pos)
   {
      Random rand = new Random();
      
      Wyvern wyvern = new Wyvern("wyvern", iStore.get("wyvern"), pos,WVRN_RATE_MAX - rand.nextInt(WVRN_RATE_MIN),WVRN_ANIM_RATE);
      
      return wyvern;
   }
   
   public void scheduleWyvern(WorldModel world, Wyvern wyvern)
   {
      world.scheduleAction(new WyvernAction(wyvern, iStore),
            wyvern.getRate());
      world.scheduleAction(new AnimationAction(wyvern, 0),
            wyvern.getAnimationRate());
      return; 
   }
}
