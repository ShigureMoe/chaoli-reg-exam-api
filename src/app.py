from flask import Flask, request
from flask_restful import Resource, Api
import uuid
import json
import libexam
from flask_sqlalchemy import SQLAlchemy


app = Flask('ChaoliExam')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
api = Api(app)


class Choices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.String(2000), unique=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    topic = db.relationship('Topics', backref=db.backref('choices'))
    true = db.Column(db.Integer, primary_key=True)


class Topics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    type = db.Column(db.Integer, unique=False)
    subject = db.relationship('Subjects', backref=db.backref('topics'))
    name = db.Column(db.String(20), unique=False)


class Subjects(db.Model):
    name = db.Column(db.String(80), unique=True)
    id = db.Column(db.Integer, primary_key=True)


db_operate = libexam.DBOperate(Subjects,Topics,Choices,db)


class DoNotCheat(Exception):
    def __init__(self, error_word):
        self.error_word = error_word


class SessionFailed(Exception):
    def __init__(self, error_word):
        self.error_word = error_word


class RegExam(Resource):
    def get(self):
        exam = db_operate.get_all_exam()
        return exam


class RegExamSub(Resource):
    def get(self,sub_name):
        exam = {}
        exam['session'] = str(uuid.uuid4())
        exam['exam'] = sub_name
        subjects = []
        db_operate.generate_subjects(subjects,exam['session'],sub_name)
        exam['subjects'] = subjects
        return exam

    def post(self,sub_name):
        session_id = request.form['session']
        answer = request.form['answer']
        try:
            return db_operate.solve_answer(session_id,answer)
        except DoNotCheat:
            return {'Warning': 'DoNotCheat'}
        except SessionFailed:
            return {'message': 'Some Things wrong'},500
        

api.add_resource(RegExam, '/reg-exam-api')
api.add_resource(RegExamSub, '/reg-exam-api/<string:sub_name>')

if __name__ == '__main__':
    app.run()
