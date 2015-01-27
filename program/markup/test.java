
import java.lang.Thread;
class test {
    public static void main(String[] args) {
System.out.println("push main test " + Thread.currentThread().getId());
        String numString = recursiveString(5);
        System.out.println(numString);
        int num = addNumbersInString(numString);
        System.out.println(num);
        nothing();
System.out.println("pop main test " + Thread.currentThread().getId());
    }

    public static String recursiveString(int num){
System.out.println("push recursiveString test " + Thread.currentThread().getId());
        if(num == 0){
            int whoCares = 1;
String __TEMP_VAR__ = ((Integer)num).toString();
System.out.println("pop recursiveString test " + Thread.currentThread().getId());
return __TEMP_VAR__;
        }
        else{
String __TEMP_VAR__ = ((Integer)num).toString() + recursiveString(decrementNumber(num));
System.out.println("pop recursiveString test " + Thread.currentThread().getId());
return __TEMP_VAR__;
        }
    }

    public static int decrementNumber(int num){
System.out.println("push decrementNumber test " + Thread.currentThread().getId());
int __TEMP_VAR__ = num - 1;
System.out.println("pop decrementNumber test " + Thread.currentThread().getId());
return __TEMP_VAR__;
    }

    public static int addNumbers(int num1, int num2){
System.out.println("push addNumbers test " + Thread.currentThread().getId());
int __TEMP_VAR__ = num1 + num2;
System.out.println("pop addNumbers test " + Thread.currentThread().getId());
return __TEMP_VAR__;
    }

    public static int addNumbersInString(String s){
System.out.println("push addNumbersInString test " + Thread.currentThread().getId());
        int sum = 0;
        nothing();
        for(int i = 0; i < s.length(); i++){
            sum = addNumbers(sum, Character.getNumericValue(s.charAt(i)));
        }
int __TEMP_VAR__ = sum;
System.out.println("pop addNumbersInString test " + Thread.currentThread().getId());
return __TEMP_VAR__;
    }

    public static void nothing(){
System.out.println("push nothing test " + Thread.currentThread().getId());
        int i = 5;
        while(i > 0){
            i = decrementNumber(i);
        }
System.out.println("pop nothing test " + Thread.currentThread().getId());
        return;
    }
}