from flask import Flask, request
from flask_restful import Resource, Api
import uuid
import json
import libexam


app = Flask(__name__)
api = Api(app)


class DoNotCheat(Exception):
    def __init__(self, error_word):
        self.error_word = error_word


class SessionFailed(Exception):
    def __init__(self, error_word):
        self.error_word = error_word


class RegExam(Resource):
    def get(self):
        exam = libexam.get_all_exam()
        return exam


class RegExamSub(Resource):
    def get(self,sub_name):
        exam = {}
        exam['session'] = str(uuid.uuid4())
        exam['exam'] = sub_name
        subjects = []
        libexam.generate_subjects(subjects,exam['session'],sub_name)
        exam['subjects'] = subjects
        return exam

    def post(self,sub_name):
        session_id = request.form['session']
        answer = request.form['answer']
        try:
            return libexam.solve_answer(session_id,answer)
        except DoNotCheat:
            return {'Warning': 'DoNotCheat'}
        except SessionFailed:
            return {'message': 'Some Things wrong'},500
        

api.add_resource(RegExam, '/reg-exam-api')
api.add_resource(RegExamSub, '/reg-exam-api/<string:sub_name>')

if __name__ == '__main__':
    app.run()
