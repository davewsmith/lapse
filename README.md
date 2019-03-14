# Lapse - Easy time-lapse setup for the Raspberry Pi

Lapse reduces the hassle of setting up a time-lapse shoot from a headless Raspberry Pi.

Lapse is a command-line app that provides UI that can be accessed from a browser elsewhere on your intranet.

## Status

Lapse is a working rough draft. I'm developing it to scratch a personal itch.  At the moment, stitching pics together to make the time-lapse video is done manually. Eventually, Lapse will invoke `mencoder`.

The presentation needs work.

Pull Requests for bugs will be appreciated; PRs for features might get ignored. You're welcome to fork this and head off in your own direction.

## Setting up a Raspberry Pi

The latest Raspian includes the `picamara` packages.

    pip install flask

gets you everything else you need.

    python lapse.py

starts the application. Issuing `/quit` through a browser stops it.

## Setting up Lapse on some other Linux environment

Lapse can run in a Python virtual environment.  It requires `OpenCV` and the `cv2` Python bindings. To get those for Python 2.7:

    sudo apt-get install python-dev python-opencv libjpeg-dev

(At present, using Python 3.x requires building `OpenCV` manually.)

To make `cv2` available inside the virtual environment, create the environment via

    virtualenv --system-site-packages venv
    . venv/bin/activate
    pip install -r requirements.txt

Then,

    python lapse.py

starts the app. From a browser elsewhere on your intranet, visit http://yourpi:5000/

Clicking on the image will refresh it, allowing you to adjust the camera position to your liking before starting collection.

*Path Prefix* is the path to where images will be saved, plus a prefix. The path must exist. A timestamp and ".jpg" are appended to the prefix for each image saved.

*Delay* is the amount of time to delay before starting to record. A simple number is interepreted as seconds. Appending 'h', 'm', or 's' specifies hours, minutes, and seconds, respectively. These can combined. `1h 30m` will delay for an hour and a half before beginning to record.

*Record* is the length of time to record. `12h` will record for half a day.

*Sec/Pic* is the the number of seconds between each picture. A Raspberry Pi 3 is just fast enough to record 1 medium-sized JPEG per second to fast media (e.g., a good class 10 SD card or a fast thumb drive). If you notice stuttering in the final video, try a larger number.

Make sure you have sufficient storage for the number of images that you'll be capturing.

Click *Start* to begin.

After the Delay + Record time has elapsed, quit the lapse via `/quit` from a remote browser, and use `mencoder` or the tool of your choice to convert the images into a video.

There are some settings in `lapse.py` that may need manual adjustment. Consult the code. These may be exposed through the UI in the future.

## Credits

I borrowed from several sources. Credits are in the source.

## License

MIT
