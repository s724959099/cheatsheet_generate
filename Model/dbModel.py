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
    SoftDelete = db.Column(TINYINT, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    Html = db.Column(db.TEXT, nullable=True)
    MarkDown = db.Column(db.TEXT, nullable=True)


class Table(db.Model):
    __tablename__ = 'Table'
    TableId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TopicId = db.Column(db.Integer, db.ForeignKey("Topic.TopicId"),nullable=False)
    Name = db.Column(db.String(256), nullable=False)
    Color = db.Column(db.String(256), nullable=False)
    SoftDelete = db.Column(TINYINT, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)


class TableColumn(db.Model):
    __tablename__ = 'TableColumn'
    TableColumnId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TableId = db.Column(db.Integer, db.ForeignKey("Table.TableId"), nullable=False)
    Name = db.Column(db.String(256), nullable=False)
    Comment = db.Column(db.String(256), nullable=True)
    SoftDelete = db.Column(TINYINT, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    Html = db.Column(db.TEXT, nullable=True)
    MarkDown = db.Column(db.TEXT, nullable=True)


if __name__ == '__main__':
    manager.run()
