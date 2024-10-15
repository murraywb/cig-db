import os
import re

class Config:
    # Get the DATABASE_URL from Render or fall back to local Postgres
    uri = os.getenv('DATABASE_URL') or 'postgresql://postgres:password@localhost/book_quotes'
    
    # Fix for Heroku-style `postgres://` URL prefix
    if uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
