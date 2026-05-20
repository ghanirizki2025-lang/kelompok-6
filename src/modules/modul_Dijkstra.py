# =============================================================================
# modul_5.py
# Modul 5 — Dijkstra & Audit Jarak
#
# Tanggung jawab modul ini:
#   - Menghitung rute terpendek dari depot ke lokasi tujuan (RUTE_OPTIMAL)
#   - Mengaudit jarak semua lokasi dari depot tertentu (LAPORAN_BENCANA)
#   - Mengurutkan hasil audit menggunakan Selection Sort pada Linked List
#
# Mata Kuliah : ELT60213 Algoritma dan Struktur Data
# Topik       : 9 — Disaster Response Logistics System
# =============================================================================

from src.data_structures.graph import (
    GraphRute,
    dijkstra_logistik,
    rekonstruksi_rute,
    selection_sort_jarak,
)


def tampilkan_rute_optimal(graph: GraphRute, depot: str, tujuan: str):
    """
    Hitung dan tampilkan rute terpendek dari depot ke tujuan menggunakan Dijkstra.

    Langkah:
        1. Jalankan dijkstra_logistik dari depot.
        2. Rekonstruksi jalur menggunakan parent map.
        3. Tampilkan jalur + total jarak.

    Parameter:
        graph  : objek GraphRute
        depot  : kode node titik berangkat
        tujuan : kode node tujuan pengiriman
    """
    # Validasi node ada di graph
    if depot not in graph.adj:
        print(f"  Depot '{depot}' tidak dikenal dalam jaringan.")
        return
    if tujuan not in graph.adj:
        print(f"  Lokasi '{tujuan}' tidak dikenal dalam jaringan.")
        return

    # Jalankan Dijkstra dari depot
    dist, parent = dijkstra_logistik(graph, depot)

    if dist[tujuan] == float('inf'):
        print(f"  Tidak ada rute yang bisa dilalui dari {depot} ke {tujuan}.")
        return

    # Bangun urutan node jalur terpendek
    jalur = rekonstruksi_rute(parent, depot, tujuan)

    print(f"\n  RUTE OPTIMAL: {depot} → {tujuan}")
    print(f"  {'─'*50}")
    if jalur:
        print(f"  Jalur  : {' → '.join(jalur)}")
        print(f"  Panjang: {len(jalur) - 1} segmen")
    else:
        print(f"  Jalur  : Tidak dapat direkonstruksi")
    print(f"  Jarak  : {dist[tujuan]} km")
    print(f"  {'─'*50}\n")


def audit_jarak_depot(graph: GraphRute, depot: str, hanya_lokasi: bool = True) -> list:
    """
    Hitung jarak terpendek dari depot ke semua node, lalu urutkan
    menggunakan Selection Sort (tanpa sort bawaan Python).

    Parameter:
        graph        : objek GraphRute
        depot        : kode depot yang dijadikan titik referensi
        hanya_lokasi : jika True, depot lain tidak dimasukkan ke hasil

    Return:
        list tuple (kode, jarak) terurut ascending.
    """
    if depot not in graph.adj:
        return []

    dist, _ = dijkstra_logistik(graph, depot)

    # Kumpulkan pasangan (kode, jarak) untuk lokasi yang terjangkau
    pasangan = []
    for kode, jarak in dist.items():
        if jarak == float('inf'):
            continue   # lokasi tidak terjangkau, lewati
        if hanya_lokasi and 'DEPOT' in kode:
            continue   # skip depot lain jika tidak diperlukan
        pasangan.append((kode, jarak))

    # Urutkan dengan Selection Sort (implementasi manual di graph.py)
    pasangan = selection_sort_jarak(pasangan)
    return pasangan


def tampilkan_audit_jarak(graph: GraphRute, depot: str, top_n: int = 10):
    """
    Tampilkan tabel audit jarak dari depot, diurutkan dari yang terdekat.
    Digunakan dalam LAPORAN_BENCANA.

    Parameter:
        graph  : objek GraphRute
        depot  : kode depot referensi
        top_n  : jumlah baris yang ditampilkan (default 10)
    """
    hasil = audit_jarak_depot(graph, depot)

    print(f"\n  AUDIT JARAK dari {depot} (Selection Sort)")
    print(f"  {'─'*38}")
    print(f"  {'Rank':<6} {'Lokasi':<12} {'Jarak (km)':>12}")
    print(f"  {'─'*38}")

    for i, (kode, jarak) in enumerate(hasil[:top_n], 1):
        print(f"  {i:<6} {kode:<12} {jarak:>12} km")

    if len(hasil) > top_n:
        print(f"  ... dan {len(hasil) - top_n} lokasi lainnya")

    print(f"  {'─'*38}")
    print(f"  Total lokasi terjangkau: {len(hasil)}\n")
