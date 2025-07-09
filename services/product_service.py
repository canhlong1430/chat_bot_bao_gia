import pandas as pd

class ProductService:
    def __init__(self, file_path):
        self.file_path = file_path

    def find_product_detail(self, product_name):
        """
        Dò toàn bộ sheet.
        Auto tìm dòng header có 'Sản phẩm'.
        Bỏ qua HOA/thường, strip() dấu cách.
        Tìm theo 'chứa' để linh hoạt hơn.
        """
        xls = pd.ExcelFile(self.file_path)
        keyword = product_name.lower().strip()

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
                if keyword in name:
                    row_data = row.to_dict()
                    row_data['sheet'] = sheet
                    print(f"✅ Tìm thấy SP '{product_name}' tại sheet: {sheet}")
                    return row_data

        print(f"❌ Không tìm thấy SP '{product_name}'")
        return None
