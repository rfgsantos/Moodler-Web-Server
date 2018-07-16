
class User:

    def __init__(self, id, user_id, date):
        self.id = id
        self.user_id = user_id
        self.date = date
    
    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def get_date(self):
        return self.date

    