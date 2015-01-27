/**
 * Class for a basic linked list.
 *
 * @version Program 06
 */
public class BasicLinkedList<E> implements BasicList<E>, java.lang.Iterable<E>
{
   
   private int size;	               //Size of Linked List
   private Node head, place;        //head = start of linked list. 
                                    //place = marker for iterator
	//Node Class
   private class Node
	{
		public E data;
		public Node next, prev;
	}
   
   //Default Constructor for BasicLinkedList - 
   //Not Strictly Nessicary, but nice for looks.
   public BasicLinkedList()
   {
   }

   /**
    * Adds the element passed into the END of the list with O(1) preforamance.
    * @param element Generic element to be added to the list.
    */
   public void add(E element)
   {
		Node n = new Node();
      n.data = element;
      if(head == null | size == 0)
      {
         head = n;
         head.next = n;
         head.prev = n;
      }
      else
      {
         n.next = head;
         n.prev = head.prev; //Add to previous tail..
         head.prev.next = n;
         head.prev = n;
      } 
      size++;
      return;
   }
   /**
    * Adds (inserts) the specified element at the specified index of the list -
    * note that it does not otherwise add any existing data at the location.
    * @param index - The index to add(insert) the specified element.
    * @param element - The element to add (insert) to the specified position.
    */
   public void add(int index, E element)
   {
		Node n = new Node();
		n.data = element;
		if(index > size | index < 0)
		{
			throw new java.lang.IndexOutOfBoundsException();
		}
      if(head == null | size == 0)
      {
         head = n;
         head.next = n;
         head.prev = n;
      }
      else if(index == 0)
      {
         n.prev = head.prev;
         n.next = head.next;
         n.next.prev = n;
         n.prev.next = n;
         head = n;
      }  
      else
      {
			Node scan = head;
         for(int i = 0; i < index; i++)
			{
				scan = scan.next;
			}
         n.next = scan;
         n.prev = scan.prev;
         scan.prev.next = n;
         scan.prev = n;
      }
      size++;
      return;
   }
   /**
    * Returns a refrence to a unique instance of a private inner class
    * implementing the BasicListInterator interface.
    *
    */
   public BasicListIterator<E> basicListIterator() 
   {
      ListIterator<E> listIterator = new ListIterator<E>();
      place = head;
      return listIterator;  
   }
   /**
    * Helper class to use the Iterator
    */
   private class ListIterator<E> implements BasicListIterator<E>
   {
      private int index;
      public ListIterator()
      {
         index = 0;
      }
      public boolean hasPrevious()
      {
         return (index > 0);
      }
      public E previous()
      {
         index--;
         if(index < 0)
         {
            throw new java.util.NoSuchElementException();
         }
         place = place.prev;
         return ((E)place.data);
      }
      public boolean hasNext()
      {
         return (index < size);
      }
      public E next()
      {
         if(index == size)
         {
            throw new java.util.NoSuchElementException();
         }
         place = place.next;
         index++;
         return ((E)place.prev.data);
      }
      public void remove()
      {
         throw new java.lang.UnsupportedOperationException();
      }
      
   }
   /**
    * Returns the number of elements in the list with O(1) preformance.
    */
   public void clear()
   {
      head = null;
      size = 0;	
   }
   /**
    * Using the provided element's equals method, this method determines
    * if the list contains the specified element or not.
    * @param element - The element to search for in the list
    */
   public boolean contains(E element)
   {
      Node scan = head;
      for(int i = 0; i < size; i++)
      {
         if(element == null)
         {
            if(scan.data == null)
            {
               return true;
            }   
         }
         else if(scan.data.equals(element))
         {
            return true;
         }
         scan = scan.next;
      }
      return false;   
   }
   /**
    * Returns a refrence to the element at the specified index.
    * @param index - The index of the element you want to get.
    */
   public E get(int index)
   {
      if(size == 0 | index >= size)
      {
         throw new IndexOutOfBoundsException();
      }
      Node scan = head;
      for(int i = 0; i < index; i++)
      {
         scan = scan.next;
      } 
      return scan.data;
   }
   /**
    * Using the provided element's equals method, this method returns
    * the index of the first element in the list that is equal to the 
    * provided element,if any.
    * @param - The element to search for.
    */
   public int indexOf(E element)
   {
      Node scan = head;
      for(int i = 0; i < size; i++)
      {
         if(element == null)
         {
            if(scan.data == null)
            {
               return i;
            }   
         }
         else if(element.equals(scan.data))
         {
            return (i);  
         }
         scan = scan.next;
      } 
      throw new java.util.NoSuchElementException();  
   }
   /**
    * Returns an iterator over the list of elements of type E.
    */
   public java.util.Iterator<E> iterator()
   {
      return null; 
   }
   public E remove(int index)
   {
      if(size == 0 | index >= size | index < 0)
      {
         throw new IndexOutOfBoundsException();
      }
      Node scan = head;
      for(int i = 0; i < index; i++)
      {
         scan = scan.next;
      }

      scan.prev.next = scan.next; //Assign the previous' node's "next" to the next node.
      scan.next.prev = scan.prev; //Assign the next nodes "prev" to the previous node.
      size--;
      //Special case where head needs to move.
      if(index == 0)
      {
         head = scan.next;
      }
      return scan.data;
   }
   /**
    * Replaces the element at the specified index with the specified element.
    * @param index - The index of the element whose value you want to set (change).
    * @param element - The element you wish to set at the specified index.
    */
   public E set(int index, E element)
   {
      Node scan = head;
      if(index < 0 | index >= size)
      {
         throw new java.lang.IndexOutOfBoundsException();
      }   
      for(int i = 0; i < index; i++)
      {
         scan = scan.next;
      }
      E data = scan.data;
      scan.data = element;
      return data;
   }
   /**
    * Size of the linked list. 
    */
   public int size()
   {
      return size; 
   }
}
