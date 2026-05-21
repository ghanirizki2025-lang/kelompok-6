class NodeQueue:
    """Node untuk menyimpan data di dalam Linked List Queue."""
    def __init__(self, data):
        self.data = data    # Menyimpan data/informasi
        self.next = None    # Pointer ke node berikutnya


class QueueStrukturData:
    """Struktur data Queue murni berbasis Linked List dengan prinsip FIFO."""
    def __init__(self):
        self.front = None   # Pointer ke elemen terdepan (untuk Dequeue)
        self.rear = None    # Pointer ke elemen paling belakang (untuk Enqueue)
        self._ukuran = 0    # Menyimpan jumlah elemen dalam antrean

    def is_empty(self):
        """Memeriksa apakah antrean kosong."""
        return self.front is None

    def ukuran(self):
        """Mengembalikan jumlah elemen aktif di dalam antrean."""
        return self._ukuran

    # 1. OPERASI: ENQUEUE (Menambah elemen ke belakang antrean - O(1))
    def enqueue(self, data):
        """Memasukkan data baru ke ujung belakang antrean."""
        node_baru = NodeQueue(data)
        
        # Jika antrean masih kosong, node baru menjadi front sekaligus rear
        if self.is_empty():
            self.front = node_baru
            self.rear = node_baru
        else:
            # Sambungkan rear lama ke node baru, lalu geser rear ke node baru
            self.rear.next = node_baru
            self.rear = node_baru
            
        self._ukuran += 1
        print(f"📥 [Enqueue O(1)] Berhasil memasukkan: {data}")

    # 2. OPERASI: DEQUEUE (Mengambil elemen dari depan antrean - O(1))
    def dequeue(self):
        """Mengambil dan menghapus data dari ujung depan antrean."""
        if self.is_empty():
            print("⚠️ [Dequeue] Gagal, antrean kosong!")
            return None
        
        # Ambil data dari front lama
        node_diambil = self.front
        data_diambil = node_diambil.data
        
        # Geser pointer front ke node selanjutnya
        self.front = self.front.next
        
        # Jika setelah digeser front menjadi None, berarti rear juga harus di-reset ke None
        if self.front is None:
            self.rear = None
            
        self._ukuran -= 1
        return data_diambil

    # 3. OPERASI: PEEK / FRONT (Melihat elemen terdepan tanpa menghapusnya - O(1))
    def peek(self):
        """Melihat data yang berada di antrean paling depan."""
        if self.is_empty():
            return None
        return self.front.data

    # 4. OPERASI: TAMPILKAN QUEUE
    def tampilkan_queue(self):
        """Mencetak seluruh isi antrean dari Depan (Front) ke Belakang (Rear)."""
        if self.is_empty():
            print("📋 Antrean Kosong.")
            return
        
        current = self.front
        elemen = []
        while current:
            elemen.append(str(current.data))
            current = current.next
        
        print("📋 BARISAN ANTREAN: " + " -> ".join(elemen) + " [REAR]")


# ==============================================================================
# PENGUJIAN MANDIRI STRUCTURE DATA QUEUE
# ==============================================================================
if __name__ == "__main__":
    print("=== DEMO TESTING STRUKTUR DATA QUEUE (FIFO) ===")
    antrean_posko = QueueStrukturData()

    # 1. Menguji fungsi Enqueue (Masuk Antrean)
    print("\n--- Proses Enqueue ---")
    antrean_posko.enqueue("Mobil Logistik 1")
    antrean_posko.enqueue("Mobil Logistik 2")
    antrean_posko.enqueue("Mobil Logistik 3")
    
    # Tampilkan kondisi antrean saat ini
    antrean_posko.tampilkan_queue()
    print(f"Data terdepan saat ini (Peek): {antrean_posko.peek()}")
    print(f"Total kendaraan antre       : {antrean_posko.ukuran()}")

    # 2. Menguji fungsi Dequeue (Keluar Antrean)
    print("\n--- Proses Dequeue ---")
    # Karena FIFO, "Mobil Logistik 1" harus keluar pertama kali
    terlayani1 = antrean_posko.dequeue()
    print(f"🚀 [Proses] {terlayani1} keluar dari antrean untuk bongkar muat.")
    
    terlayani2 = antrean_posko.dequeue()
    print(f"🚀 [Proses] {terlayani2} keluar dari antrean untuk bongkar muat.")

    # Tampilkan sisa antrean
    print("\n--- Sisa Antrean Setelah Dequeue ---")
    antrean_posko.tampilkan_queue()
    print(f"Data terdepan baru (Peek)   : {antrean_posko.peek()}")