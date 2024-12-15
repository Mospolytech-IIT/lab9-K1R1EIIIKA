"""Модели данных для приложения"""
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    posts = relationship('Post', back_populates='user', cascade='all, delete-orphan')


class Post(Base):
    """Модель поста"""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='posts')


DATABASE_URL = "sqlite:///app.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
