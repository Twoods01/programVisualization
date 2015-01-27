package physics;

import entities.*;
import entity_super.EntityPosn;

import java.util.ArrayList;

import processing.core.*;

public class OccuGrid
{   
   private int width;
   private int height;
   private EntityPosn [][] cells;
     
   public OccuGrid(int width, int height)
   {
      this.width = width;
      this.height = height;
      this.cells = new EntityPosn [height][width];
   }
   
   public void setCell(Point pt, EntityPosn value)
   {
      cells[pt.yCoord()][pt.xCoord()] = value;
      return;
   }
   
   public EntityPosn getCell(Point pt) 
   {
      return cells[pt.yCoord()][pt.xCoord()];
   }
}
