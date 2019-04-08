from flask import Flask, request
from flask_restful import Resource, Api
import uuid
import redis
import json
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'mysql://root:3a88a6fe364442905653779aa3231615@127.0.0.1:3306/petertest'
db = SQLAlchemy(app)
api = Api(app)
r_coon= redis.StrictRedis(host='localhost', port=6379, db=0)


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


def get_all_exam():
    all_exam = SubNameDB.query.all()
    all_exam = (list(map(lambda x: x.sub_name, SubNameDB.query.all())))
    return { 'exam': all_exam }


def get_sub_num(sub_name):
    return json.loads(SubNameDB.query.filter_by(sub_name=sub_name).first())['sub_num']

#TODO 
def get_sub(sub_type):
    return {'sub_id':10000,'type': sub_type, 'title':'Titles for exan','choice': {'A': 'AAAAA','B':'BBBBB','C':'CCCCC','D':'DDDDD'} }, {'sub_id':10000, 'answer': ['A'] }


def generate_subjects(subjects, session_id, sub_name):
    choice_num = get_sub_num(sub_name)
    session_answers = []
    for sub_type in choice_num:
        while choice_num[sub_type] > 0:
            subject, answer = get_sub(sub_type)
            subjects.append(subject)
            session_answers.append(answer)
            choice_num[sub_type] = choice_num[sub_type] -1
    r_coon.hset('session', session_id, json.dumps(session_answers))

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
        generate_subjects(subjects,exam['session'],sub_name)
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
