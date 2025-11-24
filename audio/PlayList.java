package audio;
import java.util.ArrayList;
import java.util.List;

public class PlayList {
    private final List<FileAudio> items = new ArrayList<>();

    public void addElement(FileAudio audio) {
        if (audio != null) items.add(audio);
    }

    public boolean removeElement(FileAudio audio) {
        return items.remove(audio);
    }

    public FileAudio findByTitle(String title) {
        for (FileAudio f : items) {
            if (f.getTitle().equalsIgnoreCase(title)) return f;
        }
        return null;
    }

    public boolean playByTitle(String title) {
        FileAudio f = findByTitle(title);
        if (f == null) return false;
        f.play();
        return true;
    }

    public boolean stopByTitle(String title) {
        FileAudio f = findByTitle(title);
        if (f == null) return false;
        f.stop();
        return true;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("PlayList:\n");
        for (int i = 0; i < items.size(); i++) {
            sb.append("  ").append(i + 1).append(". ").append(items.get(i)).append("\n");
        }
        return sb.toString();
    }
}