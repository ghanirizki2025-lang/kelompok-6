class NodeStack:
    """Node untuk menyimpan data transaksi logistik di dalam Linked List Stack."""
    def __init__(self, data_log):
        self.data_log = data_log  # Menyimpan dictionary data pengiriman
        self.next = None          # Pointer ke node di bawahnya


class StackLogPengiriman:
    """Struktur data Stack (LIFO) untuk mencatat riwayat dan pembatalan logistik."""
    def __init__(self):
        self.top = None           # Pointer ke elemen teratas stack
        self._ukuran = 0          # Menghitung jumlah log tersimpan

    def is_empty(self):
        """Memeriksa apakah stack dalam kondisi kosong."""
        return self.top is None

    # 1. OPERASI: PUSH (Mencatat transaksi logistik baru - O(1))
    def push(self, depot, lokasi, jenis, jumlah):
        """
        Memasukkan log pengiriman bantuan baru ke bagian atas stack.
        Mendukung Big-O: push O(1).
        """
        data_log = {
            "depot": depot,
            "lokasi": lokasi,
            "jenis": jenis,
            "jumlah": jumlah
        }
        node_baru = NodeStack(data_log)
        
        # Kaitkan node baru ke top yang lama, lalu geser top ke node baru
        node_baru.next = self.top
        self.top = node_baru
        self._ukuran += 1
        return True

    # 2. OPERASI: POP / ROLLBACK (Membatalkan pengiriman terakhir - O(1))
    def pop(self):
        """
        Mengambil dan menghapus log pengiriman teratas (terbaru).
        Mendukung Big-O: pop O(1).
        Returns: dictionary data log jika ada, None jika stack kosong.
        """
        if self.is_empty():
            return None
        
        node_diambil = self.top
        self.top = self.top.next  # Geser top ke elemen di bawahnya
        self._ukuran -= 1
        
        return node_diambil.data_log

    # 3. OPERASI: LOG_PENGIRIMAN (Menampilkan riwayat Terbaru -> Lama)
    def tampilkan_log(self):
        """
        Menampilkan seluruh riwayat pengiriman dari yang paling baru ke terlama.
        Sesuai spesifikasi perintah LOG_PENGIRIMAN.
        """
        if self.is_empty():
            print("📋 Riwayat log pengiriman kosong.")
            return

        print("📋 RIWAYAT LOG PENGIRIMAN (Terbaru -> Lama):")
        current = self.top
        no = 1
        while current is not None:
            log = current.data_log
            print(f"   {no}. {log['jumlah']} {log['jenis']} ke {log['lokasi']} (Asal: {log['depot']})")
            current = current.next
            no += 1


# ==============================================================================
# CONTOH PENGGUNAAN & PENGUJIAN MODULE STACK
# ==============================================================================
if __name__ == "__main__":
    print("=== DEMO TESTING STACK LOG PENGIRIMAN ===")
    stack_logistik = StackLogPengiriman()

    # 1. Simulasi mencatat beberapa pengiriman (PUSH)
    print("\n🚀 Menambahkan log pengiriman logistik...")
    stack_logistik.push(depot="DEPOT_0", lokasi="L002", jenis="Beras", jumlah="500 kg")
    stack_logistik.push(depot="DEPOT_1", lokasi="L001", jenis="Tenda", jumlah="50 unit")
    stack_logistik.push(depot="DEPOT_0", lokasi="L004", jenis="Obat-obatan", jumlah="200 paket")

    # 2. Menampilkan riwayat (LOG_PENGIRIMAN)
    # Harus tercetak urutan terbalik dari input (L004 -> L001 -> L002)
    stack_logistik.tampilkan_log()

    # 3. Simulasi Fitur Rollback Pengiriman Terakhir (POP)
    print("\n⏪ Melakukan ROLLBACK pengiriman terakhir...")
    log_batal = stack_logistik.pop()
    if log_batal:
        print(f"[ROLLBACK BERHASIL] Pengiriman terakhir dibatalkan!")
        print(f"   Stok sebanyak {log_batal['jumlah']} {log_batal['jenis']} dikembalikan ke {log_batal['depot']}.")
    else:
        print("❌ Gagal Rollback: Tidak ada riwayat transaksi pengiriman yang bisa dibatalkan.")

    # 4. Menampilkan kembali riwayat setelah rollback
    print("\n📊 Kondisi log setelah dilakukan rollback:")
    stack_logistik.tampilkan_log()