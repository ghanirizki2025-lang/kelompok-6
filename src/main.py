import sys
import os
from dataclasses import dataclass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from data_structures.BST_Registry_Lokasi import BSTLokasi
from modules.modul_Graph import GraphJaringanRute
from modules.modul_Queue import PriorityQueueBantuan
from modules.modul_Stack import StackLogPengiriman
from modules.modul_Dijkstra import DijkstraAuditJarak
import modules.modul_BST as bst_utils


# ==========================================
# MODEL DATA
# ==========================================

@dataclass
class Lokasi:
    kode: str
    nama: str
    level: int
    populasi: int


# ==========================================
# INISIALISASI DATA AWAL
# ==========================================

DAFTAR_DEPOT = ["DEPOT_0", "DEPOT_1"]

DAFTAR_LOKASI = [
    Lokasi("DEPOT_0", "Gudang Utara",       3,    0),
    Lokasi("DEPOT_1", "Gudang Selatan",     3,    0),
    Lokasi("L001",    "Desa Sejahtera",     3,  670),
    Lokasi("L002",    "Desa Sukamaju",      2, 1500),
    Lokasi("L003",    "Kel. Maju",          1,  800),
    Lokasi("L004",    "Dusun Terisolir",    1,  400),
    Lokasi("L005",    "Kec. Rayon A",       1, 3000),
    Lokasi("L006",    "Posko Pengungsian",  3,  800),
    Lokasi("L007",    "Dusun Melati",       1,  430),
    Lokasi("L008",    "Desa Harapan",       2, 2000),
]

DAFTAR_RUTE = [
    ("DEPOT_0", "L001",  10),
    ("DEPOT_0", "L002",  15),
    ("DEPOT_0", "L003",  20),
    ("DEPOT_1", "L005",   8),
    ("DEPOT_1", "L006",  12),
    ("DEPOT_1", "L007",  18),
    ("L001",    "L002",   7),
    ("L002",    "L003",   5),
    ("L003",    "L004",  25),
    ("L005",    "L006",   6),
    ("L006",    "L007",   9),
    ("L007",    "L008",  14),
    ("L002",    "L005",  11),
    ("DEPOT_0", "L008",  30),
]

LABEL_LEVEL = {1: "KRITIS", 2: "SEDANG", 3: "AMAN"}


# ==========================================
# SETUP SISTEM
# ==========================================

def setup_graph(rute_list):
    graph = GraphJaringanRute()
    for asal, tujuan, bobot in rute_list:
        graph.tambah_rute(asal, tujuan, bobot)
    return graph


def setup_bst(lokasi_list):
    bst = BSTLokasi()
    bst_utils.isi_bst(bst, lokasi_list)
    return bst


# ==========================================
# CLI UTAMA
# ==========================================

class SistemLogistik:
    def __init__(self):
        print("Memuat sistem...")
        self.graph   = setup_graph(DAFTAR_RUTE)
        self.bst     = setup_bst(DAFTAR_LOKASI)
        self.queue   = PriorityQueueBantuan()
        self.stack   = StackLogPengiriman()
        self.dijkstra = DijkstraAuditJarak(self.graph)
        print("Sistem siap.\n")

    def cetak_header(self):
        print("\n" + "=" * 60)
        print("     SISTEM LOGISTIK BENCANA - KELOMPOK 6")
        print("=" * 60)
        print(" PERINTAH:")
        print("  KIRIM <depot> <lokasi> <jenis> <jumlah>")
        print("  PROSES_BANTUAN")
        print("  ANTRIAN")
        print("  RUTE <depot> <tujuan>")
        print("  AUDIT_JARAK")
        print("  UPDATE_LEVEL <kode> <KRITIS|SEDANG|AMAN>")
        print("  TIDAK_TERJANGKAU <depot>")
        print("  LOG_PENGIRIMAN")
        print("  ROLLBACK")
        print("  LAPORAN_BENCANA")
        print("  KELUAR")
        print("-" * 60)

    def jalankan(self):
        while True:
            self.cetak_header()
            try:
                raw = input(">> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nKeluar.")
                break

            if not raw:
                continue

            parts   = raw.split()
            perintah = parts[0].upper()
            args    = parts[1:]

            # KIRIM
            if perintah == "KIRIM":
                if len(args) < 4:
                    print("Format: KIRIM <depot> <lokasi> <jenis> <jumlah>")
                    continue
                depot, lokasi, jenis, jumlah = args[0], args[1], args[2], args[3]
                lok_obj = bst_utils.cari_lokasi(self.bst, lokasi)
                level   = lok_obj.level if lok_obj else 2
                ok = self.queue.kirim_enqueue(depot, lokasi, jenis, jumlah, level)
                if ok:
                    print(f"[OK] Bantuan {jenis} ({jumlah}) ke {lokasi} dijadwalkan [Level {LABEL_LEVEL[level]}].")

            # PROSES_BANTUAN
            elif perintah == "PROSES_BANTUAN":
                hasil = self.queue.proses_bantuan_dequeue()
                if hasil:
                    self.stack.push(
                        hasil["depot"], hasil["lokasi"],
                        hasil["jenis"], hasil["jumlah"]
                    )

            # ANTRIAN
            elif perintah == "ANTRIAN":
                self.queue.tampilkan_antrian()

            # RUTE
            elif perintah == "RUTE":
                if len(args) < 2:
                    print("Format: RUTE <depot> <tujuan>")
                    continue
                depot, tujuan = args[0], args[1]
                semua_node = self.graph.get_all_nodes()
                if depot not in semua_node:
                    print(f"Depot '{depot}' tidak ditemukan di graph.")
                    continue
                if tujuan not in semua_node:
                    print(f"Tujuan '{tujuan}' tidak ditemukan di graph.")
                    continue
                hasil_jarak = self.dijkstra.hitung_dijkstra(depot)
                jarak = hasil_jarak.get(tujuan)
                import math
                if jarak == math.inf:
                    print(f"[!] {tujuan} tidak terjangkau dari {depot}.")
                else:
                    print(f"Jarak terpendek {depot} -> {tujuan}: {jarak} km")

            # AUDIT_JARAK
            elif perintah == "AUDIT_JARAK":
                lokasi_bencana = [
                    lok.kode for lok in bst_utils.daftar_semua_lokasi(self.bst)
                    if "DEPOT" not in lok.kode
                ]
                self.dijkstra.audit_jarak(DAFTAR_DEPOT, lokasi_bencana)

            # UPDATE_LEVEL
            elif perintah == "UPDATE_LEVEL":
                if len(args) < 2:
                    print("Format: UPDATE_LEVEL <kode> <KRITIS|SEDANG|AMAN>")
                    continue
                bst_utils.perbarui_level(self.bst, args[0], args[1])

            # TIDAK_TERJANGKAU
            elif perintah == "TIDAK_TERJANGKAU":
                if len(args) < 1:
                    print("Format: TIDAK_TERJANGKAU <depot>")
                    continue
                depot = args[0]
                terjangkau = self.graph.bfs_deteksi_terjangkau(depot)
                semua = set(self.graph.get_all_nodes())
                tidak_terjangkau = semua - terjangkau
                if tidak_terjangkau:
                    print(f"[!] Lokasi tidak terjangkau dari {depot}:")
                    for lok in sorted(tidak_terjangkau):
                        print(f"    - {lok}")
                else:
                    print(f"[OK] Semua lokasi terjangkau dari {depot}.")

            # LOG_PENGIRIMAN
            elif perintah == "LOG_PENGIRIMAN":
                self.stack.tampilkan_log()

            # ROLLBACK
            elif perintah == "ROLLBACK":
                log = self.stack.pop()
                if log:
                    print(f"[ROLLBACK] Dibatalkan: {log['jumlah']} {log['jenis']} ke {log['lokasi']} dari {log['depot']}.")
                else:
                    print("[!] Tidak ada log yang bisa di-rollback.")

            # LAPORAN_BENCANA
            elif perintah == "LAPORAN_BENCANA":
                print("\n=== LAPORAN KONDISI BENCANA ===")
                bst_utils.tampilkan_semua_lokasi(self.bst, skip_depot=True)
                bst_utils.tampilkan_rekap_level(self.bst)
                bst_utils.tampilkan_info_bst(self.bst)

            # KELUAR
            elif perintah == "KELUAR":
                print("Keluar dari sistem. Terima kasih.")
                sys.exit(0)

            else:
                print(f"Perintah '{perintah}' tidak dikenal.")


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":
    sistem = SistemLogistik()
    sistem.jalankan()
