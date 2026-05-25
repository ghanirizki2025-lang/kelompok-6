"""
benchmark.py
Pengujian performa (Big-O) untuk 6 Modul Sistem Logistik Bencana
Kelompok 6 | ELT60213 Algoritma dan Struktur Data

Modul yang diuji:
  1. modul_Graph   -> tambah_rute, get_tetangga, bfs_deteksi_terjangkau
  2. modul_BST     -> insert, search, update_level, inorder
  3. modul_Queue   -> kirim_enqueue, proses_bantuan_dequeue
  4. modul_Stack   -> push, pop, tampilkan_log
  5. modul_Dijkstra-> hitung_dijkstra, selection_sort (LinkedList)
  6. modul_CLI     -> audit_jarak (integrasi semua modul)
"""

import sys
import os
import time
import random
from dataclasses import dataclass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from data_structures.BST_Registry_Lokasi import BSTLokasi
from modules.modul_Graph    import GraphJaringanRute
from modules.modul_Queue    import PriorityQueueBantuan
from modules.modul_Stack    import StackLogPengiriman
from modules.modul_Dijkstra import DijkstraAuditJarak, LinkedListJarak
import modules.modul_BST as bst_utils

random.seed(42)

SEP  = "=" * 65
SEP2 = "-" * 65


# ══════════════════════════════════════════════════════════════
# HELPER
# ══════════════════════════════════════════════════════════════

@dataclass
class Lokasi:
    kode: str
    nama: str
    level: int
    populasi: int


def ukur(fn, *args, ulang=5):
    """Jalankan fn(*args) sebanyak `ulang` kali, kembalikan rata-rata ms."""
    times = []
    for _ in range(ulang):
        t0 = time.perf_counter()
        fn(*args)
        times.append((time.perf_counter() - t0) * 1000)
    return sum(times) / len(times)


def header(judul):
    print(f"\n{SEP}")
    print(f"  {judul}")
    print(SEP)


def baris(label, n, ms, bigo):
    print(f"  {label:<30} N={n:<6} {ms:>9.4f} ms   {bigo}")


def cetak_tabel(label_kolom, rows):
    print(f"\n  {'N':<8}", end="")
    for lbl in label_kolom:
        print(f"  {lbl:>15}", end="")
    print()
    print("  " + "-" * (8 + 17 * len(label_kolom)))
    for row in rows:
        print(f"  {row[0]:<8}", end="")
        for val in row[1:]:
            print(f"  {val:>15.4f}", end="")
        print()


# ══════════════════════════════════════════════════════════════
# GENERATOR DATA
# ══════════════════════════════════════════════════════════════

def buat_graph(n_node, n_edge=None):
    """Graph dengan n_node node dan n_edge edge acak."""
    g = GraphJaringanRute()
    kodes = [f"L{i:03d}" for i in range(n_node)]
    for k in kodes:
        g.tambah_rute(k, k, 0)   # daftarkan node
    n_edge = n_edge or min(n_node * 2, n_node * (n_node - 1) // 2)
    edges_added = set()
    attempts = 0
    while len(edges_added) < n_edge and attempts < n_edge * 10:
        a, b = random.sample(kodes, 2)
        key  = tuple(sorted([a, b]))
        if key not in edges_added:
            bobot = random.randint(1, 100)
            g.tambah_rute(a, b, bobot)
            edges_added.add(key)
        attempts += 1
    return g, kodes


def buat_lokasi_list(n):
    levels = [1, 2, 3]
    return [
        Lokasi(f"L{i:03d}", f"Lokasi {i}", random.choice(levels), random.randint(100, 5000))
        for i in range(n)
    ]


def buat_bst(n):
    bst  = BSTLokasi()
    loks = buat_lokasi_list(n)
    for lok in loks:
        bst.insert(lok)
    return bst, loks


# ══════════════════════════════════════════════════════════════
# MODUL 1 – GRAPH JARINGAN RUTE
# ══════════════════════════════════════════════════════════════

def bench_graph():
    header("MODUL 1 — GraphJaringanRute")
    print(f"  {'Operasi':<30} {'N':<6}  {'Waktu (ms)':>12}   Big-O")
    print(f"  {SEP2}")

    # tambah_rute
    rows_tambah = []
    for n in [50, 100, 200, 500]:
        g = GraphJaringanRute()
        kodes = [f"L{i:03d}" for i in range(n)]

        def _tambah():
            a, b = random.sample(kodes, 2)
            g.tambah_rute(a, b, random.randint(1, 100))

        ms = ukur(_tambah)
        baris("tambah_rute", n, ms, "O(1)")
        rows_tambah.append((n, ms))

    # get_tetangga
    print()
    for n in [50, 100, 200, 500]:
        g, kodes = buat_graph(n)
        node = kodes[0]
        ms   = ukur(g.get_tetangga, node)
        baris("get_tetangga", n, ms, "O(deg)")

    # bfs_deteksi_terjangkau
    print()
    rows_bfs = []
    for n in [50, 100, 200, 500]:
        g, kodes = buat_graph(n)
        ms = ukur(g.bfs_deteksi_terjangkau, kodes[0])
        baris("bfs_deteksi_terjangkau", n, ms, "O(V+E)")
        rows_bfs.append((n, ms))

    print(f"\n  Analisis BFS:")
    print(f"  {'N':<8} {'ms':>10}")
    for n, ms in rows_bfs:
        print(f"  {n:<8} {ms:>10.4f}")


# ══════════════════════════════════════════════════════════════
# MODUL 2 – BST REGISTRY LOKASI
# ══════════════════════════════════════════════════════════════

def bench_bst():
    header("MODUL 2 — BSTLokasi (BST Registry Lokasi)")
    print(f"  {'Operasi':<30} {'N':<6}  {'Waktu (ms)':>12}   Big-O")
    print(f"  {SEP2}")

    rows = {"insert": [], "search": [], "inorder": []}

    for n in [50, 100, 200, 500]:
        bst, loks = buat_bst(n)

        # insert
        def _insert():
            lok = Lokasi(f"X{random.randint(0,9999):04d}", "Test", 1, 100)
            bst.insert(lok)
        ms_ins = ukur(_insert)
        baris("insert", n, ms_ins, "O(log n) avg")
        rows["insert"].append((n, ms_ins))

        # search
        target = random.choice(loks).kode
        ms_srch = ukur(bst.search, target)
        baris("search", n, ms_srch, "O(log n) avg")
        rows["search"].append((n, ms_srch))

        # inorder
        ms_ino = ukur(bst.inorder)
        baris("inorder", n, ms_ino, "O(n)")
        rows["inorder"].append((n, ms_ino))
        print()

    print("\n  Perbandingan runtime:")
    cetak_tabel(["insert (ms)", "search (ms)", "inorder (ms)"],
                [(rows["insert"][i][0],
                  rows["insert"][i][1],
                  rows["search"][i][1],
                  rows["inorder"][i][1]) for i in range(len(rows["insert"]))])


# ══════════════════════════════════════════════════════════════
# MODUL 3 – PRIORITY QUEUE BANTUAN
# ══════════════════════════════════════════════════════════════

def bench_queue():
    header("MODUL 3 — PriorityQueueBantuan")
    print(f"  {'Operasi':<30} {'N':>6}  {'Waktu (ms)':>12}   Big-O")
    print(f"  {SEP2}")

    rows_enq = []
    rows_deq = []

    for n in [50, 100, 200, 500]:
        pq = PriorityQueueBantuan()

        # Isi dulu
        for i in range(n):
            lvl = random.randint(1, 3)
            pq.kirim_enqueue(f"DEPOT_{i%2}", f"L{i:03d}", "Beras", f"{i*10}kg", lvl)

        # kirim_enqueue
        def _enq():
            pq.kirim_enqueue("DEPOT_0", "L999", "Tenda", "10unit", random.randint(1, 3))
        ms_enq = ukur(_enq)
        baris("kirim_enqueue", n, ms_enq, "O(n) worst")
        rows_enq.append((n, ms_enq))

        # proses_bantuan_dequeue
        ms_deq = ukur(pq.proses_bantuan_dequeue)
        baris("proses_bantuan_dequeue", n, ms_deq, "O(1)")
        rows_deq.append((n, ms_deq))
        print()

    print("\n  Perbandingan runtime:")
    cetak_tabel(["enqueue (ms)", "dequeue (ms)"],
                [(rows_enq[i][0], rows_enq[i][1], rows_deq[i][1])
                 for i in range(len(rows_enq))])

    print("\n  Catatan: enqueue O(n) karena cari posisi berdasarkan level prioritas.")


# ══════════════════════════════════════════════════════════════
# MODUL 4 – STACK LOG PENGIRIMAN
# ══════════════════════════════════════════════════════════════

def bench_stack():
    header("MODUL 4 — StackLogPengiriman")
    print(f"  {'Operasi':<30} {'N':>6}  {'Waktu (ms)':>12}   Big-O")
    print(f"  {SEP2}")

    rows_push = []
    rows_pop  = []
    rows_log  = []

    for n in [50, 100, 200, 500]:
        st = StackLogPengiriman()
        for i in range(n):
            st.push(f"DEPOT_{i%2}", f"L{i:03d}", "Obat", f"{i}paket")

        # push
        ms_push = ukur(st.push, "DEPOT_0", "L999", "Tenda", "5unit")
        baris("push", n, ms_push, "O(1)")
        rows_push.append((n, ms_push))

        # pop
        ms_pop = ukur(st.pop)
        baris("pop", n, ms_pop, "O(1)")
        rows_pop.append((n, ms_pop))

        # tampilkan_log (O(n) traversal)
        import io
        from contextlib import redirect_stdout
        with redirect_stdout(io.StringIO()):
            ms_log = ukur(st.tampilkan_log)
        baris("tampilkan_log", n, ms_log, "O(n)")
        rows_log.append((n, ms_log))
        print()

    print("\n  Perbandingan runtime:")
    cetak_tabel(["push (ms)", "pop (ms)", "tampilkan_log (ms)"],
                [(rows_push[i][0], rows_push[i][1], rows_pop[i][1], rows_log[i][1])
                 for i in range(len(rows_push))])


# ══════════════════════════════════════════════════════════════
# MODUL 5 – DIJKSTRA + SELECTION SORT (LINKED LIST)
# ══════════════════════════════════════════════════════════════

def bench_dijkstra():
    header("MODUL 5 — DijkstraAuditJarak + Selection Sort LinkedList")
    print(f"  {'Operasi':<30} {'N':>6}  {'Waktu (ms)':>12}   Big-O")
    print(f"  {SEP2}")

    rows_dijkstra = []
    rows_sort     = []
    rows_audit    = []

    for n in [10, 20, 50, 100]:
        g, kodes = buat_graph(n, n_edge=n * 2)
        dijkstra = DijkstraAuditJarak(g)
        asal     = kodes[0]

        # hitung_dijkstra
        ms_dijk = ukur(dijkstra.hitung_dijkstra, asal)
        baris("hitung_dijkstra", n, ms_dijk, "O(V²+E)")
        rows_dijkstra.append((n, ms_dijk))

        # selection_sort LinkedList
        def _sort():
            import math
            ll = LinkedListJarak()
            for k in kodes:
                ll.append(k, random.uniform(0, 500))
            ll.selection_sort()
        ms_sort = ukur(_sort)
        baris("selection_sort (LinkedList)", n, ms_sort, "O(n²)")
        rows_sort.append((n, ms_sort))

        # audit_jarak
        depots = kodes[:2]
        locs   = kodes[2:]
        ms_audit = ukur(dijkstra.audit_jarak, depots, locs)
        baris("audit_jarak", n, ms_audit, "O(D*(V²+E)+n²)")
        rows_audit.append((n, ms_audit))
        print()

    print("\n  Perbandingan runtime:")
    cetak_tabel(["dijkstra (ms)", "sel_sort (ms)", "audit_jarak (ms)"],
                [(rows_dijkstra[i][0],
                  rows_dijkstra[i][1],
                  rows_sort[i][1],
                  rows_audit[i][1]) for i in range(len(rows_dijkstra))])

    print("\n  Catatan: D = jumlah depot, V = node, E = edge")


# ══════════════════════════════════════════════════════════════
# MODUL 6 – INTEGRASI (CLI + semua modul)
# ══════════════════════════════════════════════════════════════

def bench_integrasi():
    header("MODUL 6 — Integrasi Sistem (simulasi skenario nyata)")
    print(f"  {'Skenario':<35} {'N':>6}  {'Waktu (ms)':>12}   Keterangan")
    print(f"  {SEP2}")

    rows = []

    for n in [10, 25, 50, 100]:
        # Bangun sistem lengkap
        g, kodes = buat_graph(n, n_edge=n * 2)
        dijkstra  = DijkstraAuditJarak(g)
        bst       = BSTLokasi()
        pq        = PriorityQueueBantuan()
        st        = StackLogPengiriman()

        loks = buat_lokasi_list(n)
        for lok in loks:
            bst.insert(lok)

        depots = [kodes[0], kodes[1]] if n >= 2 else [kodes[0]]
        lokasi_bencana = kodes[2:] if n > 2 else kodes

        # Skenario: enqueue n bantuan, proses setengah, rollback 2
        def skenario_lengkap():
            pq2 = PriorityQueueBantuan()
            st2 = StackLogPengiriman()
            for i in range(n):
                lvl = random.randint(1, 3)
                pq2.kirim_enqueue(depots[0], f"L{i:03d}", "Beras", f"{i*10}kg", lvl)
            for _ in range(n // 2):
                hasil = pq2.proses_bantuan_dequeue()
                if hasil:
                    st2.push(hasil["depot"], hasil["lokasi"], hasil["jenis"], hasil["jumlah"])
            st2.pop()
            st2.pop()

        ms_sk = ukur(skenario_lengkap, ulang=3)
        baris("Enqueue+Dequeue+Stack", n, ms_sk, "Simulasi kirim bantuan")
        rows.append((n, ms_sk))

        # Skenario: audit jarak penuh
        import io
        from contextlib import redirect_stdout
        def skenario_audit():
            with redirect_stdout(io.StringIO()):
                dijkstra.audit_jarak(depots, lokasi_bencana)

        ms_audit = ukur(skenario_audit, ulang=3)
        baris("Audit Jarak Penuh", n, ms_audit, "Dijkstra + Sort + Report")
        print()

    print("\n  Ringkasan Skenario Enqueue+Stack:")
    cetak_tabel(["total (ms)"],
                [(r[0], r[1]) for r in rows])


# ══════════════════════════════════════════════════════════════
# RANGKUMAN BIG-O
# ══════════════════════════════════════════════════════════════

def cetak_rangkuman():
    header("RANGKUMAN BIG-O SELURUH MODUL")
    tabel = [
        ("MODUL 1 - Graph", "tambah_rute",            "O(1)",            "O(V+E)"),
        ("",                "get_tetangga",            "O(deg)",          "O(V+E)"),
        ("",                "bfs_deteksi_terjangkau",  "O(V+E)",          "O(V)"),
        ("MODUL 2 - BST",   "insert",                  "O(log n) avg",    "O(n)"),
        ("",                "search",                  "O(log n) avg",    "O(n)"),
        ("",                "inorder",                 "O(n)",            "O(n)"),
        ("MODUL 3 - Queue", "kirim_enqueue",            "O(n) worst",      "O(n)"),
        ("",                "proses_bantuan_dequeue",   "O(1)",            "O(1)"),
        ("MODUL 4 - Stack", "push",                    "O(1)",            "O(n)"),
        ("",                "pop",                     "O(1)",            "O(1)"),
        ("",                "tampilkan_log",            "O(n)",            "O(1)"),
        ("MODUL 5 - Dijkstra","hitung_dijkstra",        "O(V²+E)",         "O(V)"),
        ("",                "selection_sort (LL)",      "O(n²)",           "O(1)"),
        ("",                "audit_jarak",              "O(D*(V²+E)+n²)",  "O(V+n)"),
        ("MODUL 6 - CLI",   "Integrasi semua operasi",  "O(D*(V²+E)+n²)",  "O(V+n)"),
    ]
    print(f"\n  {'Modul':<22} {'Operasi':<28} {'Waktu':>16} {'Ruang':>12}")
    print(f"  {'─'*22} {'─'*28} {'─'*16} {'─'*12}")
    for modul, op, waktu, ruang in tabel:
        print(f"  {modul:<22} {op:<28} {waktu:>16} {ruang:>12}")
    print()


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    print(SEP)
    print("  BENCHMARK — Sistem Logistik Bencana")
    print("  Kelompok 6 | ELT60213 Algoritma dan Struktur Data")
    print(SEP)
    print("  Setiap pengukuran diulang 5x, diambil rata-rata.\n")

    import io
    from contextlib import redirect_stdout

    bench_graph()
    bench_bst()
    bench_queue()
    bench_stack()

    # Dijkstra benchmark suppress print noise
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        bench_dijkstra_quiet()
    finally:
        captured = sys.stdout.getvalue()
        sys.stdout = old_stdout
    # Print ulang tapi filter baris dari audit_jarak (===)
    for line in captured.splitlines():
        if not (line.startswith("===") or line.startswith("-") and "km" in line):
            print(line)

    bench_integrasi()
    cetak_rangkuman()

    print(SEP)
    print("  Benchmark selesai.")
    print(SEP)


def bench_dijkstra_quiet():
    """Wrapper bench_dijkstra yang output-nya bisa di-capture."""
    header("MODUL 5 — DijkstraAuditJarak + Selection Sort LinkedList")
    print(f"  {'Operasi':<30} {'N':>6}  {'Waktu (ms)':>12}   Big-O")
    print(f"  {SEP2}")

    import math, io
    from contextlib import redirect_stdout

    rows_dijkstra = []
    rows_sort     = []
    rows_audit    = []

    for n in [10, 20, 50, 100]:
        g, kodes = buat_graph(n, n_edge=n * 2)
        dijkstra  = DijkstraAuditJarak(g)
        asal      = kodes[0]

        ms_dijk = ukur(dijkstra.hitung_dijkstra, asal)
        baris("hitung_dijkstra", n, ms_dijk, "O(V²+E)")
        rows_dijkstra.append((n, ms_dijk))

        def _sort():
            ll = LinkedListJarak()
            for k in kodes:
                ll.append(k, random.uniform(0, 500))
            ll.selection_sort()
        ms_sort = ukur(_sort)
        baris("selection_sort (LinkedList)", n, ms_sort, "O(n²)")
        rows_sort.append((n, ms_sort))

        depots = kodes[:2]
        locs   = kodes[2:]
        def _audit():
            with redirect_stdout(io.StringIO()):
                dijkstra.audit_jarak(depots, locs)
        ms_audit = ukur(_audit, ulang=3)
        baris("audit_jarak", n, ms_audit, "O(D*(V²+E)+n²)")
        rows_audit.append((n, ms_audit))
        print()

    print("\n  Perbandingan runtime:")
    cetak_tabel(["dijkstra (ms)", "sel_sort (ms)", "audit_jarak (ms)"],
                [(rows_dijkstra[i][0],
                  rows_dijkstra[i][1],
                  rows_sort[i][1],
                  rows_audit[i][1]) for i in range(len(rows_dijkstra))])
    print("\n  Catatan: D = jumlah depot, V = node, E = edge")


if __name__ == "__main__":
    main()
