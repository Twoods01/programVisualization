public class LinkedListTest
{
   public static void main(String[] args)
   {
      System.out.println("Testing Linked List");
      try
      {
         BasicLinkedList myLinkedList = new BasicLinkedList<String>();
      }
      catch(Exception e)
      {
         System.out.println("Exception in construction");
         System.out.println(e);
      }
      BasicLinkedList myLinkedList = new BasicLinkedList<String>();
      myLinkedList.add("First Index");
      myLinkedList.add("Second Object");
      myLinkedList.add("thired String");
      myLinkedList.add("Fourth asdf");
      myLinkedList.add("Fifth thing..");
      myLinkedList.add("Sixth object");
         
      System.out.println("Size: " + myLinkedList.size());
      System.out.println("LIST CONTENTS: ");
      for(int i = 0; i < myLinkedList.size(); i++)
      {
         System.out.println(myLinkedList.get(i));
      }
      
      myLinkedList.add(0, "Real First Index");

   }
}
