package actions;

import physics.*;
import entities.*;
import entity_super.EntityPosn;
import action_super.Seeker;

import java.util.ArrayList;
import java.util.HashMap;

import processing.core.*;

public class OreBlobAction
   extends Seeker
   implements Action
{  
   final static int NUM_VEINS = 20;
   
   final static int QUKE_ANIM_RATE = 100;
   final static int QUKE_STEPS = 10;
   final static int QUKE_DURATION = 1100;
   
   private OreBlob blob;
   private HashMap<String, ArrayList<PImage>> iStore;
   
   public OreBlobAction(OreBlob blob,
                        HashMap<String, ArrayList<PImage>> iStore)
   {
      this.blob = blob;
      this.iStore = iStore;
   }
   
   public void entAction(WorldModel world)
   {
      EntityPosn vein = findNearestItem(world, "vein", blob);
      Point veinPt = vein.getPosition();
      
      boolean found = blobToVein(world, vein);
      
      int nextTime = blob.getRate();
      
      if (found)
      {
         Quake quake = createQuake(world, veinPt);
         scheduleQuake(world, quake);
         world.addEntity(quake);
         nextTime *= 2;
      }
      
      world.scheduleAction(this, nextTime);
      return; 
   }
   
   public EntityPosn findNearestVein(WorldModel world)
   {
      Point blobPt = blob.getPosition();
      ArrayList<Point> veinsPos = new ArrayList<Point>();
      
      for (int yi = 0; yi < world.getRows(); yi++)
      {
         for (int xi = 0; xi < world.getCols(); xi++)
         {
            if (world.withinBounds(new Point(xi, yi)))
            {
               
               Point veinPt = new Point(xi, yi);
               if (world.getOccupant(veinPt) instanceof Vein)
               {
                  veinsPos.add(veinPt);
               }
            
            }
         }
      }
      
      return world.getOccupant(nearestVein(veinsPos, blobPt));
   }
   
   public Point nearestVein(ArrayList<Point> veinsPos, Point blobPt)
   {      
      if (veinsPos.size() > 0)
      {             
         double dist = blobPt.distanceSq(veinsPos.get(0));
         Point nearest = veinsPos.get(0);
         
         for (int i = 1; i < veinsPos.size(); i++)
         {
            double newDist = blobPt.distanceSq(veinsPos.get(i));
            if (newDist < dist)
            {
               dist = newDist;
               nearest = veinsPos.get(i);
            }
         }
         
         return nearest;
      }
      
      return blobPt;
   }
   
   public boolean blobToVein(WorldModel world, EntityPosn entity)
   {          
      if (!(entity instanceof Vein))
      {
         return false;
      }
      
      Point blobPt = blob.getPosition();
      Point veinPt = entity.getPosition();
      
      if (blobPt.adjacent(veinPt))
      {
         world.removeEntity(entity);
         return true;
      }
      else
      {
         Point newPt = blobNextPosition(world, veinPt);
         if (world.withinBounds(newPt))
         {
            EntityPosn oldEntity = world.getOccupant(newPt);
            if (oldEntity instanceof Ore)
            {
               world.removeEntity(oldEntity);
            }
         }

         world.moveEntity(blob, newPt);
         return false;
      }  
   }
   
   public Point blobNextPosition(WorldModel world, Point destPt)
   {
      Point blobPt = blob.getPosition();
      
      int horiz = sign(destPt.xCoord() - blobPt.xCoord());
      Point newPt = new Point(blobPt.xCoord() + horiz, blobPt.yCoord());
      
      if (horiz == 0 || (world.isOccupied(newPt) &&
          world.getOccupant(newPt).getName() != "ore"))
      {
         int vert = sign(destPt.yCoord() - blobPt.yCoord());
         newPt.setX(blobPt.xCoord());
         newPt.setY(blobPt.yCoord() + vert);
         
         if (vert == 0 || (world.isOccupied(newPt) &&
             world.getOccupant(newPt).getName() != "ore"))
         {
            newPt.setY(blobPt.yCoord());
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
}
