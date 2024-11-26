from bcrypt import checkpw
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @staticmethod
    def get_by_id(user_id: int, db_session: Session):
        """Получить пользователя по ID."""
        return db_session.query(User).filter(User.id == user_id).first()
