import os
import datetime
import xlwings as xw

class TemplateService:
    def __init__(self, template_folder, export_folder):
        self.template_folder = template_folder
        self.export_folder = export_folder

    def export_quote(self, items, start_row=15, template_file_name="baogia_template.xlsx", sheet_idx=0):
        """
        items: list dict. VD: [{'name':'A',...}]
        start_row: dòng mẫu (template row) dùng để clone format
        """
        template_path = os.path.join(self.template_folder, template_file_name)
        os.makedirs(self.export_folder, exist_ok=True)
        out_name = f"BaoGia_{datetime.datetime.now():%Y%m%d%H%M%S}.xlsx"
        output_path = os.path.join(self.export_folder, out_name)

        app = xw.App(visible=False)
        wb = app.books.open(template_path)
        ws = wb.sheets[sheet_idx]

        # 1. Insert đủ dòng trống bên dưới dòng mẫu
        n = len(items)
        if n > 1:
            # Insert n-1 dòng sau start_row (vì dòng đầu là mẫu)
            for i in range(n-1):
                ws.api.Rows(start_row + 1).Insert()  # luôn insert tại vị trí sau dòng mẫu

            # 2. Copy style/merge dòng mẫu xuống các dòng vừa insert
            # (Dòng mẫu là start_row, dòng vừa insert nằm dưới)
            for i in range(1, n):
                src = ws.range(f"A{start_row}:I{start_row}").api
                tgt = ws.range(f"A{start_row + i}:I{start_row + i}").api
                src.Copy(Destination=tgt)

        # 3. Gán value cho từng dòng
        for idx, item in enumerate(items):
            row = start_row + idx
            ws[f"A{row}"].value = idx + 1
            ws[f"C{row}"].value = item.get('name', '')
            ws[f"D{row}"].value = item.get('quantity', 0)
            ws[f"E{row}"].value = item.get('unit', '')
            ws[f"F{row}"].value = item.get('unit_price', 0)
            ws[f"G{row}"].value = item.get('unit_price', 0) * item.get('quantity', 0)
            # Approved
            extra = item.get('extra_data', {})
            approved = extra.get('Giá bán C1 Có VAT', 0)
            ws[f"H{row}"].value = approved
            ws[f"I{row}"].value = approved * item.get('quantity', 0)

        # (Tuỳ chọn) Nếu muốn clear các dòng dư phía dưới có sẵn trong template, tự xử lý thêm!

        wb.save(output_path)
        wb.close()
        app.quit()
        return out_name
