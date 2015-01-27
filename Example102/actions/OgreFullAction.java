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

public class OgreFullAction
   extends Seeker
   implements Action
{
   private OgreFull ogre;
   private HashMap<String, ArrayList<PImage>> iStore;
   
   public OgreFullAction(OgreFull ogre,
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
            EntityPosn glob = findNearestItem(world, "glob", ogre);
            Point globPt = glob.getPosition();
            Ogre newOgre = ogre;
            
            if (path.size() == 0)
            {
               AStar astar = new AStar();
               path = astar.starPath(ogre, glob, "glob", world);
               if (path.size() > 1)
               {
                  path.remove(0);
               }
            }
            
            boolean found = ogreToGlob(world, globPt);
            
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
      EntityPosn glob = findNearestItem(world, "glob", ogre);
      Point globPt = glob.getPosition();
      Ogre newOgre = ogre;
   
      boolean found = orig_ogreToGlob(world, globPt);
      
      if (found)
      {
         newOgre = tryTransformOgre(world);
      }
      
   
      createOgreAction(world, newOgre);     
      return;
   }
   
   public boolean ogreToGlob(WorldModel world, Point globPt)
   {
      {
         Point ogrPt = ogre.getPosition();
         EntityPosn glob = world.getOccupant(globPt);
         
         if (glob.getName() != "glob")
         {
            return false;
         }
         if (ogrPt.adjacent(globPt))
         {
            // set glob resource count
            ogre.setResourceCount(0);
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
   
   public boolean orig_ogreToGlob(WorldModel world, Point globPt)
   {
      Point ogrPt = ogre.getPosition();
      EntityPosn glob = world.getOccupant(globPt);
      
      if (glob.getName() != "glob")
      {
         return false;
      }
      if (ogrPt.adjacent(globPt))
      {
         // set glob resource count
         ogre.setResourceCount(0);
         return true;
      }
      else
      {
         Point newPt = ogrPt.nextPosition(world, ogrPt);
         world.moveEntity(ogre, newPt);
         return false;
      }  
   }
   
   public Ogre tryTransformOgre(WorldModel world)
   {
      if (ogre.getResourceCount() == ogre.getResourceLimit())
      {
         return ogre;
      }
      else
      {
         OgreNotFull newOgre = new OgreNotFull(ogre.getName(), iStore.get("ogre"),
               ogre.getPosition(), ogre.getRate(), ogre.getAnimationRate(),
               ogre.getResourceLimit(), ogre.getWasMiner());
         updateWorld_OgreNotFull(world, newOgre);
         world.scheduleAction(new AnimationAction(newOgre, 0),
               newOgre.getAnimationRate());
         return newOgre;
      }
   }
   
   public void updateWorld_OgreNotFull(WorldModel world, OgreNotFull newOgre)
   {
      world.removeEntity(ogre);
      world.addEntity(newOgre);
      return;
   }
   
   public void createOgreAction(WorldModel world, Ogre newOgre)
   {     
      if (newOgre instanceof OgreNotFull)
      {
         world.scheduleAction(new OgreNotFullAction((OgreNotFull) newOgre,
               iStore), newOgre.getRate());
      }
      else if (newOgre instanceof OgreFull)
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
               EntityPosn adjEnt = world.getOccupant(entPt);
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
