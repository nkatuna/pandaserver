from flask import (
    Flask, Response, request, abort, render_template, send_file,
    redirect, url_for)
import gpiozero
import picamera
from io import BytesIO
from time import sleep
import os
import datetime


app = Flask(__name__)
app.config.from_object('config')


button = gpiozero.Button(app.config['GPIOZERO_PIN'])
camera = picamera.PiCamera()
camera.resolution = (768, 1024)

armed_file = app.config['ARMED_FILE']


NUM_IMAGES_UPON_WINDOW_OPEN = 20
SECONDS_SLEEP_BETWEEN_SNAPS = 2


def is_armed():
    with open(armed_file, 'r') as f:
        if f.read() == 'armed':
            return True
        else:
            return False


def capture_image(to_stream=True, file_name='image.jpg'):
    resize_size = (384, 512)
    camera.start_preview()
    sleep(2)  # warmup
    
    if to_stream:
        stream = BytesIO()
        camera.capture(stream, format='jpeg', resize=resize_size)
        stream.seek(0)
        return stream
    else:
        file_path = os.path.join(app.config['MEDIA_DIR'], file_name)
        camera.capture(file_path, resize=resize_size)
        return file_path


def capture_video():
    pass


def window_opened():
    if not is_armed():
        return

    folder_name = '{:%Y-%m-%d_%H:%M}'.format(datetime.datetime.now())
    os.makedirs(os.path.join(app.config['MEDIA_DIR'], folder_name))
    for i in range(NUM_IMAGES_UPON_WINDOW_OPEN):
        capture_image(
            to_stream=False,
            file_name=os.path.join(folder_name, 'image_{}.jpg'.format(i)))
        sleep(SECONDS_SLEEP_BETWEEN_SNAPS)

        
button.when_released = window_opened


@app.route('/', methods=['GET'])
def index():
    context = {
        'is_armed': is_armed(),
        'random_querystring': int(
            datetime.datetime.now().timestamp()),}
    return render_template('index.html', **context)


@app.route('/image', methods=['GET'])
def image():
    image_stream = capture_image()
    return send_file(
       image_stream,
       attachment_filename='image.jpeg',
       mimetype='image/jpg')


@app.route('/images/stored', methods=['GET'])
def stored_image():
    pass


@app.route('/arm', methods=['GET'])
def arm():
    with open(armed_file, 'w') as f:
        f.write('armed')
    return redirect(url_for('index'), code=302)


@app.route('/disarm', methods=['GET'])
def disarm():
    with open(armed_file, 'w') as f:
        f.write('disarmed')
    return redirect(url_for('index'), code=302)


@app.route('/simulate', methods=['GET'])
def simulate_opened():
    window_opened()
    return redirect(url_for('index'), code=302)
