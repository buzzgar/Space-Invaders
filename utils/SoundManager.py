import threading

import stdaudio


def play_audio_background(filename):
    thread = threading.Thread(target=stdaudio.playFile, args=(filename,))
    thread.daemon = True  # Ensures the thread stops when the main program exits
    thread.start()