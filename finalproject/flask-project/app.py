from flask import Flask,render_template,request,make_response
from werkzeug import datastructures
from flask_cors import CORS
from PIL import Image
import base64
from flask_restful import Api
from ml import TFModel
import os,json,requests
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

#UPLOAD_FOLDER = './static/uploads'

from flask import Flask,jsonify,make_response,request
from flask_restx import Resource,Api
from security import authenticate,identity
from flask_jwt import JWT,jwt_required

from itertools import islice

UPLOAD_FOLDER = './static/uploads'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-super-secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
jwt = JWT(app, authenticate, identity)

model = TFModel(model_dir='./ml-model/')
model.load()


"""config = {
    'JSON_SORT_KEYS': False,
    'JWT_SECRET_KEY': 'rrunvuernvurneve',
    'JWT_ACCESS_TOKEN_EXPIRES': 300,
    'JWT_REFRESH_TOKEN_EXPIRES': 604800
}"""



def jsonread() :
    f = open('music.json')
    data_music = json.load(f)
    return data_music


def writejson(music_dict,type):
    music_list = jsonread()
    for key, value in music_list.items(): 
        if type.lower() == key.lower() :
            music_list[key].append(music_dict)
            open_json_file = open('music.json', 'w')
            json.dump(music_list, open_json_file, indent=4) ##สำคัญ
    return 200


def deleteJson(musicname):
    music_list = jsonread()
    response = 0

    music_key = list(music_list.keys())

    for i in music_key:
        for j in range(len(music_list[i])):
            if music_list[i][j]['title'].lower() == musicname.lower():
                music_list[i].pop(j)
                response = 200
                open_json_file = open('music.json', 'w')
                json.dump(music_list, open_json_file, indent=4)
                break
    if response == 200 : return response
    else : return 500

####################################################################

def updatejson(title,typemusic,new_info):
    music_list = jsonread()
    music_key = list(music_list.keys())
    response = 0
    for i in music_key:
        print(i)
        if typemusic.lower() == i.lower():
            for j in range(len(music_list[i])):
                print(j)
                if title.lower() == music_list[i][j]['title'].lower():
                    response = 200
                    music_list[i][j].update(new_info)
                    open_json_file = open('music.json', 'w')
                    json.dump(music_list, open_json_file, indent=4) ##สำคัญ
                    break
    if response == 200 : return response
    else : return 500

#####################################################################

class video(Resource):
    def get(self):
        music_data = jsonread() #ดึงข้อมูลมาจาก function jsonread
        title = request.args.get('title') #ดึงค่ามาจากที่เขาส่งมา title

        if title != None : #ถ้าเขาส่ง title มาให้เข้าเงื่อนไข
            listcheck = []
            for key, value in music_data.items():
                for check in range(len(music_data[key])): # loop
                    if title.lower() in music_data[key][check]['title'].lower() : #check ค่า
                        addlist = {
                        'title' : music_data[key][check]['title'],
                        'yt_url' : music_data[key][check]['yt_url']
                        }
                        listcheck.append(addlist)
        if (len(listcheck)) != 0: return listcheck,200
        else : return {"message": "Not Found"},500

############################################################################

class Music(Resource):
    def get(self):
        music_data = jsonread() 
        title = request.args.get('title') 
        artist = request.args.get('artist')
        #None not in (title,artist)
        if all(v is not  None for v in [title,artist])  : 
            listcheck = []
            for key, value in music_data.items():
                for check in range(len(music_data[key])):
                    if title.lower() in music_data[key][check]['title'].lower() and artist.lower() in music_data[key][check]['artist'].lower() : #check ค่า
                        addlist = {
                        'title' : music_data[key][check]['title'],
                        'artist' : music_data[key][check]['artist']
                    }
                        listcheck.append(addlist)
            if len(listcheck) != 0: return listcheck,200
            else : return {"message": "Not Found"},500
        else : return {"message": "Missing parameter"},500


################################################################################


class lyrics(Resource):
    def get(self):
        music_data = jsonread() 
        title = request.args.get('title') 
        artist = request.args.get('artist')
        #None not in (title,artist)
        if title != None and artist == None: 
            listcheck = []
            for key, value in music_data.items():
                for check in range(len(music_data[key])):
                    if title.lower() in music_data[key][check]['title'].lower() : #check ค่า
                        addlist = {
                        'title' : music_data[key][check][check]['title'],
                        'artist' : music_data[key][check][check]['artist'],
                        'web_url' : music_data[key][check][check]['web_url']
                    }
                        listcheck.append(addlist)
            if len(listcheck) != 0: return listcheck,200
            else : return {"message": "Not Found"},500
        elif  title == None and artist != None: 
            listcheck = []
            for key, value in music_data.items():
                for check in range(len(music_data[key])):
                    if title.lower() in music_data[key][check]['artist'].lower() : #check ค่า
                        addlist = {
                        'title' : music_data[key][check]['title'],
                        'artist' : music_data[key][check]['artist'],
                        'web_url' : music_data[key][check]['web_url']
                    }
                        listcheck.append(addlist)
            if len(listcheck) != 0: return listcheck,200
            else : return {"message": "Not Found"},500
        elif  title != None and artist != None: 
            listcheck = []
            for key, value in music_data.items():
                for check in range(len(music_data[key])):
                    if title.lower() in music_data[key][check]['title'].lower() and artist.lower() in music_data[key][check]['artist'].lower() : #check ค่า
                        addlist = {
                        'title' : music_data[key][check]['title'],
                        'artist' : music_data[key][check]['artist'],
                        'web_url' : music_data[key][check]['web_url']
                    }
                        listcheck.append(addlist)
            if len(listcheck) != 0: return listcheck,200
            else : return {"message": "Not Found"},500
        else : return {"message": "Missing parameter"},500

#######################################################################################################


class songpost(Resource):
    @jwt_required()
    def post(self,type):
        print(type)
        print(request.get_json())
        status = writejson(request.get_json(),type)
        if status == 200:
            return {"message":"Music has been added."}, 200
        elif status == 500:
            {"message": "มีข้อมูลอยู่แล้ว."}, 500

class song(Resource):
    @jwt_required()
    def delete(self,title): #รับ DELETE
        status = deleteJson(title)
        if status == 200:
            return {"message":"Music has been deleted."}, 200
        elif status == 500:
            return {"message":title+" not found."}, 500


class songput(Resource):
    @jwt_required()
    def put(self,type,title):#รับ PUT
        music_dict = api.payload
        status = updatejson(title,type,music_dict)
        if status == 200:
            return {
                "message":"Music HAS BEEN UPDATED."
                }, 200
        elif status == 500:
            return {"message": "FAIL TO UPDATED."}, 500

class allSong(Resource):
    def get(self):
        data = jsonread()
        return {"data": data}

#############################################################################################


api.add_resource(lyrics,'/lyrics')
api.add_resource(song,'/song/<title>')
api.add_resource(songpost,'/song/<type>')
api.add_resource(songput,'/song/<type>/<title>')
api.add_resource(video,'/video')
api.add_resource(Music,'/music')
api.add_resource(allSong,'/allsong')







#model = TFModel(model_dir='.client/ml-model')
#model.load()

# swagger specific





@app.route('/home')
def home():
    ly = requests.request("GET", "http://127.0.0.1:5000/allsong").json()
    return render_template("main.html",sound=ly['data'],ly = ly['data'])


@app.route("/you")
def video1():
    video = requests.request("GET", "http://127.0.0.1:5000/allsong").json()
    return render_template("video.html", sound=video['data'], vdo=video['data'])

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