package buh;    
import java.time.LocalDate;

public class Employee {
    private String name;
    private Double salary;
    private LocalDate hireDate;
    private HomeAddress homeAddress;
    
    public Employee(String name, Double salary, LocalDate hireDate, HomeAddress homeAddress) {
        this.name = name;
        this.salary = salary;
        this.hireDate = hireDate;
        this.homeAddress = homeAddress;
    }
    
    public Employee(String name, LocalDate hireDate, HomeAddress homeAddress) {
        this.name = name;
        this.salary = 3000.0;
        this.hireDate = hireDate;
        this.homeAddress = homeAddress;
    }
    
    public String getInfo() {
        return "Pracownik: " + name + 
               ", Wypłata: " + String.format("%.2f", salary) + " zł" +
               ", Data zatrudnienia: " + hireDate + 
               ", Adres: " + homeAddress;
    }
    
    public void setNewAddress(HomeAddress newAddress) {
        this.homeAddress = newAddress;
    }
    
    public void raiseSalary(Double byPercent) {
        this.salary = this.salary * (1 + byPercent / 100.0);
    }
}