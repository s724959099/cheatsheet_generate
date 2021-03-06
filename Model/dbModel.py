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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cheat_sheet.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Topic(db.Model):
    __tablename__ = 'Topic'
    TopicId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(256), nullable=False)
    SoftDelete = db.Column(db.Integer, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    Html = db.Column(db.TEXT, nullable=True)
    MarkDown = db.Column(db.TEXT, nullable=True)
    Table = db.relationship('Table', backref='Topic', lazy='dynamic')

    def __init__(
            self,
            Name,
            CreateBy,
            Html=None,
            MarkDown=None,
    ):
        self.Name = Name
        self.SoftDelete = False
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.Html = Html
        self.MarkDown = MarkDown


class Table(db.Model):
    __tablename__ = 'Table'
    TableId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TopicId = db.Column(db.Integer, db.ForeignKey("Topic.TopicId"), nullable=False)
    Title = db.Column(db.String(256), nullable=False)
    SubTitle = db.Column(db.String(256), nullable=False)
    Color = db.Column(db.String(256), nullable=False)
    SoftDelete = db.Column(db.Integer, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    TableColumn= db.relationship('TableColumn', backref='Table', lazy='dynamic')

    def __init__(
            self,
            TopicId,
            Title,
            SubTitle,
            Color,
            CreateBy,
    ):
        self.TopicId = TopicId
        self.Title = Title
        self.SubTitle = SubTitle
        self.Color = Color
        self.SoftDelete = False
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.ModifiedDate = None
        self.ModifiedBy = None


class TableColumn(db.Model):
    __tablename__ = 'TableColumn'
    TableColumnId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TableId = db.Column(db.Integer, db.ForeignKey("Table.TableId"), nullable=False)
    Name = db.Column(db.String(256), nullable=False)
    Comment = db.Column(db.String(256), nullable=True)
    SoftDelete = db.Column(db.Integer, nullable=False)
    CreateDate = db.Column(db.DateTime(timezone=True), nullable=False)
    CreateBy = db.Column(db.String(128), nullable=False)
    ModifiedDate = db.Column(db.DateTime(timezone=True), nullable=True)
    ModifiedBy = db.Column(db.String(128), nullable=True)
    Html = db.Column(db.TEXT, nullable=True)
    MarkDown = db.Column(db.TEXT, nullable=True)

    def __init__(
            self,
            TableId,
            Name,
            CreateBy,
            Comment=None,
            Html=None,
            MarkDown=None,
    ):
        self.TableId = TableId
        self.Name = Name
        self.SoftDelete = False
        self.CreateDate = datetime.datetime.now()
        self.CreateBy = CreateBy
        self.Comment = Comment
        self.ModifiedDate = None
        self.ModifiedBy = None
        self.Html = Html
        self.MarkDown = MarkDown


if __name__ == '__main__':
    manager.run()
