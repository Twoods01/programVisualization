package physics;

import entities.*;
import entity_super.Entity;
import entity_super.EntityPosn;
import actions.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

import processing.core.PImage;

public class Outbreak
{   
  final static int WIDTH = 20 * 2;
  final static int HEIGHT = 15 * 2;
   
   final static int VEIN_RATE_MIN = 8000;
   final static int VEIN_RATE_MAX = 17000;
   
   final static int OGRE_RATE_MIN = 600;
   final static int OGRE_RATE_MAX = 1000;
   
   public void outbreakEvent(WorldModel world, HashMap<String, ArrayList<PImage>> iStore)
   {
      Random rand = new Random();
      
      Point epicenter = new Point(rand.nextInt(WIDTH - 4),
                                  rand.nextInt(HEIGHT - 4));
      
         // how should I figure out the region...
         // maybe a center and a spread;
         // the center always with a border of 2 tiles
         // default spread from there
            // with random possible increase
      
      ArrayList<Point> groundZero = backgroundToDirt(world, epicenter, iStore);
      
      infectEntities(world, groundZero, iStore);
     
      spawnEntities(world, groundZero, iStore);
      
      return;
   }
   
   public ArrayList<Point> backgroundToDirt(WorldModel world, Point epicenter, HashMap<String, ArrayList<PImage>> iStore)
   {      
      ArrayList<Point> groundZero = new ArrayList<Point>();
      
      Background bkgd = new Background("dirt", iStore.get("dirt"));
      for (int yi = epicenter.yCoord(); yi < epicenter.yCoord() + 4; yi++)
      {
         for (int xi = epicenter.xCoord(); xi < epicenter.xCoord() + 4; xi++)
         {
            world.setBackgroundCell(new Point(xi, yi), bkgd);
            groundZero.add(new Point(xi, yi));
         }
      }
      
      return groundZero;
   }
   
   public void infectEntities(WorldModel world, ArrayList<Point> groundZero,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      for (Point pt : groundZero)
      {
         Entity entity = world.getOccupant(pt);
         if (entity != null)
         {
            switch (entity.getName())
            {
               case "obstacle":
                  sickObstacle((Obstacle) entity, world, iStore);
                  break;
               case "vein":
                  sickVein((Vein) entity, world, iStore);
                  break;
               case "miner":
                  sickMiner((Miner) entity, world, iStore);
                  break;
               case "wyvern":
                  sickWyvern((Wyvern) entity, world, iStore);
                  break;
            }
         }
      }
      return;
   }
   
   public void sickObstacle(Obstacle entity, WorldModel world,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      Obstacle obsc = new Obstacle("sick obstacle", iStore.get("sick obstacle"),
            entity.getPosition());
      world.removeEntity(entity);
      world.addEntity(obsc);
      return;
   }
   
   public void sickVein(Vein entity, WorldModel world,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      SickVein skvn = new SickVein("sick vein", iStore.get("sick vein"),
            entity.getPosition(), entity.getRate());
      world.scheduleAction(new SickVeinAction(skvn, iStore), skvn.getRate());
      world.removeEntity(entity);
      world.addEntity(skvn);
      return;
   }
   
   public void sickMiner(Miner entity, WorldModel world,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      if (entity.getResourceLimit() == entity.getResourceCount())
      {
         Ogre ogre = new OgreFull("ogre", iStore.get("ogre"),
               entity.getPosition(), entity.getRate(),
               entity.getAnimationRate(), entity.getResourceLimit(), true);

         world.scheduleAction(new OgreFullAction((OgreFull) ogre, iStore), ogre.getRate());
         world.scheduleAction(new AnimationAction(ogre, 0), ogre.getAnimationRate());
         
         world.removeEntity(entity);
         world.addEntity(ogre);
      }
      else
      {
         Ogre ogre = new OgreNotFull("ogre", iStore.get("ogre"),
               entity.getPosition(), entity.getRate(),
               entity.getAnimationRate(), entity.getResourceLimit(), true);

         world.scheduleAction(new OgreNotFullAction((OgreNotFull) ogre, iStore), ogre.getRate());
         world.scheduleAction(new AnimationAction(ogre, 0), ogre.getAnimationRate());
         
         world.removeEntity(entity);
         world.addEntity(ogre);
      }
      return;
   }
   
   public void sickWyvern(Wyvern wyvern, WorldModel world,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      wyvern.setImgs(iStore.get("none"));
      world.scheduleAction(new EntityDeathAction(wyvern), 2000);
      wyvern.setInfected(false);
      return;
   }
   
   public void spawnEntities(WorldModel world, ArrayList<Point> groundZero,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      Random rand = new Random();
      
      Point veinPt = groundZero.get(rand.nextInt(groundZero.size()));
      Point ogrePt = groundZero.get(rand.nextInt(groundZero.size()));
      
      EntityPosn skvn = createSickVein(world, veinPt, iStore);
      if (skvn != null)
      {
         world.addEntity(skvn);
      }
      EntityPosn ogre = createOgre(world, ogrePt, iStore);
      if (ogre != null)
      {
         world.addEntity(ogre);
      }
      return;
   }
   
   public SickVein createSickVein(WorldModel world, Point pos,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      if (world.isOccupied(pos))
      {
         return null;
      }
      
      ArrayList<PImage> imgs = iStore.get("sick vein");
      
      Random rand = new Random();
      
      SickVein vein = new SickVein("sick vein", imgs, pos,
            VEIN_RATE_MAX - rand.nextInt(VEIN_RATE_MIN));
      
      world.scheduleAction(new SickVeinAction(vein, iStore), vein.getRate());
      
      return vein;
   }
   
   public Ogre createOgre(WorldModel world, Point pos,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      if (world.isOccupied(pos))
      {
         return null;
      }
      
      ArrayList<PImage> imgs = iStore.get("ogre");
      
      Random rand = new Random();
      
      int resourceLimit = 2;
      int animationRate = (4 - rand.nextInt(2)) * 75;
      
      OgreNotFull ogre = new OgreNotFull("ogre", imgs, pos,
            OGRE_RATE_MAX - rand.nextInt(OGRE_RATE_MIN),
            animationRate, resourceLimit, false);
      
      world.scheduleAction(new OgreNotFullAction(ogre, iStore), ogre.getRate());
      world.scheduleAction(new AnimationAction(ogre, 0), ogre.getAnimationRate());
      
      return ogre;
   }

}
