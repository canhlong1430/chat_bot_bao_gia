import os

class Config:
    BASE_DIR = os.getcwd()
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, "uploads", "templates")  # <-- QUAN TRỌNG!
    EXPORT_FOLDER = os.path.join(BASE_DIR, "exports")
