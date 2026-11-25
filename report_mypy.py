import os

os.makedirs("hasil/GRAFIK", exist_ok=True)
os.makedirs("hasil/TABEL", exist_ok=True)

import subprocess
import csv
import os

os.makedirs("hasil", exist_ok=True)

result = subprocess.run(
    ["mypy", "--strict", "typecheck_demo.py"],
    capture_output=True,
    text=True
)

output = result.stdout + result.stderr

errors = [
    line for line in output.splitlines()
    if ": error:" in line
]

type_errors = [
    line for line in errors
    if "[arg-type]" in line
]

implementation_errors = [
    line for line in errors
    if "[arg-type]" not in line
]

detected = len(type_errors) > 0

# Data tabel
headers = [
    "No",
    "Skenario Pengujian",
    "Tipe Diharapkan",
    "Tipe Aktual",
    "Hasil"
]

rows = [
    [
        1,
        "Memasukkan angka ke list integer",
        "int",
        "int",
        "Diterima"
    ],
    [
        2,
        "Memasukkan teks ke list integer",
        "int",
        "str",
        "Terdeteksi" if detected else "Tidak terdeteksi"
    ]
]

# Simpan CSV
with open("hasil/tabel_mypy.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)

# Tampilkan tabel di terminal
print("\n" + "=" * 85)
print("              TABEL HASIL PENGUJIAN TYPE SAFETY")
print("=" * 85)

print(
    f"{'No':<5}"
    f"{'Skenario Pengujian':<38}"
    f"{'Diharapkan':<13}"
    f"{'Aktual':<10}"
    f"{'Hasil':<15}"
)

print("-" * 85)

for row in rows:
    print(
        f"{row[0]:<5}"
        f"{row[1]:<38}"
        f"{row[2]:<13}"
        f"{row[3]:<10}"
        f"{row[4]:<15}"
    )

print("=" * 85)

print("\nRINGKASAN PENGUJIAN")
print("Kesalahan tipe data :", len(type_errors))
print("Kesalahan implementasi :", len(implementation_errors))

if detected and not implementation_errors:
    print("Status: PENGUJIAN BERHASIL")
else:
    print("Status: PERLU DIPERIKSA")

print("\nDetail pesan MyPy:")
print(output)

print("\nTabel berhasil disimpan:")
print("hasil/tabel_mypy.csv")
