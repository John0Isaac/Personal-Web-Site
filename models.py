from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
import os


# For using locally
database_name = 'personal_web_site'
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

# For production
#database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

''' 
    setup_db(app)
    binds a flask application to SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Diary
'''


class Diaries(db.Model):
    ___tablename__ = 'diaries'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    category = Column(String)
    content = Column(String)
    date = Column(DateTime(timezone=True))
    feeling = Column(Integer)

    def __init__(self, title, category, content, date, feeling):
        self.title = title
        self.category = category
        self.content = content
        self.date = date 
        self.feeling = feeling

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'contnet': self.content,
            'date': self.date,
            'feeling': self.feeling
        }
