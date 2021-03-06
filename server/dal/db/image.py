from typing import Tuple

import os

import config
from . import db
from sonyflake import SonyFlake


class Image(db.Model):
    # 声明表名
    __tablename__ = 'image'
    # 声明字段
    Id = db.Column('id', db.BIGINT, primary_key=True)
    Uid = db.Column('uid', db.BIGINT)
    Name = db.Column('name', db.VARCHAR(128))
    Url = db.Column('url', db.VARCHAR(8182))
    UploadTime = db.Column('upload_time', db.TIMESTAMP)
    # tools
    sonyflake = SonyFlake()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def Upload(cls, name: str, uid: int) -> Tuple[int, str]:
        """
            Upload image Info to MySQL.

            :param name: filename
            :param uid: uploader id
            :return: (image id, image url)
        """
        pid = cls.sonyflake.next_id()
        url = os.path.join(config.uploadFolder, str(pid) + '_' + name)
        img = Image(Id=pid, Uid=uid, Name=name, Url=url, UploadTime=None)
        img.save()
        return pid, url

    @classmethod
    def QueryUrl(cls, pid: int) -> "str | None":
        """
        Query the save url with id
        :param pid: id
        :return: url
        """
        try:
            img: Image = cls.query.filter_by(Id=pid).first()
        except:
            print('QueryUrl error')
            return None
        else:
            return img.Url
