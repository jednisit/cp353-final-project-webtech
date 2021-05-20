from flask_restful import Api

from api.music import video,Music,lyrics,songpost,song,songput,allSong

def create_route(api: Api):

    api.add_resource(lyrics,'/lyrics')
    api.add_resource(song,'/song/<title>')
    api.add_resource(songpost,'/song/<type>')
    api.add_resource(songput,'/song/<type>/<title>')
    api.add_resource(video,'/video')
    api.add_resource(Music,'/music')
    api.add_resource(allSong,'/allsong')

