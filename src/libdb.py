from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask('ChaoliExam')
#    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db.init_app(app)
    return app


class Choices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.String(2000), unique=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    true = db.Column(db.Integer, primary_key=True)


class TopicDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    type = db.Column(db.Integer, unique=False)
    choices = db.relationship('Choices', backref='topic',
                                lazy='dynamic')
    name = db.Column(db.String(20), unique=False)


class ExamSubjectDB(db.Model):
    name = db.Column(db.String(80), unique=True)
    id = db.Column(db.Integer, primary_key=True)
    topics = db.relationship('Choices', backref='subject',
                                lazy='dynamic')