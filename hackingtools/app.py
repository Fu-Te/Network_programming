from urllib import request
from flask import Flask, render_template,request
from hackingtools import lan_scan


app = Flask(__name__, static_folder='.', static_url_path='')
@app.route('/',methods = ['GET','POST'])
def flask_lanscan():
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.method == 'POST':
        lanscan_result = lan_scan()
        
        return render_template('index.html',lanscan_result=lanscan_result)
        
if __name__ == '__main__':
    app.run(port=8000, debug=True)