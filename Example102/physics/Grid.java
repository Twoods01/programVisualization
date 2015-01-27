package physics;

import entities.*;
import entity_super.Entity;

import java.util.ArrayList;

import processing.core.*;

public class Grid
{   
   private int width;
   private int height;
   private Entity [][] cells;
   
   public Grid(int width, int height, ArrayList<PImage> autoLawn)
   {
      this.width = width;
      this.height = height;
      this.cells = new Entity [height][width];

       for (int yi = 0; yi < height; yi++)
       {
         for (int xi = 0; xi < width; xi++)
         {
            this.cells[yi][xi] = new Background("auto lawn", autoLawn);
         }
       }
   }
   
   public void setCell(Point pt, Entity value)
   {
      cells[pt.yCoord()][pt.xCoord()] = value;
      return;
   }
   
   public Entity getCell(Point pt) 
   {
      return cells[pt.yCoord()][pt.xCoord()];
   }
}
