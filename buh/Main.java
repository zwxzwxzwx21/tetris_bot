package buh;
import java.time.LocalDate;

public class Main {
    public static void main(String[] args) {
        
        
        System.out.println("===== ZADANIE 1: Student =====");
        Student student1 = new Student(); 
        student1.setName("Jan Kowalski");
        student1.setAge(20);
        student1.setHeight(175.5);
        
        Student student2 = new Student(22, "Anna Nowak", 165.0); 
        
        System.out.println("Student 1: " + student1.getName() + ", wiek: " + student1.getAge() + ", wzrost: " + student1.getHeight());
        System.out.println("Student 2: " + student2.getName() + ", wiek: " + student2.getAge() + ", wzrost: " + student2.getHeight());
        
        System.out.println("\n===== ZADANIE 2: Person =====");
        Person person = new Person(18);
        System.out.println("Startowy wiek: " + person.getAge());
        person.yearPasses();
        System.out.println("Po yearPasses(): wiek = " + person.getAge() + ", status: " + person.amIOld());
        person.yearPasses();
        System.out.println("Po yearPasses(): wiek = " + person.getAge() + ", status: " + person.amIOld());
        
        System.out.println("\n===== ZADANIE 3: StringUtils (anagramy) =====");
        StringUtils utils = new StringUtils();
        System.out.println("'listen' i 'silent': " + utils.isAnagram("listen", "silent"));
        System.out.println("'hello' i 'world': " + utils.isAnagram("hello", "world"));
        System.out.println("'anagram' i 'nagaram': " + utils.isAnagram("anagram", "nagaram"));
        
        System.out.println("\n===== ZADANIE 4 & 5: Employee =====");
        Employee[] employees = new Employee[3];
        employees[0] = new Employee("Jan Kowalski", 5000.0, LocalDate.of(2020, 1, 15),
                new HomeAddress("Główna 1", "Warszawa", "00-001"));
        employees[1] = new Employee("Anna Nowak", 6000.0, LocalDate.of(2019, 5, 20),
                new HomeAddress("Polna 5", "Kraków", "30-001"));
        employees[2] = new Employee("Piotr Wiśniewski", LocalDate.of(2021, 3, 10),
                new HomeAddress("Leśna 10", "Gdańsk", "80-001")); 
        
        System.out.println("Przed podwyżką:");
        for (Employee emp : employees) {
            System.out.println(emp.getInfo());
        }
        
        System.out.println("\nPo podwyżce 10%:");
        for (Employee emp : employees) {
            emp.raiseSalary(10.0);
            System.out.println(emp.getInfo());
        }
        
        System.out.println("\n===== ZADANIE 6: Bankomat =====");
        ATMService atm = new ATMService();
    
        System.out.println("--- Wpłata ---");
        atm.deposit(50, 10);
        atm.deposit(100, 5);
        atm.deposit(200, 3);
        atm.deposit(10, 20);
        atm.showStatus();
        
        System.out.println("--- Wypłata 350 zł ---");
        atm.withdraw(350);
        atm.showStatus();
        
        System.out.println("--- Wypłata 5000 zł (za dużo) ---");
        atm.withdraw(5000);
        atm.showStatus();
        
        System.out.println("--- Wypłata 470 zł ---");
        atm.withdraw(470);
        atm.showStatus();
    }
}