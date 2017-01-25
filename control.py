"""
Threadsafe recording control
"""

import threading

class Control(object):
    def __init__(self):
        self.control_lock = threading.Lock()
        self._running = True
        self._recording = False
        self._secs_to_delay = 0
        self._secs_to_record = 0
        self._secs_per_pic = 0
        self._prefix = ''

    def running(self):
        with self.control_lock:
            return self._running

    def stop(self):
        with self.control_lock:
            self._running = False
            self._recording = False

    def recording(self):
        with self.control_lock:
            return self._recording

    def stop_recording(self):
        with self.control_lock:
            self._recording = False

    def record(self, secs_to_delay, secs_to_record, secs_per_pic, path_prefix):
        with self.control_lock:
            self._secs_to_delay = secs_to_delay
            self._secs_to_record = secs_to_record
            self._secs_per_pic = secs_per_pic
            self._path_prefix = path_prefix
            self._recording = True

    def secs_to_delay(self):
        with self.control_lock:
            return self._secs_to_delay

    def secs_to_record(self):
        with self.control_lock:
            return self._secs_to_record

    def secs_per_pic(self):
        with self.control_lock:
            return self._secs_per_pic

    def path_prefix(self):
        with self.control_lock:
            return self._path_prefix

