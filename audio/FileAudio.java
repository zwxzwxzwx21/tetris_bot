package audio;
import java.util.ArrayList;
import java.util.List;

public abstract class FileAudio {
    private final String title;
    private final double duration;
    private static final List<FileAudio> registry = new ArrayList<>();
    private static FileAudio currentlyPlaying = null;

    protected FileAudio(String title, double duration) {
        this.title = title;
        this.duration = duration;
        registry.add(this);
    }

    public String getTitle() { return title; }
    public double getDuration() { return duration; }

    public static FileAudio findByTitle(String title) {
        for (FileAudio f : registry) {
            if (f.getTitle().equalsIgnoreCase(title)) return f;
        }
        return null;
    }

    protected final void requestStartPlayback() {
        if (currentlyPlaying != null && currentlyPlaying != this) {
            currentlyPlaying.stop();
        }
        currentlyPlaying = this;
    }

    protected static final void clearCurrent() { currentlyPlaying = null; }
    protected final boolean isCurrentlyPlaying() { return currentlyPlaying == this; }
    public static boolean isAnythingPlaying() { return currentlyPlaying != null; }

    public static void stopCurrent() {
        if (currentlyPlaying != null) currentlyPlaying.stop();
    }

    @Override
    public String toString() {
        return String.format("%s (duration: %.2f)", title, duration);
    }

    public abstract void play();
    public abstract void stop();
}