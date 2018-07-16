
from dao.user_dao import UserDao
from dao.playlist_dao import PlaylistDao
from dao.reaction_dao import ReactionDao
from dao.track_dao import TrackDao
from datetime import date, datetime, timedelta

class Business:
    def __init__(self):
        self.user_dao = UserDao()
        self.playlist_dao = PlaylistDao()
        self.reaction_dao = ReactionDao()
        self.track_dao = TrackDao()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Business, cls).__new__(cls)
        return cls.instance

    def process_insertion_of_musics(self, playlist_id, user_id, tracks, hrv, current_track_id, user_evaluation):
        user = self.user_dao.get_user_by_id(user_id)
        playlist = self.playlist_dao.get_playlist_by_id(playlist_id)

        if(bool(user_evaluation)):
            user_evaluation = 1
        else:
            user_evaluation = 0

        if(user and playlist):
            for track_id in tracks:
                track_to_insert = self.track_dao.map_track({'id':'0','track_id': track_id, 'playlist_id': playlist[0]['id']})
                track_inserted_id = self.track_dao.insert_track(track_to_insert)
            
            reaction_to_insert = self.reaction_dao.map_reaction({'id':'0', 'user_id':user[0]['id'], 'track_id':current_track_id, 'hrv':hrv, 'evaluation': 1, 'user_evaluation':user_evaluation})
            self.reaction_dao.insert_reaction(reaction_to_insert)

        else:
            user = self.user_dao.map_user({'id':'0','user_id':user_id,'date':datetime.now().strftime("%Y-%m-%d")})
            id_user = self.user_dao.insert_user(user)

            playlist = self.playlist_dao.map_playlist({'id':'0','playlist_id':playlist_id, 'user_id':id_user})
            id_playlist = self.playlist_dao.insert_playlist(playlist)

            for track_id in tracks:
                track_to_insert = self.track_dao.map_track({'id':'0','track_id': track_id, 'playlist_id': id_playlist})
                track_inserted_id = self.track_dao.insert_track(track_to_insert)

            reaction_to_insert = self.reaction_dao.map_reaction({'id':'0', 'user_id':id_user, 'track_id':current_track_id, 'hrv':hrv, 'evaluation': 1, 'user_evaluation':user_evaluation})
            self.reaction_dao.insert_reaction(reaction_to_insert)

            
    def remove_track_from_list(self, playlist_id, user_id, tracks, hrv, current_track_id, user_evaluation):

        user = self.user_dao.get_user_by_id(user_id)

        if(bool(user_evaluation)):
            user_evaluation = 1
        else:
            user_evaluation = 0

        if(user):
            reaction_to_insert = self.reaction_dao.map_reaction({'id':'0', 'user_id':user[0]['id'], 'track_id':current_track_id, 'hrv':hrv, 'evaluation': 0,'user_evaluation':user_evaluation})
            self.reaction_dao.insert_reaction(reaction_to_insert)
        else:
            user = self.user_dao.map_user({'id':'0','user_id':user_id,'date':datetime.now().strftime("%Y-%m-%d")})
            id_user = self.user_dao.insert_user(user)

            reaction_to_insert = self.reaction_dao.map_reaction({'id':'0', 'user_id':id_user, 'track_id':current_track_id, 'hrv':hrv, 'evaluation': 0,'user_evaluation':user_evaluation})
            self.reaction_dao.insert_reaction(reaction_to_insert)

