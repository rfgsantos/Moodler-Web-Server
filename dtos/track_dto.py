class Track:

    def __init__(self,id,track_id,playlist_id):
        self.id = id
        self.track_id = track_id
        self.playlist_id = playlist_id
    
    def get_id(self):
        return self.id

    def get_track_id(self):
        return self.track_id

    def get_playlist_id(self):
        return self.playlist_id
