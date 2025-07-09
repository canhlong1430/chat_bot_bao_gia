from flask import Flask, render_template, send_from_directory, current_app
from routes.chat import chat_bp
from routes.upload import upload_bp
import os

app = Flask(__name__)
app.config.from_object("config.Config")

# Register routes
app.register_blueprint(chat_bp)
app.register_blueprint(upload_bp)

# Giao diện chính
@app.route("/")
def index():
    return render_template("chatbot_ui_dark.html")

# Serve file xuất báo giá
@app.route('/exports/<path:filename>')
def download_file(filename):
    return send_from_directory(
        directory=current_app.config["EXPORT_FOLDER"],
        path=filename,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
