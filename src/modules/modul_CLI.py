import sys

# ==============================================================================
# MOCK-UP MODULE 1 - 5 (Diperlukan agar CLI Module 6 bisa berjalan & di-test)
# ==============================================================================

class DummyGraph:
    def __init__(self):
        # Struktur adjacency list sederhana
        self.adj_list = {
            "DEPOT_A": [("L001", 5), ("L002", 12)],
            "L001": [("DEPOT_A", 5), ("L003", 7)],
            "L002": [("DEPOT_A", 12)],
            "L003": [("L001", 7)],
            "L004": [] # Isolasi untuk simulasi TIDAK_TERJANGKAU
        }
    def bfs_tidak_terjangkau(self, start):
        # Simulasi deteksi lokasi terisolasi
        terjangkau = ["DEPOT_A", "L001", "L002", "L003"]
        if start not in self.adj_list:
            return []
        return ["L004"] if start == "DEPOT_A" else []

class DummyPriorityQueue:
    def __init__(self):
        self.queue = []
    def enqueue(self, item, prioritas):
        # Makin kecil angka prioritas (misal: level 1), makin kritis / didahulukan
        self.queue.append((prioritas, item))
        self.queue.sort(key=lambda x: x[0])
    def dequeue(self):
        if not self.queue: return None
        return self.queue.pop(0)[1]

class DummyBST:
    def __init__(self):
        self.data = {
            "L001": {"nama": "Desa Sukamaju", "level": 2, "populasi": 1500, "status": "SIAGA"},
            "L002": {"nama": "Kecamatan Rayon A", "level": 1, "populasi": 3000, "status": "KRITIS"},
            "L003": {"nama": "Posko Pengungsian 3", "level": 3, "populasi": 800, "status": "AMAN"},
            "L004": {"nama": "Dusun Terisolir", "level": 1, "populasi": 400, "status": "KRITIS"}
        }
    def update_level(self, kode, level_baru):
        if kode in self.data:
            self.data[kode]["level"] = level_baru
            self.data[kode]["status"] = "KRITIS" if level_baru == 1 else "SIAGA" if level_baru == 2 else "AMAN"
            return True
        return False
    def print_inorder(self):
        for k, v in sorted(self.data.items()):
            print(f"  [{k}] {v['nama']} | Level Bencana: {v['level']} | Status: {v['status']} | Pop: {v['populasi']}")

class DummyStack:
    def __init__(self):
        self.history = []
    def push(self, log_data):
        self.history.append(log_data)
    def pop(self):
        if not self.history: return None
        return self.history.pop()

def dummy_dijkstra(start, target):
    # Simulasi hasil rute terpendek
    if start == "DEPOT_A" and target == "L003":
        return ["DEPOT_A", "L001", "L003"], 12
    return [start, target], 15

# ==============================================================================
# UTAMA: MODULE 6 - CLI LOGISTIK
# ==============================================================================

class CLILogistik:
    def __init__(self):
        # Inisialisasi/menghubungkan semua sistem komponen arsitektur
        self.graph = DummyGraph()
        self.pq_bantuan = DummyPriorityQueue()
        self.bst_lokasi = DummyBST()
        self.stack_log = DummyStack()

    def cetak_header(self):
        print("\n" + "="*60)
        print("          SISTEM CLI LOGISTIK BANCANA - KELOMPOK 6")
        print("="*60)
        print(" PERINTAH YANG TERSEDIA:")
        print(" 1. KIRIM <depot> <lokasi> <jenis> <jumlah>")
        print(" 2. PROSES_BANTUAN")
        print(" 3. RUTE OPTIMAL <depot> <tujuan>")
        print(" 4. UPDATE LEVEL <kode_lokasi> <level_baru>")
        print(" 5. TIDAK_TERJANGKAU <depot>")
        print(" 6. LOG_PENGIRIMAN / ROLLBACK")
        print(" 7. LAPORAN_BENCANA")
        print(" 8. KELUAR")
        print("─"*60)

    def jalankan(self):
        while True:
            self.cetak_header()
            input_user = input("Masukan Perintah CLI >> ").strip()
            if not input_user:
                continue

            # Parsing argumen CLI berbasis spasi
            parts = input_user.split()
            perintah = parts[0].upper()
            args = parts[1:]

            # 1. PERINTAH: KIRIM
            if perintah == "KIRIM":
                if len(args) < 4:
                    print("❌ Error: Format salah! Gunakan: KIRIM <depot> <lokasi> <jenis> <jumlah>")
                    continue
                depot, lokasi, jenis, jumlah = args[0], args[1], args[2], args[3]
                
                # Mengambil tingkat prioritas lokasi berdasarkan data di BST Registry
                info_lokasi = self.bst_lokasi.data.get(lokasi, {"level": 2})
                level_prioritas = info_lokasi["level"]
                
                item_bantuan = {
                    "depot": depot, "lokasi": lokasi,
                    "jenis": jenis, "jumlah": jumlah
                }
                # Masukkan ke antrean Priority Queue
                self.pq_bantuan.enqueue(item_bantuan, prioritas=level_prioritas)
                print(f"✔️ Berhasil menjadwalkan bantuan {jenis} ({jumlah} unit) ke {lokasi} [Prioritas Level {level_prioritas}].")

            # 2. PERINTAH: PROSES_BANTUAN
            elif perintah == "PROSES_BANTUAN":
                item_diproses = self.pq_bantuan.dequeue()
                if not item_diproses:
                    print("⚠️ Antrean kosong. Tidak ada bantuan yang perlu diproses saat ini.")
                else:
                    print(f"🚀 [PROSES] Mengirim {item_diproses['jumlah']} {item_diproses['jenis']} dari {item_diproses['depot']} menuju {item_diproses['lokasi']}!")
                    # Catat transaksi ke dalam Stack Log Pengiriman (LIFO) untuk fitur Rollback
                    self.stack_log.push(item_diproses)

            # 3. PERINTAH: RUTE OPTIMAL
            elif perintah == "RUTE":
                if len(args) >= 2 and args[0].upper() == "OPTIMAL":
                    # Menangani jika user mengetik 'RUTE OPTIMAL <depot> <tujuan>'
                    depot, tujuan = args[1], args[2]
                elif len(args) == 2:
                    # Menangani jika user langsung mengetik 'RUTE <depot> <tujuan>'
                    depot, tujuan = args[0], args[1]
                else:
                    print("❌ Error: Format salah! Gunakan: RUTE OPTIMAL <depot> <tujuan>")
                    continue
                
                jalur, jarak = dummy_dijkstra(depot, tujuan)
                print(f"📍 Rute Terpendek (Dijkstra): {' -> '.join(jalur)}")
                print(f"📏 Total Jarak Jangkauan    : {jarak} km")

            # 4. PERINTAH: UPDATE LEVEL
            elif perintah == "UPDATE":
                if len(args) < 3 or args[0].upper() != "LEVEL":
                    print("❌ Error: Format salah! Gunakan: UPDATE LEVEL <kode_lokasi> <level_baru>")
                    continue
                kode_lokasi = args[1]
                try:
                    level_baru = int(args[2])
                except ValueError:
                    print("❌ Error: Level harus berupa angka bulat (1=Kritis, 2=Siaga, 3=Aman)!")
                    continue

                berhasil = self.bst_lokasi.update_level(kode_lokasi, level_baru)
                if berhasil:
                    print(f"🔄 Registry BST Diperbarui: Status {kode_lokasi} sekarang berada di Level {level_baru}.")
                else:
                    print(f"❌ Error: Kode lokasi '{kode_lokasi}' tidak ditemukan di registrasi BST.")

            # 5. PERINTAH: TIDAK_TERJANGKAU
            elif perintah == "TIDAK_TERJANGKAU":
                if len(args) < 1:
                    print("❌ Error: Format salah! Gunakan: TIDAK_TERJANGKAU <depot>")
                    continue
                depot = args[0]
                lokasi_terisolasi = self.graph.bfs_tidak_terjangkau(depot)
                if lokasi_terisolasi:
                    print(f"⚠️ Peringatan BFS: Ditemukan {len(lokasi_terisolasi)} lokasi tidak terjangkau dari {depot}:")
                    for lok in lokasi_terisolasi:
                        print(f"   - {lok}")
                else:
                    print(f"🟢 Sukses BFS: Semua lokasi terkoneksi dengan baik dari {depot}.")

            # 6. PERINTAH: LOG_PENGIRIMAN & ROLLBACK
            elif perintah == "LOG_PENGIRIMAN":
                logs = self.stack_log.history
                if not logs:
                    print("📋 Riwayat log pengiriman kosong.")
                else:
                    print("📋 RIWAYAT LOG PENGIRIMAN (Terbaru -> Lama):")
                    for i, log in enumerate(reversed(logs), 1):
                        print(f"   {i}. {log['jumlah']} {log['jenis']} ke {log['lokasi']} (Asal: {log['depot']})")

            elif perintah == "ROLLBACK":
                log_terakhir = self.stack_log.pop()
                if log_terakhir:
                    print(f"⏪ [ROLLBACK BERHASIL] Pengiriman terakhir dibatalkan!")
                    print(f"   Stok sebanyak {log_terakhir['jumlah']} {log_terakhir['jenis']} dikembalikan ke {log_terakhir['depot']}.")
                else:
                    print("❌ Gagal Rollback: Tidak ada riwayat transaksi pengiriman yang bisa dibatalkan.")

            # 7. PERINTAH: LAPORAN_BENCANA
            elif perintah == "LAPORAN_BENCANA":
                print("📊 LAPORAN REGISTRY KONDISI BENCANA (Inorder BST):")
                self.bst_lokasi.print_inorder()

            # 8. PERINTAH: KELUAR
            elif perintah == "KELUAR":
                print("👋 Keluar dari sistem logistik. Terima kasih!")
                sys.exit(0)

            else:
                print("❌ Perintah tidak dikenal! Periksa kembali daftar perintah di atas.")


if __name__ == "__main__":
    # Menjalankan aplikasi CLI utama
    aplikasi = CLILogistik()
    aplikasi.jalankan()