import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;

import processing.core.*;
import physics.*;
import entities.*;
import entity_super.Entity;

public class ProcessingSketch
   extends PApplet
{      
   final static int SCREEN_WIDTH  = 640;
   final static int SCREEN_HEIGHT = 480;
   
   final static int CELLSIZE = 32;
   
   final static int WORLD_SCALE = 2;
   
   final static int W_VIEWGRID = 20;
   final static int H_VIEWGRID = 15;
   
   private int xView;
   private int yView;
   
   private HashMap<String, ArrayList<PImage>> iStore;
   
   private int numCols;
   private int numRows;
   private WorldModel world;
   
   private RandomInit randCreate;
   
   private boolean msgBool;
   
   public ProcessingSketch()
   {
      iStore = new HashMap<String, ArrayList<PImage>>();
      
      xView = 0;
      yView = 0;
      
      numCols = SCREEN_WIDTH / CELLSIZE * WORLD_SCALE;
      numRows = SCREEN_HEIGHT / CELLSIZE * WORLD_SCALE;
      
      msgBool = true;
   }
   
   public void openMessage()
   {
      textSize(20);
      textAlign(CENTER, TOP);
      text("navigation is 'wasd' keys.\n\n" +
           "'e' causes world event.\n" +
           "'c' toggles the miners' pathing.\n" +
           "'v' toggles the wyverns'.\n\n" +
           "press 'p' to begin! :)",
           SCREEN_WIDTH/2, SCREEN_HEIGHT/4);
   }
   
   public void setup()
   {
      size(SCREEN_WIDTH, SCREEN_HEIGHT);
      background(100, 128, 230);
      
      randCreate = new RandomInit();

      makeImageMap(iStore);
      
      world = new WorldModel(numCols, numRows, iStore.get("grass"));

      randCreate.createRandomWorld(world, iStore);
      
      openMessage(); 
      
   }

   public void draw()
   {      
      if (!msgBool)
      {
         for (int yi = 0; yi < SCREEN_HEIGHT / CELLSIZE; yi++)
         {
            for (int xi = 0; xi < SCREEN_WIDTH / CELLSIZE; xi++)
            {
               Point pt = new Point(xView + xi, yView + yi);
               
               Entity bg = world.getBackgroundCell(pt);
               image(bg.getImg(), xi * CELLSIZE, yi * CELLSIZE);
               
               if (world.getOccupant(pt) != null)
               {
                  Entity occupant = world.getOccupant(pt);
                  image(occupant.getImg(), xi * CELLSIZE, yi * CELLSIZE);
               }         
            }
         }
      }
   }

   public static void main(String args[])
   {
      PApplet.main(new String[] {"ProcessingSketch" });
   }   
   
   public void keyPressed()
   {
      if (key == 'p')
      {
         background(0);
         msgBool = false;
      }
      if (key == 'w')
      {
         Point temPt = new Point(xView, yView - 1);
         if(world.withinBounds(temPt))
         {
            yView--;
         }
      }
      if (key == 'a')
      {
         Point temPt = new Point(xView - 1, yView);
         if(world.withinBounds(temPt))
         {
            xView--;
         }
      }
      if (key == 's')
      {
         Point temPt = new Point(xView + H_VIEWGRID-1, yView + H_VIEWGRID);
         if(world.withinBounds(temPt))
         {
            yView++;
         }
      }
      if (key == 'd')
      {
         Point temPt = new Point(xView + W_VIEWGRID, yView + H_VIEWGRID-1);
         if(world.withinBounds(temPt))
         {
            xView++;
         }
      }
      if (key == 'c')
      {
         world.toggleMiner();
      }
      if (key == 'v')
      {
         world.toggleWyvern();
      }
      if (key == 'e')
      {
         world.causeOutbreak(iStore);
      }

      if (key == 'f')
      {
         world.containOutbreak(iStore);
      }

   }
   
   public void makeImageMap(HashMap<String, ArrayList<PImage>> iStore)
   {
      ArrayList<PImage> none = new ArrayList<PImage>();
      none.add(loadImage("images/none.bmp"));
      
      iStore.put("none", none);
      
      ArrayList<PImage> bkgd = new ArrayList<PImage>();
      bkgd.add(loadImage("images/grass.bmp"));
      
      iStore.put("grass", bkgd);
      
      ArrayList<PImage> rock = new ArrayList<PImage>();
      rock.add(loadImage("images/rock.bmp"));
      
      iStore.put("rock",  rock);
      
      ArrayList<PImage> obsc = new ArrayList<PImage>();
      obsc.add(loadImage("images/obstacle.bmp"));
      
      iStore.put("obstacle", obsc);
      
      ArrayList<PImage> blsm = new ArrayList<PImage>();
      blsm.add(loadImage("images/blacksmith.bmp"));
      
      iStore.put("blacksmith",  blsm);
      
      ArrayList<PImage> minr = new ArrayList<PImage>();
      for (int i = 1; i < 6; i++)
      {
         minr.add(loadImage(new String("images/miner" + i + ".png")));
      }
      
      iStore.put("miner", minr);
      
      ArrayList<PImage> ores = new ArrayList<PImage>();
      ores.add(loadImage("images/ore.png"));
      
      iStore.put("ore", ores);
      
      ArrayList<PImage> blob = new ArrayList<PImage>();
      for (int i = 1; i < 13; i++)
      {
         blob.add(loadImage(new String("images/blob" + i + ".png")));
      }
      
      iStore.put("blob", blob);
      
      ArrayList<PImage> frze = new ArrayList<PImage>();
      for (int i = 1; i < 5; i++)
      {
         frze.add(loadImage(new String("images/freeze" + i + ".png")));
      }

      iStore.put("freeze",  frze);
      
      ArrayList<PImage> vein = new ArrayList<PImage>();
      vein.add(loadImage("images/vein.bmp"));
      
      iStore.put("vein",  vein);
      
      ArrayList<PImage> quke = new ArrayList<PImage>();
      for (int i = 1; i < 7; i++)
      {
         quke.add(loadImage(new String("images/quake" + i + ".png")));
      }
      
      iStore.put("quake", quke);
      
      ArrayList<PImage> wvrn = new ArrayList<PImage>();
      for (int i = 1; i < 9; i++)
      {
         wvrn.add(loadImage(new String("images/wyvern" + i + ".png")));
      }
      
      iStore.put("wyvern", wvrn);
      
      ArrayList<PImage> dirt = new ArrayList<PImage>();
      dirt.add(loadImage(new String("images/dirt.png")));
      
      iStore.put("dirt", dirt);
      
      ArrayList<PImage> skvn = new ArrayList<PImage>();
      skvn.add(loadImage(new String("images/sick_vein.png")));
      
      iStore.put("sick vein", skvn);
      
      ArrayList<PImage> mite = new ArrayList<PImage>();
      for (int i = 1; i < 5; i++)
      {
         mite.add(loadImage(new String("images/mite" + i + ".png")));
      }
      
      iStore.put("mite", mite);
      
      ArrayList<PImage> ogre = new ArrayList<PImage>();
      for (int i = 1; i < 6; i++)
      {
         ogre.add(loadImage(new String("images/ogre" + i + ".png")));
      }
      
      iStore.put("ogre", ogre);
      
      ArrayList<PImage> skob = new ArrayList<PImage>();
      skob.add(loadImage(new String("images/sick_obstacle.png")));
      
      iStore.put("sick obstacle", skob);
      
      ArrayList<PImage> glob = new ArrayList<PImage>();
      for (int i = 1; i < 13; i++)
      {
         glob.add(loadImage(new String("images/sick_blob" + i + ".png")));
      }
      
      iStore.put("glob", glob);
   }
}
