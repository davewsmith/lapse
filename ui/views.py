import logging
import time

from flask import redirect
from flask import render_template
from flask import request
from flask import Response

from ui import app


@app.route('/')
def home():
    context = dict(time=time.time())
    return render_template("index.html", **context)

@app.route('/snap')
def snap():
    camera = app.config['CAMERA']
    bits = camera.capture_image_bits()
    return Response(bits, mimetype='image/{}'.format(camera.image_format()))

@app.route('/start', methods=['POST'])
def start():
    try:
        path_prefix = request.form.get('path_prefix', default='pics/img')
        secs_to_delay = to_seconds(request.form.get('secs_to_delay', default=''))
        secs_to_record = to_seconds(request.form.get('secs_to_record', default=''))
        secs_per_pic = to_seconds(request.form.get('secs_per_pic', default=''))

        logging.debug("secs_to_delay={}, secs_to_record={}, secs_per_pic={}".format(secs_to_delay, secs_to_record, secs_per_pic))

	control = app.config['CONTROL']
	control.record(secs_to_delay, secs_to_record, secs_per_pic, path_prefix)

    except Exception as e:
        logging.error("start(): {!r}".format(e))
        return redirect('/')

    # TODO redirect instead to a timer page with a [cancel] button
    return redirect('/')

def to_seconds(s):
    """convert hh:mm:ss (or mm:ss, or just ss) to seconds"""
    try:
	parts = [int(nn) for nn in s.split(':')]
	parts.reverse()
        return sum([nn * s for (nn, s) in zip(parts, [1, 60, 60*60])])
    except:
        return None

@app.route('/quit')
def shutdown():
    control = app.config['CONTROL']
    control.stop()
    # http://flask.pocoo.org/snippets/67/
    shutdown_hook = request.environ.get('werkzeug.server.shutdown')
    if shutdown_hook is not None:
        shutdown_hook()
    return Response("Bye", mimetype='text/plain')

@app.route('/debug')
def debug():
    r = "\n".join(["{}={!r}".format(key, app.config[key]) for key in app.config])
    return Response(r, mimetype='text/plain')

