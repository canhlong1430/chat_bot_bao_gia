# app.py
from flask import Flask, render_template, send_from_directory, current_app
from routes.chat import chat_bp
from routes.upload import upload_bp
from dotenv import load_dotenv
import os

# nạp biến môi trường từ .env (nếu có)
load_dotenv()

app = Flask(__name__)
app.config.from_object("config.Config")

# Đăng ký blueprint
app.register_blueprint(chat_bp)
app.register_blueprint(upload_bp)

# đảm bảo thư mục tồn tại khi chạy bằng systemd
os.makedirs(app.config["EXPORT_FOLDER"], exist_ok=True)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Health check (để kiểm tra nhanh)
@app.route("/healthz")
def healthz():
    return "ok", 200

# Giao diện chính
@app.route("/")
def index():
    return render_template("chatbot_ui_dark.html")

# Serve file xuất báo giá (Flask ≥2.2 dùng tham số 'path')
@app.route("/exports/<path:filename>")
def download_file(filename):
    return send_from_directory(
        directory=current_app.config["EXPORT_FOLDER"],
        path=filename,            # nếu dùng Flask <2.2 thì đổi thành: filename=filename
        as_attachment=True
    )

# Chỉ dùng khi chạy local/dev. Trên VPS sẽ chạy bằng Gunicorn, KHÔNG vào nhánh này.
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
