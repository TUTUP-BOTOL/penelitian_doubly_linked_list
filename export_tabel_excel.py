
import csv
import os

from openpyxl import Workbook
from openpyxl.styles import (
    Font,
    PatternFill,
    Border,
    Side,
    Alignment
)
from openpyxl.utils import get_column_letter


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TABEL_DIR = os.path.join(BASE_DIR, "hasil", "TABEL")

os.makedirs(TABEL_DIR, exist_ok=True)

# Gaya border
thin_border = Border(
    left=Side(style="thin", color="000000"),
    right=Side(style="thin", color="000000"),
    top=Side(style="thin", color="000000"),
    bottom=Side(style="thin", color="000000")
)


def csv_to_excel(csv_name, excel_name, sheet_name, title):

    csv_path = os.path.join(TABEL_DIR, csv_name)
    excel_path = os.path.join(TABEL_DIR, excel_name)

    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    # Membaca CSV
    with open(csv_path, "r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if not rows:
        print(f"File kosong: {csv_name}")
        return

    total_columns = len(rows[0])

    # Judul tabel
    ws.merge_cells(
        start_row=1,
        start_column=1,
        end_row=1,
        end_column=total_columns
    )

    title_cell = ws.cell(row=1, column=1, value=title)
    title_cell.font = Font(
        bold=True,
        size=14,
        color="FFFFFF"
    )
    title_cell.fill = PatternFill(
        "solid",
        fgColor="1F4E78"
    )
    title_cell.alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    ws.row_dimensions[1].height = 30

    # Memasukkan isi CSV
    for row_index, row in enumerate(rows, start=3):

        for col_index, value in enumerate(row, start=1):

            # Konversi angka agar menjadi numerik di Excel
            try:
                value = float(value)

                if value.is_integer():
                    value = int(value)

            except (ValueError, AttributeError):
                pass

            cell = ws.cell(
                row=row_index,
                column=col_index,
                value=value
            )

            cell.border = thin_border
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

            if row_index == 3:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(
                    "solid",
                    fgColor="4472C4"
                )
            else:
                cell.font = Font(size=10)

                if row_index % 2 == 0:
                    cell.fill = PatternFill(
                        "solid",
                        fgColor="D9EAF7"
                    )

                # Format angka desimal
                if isinstance(value, float):
                    cell.number_format = "0.00000000"

    # Mengatur lebar kolom otomatis
    for col in range(1, total_columns + 1):

        max_length = 0

        for row in ws.iter_rows(
            min_col=col,
            max_col=col
        ):
            for cell in row:
                if cell.value is not None:
                    max_length = max(
                        max_length,
                        len(str(cell.value))
                    )

        ws.column_dimensions[
            get_column_letter(col)
        ].width = min(max_length + 4, 35)

    # Mengatur tinggi header
    ws.row_dimensions[3].height = 35

    ws.freeze_panes = "A4"
    ws.auto_filter.ref = (
        f"A3:{get_column_letter(total_columns)}{len(rows)+2}"
    )

    wb.save(excel_path)

    print(f"Berhasil dibuat: {excel_path}")


# Tabel waktu
csv_to_excel(
    "tabel_waktu_ringkasan.csv",
    "tabel_waktu_ringkasan.xlsx",
    "Waktu",
    "HASIL PENGUJIAN WAKTU OPERASI"
)

csv_to_excel(
    "tabel_waktu_detail.csv",
    "tabel_waktu_detail.xlsx",
    "Detail Waktu",
    "DETAIL 10 KALI PENGUJIAN WAKTU"
)

# Tabel memori
csv_to_excel(
    "tabel_memori_ringkasan.csv",
    "tabel_memori_ringkasan.xlsx",
    "Memori",
    "HASIL PENGUJIAN PENGGUNAAN MEMORI"
)

csv_to_excel(
    "tabel_memori_detail.csv",
    "tabel_memori_detail.xlsx",
    "Detail Memori",
    "DETAIL 10 KALI PENGUJIAN MEMORI"
)

print("\nSemua tabel Excel berhasil dibuat!")
