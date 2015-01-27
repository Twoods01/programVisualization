package entity_super;
import java.util.ArrayList;
import processing.core.*;

public interface Entity
{   
   public String getName();
   
   public ArrayList<PImage> getImgs();
   
   public PImage getImg();
   
   public void nextImg();
}
