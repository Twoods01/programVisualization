package entities;
import java.util.ArrayList;

import entity_super.EntityGath;
import entity_super.EntityGenr;
import entity_super.EntityPosn;
import entity_super.EntityRate;
import physics.Point;
import processing.core.*;

public class Blacksmith
   implements EntityPosn, EntityRate, EntityGath, EntityGenr
{
   private String name;
   private ArrayList<PImage> imgs;
   private int currentImg;
   private Point position;
   private int rate;
   
   private int resourceDistance;
   private int resourceLimit;
   private int resourceCount;
   
   public Blacksmith(String name, ArrayList<PImage> imgs, Point position,
         int rate, int resourceLimit)
   {
      this.name = name;
      this.imgs = imgs;
      this.currentImg = 0;
      this.position = position;
      this.rate = rate;
      
      this.resourceDistance = 1;
      this.resourceCount = 0;
   }
   
   public String getName()
   {
      return name;
   }
   
   public ArrayList<PImage> getImgs()
   {
      return imgs;
   }
   
   public PImage getImg()
   {
      return imgs.get(currentImg);
   }
   
   public void nextImg()
   {
      currentImg = (currentImg + 1) % imgs.size();
   }
   
   public Point getPosition()
   {
      return position;
   }
   
   public void setPosition(Point position)
   {
      this.position = position;
   }
   
   public int getRate()
   {
      return rate;
   }
   
   public int getResourceCount()
   {
      return resourceCount;
   }
   
   public void setResourceCount(int resourceCount)
   {
      this.resourceCount = resourceCount;
   }
   
   public int getResourceLimit()
   {
      return resourceLimit;
   }
   
   public int getResourceDistance()
   {
      return resourceDistance;
   }
}
