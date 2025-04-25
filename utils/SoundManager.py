import threading
import time
import queue
import stdaudio

import numpy as np

class SoundPlayer:
    def __init__(self):
        self.buffer = []  # Mixed samples go here
        self.lock = threading.Lock()
        self.sound_queue = queue.Queue()
        self.sound_history = {}

        self.last_play_time = {}
        self.cooldown = 0.5  # seconds between re-adding the same sound

        # Start audio playback and queue processing threads
        threading.Thread(target=self.play_audio, daemon=True).start()
        threading.Thread(target=self.process_queue, daemon=True).start()

    def play_audio(self):
        while True:
            time.sleep(0.01)
            with self.lock:
                if len(self.buffer) >= 1024:
                    chunk = self.buffer[:1024]
                    self.buffer = self.buffer[1024:]
                    stdaudio.playSamples(chunk)

    def process_queue(self):
        while True:
            filename = self.sound_queue.get()  # Waits until an item is available
            if filename in self.sound_history:
                samples = self.sound_history[filename]
            else:
                samples = stdaudio.read(filename.replace(".wav", ""))
                self.sound_history[filename] = samples

            self._mix_into_buffer(samples)

    def play_audio_background(self, filename):
        now = time.time()
        if filename in self.last_play_time and now - self.last_play_time[filename] < self.cooldown:
            return  # Skip if sound was just played
        self.last_play_time[filename] = now
        self.sound_queue.put(filename)

    def is_empty(self):
        return len(self.buffer) <= 1024

    def _mix_into_buffer(self, new_samples):
        with self.lock:
            new_len = len(new_samples)
            current_len = len(self.buffer)
            if current_len < new_len:
                self.buffer.extend([0.0] * (new_len - current_len))
            buffer_np = np.array(self.buffer[:new_len])
            new_np = np.array(new_samples)
            mixed = np.clip(buffer_np + new_np, -1.0, 1.0)
            self.buffer[:new_len] = mixed.tolist()

    def clear_buffer(self):
        with self.lock:
            self.buffer = []
