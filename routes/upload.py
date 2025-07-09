from flask import Blueprint, request, jsonify, current_app
import os

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload/products", methods=["POST"])
def upload_products():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Missing file"}), 400

    path = os.path.join(current_app.config["UPLOAD_FOLDER"], "products.xlsx")
    file.save(path)

    return jsonify({"message": "Uploaded product file"}), 200
