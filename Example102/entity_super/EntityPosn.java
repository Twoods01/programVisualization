package entity_super;
import physics.Point;

public interface EntityPosn
   extends Entity
{
   public Point getPosition();
   public void setPosition(Point position);
}
