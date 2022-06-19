from typing import Tuple

import os

import config
from . import db
from sonyflake import SonyFlake


class JudgeImage(db.Model):
    # 声明表名
    __tablename__ = 'judge_image'
    # 声明字段
    Id = db.Column('id', db.BIGINT, primary_key=True)
    Pid = db.Column('pid', db.BIGINT)
    Name = db.Column('name', db.VARCHAR(128))
    Url = db.Column('url', db.VARCHAR(8182))
    UploadTime = db.Column('upload_time', db.TIMESTAMP)
    # tools
    sonyflake = SonyFlake()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def Upload(cls, name: str, pid: int) -> Tuple[int, str]:
        """
            Upload image Info to MySQL.

            :param name: filename
            :param uid: uploader id
            :return: (image id, image url)
        """
        sony_id = cls.sonyflake.next_id()
        url = os.path.join(config.judgeFolder, str(sony_id) + '_' + name)
        img = JudgeImage(
                Id=sony_id, Pid=pid, Name=name, Url=url, UploadTime=None)
        img.save()
        return sony_id, url
