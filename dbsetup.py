from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


# Db setup
Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    password = Column(String(250))


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            }


class Movies(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String(250), nullable=False)
    cover = Column(String(250), nullable=False)
    category = Column(String(80), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    cat_rel = relationship(Categories)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.title,
            'year': self.year,
            'description': self.description,
            'category': self.category,
            'category_id': self.category_id,
            'movie id': self.id,
            }


engine = create_engine('sqlite:///movies.db')
Base.metadata.create_all(engine)
