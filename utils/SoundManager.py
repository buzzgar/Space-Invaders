import threading
import time
import stdaudio

class SoundPlayer:
    def __init__(self):
        self.buffer = []  # Mixed samples go here
        self.lock = threading.Lock()

        # Start audio playback thread
        thread = threading.Thread(target=self.play_audio)
        thread.daemon = True
        thread.start()

        self.active_thread = False

        self.sound_history = {}

    def play_audio(self):
        while True:
            time.sleep(0.01)
            with self.lock:
                if len(self.buffer) >= 1024:
                    chunk = self.buffer[:1024]
                    self.buffer = self.buffer[1024:]
                    stdaudio.playSamples(chunk)

    def play_audio_background(self, filename):
        if self.sound_history.get(filename):
            samples = self.sound_history[filename]

            if len(samples) < 1024:
                samples = samples + [0] * (1100 - len(samples))

            threading.Thread(target=self._mix_into_buffer, args=(samples,), daemon=True).start()
            return

        samples = stdaudio.read(filename.replace(".wav", ""))
        self.sound_history[filename] = samples
        threading.Thread(target=self._mix_into_buffer, args=(samples,), daemon=True).start()

    def is_empty(self):
        return len(self.buffer) <= 1024

    def _mix_into_buffer(self, new_samples):
        with self.lock:
            # Extend buffer if needed
            for i in range(len(new_samples)):
                if i >= len(self.buffer):
                    self.buffer.append(new_samples[i])
                else:
                    mixed = self.buffer[i] + new_samples[i]
                    # Clamp to [-1.0, 1.0]
                    self.buffer[i] = max(-1.0, min(1.0, mixed))

    def clear_buffer(self):
        self.buffer = []
