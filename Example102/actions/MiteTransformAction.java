package actions;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

import physics.Point;
import physics.WorldModel;
import processing.core.PImage;
import entities.*;

public class MiteTransformAction
   implements Action
{
   final static int GLOB_ANIM_MIN = 2;
   final static int GLOB_ANIM_MAX = 4;
   final static int GLOB_ANIM_SCALE = 50;
   final static int GLOB_RATE_SCALE = 4;
   
   private Mite mite;
   private HashMap<String, ArrayList<PImage>> iStore;
   
   public MiteTransformAction(Mite mite, HashMap<String, ArrayList<PImage>> iStore)
   {
      this.mite = mite;
      this.iStore = iStore;
   }
   
   public void entAction(WorldModel world)
   {
      GlowBlob glob = createGlob(world, mite.getPosition());
      scheduleGlob(world, glob);
      world.removeEntity(this.mite);
      world.addEntity(glob);
      return;
   }
   
   public GlowBlob createGlob(WorldModel world, Point pos)
   {
      Random rand = new Random();
      
      return new GlowBlob("glob", iStore.get("glob"), pos, mite.getRate() * GLOB_RATE_SCALE, (GLOB_ANIM_MAX - rand.nextInt(GLOB_ANIM_MIN)) * GLOB_ANIM_SCALE);      
   }
   
   public void scheduleGlob(WorldModel world, GlowBlob glob)
   {
      world.scheduleAction(new AnimationAction(glob, 0),
                           glob.getAnimationRate());
      world.scheduleAction(new GlowBlobAction(glob, iStore),
                           glob.getRate());
      return;
   }
}
