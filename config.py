# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    DEBUG = False

    UPLOAD_FOLDER   = os.getenv("UPLOAD_FOLDER",   os.path.join(BASE_DIR, "uploads"))
    TEMPLATE_FOLDER = os.getenv("TEMPLATE_FOLDER", os.path.join(BASE_DIR, "uploads", "templates"))
    EXPORT_FOLDER   = os.getenv("EXPORT_FOLDER",   os.path.join(BASE_DIR, "exports"))

os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.TEMPLATE_FOLDER, exist_ok=True)
os.makedirs(Config.EXPORT_FOLDER, exist_ok=True)
