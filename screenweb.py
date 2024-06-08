import os
import time
import threading
import pyautogui
from flask import Flask, send_file

app = Flask(__name__)

# Diretório onde as capturas de tela serão salvas
SCREENSHOT_DIR = 'screenshots'
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

def cleanup_screenshots():
    screenshots = sorted(os.listdir(SCREENSHOT_DIR), key=lambda x: os.path.getmtime(os.path.join(SCREENSHOT_DIR, x)))
    while len(screenshots) > 10:
        os.remove(os.path.join(SCREENSHOT_DIR, screenshots.pop(0)))

def capture_screenshots():
    while True:
        screenshot_path = os.path.join(SCREENSHOT_DIR, f'screenshot_{int(time.time())}.png')
        pyautogui.screenshot(screenshot_path)
        cleanup_screenshots()
        time.sleep(2)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="2">
        <title>SCREENSHOT WEB</title>
    </head>
    <body>
        <h1>SCREENSHOT WEB</h1>
        <img src="/screenshot" alt="Screenshot">
    </body>
    </html>
    '''

@app.route('/screenshot')
def screenshot():
    screenshots = sorted(os.listdir(SCREENSHOT_DIR), key=lambda x: os.path.getmtime(os.path.join(SCREENSHOT_DIR, x)))
    latest_screenshot = screenshots[-1] if screenshots else None
    if latest_screenshot:
        screenshot_path = os.path.join(SCREENSHOT_DIR, latest_screenshot)
        return send_file(screenshot_path, mimetype='image/png')
    else:
        return 'No screenshot available', 404

if __name__ == '__main__':
    # Inicia a thread de captura de tela
    threading.Thread(target=capture_screenshots, daemon=True).start()
    # Inicia o servidor Flask
    app.run(debug=True, use_reloader=False)
