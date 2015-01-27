package actions;

import java.util.HashMap;
import java.util.ArrayList;

import action_super.Seeker;
import astar.AStar;
import processing.core.*;
import entities.*;
import entity_super.*;
import physics.*;

public class WyvernAction
   extends Seeker
   implements Action
{
   final static int FRZE_ANIM_RATE = 100;
   final static int FRZE_STEPS = 4;
   
   final static int VEIN_SPAWN_DELAY = 500;
   
   protected Wyvern wyvern;
   protected HashMap<String, ArrayList<PImage>> iStore;
   
   private ArrayList<Point> path;
   
   public WyvernAction(Wyvern wyvern, HashMap<String, ArrayList<PImage>> iStore)
   {
      this.wyvern = wyvern;
      this.iStore = iStore;
      
      this.path = new ArrayList<Point>();
   }
   
   public void entAction(WorldModel world)
   {
      if (world.withinBounds(wyvern.getPosition()))
      {
         if (world.getWvrnTogl() == 1)
         {
            orig_entAction(world);
         }
         else
         {
            EntityPosn blob = findNearestItem(world, "blob", wyvern);
            Point blobPt = blob.getPosition();
            
            if (path.size() == 0)
            {
               AStar astar = new AStar();
               path = astar.starPath(wyvern, blob, "blob", world);
               if (path.size() > 1)
               {
                  path.remove(0);
               }
            }
            
            boolean found = wyvernToBlob(world, blob);
            
            if (found)
            {
               path.clear();
               Freeze freeze = createFreeze(world, blobPt);
               world.addEntity(freeze);
               scheduleFreeze(world, freeze);
            }
            
            world.scheduleAction(this, wyvern.getRate());
         }
      }
      return; 
   }
   
   public void orig_entAction(WorldModel world)
   {
      EntityPosn blob = findNearestItem(world, "blob", wyvern);
      Point blobPt = blob.getPosition();
      
      boolean found = orig_wyvernToBlob(world, blob);
      
      if (found)
      {
         Freeze freeze = createFreeze(world, blobPt);
         world.addEntity(freeze);
         scheduleFreeze(world, freeze);
      }
      return; 
   }
   
   private boolean wyvernToBlob(WorldModel world, EntityPosn entity)
   {
      if (!(entity instanceof OreBlob))
      {
         return false;
      }
      
      Point blobPt = entity.getPosition();
      Point wyvPt = wyvern.getPosition();
      
      if (wyvPt.adjacent(blobPt))
      {
         world.removeEntity(entity);
         return true;
      }
      else
      {
         Point newPt = path.remove(0);
         if (!world.isOccupied(newPt))
         {
            world.moveEntity(wyvern, newPt);
         }
         else
         {
            path.clear();
         }
         
         return false;
      }
   }
   
   private boolean orig_wyvernToBlob(WorldModel world, EntityPosn entity)
   {
      if (!(entity instanceof OreBlob))
      {
         return false;
      }
      
      Point blobPt = entity.getPosition();
      Point wyvPt = wyvern.getPosition();
      
      if (wyvPt.adjacent(blobPt))
      {
         world.removeEntity(entity);
         return true;
      }
      else
      {
         world.moveEntity(wyvern, wyvPt.nextPosition(world, blobPt));
         return false;
      }
   }
   
   private Freeze createFreeze(WorldModel world, Point pos)
   {
      return new Freeze("freeze", iStore.get("freeze"), pos,FRZE_ANIM_RATE);
   }
   
   private void scheduleFreeze(WorldModel world, Freeze freeze)
   {
      world.scheduleAction(new AnimationAction(freeze, FRZE_STEPS),
                           FRZE_ANIM_RATE);
      world.scheduleAction(new VeinSpawnAction(freeze, iStore), VEIN_SPAWN_DELAY);
      return; 
   }
}
