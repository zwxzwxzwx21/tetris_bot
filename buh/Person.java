package buh;
public class Person {
    private int age;
    
    public Person(int age) {
        this.age = age;
    }
    
    public int getAge() {
        return age;
    }
    
    public void yearPasses() {
        this.age++;
    }
    
    public String amIOld() {
        if (age <= 19) {
            return "dzieciak";
        } else {
            return "dorosły";
        }
    }
}