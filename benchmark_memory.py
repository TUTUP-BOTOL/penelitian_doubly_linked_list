
import tracemalloc
import csv
import os
import gc
import matplotlib.pyplot as plt

from statistics import mean
from typing import Generic, TypeVar


# ==============================
# PENGATURAN
# ==============================

T = TypeVar("T")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HASIL_DIR = os.path.join(BASE_DIR, "hasil")
TABEL_DIR = os.path.join(HASIL_DIR, "TABEL")
GRAFIK_DIR = os.path.join(HASIL_DIR, "GRAFIK")

os.makedirs(TABEL_DIR, exist_ok=True)
os.makedirs(GRAFIK_DIR, exist_ok=True)

SIZES = [10_000, 50_000, 100_000, 250_000, 500_000]
REPEAT = 10


# ==============================
# 1. LINKED LIST BIASA
# ==============================

class NodePlain:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


# ==============================
# 2. LINKED LIST GENERIC
# ==============================

class NodeGeneric(Generic[T]):
    def __init__(self, data: T):
        self.data = data
        self.prev = None
        self.next = None


# ==============================
# 3. GENERIC + SLOTS
# ==============================

class NodeOptimized(Generic[T]):
    __slots__ = ("data", "prev", "next")

    def __init__(self, data: T):
        self.data = data
        self.prev = None
        self.next = None


# ==============================
# MEMBUAT NODE
# ==============================

def build_nodes(n, node_class):
    head = None
    tail = None

    for i in range(n):
        node = node_class(i)

        if head is None:
            head = tail = node
        else:
            node.prev = tail
            tail.next = node
            tail = node

    return head


# ==============================
# MENGUKUR MEMORI
# ==============================

def measure_memory(n, node_class):
    measurements = []

    for _ in range(REPEAT):
        gc.collect()

        tracemalloc.start()

        head = build_nodes(n, node_class)

        current, peak = tracemalloc.get_traced_memory()

        measurements.append(peak / 1024)

        del head

        tracemalloc.stop()
        gc.collect()

    return measurements


# ==============================
# JENIS LINKED LIST
# ==============================

classes = {
    "Linked List Biasa": NodePlain,
    "Generic": NodeGeneric,
    "Generic + Slots": NodeOptimized
}


# ==============================
# MENJALANKAN PENGUJIAN
# ==============================

detail_results = []
summary_results = []

for n in SIZES:

    print(f"\nJumlah Node: {n}")

    for name, node_class in classes.items():

        measurements = measure_memory(n, node_class)

        avg_memory = mean(measurements)

        print(
            f"{name}: {avg_memory:.2f} KB"
        )

        summary_results.append([
            n,
            name,
            avg_memory,
            min(measurements),
            max(measurements)
        ])

        for i, memory in enumerate(measurements):
            detail_results.append([
                n,
                name,
                i + 1,
                memory
            ])


# ==============================
# TABEL DETAIL 10 PENGUJIAN
# ==============================

detail_path = os.path.join(
    TABEL_DIR, "tabel_memori_detail.csv"
)

with open(detail_path, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Jumlah Node",
        "Jenis Linked List",
        "Pengujian Ke",
        "Memori (KB)"
    ])

    writer.writerows(detail_results)


# ==============================
# TABEL RINGKASAN MEMORI
# ==============================

summary_path = os.path.join(
    TABEL_DIR, "tabel_memori_ringkasan.csv"
)

with open(summary_path, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Jumlah Node",
        "Jenis Linked List",
        "Rata-rata Memori (KB)",
        "Memori Minimum (KB)",
        "Memori Maksimum (KB)"
    ])

    writer.writerows(summary_results)


# ==============================
# GRAFIK PERBANDINGAN MEMORI
# ==============================

plt.figure(figsize=(10, 6))

for name in classes:

    x = []
    y = []

    for n, label, avg, minimum, maximum in summary_results:

        if label == name:
            x.append(n)
            y.append(avg)

    plt.plot(x, y, marker="o", label=name)


plt.title("Perbandingan Penggunaan Memori Doubly Linked List")
plt.xlabel("Jumlah Node")
plt.ylabel("Penggunaan Memori (KB)")
plt.legend()
plt.grid(True)

plt.savefig(
    os.path.join(GRAFIK_DIR, "grafik_memory.png"),
    dpi=300
)

plt.close()


print("\n================================")
print("PENGUJIAN MEMORI SELESAI")
print("================================")
print("Tabel detail:", detail_path)
print("Tabel ringkasan:", summary_path)
print("Grafik tersimpan di:", GRAFIK_DIR)
