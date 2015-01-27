package actions;

import java.util.HashMap;
import java.util.ArrayList;
import java.util.Random;

import action_super.Seeker;
import processing.core.PImage;
import entities.*;
import entity_super.EntityAnim;
import entity_super.EntityPosn;
import physics.*;

public class GlowBlobAction
   extends Seeker
   implements Action
{
   final static int QUKE_ANIM_RATE = 100;
   final static int QUKE_STEPS = 10;
   final static int QUKE_DURATION = 1100;
   
   final static int WVRN_RATE_MIN = 200;
   final static int WVRN_RATE_MAX = 600;
   final static int WVRN_ANIM_RATE = 100;
   
   final static int FRZE_ANIM_RATE = 100;
   final static int FRZE_STEPS = 4;
   
   final static int VEIN_SPAWN_DELAY = 500;
   
   private GlowBlob glob;
   private HashMap<String, ArrayList<PImage>> iStore;
   
   public GlowBlobAction(GlowBlob glob,
         HashMap<String, ArrayList<PImage>> iStore)
   {
      this.glob = glob;
      this.iStore = iStore;
   }
   
   public void entAction(WorldModel world)
   {
      if (world.withinBounds(glob.getPosition()))
      {
         EntityPosn vein = findNearestItem(world, "sick vein", glob);
         Point veinPt = vein.getPosition();
         
         boolean found = globToVein(world, vein);
         
         int nextTime = glob.getRate();
         
         if (found)
         {
            Quake quake = createQuake(world, veinPt);
            scheduleQuake(world, quake);
            world.addEntity(quake);
            scheduleGlobDecay(world, veinPt);
         }
         
         world.scheduleAction(this, nextTime);
      }
      return;
   }
   
   public boolean globToVein(WorldModel world, EntityPosn entity)
   {
      if (!(entity instanceof SickVein ||
          !(entity instanceof Vein)))
      {
         return false;
      }
      
      Point globPt = glob.getPosition();
      Point veinPt = entity.getPosition();
      
      if (globPt.adjacent(veinPt))
      {
         world.removeEntity(entity);
         return true;
      }
      else
      {
         Point newPt = globNextPosition(world, veinPt);
         if (world.withinBounds(newPt))
         {
            EntityPosn oldEntity = world.getOccupant(newPt);
            if (oldEntity instanceof Mite)
            {
               world.removeEntity(oldEntity);
            }
         }

         world.moveEntity(glob, newPt);
         return false;
      }  
   }
   
   public Point globNextPosition(WorldModel world, Point destPt)
   {
      Point globPt = glob.getPosition();
      
      int horiz = sign(destPt.xCoord() - globPt.xCoord());
      Point newPt = new Point(globPt.xCoord() + horiz, globPt.yCoord());
      
      if (horiz == 0 || (world.isOccupied(newPt) &&
          world.getOccupant(newPt).getName() != "mite"))
      {
         int vert = sign(destPt.yCoord() - globPt.yCoord());
         newPt.setX(globPt.xCoord());
         newPt.setY(globPt.yCoord() + vert);
         
         if (vert == 0 || (world.isOccupied(newPt) &&
             world.getOccupant(newPt).getName() != "mite"))
         {
            newPt.setY(globPt.yCoord());
         }
      }
      
      return newPt;
   }
   
   public int sign(int x)
   {
      if (x < 0)
      {
         return -1;
      }
      else if (x > 0)
      {
         return 1;
      }
      else
      {
         return 0;
      }
   }
   
   public Quake createQuake(WorldModel world, Point pos)
   {
      return new Quake("quake", iStore.get("quake"), pos, QUKE_ANIM_RATE);
   }
   
   public void scheduleQuake(WorldModel world, Quake quake)
   {
      world.scheduleAction(new AnimationAction(quake, QUKE_STEPS),
            quake.getAnimationRate());
      world.scheduleAction(new EntityDeathAction(quake), QUKE_DURATION);
      return;
   }
   
   public void scheduleGlobDecay(WorldModel world, Point veinPt)
   {
      for (int dy = -1; dy < 2; dy++)
      {
         for (int dx = -1; dx < 2; dx++)
         {
            Point globPt = new Point(
                  veinPt.xCoord() + dx, veinPt.yCoord() + dy);
            if (world.getOccupant(globPt) instanceof GlowBlob ||
                world.getOccupant(globPt) instanceof OreBlob)
            {
               Quake quake = createQuake(world, globPt);
               scheduleQuake(world, quake);
               
               world.removeEntity(world.getOccupant(globPt));
               world.addEntity(quake);
               
               world.scheduleAction(new EntityDeathAction(
                     (EntityAnim) world.getOccupant(globPt)), QUKE_DURATION);
            }
                  
         }
      }
      return;
   }
}