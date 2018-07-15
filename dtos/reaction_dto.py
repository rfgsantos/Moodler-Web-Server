class Reaction:

    def __init__(self,id,user_id,track_id,hrv,evaluation):
        self.id = id
        self.user_id = user_id
        self.track_id = track_id
        self.hrv = hrv
        self.evaluation = evaluation

    
    def get_id(self):
        return self.id
    
    def get_user_id(self):
        return self.user_id
    
    def get_track_id(self):
        return self.track_id

    def get_hrv(self):
        return self.hrv
    
    def get_evaluation(self):
        return self.evaluation
    