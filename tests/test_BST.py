import unittest


class BSTNode:
    def __init__(self, kode, nama, level, populasi, status):
        self.kode = kode
        self.nama = nama
        self.level = int(level)
        self.populasi = populasi
        self.status = status
        self.left = None
        self.right = None


class BSTRegistryLokasi:
    def __init__(self):
        self.root = None
        self._size = 0

    def insert(self, kode, nama, level, populasi, status):
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
        return False

    def search(self, kode):
        return self._search_rekursif(self.root, kode)

    def _search_rekursif(self, current, kode):
        if current is None or current.kode == kode:
            return current
        if kode < current.kode:
            return self._search_rekursif(current.left, kode)
        return self._search_rekursif(current.right, kode)

    def update_level(self, kode, level_baru):
        node = self.search(kode)
        if node:
            node.level = int(level_baru)
            return True
        return False

    def inorder(self):
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


class TestBSTRegistryLokasi(unittest.TestCase):

    def setUp(self):
        self.bst = BSTRegistryLokasi()
        # data awal yang dipakai di banyak test
        self.bst.insert("L003", "Kecamatan Ciawi", 2, 4200, "Siaga")
        self.bst.insert("L001", "Kecamatan Bogor", 1, 8700, "Kritis")
        self.bst.insert("L005", "Kecamatan Dramaga", 3, 2100, "Aman")
        self.bst.insert("L002", "Kecamatan Cibinong", 2, 5300, "Siaga")
        self.bst.insert("L004", "Kecamatan Cileungsi", 1, 3600, "Kritis")

    # --- INSERT ---

    def test_insert_jumlah_node(self):
        self.assertEqual(len(self.bst), 5)

    def test_insert_root_benar(self):
        self.assertEqual(self.bst.root.kode, "L003")

    def test_insert_posisi_anak(self):
        self.assertEqual(self.bst.root.left.kode, "L001")
        self.assertEqual(self.bst.root.right.kode, "L005")

    def test_insert_duplikat_ditolak(self):
        hasil = self.bst.insert("L001", "Duplikat", 3, 0, "Aman")
        self.assertFalse(hasil)
        self.assertEqual(len(self.bst), 5)

    def test_insert_node_baru_kosong(self):
        bst_baru = BSTRegistryLokasi()
        bst_baru.insert("L010", "Kecamatan Tajur", 2, 1500, "Siaga")
        self.assertEqual(bst_baru.root.kode, "L010")
        self.assertEqual(len(bst_baru), 1)

    def test_insert_atribut_tersimpan(self):
        self.bst.insert("L020", "Kecamatan Parung", 3, 900, "Aman")
        node = self.bst.search("L020")
        self.assertEqual(node.nama, "Kecamatan Parung")
        self.assertEqual(node.level, 3)
        self.assertEqual(node.populasi, 900)
        self.assertEqual(node.status, "Aman")

    # --- SEARCH ---

    def test_search_ketemu(self):
        node = self.bst.search("L002")
        self.assertIsNotNone(node)
        self.assertEqual(node.nama, "Kecamatan Cibinong")

    def test_search_tidak_ada(self):
        self.assertIsNone(self.bst.search("L999"))

    def test_search_root(self):
        node = self.bst.search("L003")
        self.assertEqual(node.kode, "L003")

    def test_search_node_paling_kiri(self):
        node = self.bst.search("L001")
        self.assertIsNotNone(node)
        self.assertEqual(node.kode, "L001")

    def test_search_node_paling_kanan(self):
        node = self.bst.search("L005")
        self.assertIsNotNone(node)
        self.assertEqual(node.kode, "L005")

    def test_search_bst_kosong(self):
        bst_kosong = BSTRegistryLokasi()
        self.assertIsNone(bst_kosong.search("L001"))

    # --- UPDATE LEVEL ---

    def test_update_level_berhasil(self):
        self.assertTrue(self.bst.update_level("L005", 1))
        self.assertEqual(self.bst.search("L005").level, 1)

    def test_update_level_gagal_kode_salah(self):
        self.assertFalse(self.bst.update_level("L999", 1))

    def test_update_level_tipe_int(self):
        self.bst.update_level("L001", "3")
        self.assertIsInstance(self.bst.search("L001").level, int)
        self.assertEqual(self.bst.search("L001").level, 3)

    def test_update_level_tidak_ganggu_atribut_lain(self):
        self.bst.update_level("L002", 1)
        node = self.bst.search("L002")
        self.assertEqual(node.nama, "Kecamatan Cibinong")
        self.assertEqual(node.populasi, 5300)
        self.assertEqual(node.status, "Siaga")

    def test_update_level_berulang(self):
        self.bst.update_level("L001", 2)
        self.bst.update_level("L001", 3)
        self.assertEqual(self.bst.search("L001").level, 3)

    # --- INORDER ---

    def test_inorder_urutan_ascending(self):
        kode = [n.kode for n in self.bst.inorder()]
        self.assertEqual(kode, ["L001", "L002", "L003", "L004", "L005"])

    def test_inorder_jumlah_node(self):
        self.assertEqual(len(self.bst.inorder()), 5)

    def test_inorder_bst_kosong(self):
        self.assertEqual(BSTRegistryLokasi().inorder(), [])

    def test_inorder_satu_node(self):
        bst = BSTRegistryLokasi()
        bst.insert("L001", "Solo", 1, 100, "Kritis")
        hasil = bst.inorder()
        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0].kode, "L001")

    def test_inorder_sama_dengan_size(self):
        self.assertEqual(len(self.bst.inorder()), len(self.bst))

    def test_inorder_reflect_update(self):
        # pastikan inorder tetap benar setelah update level
        self.bst.update_level("L003", 1)
        kode = [n.kode for n in self.bst.inorder()]
        self.assertEqual(kode, ["L001", "L002", "L003", "L004", "L005"])
        self.assertEqual(self.bst.search("L003").level, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)