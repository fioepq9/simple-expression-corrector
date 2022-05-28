from . import db
from sonyflake import SonyFlake


class User(db.Model):
    # 声明表名
    __tablename__ = 'user'
    # 声明字段
    Id = db.Column('id', db.BIGINT, primary_key=True)
    Username = db.Column('username', db.VARCHAR(32))
    Password = db.Column('password', db.VARCHAR(32))
    # 工具
    sonyflake = SonyFlake()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def FindByUsername(cls, username: str) -> 'User':
        """
        Find User By username.

        :param username: username
        :return: user who match the username
        """
        return cls.query.filter_by(Username=username).first()

    @classmethod
    def Create(cls, username: str, password: str) -> ('User', bool):
        """
        Create User with username and password.

        :param username: username
        :param password: password
        :return: is success
        """
        uid = cls.sonyflake.next_id()
        user = User(Id=uid, Username=username, Password=password)
        try:
            user.save()
        except:
            return None, False
        else:
            return user, True
