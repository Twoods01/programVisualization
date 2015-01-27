package actions;

import java.util.ArrayList;
import java.util.HashMap;

import physics.Outbreak;
import physics.Point;
import physics.WorldModel;
import processing.core.PImage;
import action_super.Seeker;
import astar.AStar;
import entities.*;
import entity_super.EntityPosn;

public class OgreNotFullAction
   extends Seeker
   implements Action
{
   private OgreNotFull ogre;
   private HashMap<String, ArrayList<PImage>> iStore;
   
   public OgreNotFullAction(OgreNotFull ogre,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      super();
      this.ogre = ogre;
      this.iStore = iStore;
   }
   
   public void entAction(WorldModel world)
   {
      if (world.withinBounds(ogre.getPosition()))
      {
         transmit(world);
         
         if (world.getMinrTogl() == 1)
         {
            orig_entAction(world);
         }
         else
         {
            EntityPosn mite = findNearestItem(world, "mite", ogre);
            Point mtePt = mite.getPosition();
            Ogre newOgre = ogre;
            
            if (path.size() == 0)
            {
               AStar astar = new AStar();
               path = astar.starPath(ogre, mite, "mite", world);
               if (path.size() > 1)
               {
                  path.remove(0);
               }
            }
            
            boolean found = ogreToMite(world, mtePt);
            
            if (found)
            {
               path.clear();
               newOgre = tryTransformOgre(world);
            }
            
            createOgreAction(world, newOgre);
         }
      }
      return;
   }
   
   public void orig_entAction(WorldModel world)
   {
      EntityPosn mite = findNearestItem(world, "mite", ogre);
      Point mtePt = mite.getPosition();
      Ogre newOgre = ogre;
   
      boolean found = orig_ogreToMite(world, mtePt);
      
      if (found)
      {
         newOgre = tryTransformOgre(world);
      }
   
      createOgreAction(world, newOgre); 
      return;    
   }
   
   public boolean ogreToMite(WorldModel world, Point mtePt)
   {
      {
         Point ogrPt = ogre.getPosition();
         EntityPosn mite = world.getOccupant(mtePt);
         
         if (mite.getName() != "mite")
         {
            return false;
         }
         if (ogrPt.adjacent(mtePt))
         {
            ogre.setResourceCount(1 + ogre.getResourceCount());
            world.removeEntity(mite);
            return true;
         }
         else
         {
            Point newPt = path.remove(0);
            if (!(world.isOccupied(newPt)))
            {
               world.moveEntity(ogre, newPt);
            }
            else
            {
               path.clear();
            }
            return false;
         }  
      }
   }
   
   public boolean orig_ogreToMite(WorldModel world, Point mtePt)
   {
      Point mnrPt = ogre.getPosition();
      EntityPosn mite = world.getOccupant(mtePt);
      
      if (mite.getName() != "mite")
      {
         return false;
      }
      if (mnrPt.adjacent(mtePt))
      {
         ogre.setResourceCount(1 + ogre.getResourceCount());
         world.removeEntity(mite);
         return true;
      }
      else
      {
         Point newPt = mnrPt.nextPosition(world, mtePt);
         world.moveEntity(ogre, newPt);
         return false;
      }  
   }
   
   public Ogre tryTransformOgre(WorldModel world)
   {
      if (ogre.getResourceCount() < ogre.getResourceLimit())
      {
         return ogre;
      }
      else
      {
         OgreFull newOgre = new OgreFull(ogre.getName(), iStore.get("ogre"),
               ogre.getPosition(), ogre.getRate(), ogre.getAnimationRate(),
               ogre.getResourceLimit(), ogre.getWasMiner());
         updateWorld_OgreFull(world, newOgre);
         world.scheduleAction(new AnimationAction(newOgre, 0),
                              newOgre.getAnimationRate());
         return newOgre;
      }
   }
   
   public void updateWorld_OgreFull(WorldModel world, OgreFull newOgre)
   {
      world.removeEntity(ogre);
      world.addEntity(newOgre);
      return; 
   }
   
   public void createOgreAction(WorldModel world, Ogre newOgre)
   {     
      if (newOgre instanceof OgreFull)
      {
         world.scheduleAction(new OgreFullAction((OgreFull) newOgre,
               iStore), newOgre.getRate());
      }
      else if (newOgre instanceof OgreNotFull)
         world.scheduleAction(this, ogre.getRate());
      return; 
   }
   
   public void transmit(WorldModel world)
   {
      for (int dy = -1; dy < 2; dy++)
      {
         for (int dx = -1; dx < 2; dx++)
         {
            Point entPt = new Point(ogre.getPosition().xCoord() + dx,
                  ogre.getPosition().yCoord() + dy);
            if (world.withinBounds(entPt) &&
                  ogre.getPosition().adjacent(entPt))
            {
               Outbreak spreading = new Outbreak();
               EntityPosn adjEnt = world.getOccupant(new Point(
                     ogre.getPosition().xCoord() + dx,
                     ogre.getPosition().yCoord() + dy));
               if (adjEnt instanceof Miner)
               {
                  spreading.sickMiner((Miner) adjEnt, world, iStore);
               }
               if (adjEnt instanceof Wyvern)
               {
                  spreading.sickWyvern((Wyvern) adjEnt, world, iStore);
               }
            }
         }
      }
      return; 
   }
}