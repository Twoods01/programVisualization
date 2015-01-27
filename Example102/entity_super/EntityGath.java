package entity_super;

public interface EntityGath
   extends EntityRate
{
   public int getResourceLimit();
   public int getResourceCount();
   public void setResourceCount(int resourceCount);
}
