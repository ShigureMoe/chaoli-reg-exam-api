class DBOperate(object):
    def __init__(self,Subjects,Topics,Choices,db):
        self.db = db
        self.Subjects = Subjects
        self.Topics = Topics
        self.Choices = Choices
        pass

    def get_all_exam(self):
        subs = []
        for sub in self.Subjects.query.all():
            subs.append( { 'id': sub.id, 'name': sub.name } )
        return subs

    def generate_subjects(self,subjects,session,sub_name):
        pass

    def solve_answer(self,session_id,answer):
        pass