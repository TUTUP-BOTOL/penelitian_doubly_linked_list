import os

os.makedirs("hasil/GRAFIK", exist_ok=True)
os.makedirs("hasil/TABEL", exist_ok=True)

import time
import csv
import os
from statistics import mean

from doubly_linked_list import DoublyLinkedList


SIZES = [10_000, 50_000, 100_000, 250_000, 500_000]
REPEAT = 10

os.makedirs("hasil", exist_ok=True)


def create_list(n):
    dll = DoublyLinkedList[int]()

    for i in range(n):
        dll.append(i)

    return dll


def benchmark_insert(n):
    results = []

    for _ in range(REPEAT):
        dll = create_list(n)
        middle = n // 2

        start = time.perf_counter()
        dll.insert_at_index(middle, -1)
        end = time.perf_counter()

        results.append(end - start)

    return results


def benchmark_delete(n):
    results = []

    for _ in range(REPEAT):
        dll = create_list(n)
        middle = n // 2

        start = time.perf_counter()
        dll.delete_at_index(middle)
        end = time.perf_counter()

        results.append(end - start)

    return results


data = []

for n in SIZES:
    insert_times = benchmark_insert(n)
    delete_times = benchmark_delete(n)

    print(f"\nJumlah data: {n}")
    print(f"Insert tengah: {mean(insert_times):.8f} detik")
    print(f"Delete tengah: {mean(delete_times):.8f} detik")

    for i in range(REPEAT):
        data.append([
            n,
            i + 1,
            insert_times[i],
            delete_times[i]
        ])


with open("hasil/benchmark_time.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Jumlah_Data",
        "Pengujian",
        "Insert_Detik",
        "Delete_Detik"
    ])

    writer.writerows(data)


print("\nHasil disimpan di hasil/benchmark_time.csv")


import matplotlib.pyplot as plt

for operation, column, title in [
    ("Insert", 2, "Waktu Penyisipan di Tengah"),
    ("Delete", 3, "Waktu Penghapusan di Tengah")
]:
    plt.figure(figsize=(10, 6))

    x = []
    y = []

    for n in SIZES:
        times = [
            row[column]
            for row in data
            if row[0] == n
        ]

        x.append(n)
        y.append(mean(times))

    plt.plot(x, y, marker="o")

    plt.title(title)
    plt.xlabel("Jumlah Node")
    plt.ylabel("Waktu (Detik)")
    plt.grid(True)

    plt.savefig(
        f"hasil/GRAFIK/grafik_{operation.lower()}.png",
        dpi=300
    )

    plt.close()

print("Grafik waktu berhasil dibuat!")




import time
import csv
import os
import matplotlib.pyplot as plt
from statistics import mean

from doubly_linked_list import DoublyLinkedList


# ==============================
# PENGATURAN
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HASIL_DIR = os.path.join(BASE_DIR, "hasil")
TABEL_DIR = os.path.join(HASIL_DIR, "TABEL")
GRAFIK_DIR = os.path.join(HASIL_DIR, "GRAFIK")

os.makedirs(TABEL_DIR, exist_ok=True)
os.makedirs(GRAFIK_DIR, exist_ok=True)

SIZES = [10_000, 50_000, 100_000, 250_000, 500_000]
REPEAT = 10


# ==============================
# MEMBUAT LINKED LIST
# ==============================

def create_list(n):
    dll = DoublyLinkedList[int]()

    for i in range(n):
        dll.append(i)

    return dll


# ==============================
# BENCHMARK INSERT
# ==============================

def benchmark_insert(n):
    results = []

    for _ in range(REPEAT):
        dll = create_list(n)
        middle = n // 2

        start = time.perf_counter()
        dll.insert_at_index(middle, -1)
        end = time.perf_counter()

        results.append(end - start)

    return results


# ==============================
# BENCHMARK DELETE
# ==============================

def benchmark_delete(n):
    results = []

    for _ in range(REPEAT):
        dll = create_list(n)
        middle = n // 2

        start = time.perf_counter()
        dll.delete_at_index(middle)
        end = time.perf_counter()

        results.append(end - start)

    return results


# ==============================
# MENJALANKAN PENGUJIAN
# ==============================

data = []

for n in SIZES:
    insert_times = benchmark_insert(n)
    delete_times = benchmark_delete(n)

    print(f"\nJumlah data: {n}")
    print(f"Insert rata-rata: {mean(insert_times):.8f} detik")
    print(f"Delete rata-rata: {mean(delete_times):.8f} detik")

    for i in range(REPEAT):
        data.append([
            n,
            i + 1,
            insert_times[i],
            delete_times[i]
        ])


# ==============================
# TABEL DETAIL 10 PENGUJIAN
# ==============================

detail_path = os.path.join(
    TABEL_DIR, "tabel_waktu_detail.csv"
)

with open(detail_path, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Jumlah Data",
        "Pengujian Ke",
        "Insert (Detik)",
        "Delete (Detik)"
    ])

    writer.writerows(data)


# ==============================
# TABEL RINGKASAN
# ==============================

summary_path = os.path.join(
    TABEL_DIR, "tabel_waktu_ringkasan.csv"
)

with open(summary_path, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Jumlah Data",
        "Rata-rata Insert (Detik)",
        "Rata-rata Delete (Detik)",
        "Insert Tercepat (Detik)",
        "Delete Tercepat (Detik)"
    ])

    for n in SIZES:
        insert_times = [
            row[2] for row in data if row[0] == n
        ]

        delete_times = [
            row[3] for row in data if row[0] == n
        ]

        writer.writerow([
            n,
            mean(insert_times),
            mean(delete_times),
            min(insert_times),
            min(delete_times)
        ])


# ==============================
# GRAFIK INSERT DAN DELETE
# ==============================

for operation, column, title in [
    ("insert", 2, "Waktu Penyisipan di Tengah"),
    ("delete", 3, "Waktu Penghapusan di Tengah")
]:

    x = []
    y = []

    for n in SIZES:
        times = [
            row[column] for row in data if row[0] == n
        ]

        x.append(n)
        y.append(mean(times))

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker="o")

    plt.title(title)
    plt.xlabel("Jumlah Node")
    plt.ylabel("Waktu (Detik)")
    plt.grid(True)

    plt.savefig(
        os.path.join(GRAFIK_DIR, f"grafik_{operation}.png"),
        dpi=300
    )

    plt.close()


print("\n================================")
print("PENGUJIAN WAKTU SELESAI")
print("================================")
print("Tabel detail:", detail_path)
print("Tabel ringkasan:", summary_path)
print("Grafik tersimpan di:", GRAFIK_DIR)



