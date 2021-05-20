import config # to hide TMDB API keys
import requests # to make TMDB API calls
import locale # to format currency as USD
locale.setlocale( locale.LC_ALL, '' )

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from urllib.parse import quote
from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
from flask import Flask,jsonify,make_response
from flask_restx import Resource,Api

from ml import TFModel
import base64
import os
from PIL import Image
from flask_restful import Api
from flask_jwt_extended.jwt_manager import JWTManager
from flask_cors import CORS



app = Flask(__name__)
"""api = Api(app)"""


f = open('genre.json')
data_music = json.load(f)

v = open('genre.json')
data_vdo= json.load(v)


l = open('genre.json')
data_lyrics= json.load(l)


@app.route("/")
def home():
   return render_template("main.html",sound=data_music,ly = data_lyrics)


@app.route("/video")
def video():
   return render_template("video.html",vdo=data_vdo,ly = data_lyrics)

   
##@app.route("/upload")
#def upload():
#   return render_template("upload.html")

# init JWT

model = TFModel(model_dir='./ml-model/')
model.load()

jwt = JWTManager(app=app)

CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"
], supports_credentials=True)
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    data = jsonread()
    if request.method == 'POST' :
        if 'file' not in request.files:
            return 'there is no file in form!'
        file = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        image1 = Image.open(path)
        outputs = model.predict(image1)
        image = image1.filename
        return render_template('prediction.html', pred_result=outputs,pic = image)
    return render_template('upload.html')

    
def jsonread():
    open_json_file = open('genre.json', 'r') 
    read_json_file = open_json_file.read()
    data_music = json.loads(read_json_file)
    return data_music

