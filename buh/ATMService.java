package buh;
import java.util.HashMap;
import java.util.Map;

public class ATMService {
    private Map<Integer, Integer> banknotes;
    
    public ATMService() {
        banknotes = new HashMap<>();
        banknotes.put(10, 0);
        banknotes.put(20, 0);
        banknotes.put(50, 0);
        banknotes.put(100, 0);
        banknotes.put(200, 0);
        banknotes.put(500, 0);
    }
    
    public void deposit(int denomination, int count) {
        if (banknotes.containsKey(denomination)) {
            banknotes.put(denomination, banknotes.get(denomination) + count);
            System.out.println("Wpłacono " + count + " banknotów po " + denomination + " zł");
        } else {
            System.out.println("Nieprawidłowy nominał: " + denomination);
        }
    }
    
    public int withdraw(int amount) {
        Map<Integer, Integer> toWithdraw = new HashMap<>();
        int remaining = amount;
        
        int[] denominations = {500, 200, 100, 50, 20, 10};
        
        for (int denom : denominations) {
            int available = banknotes.get(denom);
            int needed = remaining / denom;
            int toTake = Math.min(needed, available);
            
            if (toTake > 0) {
                toWithdraw.put(denom, toTake);
                remaining -= toTake * denom;
            }
        }
        
        if (remaining > 0) {
            System.out.println("Brak pieniędzy. Pozostało: " + remaining + " zł");
            return 0;
        }
        
        for (Map.Entry<Integer, Integer> entry : toWithdraw.entrySet()) {
            banknotes.put(entry.getKey(), banknotes.get(entry.getKey()) - entry.getValue());
        }
        
        System.out.println("Wypłacono: " + amount + " zł");
        System.out.println("Wydane banknoty:");
        for (Map.Entry<Integer, Integer> entry : toWithdraw.entrySet()) {
            System.out.println("  " + entry.getKey() + " zł x " + entry.getValue());
        }
        return amount;
    }
    
    public void showStatus() {
        System.out.println("\n=== Stan bankomatu ===");
        int total = 0;
        for (Map.Entry<Integer, Integer> entry : banknotes.entrySet()) {
            int value = entry.getKey() * entry.getValue();
            total += value;
            System.out.println(entry.getKey() + " zł: " + entry.getValue() + " banknotów (wartość: " + value + " zł)");
        }
        System.out.println("Łączna wartość: " + total + " zł");
        System.out.println("======================\n");
    }
}