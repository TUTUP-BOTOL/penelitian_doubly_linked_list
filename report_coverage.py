import os

os.makedirs("hasil/GRAFIK", exist_ok=True)
os.makedirs("hasil/TABEL", exist_ok=True)

import json
import csv
import os

os.makedirs("hasil", exist_ok=True)

with open("hasil/coverage.json") as file:
    report = json.load(file)

rows = []

for filename, detail in report["files"].items():
    rows.append([
        filename,
        detail["summary"]["num_statements"],
        detail["summary"]["covered_lines"],
        detail["summary"]["missing_lines"],
        detail["summary"]["percent_covered"]
    ])

with open("hasil/tabel_coverage.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "File",
        "Total Baris",
        "Baris Teruji",
        "Baris Belum Teruji",
        "Coverage (%)"
    ])
    writer.writerows(rows)

print("\n=== TABEL CODE COVERAGE ===")
for row in rows:
    print(row)

print("\nTabel tersimpan di hasil/tabel_coverage.csv")
