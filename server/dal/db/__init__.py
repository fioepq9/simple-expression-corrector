from peewee import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

db: SQLAlchemy = SQLAlchemy()


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}:{}/{}'.format(
        config.MySQL_user,
        config.MySQL_passwd,
        config.MySQL_host,
        config.MySQL_port,
        config.MySQL_db,
    )
    # 设置sqlalchemy自动更跟踪数据库
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True

    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

    global db
    db = SQLAlchemy(app)



class MySQLModel(Model):
    class Meta:
        database = db


class ImageOld(MySQLModel):
    Id = BigIntegerField(column_name='id')
    Uid = BigIntegerField(column_name='uid')
    Name = TextField(column_name='name')
    Url = CharField(column_name='url')
    UploadTime = TimestampField(column_name='upload_time')


class UserOld(MySQLModel):
    Id = BigIntegerField(column_name='id')
    Username = CharField(column_name='username', max_length=32)
    Password = CharField(column_name='password', max_length=32)
