import datetime
from sqlalchemy import or_, and_
from sqlalchemy.dialects.mysql import *
from sqlalchemy import func
from sqlalchemy.orm import aliased
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://cheat_sheet.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Topic(db.Model):
    __tablename__ = 'Topic'
    TopicId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(256), nullable=False)



if __name__ == '__main__':
    manager.run()
