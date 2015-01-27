/**
 * Interface for BasicListIterator
 *
 * @version Program 06
 */
public interface BasicListIterator<E> extends java.util.Iterator<E>
{
   /**
    * Returns true if the iterator has a previous element.
    */
   boolean hasPrevious();
   /**
    * Returns the previous element and moves the iterator 
    * backward one position with O(1) performance.
    */
   E previous();
}
