class NodeBST:
    """Node untuk menyimpan data lokasi pada Binary Search Tree."""
    def __init__(self, kode, nama, level, populasi):
        self.kode = kode          # Kunci utama (Key) untuk BST (misal: "L001")
        self.nama = nama          # Nama lokasi (misal: "Desa Sukamaju")
        self.level = level        # 1 = KRITIS, 2 = SIAGA, 3 = AMAN
        self.populasi = populasi  # Jumlah populasi (integer)
        self.status = self._tentukan_status(level)
        
        self.left = None          # Pointer ke anak kiri
        self.right = None         # Pointer ke anak kanan

    def _tentukan_status(self, level):
        """Helper untuk menentukan teks status berdasarkan level bencana."""
        if level == 1:
            return "KRITIS"
        elif level == 2:
            return "SIAGA"
        elif level == 3:
            return "AMAN"
        else:
            return "TIDAK DIKETAHUI"


class BSTRegistryLokasi:
    """Struktur data Binary Search Tree untuk manajemen registrasi lokasi bencana."""
    def __init__(self):
        self.root = None

    # 1. OPERASI: INSERT (Menambahkan data lokasi baru)
    def insert(self, kode, nama, level, populasi):
        """Menambahkan lokasi baru ke dalam BST berdasarkan kode_lokasi."""
        node_baru = NodeBST(kode, nama, level, populasi)
        if self.root is None:
            self.root = node_baru
            return True
        else:
            return self._insert_rekursif(self.root, node_baru)

    def _insert_rekursif(self, current_node, node_baru):
        if node_baru.kode < current_node.kode:
            if current_node.left is None:
                current_node.left = node_baru
                return True
            else:
                return self._insert_rekursif(current_node.left, node_baru)
        elif node_baru.kode > current_node.kode:
            if current_node.right is None:
                current_node.right = node_baru
                return True
            else:
                return self._insert_rekursif(current_node.right, node_baru)
        else:
            # Jika kode sudah ada, gagalkan insert (kunci harus unik)
            return False

    # 2. OPERASI: SEARCH (Mencari data lokasi)
    def search(self, kode):
        """Mencari dan mengembalikan node lokasi berdasarkan kode_lokasi."""
        return self._search_rekursif(self.root, kode)

    def _search_rekursif(self, current_node, kode):
        if current_node is None or current_node.kode == kode:
            return current_node
        
        if kode < current_node.kode:
            return self._search_rekursif(current_node.left, kode)
        else:
            return self._search_rekursif(current_node.right, kode)

    # 3. OPERASI: UPDATE LEVEL
    def update_level(self, kode, level_baru):
        """Memperbarui level bencana dan otomatis memperbarui statusnya."""
        node = self.search(kode)
        if node:
            node.level = level_baru
            node.status = node._tentukan_status(level_baru)
            return True
        return False

    # 4. OPERASI: INORDER TRAVERSAL (Mencetak Daftar Terurut)
    def print_inorder(self):
        """Mencetak seluruh data registrasi secara terurut (A-Z berdasarkan kode)."""
        self._inorder_rekursif(self.root)

    def _inorder_rekursif(self, current_node):
        if current_node:
            self._inorder_rekursif(current_node.left)
            print(f"  [{current_node.kode}] {current_node.nama:<20} | "
                  f"Level Bencana: {current_node.level} | "
                  f"Status: {current_node.status:<6} | "
                  f"Pop: {current_node.populasi}")
            self._inorder_rekursif(current_node.right)


# ==============================================================================
# CONTOH PENGGUNAAN & PENGUJIAN MODULE BST
# ==============================================================================
if __name__ == "__main__":
    print("=== DEMO TESTING BST REGISTRY LOKASI ===")
    bst = BSTRegistryLokasi()

    # Pengujian Insert Data (Sesuai spesifikasi mock-up data)
    bst.insert("L001", "Desa Sukamaju", 2, 1500)
    bst.insert("L003", "Posko Pengungsian 3", 3, 800)
    bst.insert("L002", "Kecamatan Rayon A", 1, 3000)
    bst.insert("L004", "Dusun Terisolir", 1, 400)

    print("\n📊 LAPORAN REGISTRY KONDISI BENCANA AWAL (Inorder BST):")
    bst.print_inorder()

    # Pengujian Search Data
    print("\n🔍 Mencari lokasi L002...")
    hasil_cari = bst.search("L002")
    if hasil_cari:
        print(f"✔️ Ditemukan! Nama: {hasil_cari.nama}, Status: {hasil_cari.status}")
    else:
        print("❌ Lokasi tidak ditemukan!")

    # Pengujian Update Level (Misal: L001 memburuk dari level 2 ke level 1)
    print("\n🔄 Memperbarui L001 ke Level 1 (KRITIS)...")
    if bst.update_level("L001", 1):
        print("✔️ Update Berhasil!")
    else:
        print("❌ Update Gagal (Kode tidak ditemukan)!")

    print("\n📊 LAPORAN REGISTRY SETELAH UPDATE (Inorder BST):")
    bst.print_inorder()