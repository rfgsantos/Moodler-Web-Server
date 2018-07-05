class Playlist:

    def __init__(self,id,user_id,comment):
        self.id = id
        self.user_id = user_id
        self.comment = comment

    def get_id(self):
        return self.id
    
    def get_user_id(self):
        return self.user_id
    
    def get_comment(self):
        return self.comment