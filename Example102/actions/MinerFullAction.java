package actions;

import java.util.ArrayList;
import java.util.HashMap;

import astar.AStar;
import physics.*;
import processing.core.*;
import entities.*;
import entity_super.EntityGath;
import entity_super.EntityPosn;
import action_super.*;

public class MinerFullAction
   extends Seeker
   implements Action
{  
   private MinerFull miner;
   private HashMap<String, ArrayList<PImage>> iStore;
   
   public MinerFullAction(MinerFull miner,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      super();
      this.miner = miner;
      this.iStore = iStore;

   }
   
   public void entAction(WorldModel world)
   {
      if (world.withinBounds(miner.getPosition()))
      {
         if (world.getMinrTogl() == 1)
         {
            orig_entAction(world);
         }
         else
         {
            EntityPosn smth = findNearestItem(world, "blacksmith", miner);
            Point smthPt = smth.getPosition();
            Miner newMiner = miner;
            
            if (path.size() == 0)
            {
               AStar astar = new AStar();
               path = astar.starPath(miner, smth, "blacksmith", world);
               if (path.size() > 1)
               {
                  path.remove(0);
               }
            }
            
            boolean found = minerToSmith(world, smthPt);
            
            if (found)
            {
               path.clear();
               newMiner = tryTransformMiner(world);
               scheduleBlacksmithSpawn(world, smthPt);
            }
            
            createMinerAction(world, newMiner);
         }
      }
      return;
   }

   
   public void orig_entAction(WorldModel world)
   {
      EntityPosn smth = findNearestItem(world, "blacksmith", miner);
      Point smthPt = smth.getPosition();
      Miner newMiner = miner;

      boolean found = orig_minerToSmith(world, smthPt);
      
      if (found)
      {
         newMiner = tryTransformMiner(world);
         scheduleBlacksmithSpawn(world, smthPt);
      }
      
      createMinerAction(world, newMiner);
      return;
   }
   
   public boolean minerToSmith(WorldModel world, Point smthPt)
   {
      Point mnrPt = miner.getPosition();
      EntityGath smith = (EntityGath) world.getOccupant(smthPt);
      
      if (smith.getName() != "blacksmith")
      {
         return false;
      }
      if (mnrPt.adjacent(smthPt))
      {
         smith.setResourceCount(smith.getResourceCount() +
               miner.getResourceCount());
         miner.setResourceCount(0);
         return true;
      }
      else
      {
         Point newPt = path.remove(0);
         if (!world.isOccupied(newPt))
         {
            world.moveEntity(miner, newPt);
         }
         else
         {
            path.clear();
         }
         return false;
      }  

   }
   
   public boolean orig_minerToSmith(WorldModel world, Point smthPt)
   {
      Point mnrPt = miner.getPosition();
      EntityGath smith = (EntityGath) world.getOccupant(smthPt);
      
      if (smith.getName() != "blacksmith")
      {
         return false;
      }
      if (mnrPt.adjacent(smthPt))
      {
         smith.setResourceCount(smith.getResourceCount() +
               miner.getResourceCount());
         miner.setResourceCount(0);
         return true;
      }
      else
      {
         Point newPt = mnrPt.nextPosition(world, smthPt);
         world.moveEntity(miner, newPt);
         return false;
      }  
   }
   
   public Miner tryTransformMiner(WorldModel world)
   {
      if (miner.getResourceCount() == miner.getResourceLimit())
      {
         return miner;
      }
      else
      {
         MinerNotFull newMiner = new MinerNotFull(miner.getName(),
               iStore.get("miner"), miner.getPosition(), miner.getRate(),
               miner.getAnimationRate(), miner.getResourceLimit());
         updateWorld_MinerNotFull(world, newMiner);
         world.scheduleAction(new AnimationAction(newMiner, 0),
               newMiner.getAnimationRate());
         return newMiner;
      }
   }
   
   public void updateWorld_MinerNotFull(WorldModel world, MinerNotFull newMiner)
   {
      world.removeEntity(miner);
      world.addEntity(newMiner);
      return;
   }
   
   public void scheduleBlacksmithSpawn(WorldModel world, Point smthPt)
   {
      Blacksmith smith = (Blacksmith) world.getOccupant(smthPt);
      
      if (smith.getResourceCount() >= 10)//smith.getResourceLimit())
      {
         smith.setResourceCount(smith.getResourceCount() - 
               smith.getResourceLimit());
         world.scheduleAction(new WyvernSpawnAction(smith, iStore),
               smith.getRate());
      }
      return;
   }
   
   public void createMinerAction(WorldModel world, Miner newMiner)
   {     
      if (newMiner instanceof MinerFull)
      {
         world.scheduleAction(this, miner.getRate());
      }
      else if (newMiner instanceof MinerNotFull)
         world.scheduleAction(new MinerNotFullAction((MinerNotFull) newMiner,
               iStore), miner.getRate());

      return;
   }
}