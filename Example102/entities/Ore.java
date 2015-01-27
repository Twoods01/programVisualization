package entities;
import java.util.ArrayList;

import entity_super.EntityPosn;
import entity_super.EntityRate;
import physics.Point;
import processing.core.*;

public class Ore
   implements EntityPosn, EntityRate
{
   private String name;
   private ArrayList<PImage> imgs;
   private int currentImg;
   private Point position;
   private int rate;
   
   public Ore(String name, ArrayList<PImage> imgs, Point position,
              int rate)
   {
      this.name = name;
      this.imgs = imgs;
      this.currentImg = 0;
      this.position = position;
      this.rate = rate;
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
}
