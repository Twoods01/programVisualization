import java.util.ArrayList;
import java.util.Random;
import java.util.HashMap;

import processing.core.*;
import physics.*;
import entities.*;
import entity_super.Entity;
import entity_super.EntityPosn;
import actions.*;
public class RandomInit
{
   final static int OBSC = 0;
   final static int VEIN = 1;
   final static int MINR = 2;
   final static int SMTH = 3;
   
   final static int NUM_OBSCS = 35;
   final static int NUM_VEINS = 20;
   final static int NUM_MINRS = 15;
   final static int NUM_SMTHS = 10;
   
   final static int VEIN_RATE_MIN = 8000;
   final static int VEIN_RATE_MAX = 17000;
   
   final static int MINR_RATE_MIN = 600;
   final static int MINR_RATE_MAX = 1000;
   
   final static int SMTH_RATE_MIN = 2000;
   final static int SMTH_RATE_MAX = 4000;
   
   private Random rand;
   
   public RandomInit()
   {
      rand = new Random();
   }
   
   public EntityPosn createMyEnt(WorldModel world,
                           HashMap<String, ArrayList<PImage>> iStore,
                           Point pos, int entCode)
   {
      if (entCode == OBSC)
      {
         return createObstacle(world, pos, iStore);
      }
      else if (entCode == VEIN)
      {
         return createVein(world, pos, iStore);
      }
      else if (entCode == MINR)
      {
         return createMiner(world, pos, iStore);
      }
      else if (entCode == SMTH)
      {
         return createBlacksmith(world, pos, iStore);
      }
      else
      {
         return null;
      }
   }
   
   public Obstacle createObstacle(WorldModel world, Point pos,
                                  HashMap<String, ArrayList<PImage>> iStore)
   {
      if (world.isOccupied(pos))
      {
         return null;
      }
      
      ArrayList<PImage> imgs = iStore.get("obstacle");
      
      Obstacle obstacle = new Obstacle("obstacle", imgs, pos);
      
      return obstacle;
   }
   
   public Vein createVein(WorldModel world, Point pos,
                          HashMap<String, ArrayList<PImage>> iStore)
   {
      if (world.isOccupied(pos))
      {
         return null;
      }
      
      ArrayList<PImage> imgs = iStore.get("vein");
      
      Vein vein = new Vein("vein", imgs, pos,
                           VEIN_RATE_MAX - rand.nextInt(VEIN_RATE_MIN));
     
      world.scheduleAction(new VeinAction(vein, iStore), vein.getRate());
      
      return vein;
   }
   
   public Miner createMiner(WorldModel world, Point pos,
                            HashMap<String, ArrayList<PImage>> iStore)
   {
      if (world.isOccupied(pos))
      {
         return null;
      }
      
      ArrayList<PImage> imgs = iStore.get("miner");
      
      int resourceLimit = 2;
      int animationRate = (4 - rand.nextInt(2)) * 75;
      
      MinerNotFull miner = new MinerNotFull("miner", imgs, pos,
                                            MINR_RATE_MAX - rand.nextInt(MINR_RATE_MIN),
                                            animationRate, resourceLimit);
      
      world.scheduleAction(new MinerNotFullAction(miner, iStore), miner.getRate());
      world.scheduleAction(new AnimationAction(miner, 0), miner.getAnimationRate());
      
      return miner;
   }
   
   public Blacksmith createBlacksmith(WorldModel world, Point pos,
                                     HashMap<String, ArrayList<PImage>> iStore)
   {
      if (world.isOccupied(pos))
      {
         return null;
      }
      
      ArrayList<PImage> imgs = iStore.get("blacksmith");
      
      int resourceLimit = 15;
      
      Blacksmith smith = new Blacksmith("blacksmith", imgs, pos,
                                        SMTH_RATE_MAX - rand.nextInt(SMTH_RATE_MIN),
                                        resourceLimit);
      
      return smith;
   }
   
   public void createRandomEntities(WorldModel world, int entCode, int num,
                                    HashMap<String, ArrayList<PImage>> iStore)
   {
      Point pos;
      
      int numCreated = 0;
      while (numCreated < num)
      {
         pos = new Point(rand.nextInt(world.getCols()),
                         rand.nextInt(world.getRows()));
         EntityPosn entity = createMyEnt(world, iStore, pos, entCode);
         if (entity != null)
         {
            world.addEntity(entity);
            numCreated++;
         }
      }
   }
   
   public void createRandomWorld(WorldModel world,
                                 HashMap<String, ArrayList<PImage>> iStore)
   {
      Entity rock = new Background("rock", iStore.get("rock"));
      world.createRandomBackground(rock);
      
      createRandomEntities(world, OBSC, NUM_OBSCS, iStore);
      
      createRandomEntities(world, VEIN, NUM_VEINS, iStore);
      
      createRandomEntities(world, MINR, NUM_MINRS, iStore);
      
      createRandomEntities(world, SMTH, NUM_SMTHS, iStore);
   }
   
   
}
