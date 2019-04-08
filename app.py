from flask import Flask, request
from flask_restful import Resource, Api
import uuid
import redis
import json


app = Flask(__name__)
api = Api(app)
r_coon= redis.StrictRedis(host='localhost', port=6379, db=0)


def get_all_exam():
    return { 'exam': ['chem','bio','phy','tech'] }

#TODO 
def get_sub_num():
    single_choice,multi_choice,bool_choice = 4,4,4 
    return single_choice,multi_choice,bool_choice

#TODO 
def get_sub(sub_type):
    return {'sub_id':10000,'type': sub_type, 'title':'Titles for exan','choice': {'A': 'AAAAA','B':'BBBBB','C':'CCCCC','D':'DDDDD'} }

#TODO 
def generate_subjects(subjects, session):
    single_choice,multi_choice,bool_choice = get_sub_num()
    while single_choice > 0:
        subjects.append(get_sub('single_choice'))
        single_choice = single_choice - 1
    while multi_choice > 0:
        subjects.append(get_sub('multi_choice'))
        multi_choice = multi_choice - 1
    while bool_choice > 0:
        subjects.append(get_sub('bool_choice'))
        bool_choice = bool_choice - 1
    r_coon.hset('session', session, json.dumps(subjects))

#TODO
def get_session_status(session_id):
    return json.loads(r_coon.hget('session', session_id))


#TODO
def solve_answer(session_id,answers):
    session_answer = get_session_status(session_id)
    for answer in answers:
        if answer['sub_id'] not in session_answer:
            raise DoNotCheat


class DoNotCheat(Exception):
    def __init__(self, error_word):
        self.error_word = error_word


class SessionFailed(Exception):
    def __init__(self, error_word):
        self.error_word = error_word


class RegExam(Resource):
    def get(self):
        exam = get_all_exam()
        return exam

class RegExamSub(Resource):
    def get(self,sub_name):
        exam = {}
        exam['session'] = str(uuid.uuid4())
        exam['exam'] = sub_name
        subjects = []
        generate_subjects(subjects,exam['session'])
        exam['subjects'] = subjects
        return exam

    def post(self,sub_name):
        session_id = request.form['session']
        answer = request.form['answer']
        try:
            return solve_answer(session_id,answer)
        except DoNotCheat:
            return {'Warning': 'DoNotCheat'}
        except SessionFailed:
            return {'message': 'Some Things wrong'},500
        

api.add_resource(RegExam, '/reg-exam-api')
api.add_resource(RegExamSub, '/reg-exam-api/<string:sub_name>')

if __name__ == '__main__':
    app.run()
