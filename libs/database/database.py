from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from .models import Base, User

DATABASE_URL = "sqlite:///./litepix.db"  # Путь к вашей базе данных SQLite

# Создаем подключение к базе данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создаем сессию для взаимодействия с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Создаем все таблицы, если их ещё нет
def init_db():
    Base.metadata.create_all(bind=engine)


# Метод для получения пользователя по ID
def get_user_by_id(user_id: int, db_session):
    """Получить пользователя по ID."""
    return db_session.query(User).filter(User.id == user_id).first()
