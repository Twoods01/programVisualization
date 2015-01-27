package physics;

import entities.*;
import entity_super.Entity;
import entity_super.EntityPosn;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Timer;

import processing.core.*;

import java.util.Random;
import java.util.Timer;
import java.util.TimerTask;

import actions.*;

public class WorldModel
{ 
   private Grid background;
   private int numRows;
   private int numCols;
   private OccuGrid occupancy;

   private int minrTogl;
   private int wvrnTogl;
   
   private Timer time;

   
   public WorldModel(int numCols, int numRows, ArrayList<PImage> bkgd)
   {
      this.numCols = numCols;
      this.numRows = numRows;
      this.background = new Grid(numCols, numRows, bkgd);
      this.occupancy = new OccuGrid(numCols, numRows);
      this.time = new Timer();
      
      this.minrTogl = 0;
      this.wvrnTogl = 0;
   }
   
   public int getCols()
   {
      return numCols;
   }
   
   public int getRows()
   {
      return numRows;
   }
   
   public boolean withinBounds(Point pt)
   {
      return (pt.xCoord() >= 0 && pt.xCoord() < numCols && pt.yCoord() >= 0 && pt.yCoord() < numRows);
   }
   
   public boolean isOccupied(Point pt)
   {
      return (withinBounds(pt) && occupancy.getCell(pt) != null); 
   }
   
   public Entity getBackgroundCell(Point pt)
   {
      return background.getCell(pt);
   }
   
   public void setBackgroundCell(Point pt, Entity bkgd)
   {
      if (withinBounds(pt))
      {
         background.setCell(pt, bkgd);
      }
      return;
   }
   
   public void createRandomBackground(Entity rock)
   {
      Random rand = new Random();
      for (int yi = 0; yi < numRows; yi++)
      {
         for (int xi = 0; xi < numCols; xi++)
         {
            if (rand.nextInt(30) < 5)
            {
               setBackgroundCell(new Point(xi, yi), rock);
            }
         }
      }
      return ;
   }
   
   public EntityPosn getOccupant(Point pt)
   {
      return occupancy.getCell(pt);
   }
   
   public void addEntity(EntityPosn entity)
   {     
      Point pt = entity.getPosition();
      if (withinBounds(pt))
      {
         occupancy.setCell(pt, entity);
      }

      return;
   }
   
   public void moveEntity(EntityPosn entity, Point newPt)
   {
      if (withinBounds(newPt))
      {
         Point oldPt = entity.getPosition();
         occupancy.setCell(oldPt, null);
         occupancy.setCell(newPt, entity);
         entity.setPosition(newPt);
      }

      return;
   }
   
   public void removeEntity(EntityPosn entity)
   {
      Point entPt = entity.getPosition();
      
      if (withinBounds(entPt) && occupancy.getCell(entPt) != null)
      {
         entity.setPosition(new Point(-1, -1));
         occupancy.setCell(entPt, null);
      }

      return;
   }
   
   public ActionTimer scheduleAction(Action actor, int delay)
   {
      ActionTimer nextActor = new ActionTimer(actor, this);
      time.schedule(nextActor, delay);
      return nextActor;
   }
   
   public int getMinrTogl()
   {
      return minrTogl;
   }
   
   public int getWvrnTogl()
   {
      return wvrnTogl;
   }
   
   public void toggleMiner()
   {
      if (minrTogl == 0)
      {
         minrTogl = 1;
         System.out.println("miners switched to original pathing.");
      }
      else
      {
         minrTogl = 0;
         System.out.println("miners switched to A* pathing.");
      }

      return;
   }
   
   public void toggleWyvern()
   {
      if (wvrnTogl == 0)
      {
         wvrnTogl = 1;
         System.out.println("wyverns switched to original pathing.");
      }
      else
      {
         wvrnTogl = 0;
         System.out.println("wyverns switched to A* pathing.");
      }

      return;
   }
   
   public void causeOutbreak(HashMap<String, ArrayList<PImage>> iStore)
   {
      System.out.println("\nCDC WARNING: possible outbreak of\n" +
            "pneunaneurocytomorphicmacroscopicsilicrobialuenza.\n" +
            "extreme caution advised.\n");
      Outbreak vector = new Outbreak();
      vector.outbreakEvent(this, iStore);

      return;
   }
   
   public void containOutbreak(HashMap<String, ArrayList<PImage>> iStore)
   {
      System.out.println("\nCDC UPDATE: outbreak has been contained.\n");
      
      Containment radius = new Containment();
      radius.containmentEvent(this,  iStore);
      return;
   }

   
}
