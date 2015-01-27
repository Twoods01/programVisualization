package entities;

import java.util.ArrayList;

import physics.Point;
import processing.core.PImage;

public class OgreFull
   implements Ogre
{
  private String name;
  private ArrayList<PImage> imgs;
  private int currentImg;
  private Point position;
  private int rate;
  private int animationRate;
  private int resourceCount;
  private int resourceLimit;
  
  private boolean wasMiner;
  
  public OgreFull(String name, ArrayList<PImage> imgs, Point position,
        int rate, int animationRate, int resourceLimit, boolean wasMiner)
  {
     this.name = name;
     this.imgs = imgs;
     this.currentImg = 0;
     this.position = position;
     this.rate = rate;
     this.animationRate = animationRate;      
     this.resourceLimit = resourceLimit;
     this.resourceCount = resourceLimit;
     
     this.wasMiner = wasMiner;
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
  
  public int getResourceCount()
  {
     return resourceCount;
  }
  
  public void setResourceCount(int resourceCount)
  {
     this.resourceCount = resourceCount;
     return; 
  }
  
  public int getResourceLimit()
  {
     return resourceLimit;
  }

  public boolean getWasMiner()
  {
     return wasMiner;
  }
  
}
