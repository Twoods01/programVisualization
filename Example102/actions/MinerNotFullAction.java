package actions;

import java.util.ArrayList;
import java.util.HashMap;

import astar.AStar;
import physics.*;
import entities.*;
import entity_super.EntityPosn;
import action_super.*;
import processing.core.PImage;

public class MinerNotFullAction
   extends Seeker
   implements Action
{  
   private MinerNotFull miner;
   private HashMap<String, ArrayList<PImage>> iStore;
   
   public MinerNotFullAction(MinerNotFull miner,
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
            EntityPosn ore = findNearestItem(world, "ore", miner);
            Point orePt = ore.getPosition();
            Miner newMiner = miner;
            
            if (path.size() == 0)
            {
               AStar astar = new AStar();
               path = astar.starPath(miner, ore, "ore", world);
               if (path.size() > 1)
               {
                  path.remove(0);
               }
            }
            
            boolean found = minerToOre(world, orePt);
            
            if (found)
            {
               path.clear();
               newMiner = tryTransformMiner(world);
            }
            
            createMinerAction(world, newMiner);
         }
      }
      return;
   }
   
   public void orig_entAction(WorldModel world)
   {
      EntityPosn ore = findNearestItem(world, "ore", miner);
      Point orePt = ore.getPosition();
      Miner newMiner = miner;
   
      boolean found = orig_minerToOre(world, orePt);
      
      if (found)
      {
         newMiner = tryTransformMiner(world);
      }
   
      createMinerAction(world, newMiner); 
      return;    
   }
   
   public boolean minerToOre(WorldModel world, Point orePt)
   {
      {
         Point mnrPt = miner.getPosition();
         EntityPosn ore = world.getOccupant(orePt);
         
         if (ore.getName() != "ore")
         {
            return false;
         }
         if (mnrPt.adjacent(orePt))
         {
            miner.setResourceCount(1 + miner.getResourceCount());
            world.removeEntity(ore);
            return true;
         }
         else
         {
            Point newPt = path.remove(0);
            if (!(world.isOccupied(newPt)))
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
   }
   
   public boolean orig_minerToOre(WorldModel world, Point orePt)
   {
      Point mnrPt = miner.getPosition();
      EntityPosn ore = world.getOccupant(orePt);
      
      if (ore.getName() != "ore")
      {
         return false;
      }
      if (mnrPt.adjacent(orePt))
      {
         miner.setResourceCount(1 + miner.getResourceCount());
         world.removeEntity(ore);
         return true;
      }
      else
      {
         Point newPt = mnrPt.nextPosition(world, orePt);
         world.moveEntity(miner, newPt);
         return false;
      }  
   }
   
   public Miner tryTransformMiner(WorldModel world)
   {
      if (miner.getResourceCount() < miner.getResourceLimit())
      {
         return miner;
      }
      else
      {
         MinerFull newMiner = new MinerFull(miner.getName(), iStore.get("miner"),
               miner.getPosition(), miner.getRate(), miner.getAnimationRate(),
               miner.getResourceLimit());
         updateWorld_MinerFull(world, newMiner);
         world.scheduleAction(new AnimationAction(newMiner, 0),
                              newMiner.getAnimationRate());
         return newMiner;
      }
   }
   
   public void updateWorld_MinerFull(WorldModel world, MinerFull newMiner)
   {
      world.removeEntity(miner);
      world.addEntity(newMiner);
      return;
   }
   
   public void createMinerAction(WorldModel world, Miner newMiner)
   {     
      if (newMiner instanceof MinerFull)
      {
         world.scheduleAction(new MinerFullAction((MinerFull) newMiner,
                              iStore), newMiner.getRate());
      }
      else if (newMiner instanceof MinerNotFull)
         world.scheduleAction(this, miner.getRate());
      return;
   }

}
