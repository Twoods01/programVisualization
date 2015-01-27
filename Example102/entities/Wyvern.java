package entities;
import java.util.ArrayList;

import entity_super.EntityAnim;
import entity_super.EntityPosn;
import entity_super.EntityRate;
import physics.Point;
import processing.core.*;

public class Wyvern
    implements EntityPosn, EntityRate, EntityAnim
{
   private String name;
   private ArrayList<PImage> imgs;
   private int currentImg;
   private Point position;
   private int rate;
   private int animationRate;
   
   private boolean infected;
   
   public Wyvern(String name, ArrayList<PImage> imgs, Point position,
                 int rate, int animationRate)
   {
      this.name = name;
      this.imgs = imgs;
      this.currentImg = 0;
      this.position = position;
      this.rate = rate;
      this.animationRate = animationRate;
      
      this.infected = false;
   }
   
   public String getName()
   {
      return name;
   }
   
   public ArrayList<PImage> getImgs()
   {
      return imgs;
   }
   
   public void setImgs(ArrayList<PImage> imgs)
   {
      this.imgs = imgs;
      this.currentImg = 0;
      return; 
   }
   
   public PImage getImg()
   {
      return imgs.get(currentImg);
   }
   
   public void nextImg()
   {
      currentImg = (currentImg + 1) % imgs.size();
      return; 
   }
   
   public Point getPosition()
   {
      return position;
   }
   
   public void setPosition(Point position)
   {
      this.position = position;
      return; 
   }
   
   public int getRate()
   {
      return rate;
   }
   
   public int getAnimationRate()
   {
      return animationRate;
   }

   public void setInfected(boolean infected)
   {
      this.infected = infected;
      return; 
   }
   
   public boolean getInfected()
   {
      return infected;
   }
}