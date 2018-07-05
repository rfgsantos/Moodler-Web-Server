class Track:

    def __init__(self,id,duration_sec,danceability,energy,loudness,track_key,liveness,valance,tempo,time_signature):
        self.id = id
        self.duration_sec = duration_sec
        self.danceability = danceability
        self.energy = energy
        self.loudness = loudness
        self.track_key = track_key
        self.liveness = liveness
        self.valance = valance
        self.tempo = tempo
        self.time_signature = time_signature
    
    def get_id(self):
        return self.id

    def get_duration_sec(self):
        return self.duration_sec

    def get_danceability(self):
        return self.danceability

    def get_energy(self):
        return self.energy
    
    def get_loudness(self):
        return self.loudness
    
    def get_track_key(self):
        return self.track_key
    
    def get_liveness(self):
        return self.loudness
    
    def get_valance(self):
        return self.valance
    
    def get_tempo(self):
        return self.tempo
    
    def get_time_signature(self):
        return self.time_signature