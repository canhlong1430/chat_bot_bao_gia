from flask import Blueprint, request, jsonify, current_app
from services.product_service import ProductService
from services.template_service import TemplateService
import os
import re

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")

    matches = re.findall(r'/sp\s*:\s*(.+?)\s*/sl\s*:\s*(\d+)', message, re.I)
    print("🐞 matches =", matches)

    if not matches:
        return jsonify({"error": "Sai cú pháp!"}), 400

    # ✅ Luôn truyền file path thực tế
    ps = ProductService(os.path.join(
        current_app.config["UPLOAD_FOLDER"], "products.xlsx"
    ))

    items = []
    for sp_name, sl in matches:
        sp_name = sp_name.strip()
        sl = int(sl)
        sp_data = ps.find_product_detail(sp_name)

        if not sp_data:
            return jsonify({"error": f"Không tìm thấy SP: {sp_name}"}), 404

        unit = sp_data.get('Đvt')

        # Ưu tiên lấy lần lượt: 'Giá bán' → 'Giá bán C1' → 'Giá bán cấp 1'
        price = (
            sp_data.get('Giá bán')
            or sp_data.get('Giá bán C1')
            or sp_data.get('Giá bán cấp 1')
            or None
        )

        if price is None:
            print(f"⚠️ SP '{sp_name}' không có giá ➜ Đặt giá = None hoặc 0 theo yêu cầu")
            price = 0  # Nếu muốn mặc định giá là 0 thì bỏ comment dòng này
        # Gia ban le
        price1 = (
                sp_data.get('Giá bán lẻ')

                or None
        )
        if price1 is None:
            print(f"⚠️ SP '{sp_name}' không có giá ➜ Đặt giá = None hoặc 0 theo yêu cầu")
            price = 0  # Nếu muốn mặc định giá là 0 thì bỏ comment dòng này

        items.append({
            'name': sp_name,
            'quantity': sl,
            'unit': unit,
            'unit_price': price,
            'unit_price1':price1,
            'extra_data': sp_data
        })

    ts = TemplateService(
        current_app.config["TEMPLATE_FOLDER"],
        current_app.config["EXPORT_FOLDER"]
    )

    output_file = ts.export_quote(items)
    return jsonify({"output_file": f"/exports/{output_file}"}), 200
