# Lapse - Easy time-lapse setup for the Raspberry Pi

Lapse reduces the hassle of setting up a time-lapse shoot from a headless Raspberry Pi.

Lapso is a command-line app that provides UI that can be accessed from a browser elsewhere on your intranet.

## Status

Lapse is a working rough draft. I'm developing it to scratch a personal itch.  At the moment, stitching pics together to make the time-lapse video is done manually. Eventually, it will invoke `mencoder`. 

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

At present, there are some settings in `lapse.py` that need manual adjustment.

## License

MIT
