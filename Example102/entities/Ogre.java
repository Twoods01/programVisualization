package entities;

import java.util.ArrayList;

import entity_super.EntityAnim;
import entity_super.EntityGath;
import entity_super.EntityRate;
import physics.Point;
import processing.core.PImage;

public interface Ogre
   extends EntityRate, EntityAnim, EntityGath
{   
   public String getName();
   
   public ArrayList<PImage> getImgs();
   
   public void setImgs(ArrayList<PImage> imgs);
   
   public PImage getImg();
   
   public void nextImg();
   
   public Point getPosition();
   
   public void setPosition(Point position);
   
   public int getRate();
   
   public int getAnimationRate();
   
   public int getResourceCount();
   
   public void setResourceCount(int resourceCount);
   
   public int getResourceLimit();
   
   public boolean getWasMiner();
}