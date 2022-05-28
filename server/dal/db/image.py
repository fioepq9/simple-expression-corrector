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

    def save(self):
        db.session.add(self)
        db.session.commit()


class ImageCli:
    sonyflake = SonyFlake()

    @classmethod
    def Upload(cls, name: str, uid: int) -> (int, str):
        """
            Upload image Info to MySQL.

            :param name: filename
            :param uid: uploader id
            :return: (image id, image url)
        """
        pid = ImageCli.sonyflake.next_id()
        url = os.path.join(config.uploadFolder, str(pid) + '_' + name)
        img = Image(Id=pid, Uid=uid, Name=name, Url=url, UploadTime=None)
        img.save()
        return pid, url
