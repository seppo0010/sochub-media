from flask import Flask, request, Response
import os
import re
import subprocess
import tempfile
app = Flask(__name__)

@app.route('/video-to-gif', methods=['POST'])
def main():
    start = request.form.get('start', 0)
    end = request.form.get('end', 5)
    url = request.form.get('url', None)
    fps = request.form.get('fps', 15)
    scale  = request.form.get('scale', '320:-1')

    is_numeric = lambda val: re.match('^[0-9]+$', str(val))

    if not is_numeric(start) or not is_numeric(end) or not is_numeric(fps):
        return 'bad request', 400

    if not re.match('^-?[0-9]+:-?[0-9]+$', scale):
        return 'bad request', 400

    start = int(start)
    end = int(end)
    if end < start or start + 10 < end:
        return 'bad request', 400

    video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    palette = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    try:
        video_url = subprocess.check_output(('youtube-dl', '-f', 'best', '-g', url)).decode('utf-8').strip()
        os.unlink(video.name)
        subprocess.check_call(('ffmpeg', '-ss', str(start), '-i', video_url, '-t', str(end-start), video.name))

        filters = f'fps={fps},scale={scale}:flags=lanczos'
        subprocess.check_call(('ffmpeg', '-v', 'warning', '-i', video.name, '-vf', filters + ',palettegen', '-y', palette.name))
        gif = subprocess.check_output(('ffmpeg', '-v', 'warning', '-i', video.name, '-i', palette.name, '-lavfi', f'{filters} [x]; [x][1:v] paletteuse', '-y', '-f', 'gif', '-'))
        return Response(gif, mimetype='image/gif')
    except Exception as e:
        print(e)
        return 'internal server error', 500
    finally:
        def delfile(f):
            try:
                os.unlink(f.name)
            except:
                pass
        delfile(video.name)
        delfile(palette.name)
