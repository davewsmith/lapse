"""
Threadsafe access to a Raspberry Pi or USB webcam

See
- http://picamera.readthedocs.io/en/release-1.12/
- https://www.raspberrypi.org/documentation/usage/camera/python/README.md
- http://docs.opencv.org/3.0-beta/modules/videoio/doc/reading_and_writing_video.html
- http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
- https://github.com/patrickfuller/camp/ # for the idea of also supporting a usb camera
"""

import cStringIO as io
import logging
import threading

try:
    import picamera
    is_pi_camera = True
except:
    try:
        import cv2
        from PIL import Image
        is_pi_camera = False
    except:
        assert False, "Camera support not available"


# TODO revisit for picamera v2
RESOLUTION = {
    'high': (1280,720),
    'medium': (640,480),
    'low': (320,240),
}

# The Pi Camera can use an on-chip JPG-encoder, which is faster but grainier
# See note in http://picamera.readthedocs.io/en/release-1.10/recipes2.html#rapid-capture-and-processing
USE_VIDEO_PORT=False


class Camera(object):

    def __init__(self, resolution='medium', image_format="jpeg"):
        self._camera_lock = threading.Lock()
	self._image_format = image_format
        if is_pi_camera:
            logging.debug("Using Raspberry Pi Camera")
            self.camera = picamera.PiCamera()
            self.camera.resolution = RESOLUTION[resolution]
        else:
            logging.debug("USB Camera")
            self.camera = cv2.VideoCapture(0)    # TODO allow n>0 for USB webcam
            w, h = RESOLUTION[resolution]
            self.camera.set(3, w)
            self.camera.set(4, h)

    def image_format(self):
        return self._image_format

    def capture_image_bits(self):
        sio = io.StringIO()
        if is_pi_camera:
            with self._camera_lock:
                self.camera.capture(sio, self._image_format, use_video_port=USE_VIDEO_PORT)
        else:
            # lock only long enough to snag a frame
            with self._camera_lock:
                _, frame = self.camera.read()
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img.save(sio, self._image_format.upper())
        return sio.getvalue()
