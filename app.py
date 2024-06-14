from flask import Flask, render_template
import threading, time, webbrowser
import pandas as pd

app = Flask(__name__)

umi = 0
estado_bomba = False
tempo_total_des = 0
count_bomba_des = 0
tempo_total_lig = 0
count_bomba_lig = 0
intervalo_leitura = 1

def read_data():
    global umi, estado_bomba, tempo_total_des, count_bomba_des, tempo_total_lig, count_bomba_lig
    df = pd.DataFrame(pd.read_csv('dados_teste.csv'))
    for index, row in df.iterrows():
        umi = row['umidade']
        estado_bomba = row['bomba']
        if estado_bomba:
            tempo_total_lig += intervalo_leitura
            count_bomba_lig += 1
        else:
            tempo_total_des += intervalo_leitura
            count_bomba_des += 1
        time.sleep(intervalo_leitura)

@app.route('/')
def home():
    return render_template('index.html', umi=umi, bomba=estado_bomba, tempo_total_des=time.strftime("%H:%M:%S", time.gmtime(tempo_total_des)), count_bomba_des=count_bomba_des, tempo_total_lig=time.strftime("%H:%M:%S", time.gmtime(tempo_total_lig)), count_bomba_lig=count_bomba_lig, intervalo_leitura=intervalo_leitura)

if __name__ == '__main__':
    thread = threading.Thread(target=read_data)
    thread.daemon = True
    thread.start()
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(debug=True)