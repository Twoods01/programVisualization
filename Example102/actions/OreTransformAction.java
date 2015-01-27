package actions;

import java.util.HashMap;
import java.util.ArrayList;

import processing.core.*;

import java.util.Random;

import entities.*;
import physics.*;

public class OreTransformAction
   implements Action
{
   final static int BLOB_ANIM_MIN = 2;
   final static int BLOB_ANIM_MAX = 4;
   final static int BLOB_ANIM_SCALE = 50;
   
   final static int BLOB_RATE_SCALE = 4;
   
   private Ore ore;
   private HashMap<String, ArrayList<PImage>> iStore;
   
   public OreTransformAction(Ore ore, HashMap<String, ArrayList<PImage>> iStore)
   {
      this.ore = ore;
      this.iStore = iStore;
   }
   
   public void entAction(WorldModel world)
   {
      OreBlob blob = createBlob(world, ore.getPosition());
      scheduleBlob(world, blob);
      world.removeEntity(this.ore);
      world.addEntity(blob);
      return; 
   }
   
   public OreBlob createBlob(WorldModel world, Point pos)
   {
      Random rand = new Random();
      
      return new OreBlob("blob", iStore.get("blob"), pos,ore.getRate() * BLOB_RATE_SCALE,(BLOB_ANIM_MAX - rand.nextInt(BLOB_ANIM_MIN)) * BLOB_ANIM_SCALE);         
   }
   
   public void scheduleBlob(WorldModel world, OreBlob blob)
   {
      world.scheduleAction(new AnimationAction(blob, 0),
            blob.getAnimationRate());
      world.scheduleAction(new OreBlobAction(blob, iStore),
            blob.getRate());
      return; 
   }
}
