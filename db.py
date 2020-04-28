from sqlalchemy import Column, String, DateTime, JSON, create_engine
from flask_sqlalchemy import SQLAlchemy

database_name = 'vid_directory'
database_path = 'postgres://{}/{}'.format('localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    """
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Videos(db.Model):
    __tablename__ = 'videos'
    videoId = Column(String, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    thumbnails = Column(JSON)
    publishedAt = Column(DateTime, index=True)
    # can use brin index to optimize queries
    channelTitle = Column(String)

    def __init__(
        self,
        videoId,
        title,
        description,
        thumbnails,
        publishedAt,
        channelTitle,
    ):  # noqa
        self.videoId = videoId
        self.title = title
        self.description = description
        self.thumbnails = thumbnails
        self.publishedAt = publishedAt
        self.channelTitle = channelTitle

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'videoId': self.videoId,
            'title': self.title,
            'description': self.description,
            'thumbnails': self.thumbnails,
            'channelTitle': self.channelTitle,
            'publishedAt': self.publishedAt,
        }


"""
class Channels(db.Model):  
  __tablename__ = 'channels'

    channelId = Column(String, primary_key=True)
    channelTitle = Column(String)

    def __init__(self, channelId, channelTitle):
        self.channelId = channelId
        self.channelTitle = channelTitle

    def format(self):
        return {
            'channelId': self.channelId,
            'channelTitle': self.channelTitle
        }
"""
