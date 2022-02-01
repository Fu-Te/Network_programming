
from flask import Flask, render_template,request,redirect
from hackingtools import lan_scan
import pandas as pd


app = Flask(__name__, static_folder='.', static_url_path='')
@app.route('/',methods = ['GET','POST'])
def flask_lanscan():
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.method == 'POST':
        lanscan_result = lan_scan()
        
        return redirect('lanscan_result')
    
@app.route('/lanscan_result')
def result():
    return render_template('result.html')
        
if __name__ == '__main__':
    app.run(port=8000, debug=True)