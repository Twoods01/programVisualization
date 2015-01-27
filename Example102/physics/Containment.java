package physics;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

import actions.AnimationAction;
import actions.EntityDeathAction;
import actions.MinerNotFullAction;
import actions.OreTransformAction;
import actions.SickVeinAction;
import actions.VeinAction;
import actions.VeinSpawnAction;
import actions.WyvernAction;
import entities.Background;
import entities.Freeze;
import entities.GlowBlob;
import entities.Miner;
import entities.MinerNotFull;
import entities.Mite;
import entities.Obstacle;
import entities.Ogre;
import entities.Ore;
import entities.Quake;
import entities.SickVein;
import entities.Vein;
import entities.Wyvern;
import entity_super.Entity;
import processing.core.PImage;

public class Containment
{  
   final static int ORE_CORRUPT_MIN = 20000;
   final static int ORE_CORRUPT_MAX = 30000;
   
   final static int QUKE_ANIM_RATE = 100;
   final static int QUKE_STEPS = 10;
   final static int QUKE_DURATION = 1100;
   
   final static int WVRN_RATE_MIN = 200;
   final static int WVRN_RATE_MAX = 600;
   final static int WVRN_ANIM_RATE = 100;
   
   final static int FRZE_ANIM_RATE = 100;
   final static int FRZE_STEPS = 4;
   
   final static int VEIN_SPAWN_DELAY = 500;
   
   public void containmentEvent(WorldModel world,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      for (int yi = 0; yi < world.getRows(); yi++)
      {
         for (int xi = 0; xi < world.getCols(); xi++)
         {
            Point pt = new Point(xi, yi);
            
            if (world.getBackgroundCell(pt).getName() == "dirt")
            {
               world.setBackgroundCell(pt,
                     new Background("grass", iStore.get("grass")));
            }
            
            Entity entity = world.getOccupant(pt);
            if (entity != null)
            {
               switch (entity.getName())
               {
                  case "sick obstacle":
                     cureObstacle((Obstacle) entity, world, iStore);
                     break;
                  case "sick vein":
                     cureVein((SickVein) entity, world, iStore);
                     break;
                  case "ogre":
                     cureOgre((Ogre) entity, world, iStore);
                     break;
                  case "glob":
                     cureGlob((GlowBlob) entity, world, iStore);
                     break;
                  case "mite":
                     cureMite((Mite) entity, world, iStore);
                     break;
               }
            }
         }
      }
      return;
   }
   
   public void cureObstacle(Obstacle entity, WorldModel world,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      Obstacle obsc = new Obstacle("obstacle", iStore.get("obstacle"),
            entity.getPosition());
      world.removeEntity(entity);
      world.addEntity(obsc);
      return;
   }
   
   public void cureVein(SickVein entity, WorldModel world,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      Vein vein = new Vein("vein", iStore.get("vein"),
            entity.getPosition(), entity.getRate());
      world.scheduleAction(new VeinAction(vein, iStore), vein.getRate());
      world.removeEntity(entity);
      world.addEntity(vein);
      return;
   }
   
   public void cureOgre(Ogre entity, WorldModel world,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      if (entity.getWasMiner()== false)
      {
         entity.setImgs(iStore.get("none"));
         world.scheduleAction(new EntityDeathAction(entity), 2000);
      }
      else
      {
         Miner miner = new MinerNotFull("miner", iStore.get("miner"),
               entity.getPosition(), entity.getRate(),
               entity.getAnimationRate(), entity.getResourceLimit());
   
         world.scheduleAction(new MinerNotFullAction((MinerNotFull) miner, iStore), miner.getRate());
         world.scheduleAction(new AnimationAction(miner, 0), miner.getAnimationRate());
         
         world.removeEntity(entity);
         world.addEntity(miner);
      }
      return;
   }   
   
   public void cureGlob(GlowBlob entity, WorldModel world,
         HashMap<String, ArrayList<PImage>> iStore)
   {      
       Random rand = new Random();
       
       if (rand.nextInt(100) < 50)
       {
          Wyvern wyvern = createWyvern(world, entity.getPosition(), iStore);
          scheduleWyvern(world, wyvern, iStore);
          
          world.removeEntity(entity);
          world.addEntity(wyvern);
       }
       else 
       {
          Freeze freeze = createFreeze(world, entity.getPosition(), iStore);
          scheduleFreeze(world, freeze, iStore);
          
          world.removeEntity(entity);
          world.addEntity(freeze);
       }
       return;
   }
   
   private Wyvern createWyvern(WorldModel world, Point pos,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      Random rand = new Random();
      return new Wyvern("wyvern", iStore.get("wyvern"), pos, WVRN_RATE_MAX - rand.nextInt(WVRN_RATE_MIN), WVRN_ANIM_RATE);
   }
   
   public void scheduleWyvern(WorldModel world, Wyvern wyvern,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      world.scheduleAction(new WyvernAction(wyvern, iStore),
            wyvern.getRate());
      world.scheduleAction(new AnimationAction(wyvern, 0),
            wyvern.getAnimationRate());
      return;
   }
   
   private Freeze createFreeze(WorldModel world, Point pos,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      return new Freeze("freeze", iStore.get("freeze"), pos, FRZE_ANIM_RATE);
   }
   
   private void scheduleFreeze(WorldModel world, Freeze freeze,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      world.scheduleAction(new AnimationAction(freeze, FRZE_STEPS),
            FRZE_ANIM_RATE);
      world.scheduleAction(new VeinSpawnAction(freeze, iStore),
            VEIN_SPAWN_DELAY);
      return;
   }
   
   public void cureMite(Mite entity, WorldModel world,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      Ore ore = createOre(world, entity.getPosition(), iStore);
      world.removeEntity(entity);
      world.addEntity(ore);
      scheduleOreDecay(world, ore, iStore);
      return;
   }
   
   public Ore createOre(WorldModel world, Point openPt,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      Random rand = new Random();
      return new Ore("ore", iStore.get("ore"), openPt, ORE_CORRUPT_MIN + rand.nextInt(ORE_CORRUPT_MAX + 1));
   }
   
   public void scheduleOreDecay(WorldModel world, Ore ore,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      world.scheduleAction(new OreTransformAction(ore, iStore),
                           ore.getRate());

      return;
   }
}
