from flask import (
    Flask, Response, request, abort, render_template, send_file,
    redirect, url_for)
import gpiozero
import picamera
from io import BytesIO
from time import sleep
from os import path


app = Flask(__name__)
app.config.from_object('config')


button = gpiozero.Button(app.config['GPIOZERO_PIN'])
camera = picamera.PiCamera()
camera.resolution = (768, 1024)


is_armed = True


def capture_image(to_stream=True):
    resize_size = (384, 512)
    camera.start_preview()
    sleep(2)  # warmup
    
    if to_stream:
        stream = BytesIO()
        camera.capture(stream, format='jpeg', resize=resize_size)
        stream.seek(0)
        return stream
    else:
        filename = path.join(app.config['MEDIA_DIR'], 'image.jpg')
        camera.capture(filename, resize=resize_size)
        return filename


def capture_video():
    pass


def window_opened():
    # alarm sounds
    # send e-mail
    
    # take images or video
    
    print('Window opened')


button.when_released = window_opened


@app.route('/', methods=['GET'])
def index():
    context = {
        'is_armed': is_armed,}
    return render_template('index.html', **context)


@app.route('/image', methods=['GET'])
def image():
    image_stream = capture_image()
    return send_file(
       image_stream,
       attachment_filename='image.jpeg',
       mimetype='image/jpg')


@app.route('/arm', methods=['GET'])
def arm():
    is_armed = True
    return redirect(url_for('index'), code=302)


@app.route('/disarm', methods=['GET'])
def disarm():
    is_armed = False
    return redirect(url_for('index'), code=302)
