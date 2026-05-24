import unittest

# ==============================================================================
# 1. PURE DATA STRUCTURE : BINARY SEARCH TREE (Sesuai Spesifikasi Modul 3)
# ==============================================================================
class BSTNode:
    """Node untuk menyimpan data lokasi bencana di dalam Binary Search Tree."""
    def __init__(self, kode, nama, level, populasi, status):
        self.kode = kode            # Kunci utama (Key): kode_lokasi (e.g., "L001")
        self.nama = nama            # Nama wilayah/lokasi
        self.level = int(level)     # Level bencana: 1 (Kritis), 2 (Siaga), 3 (Aman)
        self.populasi = populasi    # Jumlah populasi terdampak
        self.status = status        # Status penanganan bencana
        self.left = None            # Pointer ke anak kiri
        self.right = None           # Pointer ke anak kanan


class BSTRegistryLokasi:
    """Struktur data BST murni untuk registrasi dan pembaruan lokasi bencana."""
    def __init__(self):
        self.root = None
        self._size = 0

    # ---- OPERASI: INSERT (O(log n) rata-rata) ----
    def insert(self, kode, nama, level, populasi, status):
        """Memasukkan data lokasi baru ke dalam BST berdasarkan kode_lokasi."""
        node_baru = BSTNode(kode, nama, level, populasi, status)
        if self.root is None:
            self.root = node_baru
            self._size += 1
            return True
        return self._insert_rekursif(self.root, node_baru)

    def _insert_rekursif(self, current, node_baru):
        if node_baru.kode < current.kode:
            if current.left is None:
                current.left = node_baru
                self._size += 1
                return True
            return self._insert_rekursif(current.left, node_baru)
        elif node_baru.kode > current.kode:
            if current.right is None:
                current.right = node_baru
                self._size += 1
                return True
            return self._insert_rekursif(current.right, node_baru)
        return False  # Mengabaikan jika ada kode_lokasi yang duplikat

    # ---- OPERASI: SEARCH (O(log n) rata-rata) ----
    def search(self, kode):
        """Mencari node lokasi berdasarkan kode_lokasi. Mengembalikan objek node atau None."""
        return self._search_rekursif(self.root, kode)

    def _search_rekursif(self, current, kode):
        if current is None or current.kode == kode:
            return current
        if kode < current.kode:
            return self._search_rekursif(current.left, kode)
        return self._search_rekursif(current.right, kode)

    # ---- OPERASI: UPDATE LEVEL (O(log n) rata-rata) ----
    def update_level(self, kode, level_baru):
        """Mencari lokasi dan memperbarui tingkat level bencananya."""
        node = self.search(kode)
        if node:
            node.level = int(level_baru)
            return True
        return False

    # ---- OPERASI: INORDER TRAVERSAL (O(n) - Daftar Terurut Ascending) ----
    def inorder(self):
        """Mengembalikan daftar seluruh objek node yang terurut berdasarkan kode_lokasi."""
        hasil = []
        self._inorder_rekursif(self.root, hasil)
        return hasil

    def _inorder_rekursif(self, current, hasil):
        if current:
            self._inorder_rekursif(current.left, hasil)
            hasil.append(current)
            self._inorder_rekursif(current.right, hasil)

    def __len__(self):
        return self._size


# ==============================================================================
# 2. SEKENARIO UNIT TESTING UNTUK BINARY SEARCH TREE
# ==============================================================================
class TestBSTRegistryMurni(unittest.TestCase):

    def setUp(self):
        """Inisialisasi BST Kosong sebelum memulai pengujian."""
        self.bst = BSTRegistryLokasi()

    def test_inisialisasi_awal(self):
        """Memastikan BST mula-mula kosong."""
        self.assertIsNone(self.bst.root)
        self.assertEqual(len(self.bst), 0)

    def test_insert_dan_pembentukan_tree(self):
        """Memastikan elemen masuk ke posisi kiri/kanan yang tepat sesuai kaidah BST."""
        # Root Node
        self.bst.insert("L002", "Kecamatan B", 2, 5000, "Siaga")
        # Harus masuk ke sebelah Kiri Root karena "L001" < "L002"
        self.bst.insert("L001", "Kecamatan A", 1, 3500, "Kritis")
        # Harus masuk ke sebelah Kanan Root karena "L003" > "L002"
        self.bst.insert("L003", "Kecamatan C", 3, 1200, "Aman")

        self.assertEqual(len(self.bst), 3)
        self.assertEqual(self.bst.root.kode, "L002")
        self.assertEqual(self.bst.root.left.kode, "L001")
        self.assertEqual(self.bst.root.right.kode, "L003")

    def test_search_lokasi(self):
        """Memastikan data lokasi bisa ditemukan dengan cepat berdasarkan kodenya."""
        self.bst.insert("L005", "Desa Sukamaju", 1, 400, "Kritis")
        self.bst.insert("L002", "Desa Sukaasih", 2, 800, "Siaga")

        # Coba cari data yang ada
        node_ketemu = self.bst.search("L002")
        self.assertIsNotNone(node_ketemu)
        self.assertEqual(node_ketemu.nama, "Desa Sukaasih")
        self.assertEqual(node_ketemu.level, 2)

        # Coba cari data yang fiktif / tidak terdaftar
        node_zonk = self.bst.search("L999")
        self.assertIsNone(node_zonk)

    def test_update_level_bencana(self):
        """Memastikan fitur pembaruan level bencana (UPDATE_LEVEL) berhasil memperbarui isi node."""
        self.bst.insert("L001", "Posko Utama", 3, 150, "Aman")
        
        # Lakukan update level dari 3 (Aman) menjadi 1 (Kritis)
        berhasil = self.bst.update_level("L001", 1)
        self.assertTrue(berhasil)
        
        # Validasi apakah data di dalam node benar-benar berubah
        node = self.bst.search("L001")
        self.assertEqual(node.level, 1)

    def test_inorder_sorting_ascending(self):
        """Memastikan traversal inorder mengembalikan data yang terurut alfabetis (A-Z)."""
        # Input dengan urutan acak
        self.bst.insert("L003", "Wilayah Timur", 2, 300, "Siaga")
        self.bst.insert("L001", "Wilayah Barat", 1, 900, "Kritis")
        self.bst.insert("L004", "Wilayah Utara", 3, 150, "Aman")
        self.bst.insert("L002", "Wilayah Selatan", 2, 450, "Siaga")

        # Ekstrak hasil inorder
        daftar_terurut = self.bst.inorder()
        kunci_terurut = [node.kode for node in daftar_terurut]

        # Hasil wajib rapi berurutan: L001 -> L002 -> L003 -> L004
        self.assertEqual(kunci_terurut, ["L001", "L002", "L003", "L004"])


# ==============================================================================
# RUNNER AUTOMATION TESTING
# ==============================================================================
if __name__ == "__main__":
    unittest.main()