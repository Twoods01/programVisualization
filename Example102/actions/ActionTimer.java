package actions;

import physics.*;
import java.util.TimerTask;

public class ActionTimer
   extends TimerTask
{
   private Action actor;
   private WorldModel world;
   
   public ActionTimer(Action actor, WorldModel world)
   {
      this.actor = actor;
      this.world = world;
   }
   
   public Action getActor()
   {
      return actor;
   }
   
   public void run()
   {
      actor.entAction(world);
      return;
   }
}
