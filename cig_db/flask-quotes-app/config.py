import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:password@localhost/book_quotes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


