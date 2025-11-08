package buh;
public class Student {
    private int age;
    private String name;
    private double height;
    
    public Student() {
    }
    
    public Student(int age, String name, double height) {
        this.age = age;
        this.name = name;
        this.height = height;
    }
    
    public int getAge() {
        return age;
    }
    
    public void setAge(int age) {
        this.age = age;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public double getHeight() {
        return height;
    }
    
    public void setHeight(double height) {
        this.height = height;
    }
}