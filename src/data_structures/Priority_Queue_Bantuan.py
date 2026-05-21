class NodeQueue:
    """Node untuk menyimpan data bantuan dan tingkat prioritasnya di Linked List."""
    def __init__(self, item, prioritas):
        self.item = item            # Menyimpan dictionary data bantuan
        self.prioritas = prioritas  # Angka prioritas: 1 (Kritis), 2 (Siaga), 3 (Aman)
        self.next = None            # Pointer ke node berikutnya


class PriorityQueueBantuan:
    """Struktur data Priority Queue berbasis Linked List untuk antrean bantuan."""
    def __init__(self):
        self.front = None           # Pointer ke elemen terdepan antrean

    def is_empty(self):
        return self.front is None

    def enqueue(self, depot, lokasi, jenis, jumlah, prioritas):
        """Memasukkan bantuan baru ke dalam antrean berdasarkan level prioritas."""
        item_bantuan = {
            "depot": depot,
            "lokasi": lokasi,
            "jenis": jenis,
            "jumlah": jumlah
        }
        node_baru = NodeQueue(item_bantuan, prioritas)

        # Kondisi A: Jika antrean kosong ATAU prioritas node baru lebih tinggi (angka lebih kecil)
        if self.is_empty() or prioritas < self.front.prioritas:
            node_baru.next = self.front
            self.front = node_baru
            return True

        # Kondisi B: Telusuri linked list untuk menemukan posisi yang tepat
        current = self.front
        while current.next is not None and current.next.prioritas <= prioritas:
            current = current.next

        node_baru.next = current.next
        current.next = node_baru
        return True

    def dequeue(self):
        """Mengambil dan menghapus bantuan dengan prioritas tertinggi (paling depan)."""
        if self.is_empty():
            return None

        node_diambil = self.front
        self.front = self.front.next  # Geser front ke elemen berikutnya
        return node_diambil.item


# ==============================================================================
# PENGUJIAN OTOMATIS
# ==============================================================================
if __name__ == "__main__":
    print("=== TESTING MODULE PRIORITY QUEUE BERHASIL ===")
    pq = PriorityQueueBantuan()
    pq.enqueue("DEPOT_0", "L001", "Tenda", "50 unit", 2)
    pq.enqueue("DEPOT_0", "L002", "Beras", "500 kg", 1)
    
    print("Sistem Queue berjalan normal!")