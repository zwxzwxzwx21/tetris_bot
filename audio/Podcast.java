package audio;

public class Podcast extends FileAudio {
    private final String guest;

    public Podcast(String title, double duration, String guest) {
        super(title, duration);
        this.guest = guest;
    }

    public String getGuest() { return guest; }

    @Override
    public String toString() {
        return super.toString() + String.format(" [guest: %s]", guest);
    }

    @Override
    public void play() {
        requestStartPlayback();
        System.out.println("PLAYING PODCAST -> " + getTitle() + " with guest " + guest +
                " (duration: " + String.format("%.2f", getDuration()) + ")");
    }

    @Override
    public void stop() {
        if (isCurrentlyPlaying()) {
            System.out.println("STOP PODCAST -> " + getTitle() + " with guest " + guest);
            clearCurrent();
        }
    }
}