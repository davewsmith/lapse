import logging
import threading
import resource
import time

from camera import Camera
from control import Control
from ui import app


logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')


def webserver(control, camera):
    app.config['CONTROL'] = control
    app.config['CAMERA'] = camera
    # It isn't safe to use the reloader in a thread
    app.run(host='0.0.0.0', debug=True, use_reloader=False)

def main():
    # TODO set these from command-line options
    resolution = 'medium'

    # image_format = 'jpeg'
    # file_suffix = 'jpg'
    image_format = 'png'
    file_suffix = 'png'

    control = Control()
    camera = Camera(resolution=resolution, image_format=image_format)
    ui_thread = threading.Thread(target=webserver, args=(control, camera))
    ui_thread.start()

    deltas = []

    while control.running():
        (ts, f) = divmod(time.time(), 1)
        # Delay until the next second
        time.sleep(1.0 - f)

        if control.recording():
            secs_to_delay = control.secs_to_delay()
            secs_to_record = control.secs_to_record()
            secs_per_pic = control.secs_per_pic()
            path_prefix = control.path_prefix()
            logging.info("delay={}, record={}, secs_per_pic={}, path_prefix={}".format(
                secs_to_delay, secs_to_record, secs_per_pic, path_prefix))

            while control.recording() and secs_to_delay > 0:
                # warm the camera up
                jpg_bits = camera.capture_image_bits()
                (_, f) = divmod(time.time(), 1)
                time.sleep(1.0 - f)
                secs_to_delay -= 1

            # record
            while control.recording() and secs_to_record > 0:
                start = time.time()

                jpg_bits = camera.capture_image_bits()
                delta_capture = time.time() - start

                save_start = time.time()
                with open("{}_{}.{}".format(path_prefix, int(start), file_suffix), "wb") as f:
                    f.write(jpg_bits)
                delta_save = time.time() - save_start

                # Accumulate debugging info
                max_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                deltas.append((delta_capture, delta_save, max_rss))

                # here we make a big assumption
                f = max(0.0, (start + secs_per_pic) - time.time())
                time.sleep(f)
                secs_to_record -= secs_per_pic

            control.stop_recording()
            logging.info("Done. Saving deltas.")

            with open("{}_deltas.csv".format(path_prefix), "w") as f:
                f.write("capture,save,maxrss\n")
                for delta in deltas:
                    f.write("{},{},{}\n".format(delta[0],delta[1],delta[2]))

    ui_thread.join()


if __name__=='__main__':
    main()
