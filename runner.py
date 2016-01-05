from flask import Flask, request, g, redirect, url_for, \
    abort, render_template, flash

from babelfish import Language
from subliminal import download_best_subtitles, region, save_subtitles, scan_video
from subliminal.subtitle import get_subtitle_path
from subprocess import Popen, PIPE, check_output, CalledProcessError
import os
import mimetypes

DEVNULL = open(os.devnull, 'wb')

mimetypes.init()
mimetypes.add_type('rom/nintendo', '.nes')

# configuration
DEBUG = True

app = Flask(__name__)

app.current_job = None

def get_path(path):
    return '/home/pi/htdocs' + path

# Play videos using omxplayer
@app.route('/run',  methods=['POST'])
def run():
    filepath = get_path(request.form['file'])
    mime = mimetypes.guess_type(filepath)[0]

    if mime == None:
        return 'FAIL'
    else:
        mime = mime.split('/')[0]

    if mime == 'video':
        play_video(filepath)
    elif mime == 'audio':
        play_audio(filepath)
    elif mime == 'rom':
        play_rom(filepath)
    else:
        return 'FAIL'

    return 'PLAYING'

# @app.route('/keypress', methods=['POST'])
# def keypress():
#     key = request.form['key']
#     app.current_job.stdin.write(key)
#     print(key)
#     return "Sending "+key

def run_in_bg(cmd):
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    env['XAUTHORITY']='/etc/X11/host-Xauthority'

    # Try to kill everything before moving ahead
    # killall('omxplayer')
    # killall('vlc')
    # killall('cvlc')
    # killall('fceux')
    if app.current_job!=None:
        app.current_job.kill()
    
    app.current_job = Popen(cmd, env=env, stdout=DEVNULL, stderr=DEVNULL)

def get_subtitle_path(filepath):
    os.path.splitext(filepath)[0]+'.srt'

def download_subtitles(filepath):
    video = scan_video(filepath)
    subtitles = download_best_subtitles([video], {Language('eng')})

    save_subtitles(video, subtitles[video], single=True)

def play_video(filepath):
    size = os.path.getsize(filepath)
    # 150MB is our lower limit for checking subtitles
    if size > 157286400:
        download_subtitles(filepath)

    if os.path.exists(get_subtitle_path(filepath)):
        sub = get_subtitle_path(filepath)
        run_in_bg(['omxplayer', '-b', '--subtitles', sub, filepath])
    else:
        run_in_bg(['omxplayer', '-b', filepath])

def play_audio(filepath):
    run_in_bg(['omxplayer', '-b', filepath])


def play_rom(filepath):
    run_in_bg(['/home/pi/fceux', filepath])

if __name__ == '__main__':
    app.run(debug=True)