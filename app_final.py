from flask import Flask, render_template
import threading, serial

app = Flask(__name__)

umi = 0
bomba = False

def read_serial():
    global umi, bomba
    ser = serial.Serial('COM3')  # A porta 'COM3' deve ser substituída pela porta utilizada pelo arduino
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if line.isdigit():
                umi = int(line)
            elif line == "bomba ligada":
                bomba = True
            elif line == "bomba desligada":
                bomba = False

@app.route('/')
def home():
    return render_template('index.html', umi=umi, bomba=bomba)

if __name__ == '_main_':
    thread = threading.Thread(target=read_serial)
    thread.daemon = True
    thread.start()

    app.run(debug=True)