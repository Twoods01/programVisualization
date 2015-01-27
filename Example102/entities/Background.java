package entities;
import java.util.ArrayList;

import entity_super.Entity;
import physics.*;
import processing.core.*;

public class Background
   implements Entity
{
   private String name;
   private ArrayList<PImage> imgs;
   private int currentImg;
   
   public Background(String name, ArrayList<PImage> imgs)
   {
      this.name = name;
      this.imgs = imgs;
      this.currentImg = 0;      
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
}
