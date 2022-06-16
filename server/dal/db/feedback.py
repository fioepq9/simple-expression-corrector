from . import db
from sonyflake import SonyFlake


class Feedback(db.Model):
    # 声明表名
    __tablename__ = 'feedback'
    # 声明字段
    Id = db.Column('id', db.BIGINT, primary_key=True)
    user_id = db.Column('user_id', db.BIGINT)
    upload_id = db.Column('upload_id', db.BIGINT)
    judge_id = db.Column('judge_id', db.BIGINT)
    email = db.Column('email', db.VARCHAR(32))
    description = db.Column('description', db.VARCHAR(500))
    # tools
    sonyflake = SonyFlake()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def FeedBack(cls, user_id: int, upload_id: int, judge_id: int, email: str, description: str):
        """
            Save Bug Info to MySQL.
        """
        id = cls.sonyflake.next_id()
        img = Feedback(
            Id=id,
            user_id=user_id,
            upload_id=upload_id,
            judge_id=judge_id,
            email=email,
            description=description)
        img.save()
        return
