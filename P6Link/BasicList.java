/**
 * Interface for a basic list
 *
 * @version Program 06
 */
public interface BasicList<E>
{
   /**
    * Adds the specfied element to the logical end of the list.
    * @param element Generic element to be added.
    */
  public void add(E element);
   /**
    * Adds (inserts) the specfied element at the specfied index of the list
    *  - note that it does not overwrite any existing data at that location.
    *  @param index Numerical index to add the new element to the list.
    *  @param element Generic element to be added.
    */
   public void add(int index, E element);
   /**
    * Clears the list of its contents - the list should be in the same state
    * it is after being constructed with the default constructor.
    */ 
   public void clear();
   /**
    * Using the provided element's equals method, this method determines if 
    * the list contains the specified element or not.
    * @param element Search the list for the passed element.
    */ 
   public boolean contains(E element);
   /**
    * Returns a reference to the element at the specified index.
    * @param index Numerical index of element to return.
    */
   public E get(int index);
   /**
    * Using the provided element's equals method, this method returns the index
    * of the first element in the list that is equal to the provided element, if any.
    * @param element Element to find the index of.
    */
   public int indexOf(E element);
   /**
    * Removes (and returns) the specified element from the list.
    * @param index Numerical index value to remove from the list.
    */
   public E remove(int index);
   /**
    * Replaces the element at the specified index with the specified element.
    * @param index Numerical index to set the specified element at.
    * @param element Element to be added to the list.
    */
   public E set(int index, E element);
   /**
    * The logical size of the list (the number of elements that have been added 
    * and not removed).
    */
   public int size();
}
