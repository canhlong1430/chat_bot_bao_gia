import pandas as pd

class ProductService:
    def __init__(self, file_path):
        self.file_path = file_path

    def find_product_detail(self, product_name, logs=None):
        """
        Dò toàn bộ sheet.
        Auto tìm dòng header có 'Sản phẩm'.
        Bỏ qua HOA/thường, strip() dấu cách.
        Tìm theo regex linh hoạt: mỗi dấu cách thành .*
        """
        import re
        xls = pd.ExcelFile(self.file_path)
        # Chuyển mỗi dấu cách thành .*, escape các ký tự đặc biệt
        keyword = product_name.lower().strip()
        regex_pattern = ".*".join([re.escape(part) for part in keyword.split()])
        regex_pattern = rf"{regex_pattern}"


        for sheet in xls.sheet_names:
            print(f"🔍 Đang dò sheet: {sheet}")

            # Tìm dòng header
            preview = pd.read_excel(xls, sheet_name=sheet, header=None, nrows=10)
            header_row = None
            for idx, row in preview.iterrows():
                if row.astype(str).str.contains("Sản phẩm", case=False).any():
                    header_row = idx
                    break

            if header_row is None:
                continue

            df = pd.read_excel(xls, sheet_name=sheet, skiprows=header_row)
            df.columns = df.columns.map(str).str.strip()

            if 'Sản phẩm' not in df.columns:
                continue

            for _, row in df.iterrows():
                name = str(row['Sản phẩm']).lower().strip()
                if re.search(regex_pattern, name):
                    row_data = row.to_dict()
                    row_data['sheet'] = sheet
                    if logs is not None:
                        logs.append(f"🔎 Tìm thấy:<b> {row['Sản phẩm']}</b> tại <b>. Sheet: {sheet} </b>.")
                    print(f"✅ Tìm thấy SP '{product_name}' tại sheet: {sheet}")
                    return row_data

        print(f"❌ Không tìm thấy SP '{product_name}'")
        return None
