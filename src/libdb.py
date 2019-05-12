class SubjectsDB(db.Model):
    sub_id = db.Column(db.Integer, primary_key=True)
    sub_type = db.Column(db.String(80), unique=False)
    sub_choice = db.Column(db.String(2000), unique=False)
    sub_answer = db.Column(db.String(20), unique=False)
    sub_sub_name = db.Column(db.String(20), unique=False)

    def __init__(self, sub_id, sub_type, sub_sub_name, sub_choice, sub_answer):
        self.sub_id = sub_id
        self.sub_type = sub_type
        self.sub_sub_name = sub_sub_name
        self.sub_choice = sub_choice
        self.sub_answer = sub_answer


class SubNameDB(db.Model):
    sub_name = db.Column(db.String(80), unique=True)
    sub_name_id = db.Column(db.Integer, primary_key=True)
    sub_num = db.Column(db.String(80),  unique=False)
    
    def __init__(self, sub_name, sub_name_id, sub_num):
        self.sub_name = sub_name
        self.sub_name_id = sub_name_id
        self.sub_num = sub_num