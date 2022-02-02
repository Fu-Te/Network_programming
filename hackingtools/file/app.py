
from flask import Flask, render_template,request,redirect
from hackingtools import lan_scan,port_scan,binary_analysis
import pandas as pd
import webbrowser
import os


app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def show():
    return render_template('index.html')

@app.route('/lanscan',methods = ['GET','POST'])
def flask_lanscan():
    if request.method == 'GET':
        return render_template('lanscan.html')
    try:
        if request.method == 'POST':
            lanscan_result = lan_scan()
        
            return webbrowser.open_new_tab('http://127.0.0.1:8000/lanscan_result'),render_template('lanscan.heml')
    except:
        return render_template('lanscan.html')
    
@app.route('/lanscan_result')
def result():
    return render_template('result.html')

@app.route('/portscan',methods=['GET','POST'])
def flask_portscan():
    if request.method == 'GET':
        return render_template('portscan.html')
    if request.method == 'POST':
        web_input = request.form.get('web_input')
        ip,port,port_end = web_input.split(',')
        

        
        
        result = port_scan(ip,port,port_end)
        return render_template('portscan.html',result = result)
    
@app.route('/binary',methods=['POST','GET'])
def flask_binary():
    if request.method == 'GET':
        return render_template('binary.html')
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join('./file/',file.filename))
        file = './file/'+ file.filename
        with open(file,'rb') as f:
            b=f.read()
            result=b.decode()

        return render_template('binary.html',result=result)
    
if __name__ == '__main__':
    app.run(port=8000, debug=True)