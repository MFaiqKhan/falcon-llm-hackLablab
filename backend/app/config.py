import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEEPGRAM_API_KEY = os.environ.get('DEEPGRAM_API_KEY')
    AI71_API_KEY = os.environ.get('AI71_API_KEY')
    ZILLIZ_CLOUD_URI = os.environ.get('ZILLIZ_CLOUD_URI')
    ZILLIZ_CLOUD_TOKEN = os.environ.get('ZILLIZ_CLOUD_TOKEN')
