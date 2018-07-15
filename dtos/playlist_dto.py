class Playlist:

    def __init__(self,id,user_id,playlist_id):
        self.id = id
        self.user_id = user_id
        self.playlist_id = playlist_id

    def get_id(self):
        return self.id
    
    def get_user_id(self):
        return self.user_id
    
    def get_playlist_id(self):
        return self.playlist_id