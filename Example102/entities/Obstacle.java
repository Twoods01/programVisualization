package entities;
import java.util.ArrayList;

import entity_super.EntityPosn;
import physics.Point;
import processing.core.*;

public class Obstacle
   implements EntityPosn
{
   private String name;
   private ArrayList<PImage> imgs;
   private int currentImg;
   private Point position;
   
   public Obstacle(String name, ArrayList<PImage> imgs, Point position)
   {
      this.name = name;
      this.imgs = imgs;
      this.currentImg = 0;
      this.position = position;
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
}
