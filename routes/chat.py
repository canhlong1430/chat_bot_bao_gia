from flask import Blueprint, request, jsonify, current_app
from services.product_service import ProductService
from services.template_service import TemplateService
import os
import re

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    logs = []  # ✅ Danh sách log để phản hồi về cho client

    data = request.json
    message = data.get("message", "")


    # New syntax: each line is <product>:<quantity> Đã match
    matches = []
    for line in message.splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r'^(.+?):\s*(\d+)$', line)
        if m:
            matches.append((m.group(1).strip(), int(m.group(2))))
    logs.append(f"🐞 matches = {matches}")

    if not matches:
        logs.append("❌ Sai cú pháp! Định dạng đúng: mỗi dòng là <sản phẩm>:<số lượng>")
        return jsonify({"error": "Sai cú pháp! Định dạng đúng: mỗi dòng là <sản phẩm>:<số lượng>", "logs": logs}), 400

    ps = ProductService(os.path.join(
        current_app.config["UPLOAD_FOLDER"], "products.xlsx"
    ))

    items = []
    for sp_name, sl in matches:
        sp_name = sp_name.strip()
        sl = int(sl)
        sp_data = ps.find_product_detail(sp_name, logs)

        if not sp_data:
            logs.append(f"❌ Không tìm thấy SP: {sp_name}")
            return jsonify({"error": f"Không tìm thấy SP: {sp_name}", "logs": logs}), 404

        unit = sp_data.get('Đvt')
        fullname = sp_data.get('Sản phẩm')
        price = (
            sp_data.get('Giá bán')
            or sp_data.get('Giá bán C1')
            or sp_data.get('Giá bán cấp 1')
            or None
        )

        if price is None:
            logs.append(f"⚠️ SP '{sp_name}' không có giá ➜ Đặt giá = 0")
            price = 0

        price1 = sp_data.get('Giá bán lẻ') or None
        if price1 is None:
            logs.append(f"⚠️ SP '{sp_name}' không có giá lẻ ➜ Đặt giá = 0")
            price1 = 0

        logs.append(f"Số lượng: {sl}, Giá: {price}, Giá lẻ: {price1}")

        items.append({
            'name': fullname,
            'quantity': sl,
            'unit': unit,
            'unit_price': price,
            'unit_price1': price1,
            'extra_data': sp_data
        })

    ts = TemplateService(
        current_app.config["TEMPLATE_FOLDER"],
        current_app.config["EXPORT_FOLDER"]
    )

    output_file = ts.export_quote(items)
    logs.append(f"✅ Xuất file thành công: /exports/{output_file}")

    return jsonify({
        "output_file": f"/exports/{output_file}",
        "logs": logs
    }), 200
