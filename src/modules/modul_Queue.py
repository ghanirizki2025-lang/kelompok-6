import unittest

class QueueNode:
    def __init__(self, asal_depot, tujuan_lokasi, jenis_bantuan, jumlah, level_bencana):
        self.asal_depot = asal_depot
        self.tujuan_lokasi = tujuan_lokasi
        self.jenis_bantuan = jenis_bantuan
        self.jumlah = jumlah
        self.level_bencana = level_bencana
        self.next = None

class PriorityQueueBantuan:
    def __init__(self):
        self.head = None
        self._size = 0

    def kirim_enqueue(self, depot, lokasi, jenis, jumlah, level):
        new_node = QueueNode(depot, lokasi, jenis, jumlah, level)
        if self.head is None or level < self.head.level_bencana:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next is not None and current.next.level_bencana <= level:
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self._size += 1
        print(f"[ENQUEUE] Berhasil mendaftarkan antrian bantuan ke {lokasi} (Level: {level})")

    def proses_bantuan_dequeue(self):
        if self.is_empty():
            print("[PERINGATAN] Antrian Kosong! Tidak ada bantuan yang perlu diproses.")
            return None
        node_diproses = self.head
        self.head = self.head.next
        self._size -= 1
        print(f"[DEQUEUE & KIRIM] Memproses bantuan [{node_diproses.jenis_bantuan}] sebanyak {node_diproses.jumlah} dari {node_diproses.asal_depot} ke {node_diproses.tujuan_lokasi}.")
        return {
            "depot": node_diproses.asal_depot,
            "lokasi": node_diproses.tujuan_lokasi,
            "jenis": node_diproses.jenis_bantuan,
            "jumlah": node_diproses.jumlah,
            "level": node_diproses.level_bencana
        }

    def is_empty(self):
        return self.head is None

    def size(self):
        return self._size

    def tampilkan_antrian(self):
        if self.is_empty():
            print("[INFO] Tidak ada antrian pengiriman aktif.")
            return
        print("\n=== DAFTAR ANTRIAN PENGIRIMAN LOGISTIK (PRIORITY QUEUE) ===")
        current = self.head
        nomor = 1
        while current:
            str_level = "KRITIS" if current.level_bencana == 1 else "SEDANG" if current.level_bencana == 2 else "RINGAN"
            print(f"{nomor}. [{str_level}] {current.asal_depot} -> {current.tujuan_lokasi} | Bantuan: {current.jenis_bantuan} ({current.jumlah})")
            current = current.next
            nomor += 1
        print("============================================================\n")

class TestPriorityQueueBantuan(unittest.TestCase):
    def setUp(self):
        self.pq = PriorityQueueBantuan()

    def test_priority_queue_operations(self):
        print("\n--- TEST RUN PRIORITY QUEUE ---")
        self.pq.kirim_enqueue("DEPOT_0", "LOK_02", "Beras", "500kg", 2)
        self.pq.kirim_enqueue("DEPOT_1", "LOK_05", "Obat", "10 Box", 3)
        self.pq.kirim_enqueue("DEPOT_0", "LOK_01", "Tenda", "20 Unit", 1)
        
        self.pq.tampilkan_antrian()
        
        self.assertEqual(self.pq.size(), 3)
        
        data_1 = self.pq.proses_bantuan_dequeue()
        self.assertEqual(data_1["level"], 1)
        self.assertEqual(data_1["lokasi"], "LOK_01")
        
        data_2 = self.pq.proses_bantuan_dequeue()
        self.assertEqual(data_2["level"], 2)
        
        data_3 = self.pq.proses_bantuan_dequeue()
        self.assertEqual(data_3["level"], 3)
        
        self.assertTrue(self.pq.is_empty())
        self.assertIsNone(self.pq.proses_bantuan_dequeue())

if __name__ == "__main__":
    unittest.main()