import unittest

# ==============================================================================
# STRUCTURE DATA: BST REGISTRY LOKASI (PURE IMPLEMENTATION)
# ==============================================================================
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

    def insert(self, kode, nama, level, populasi, status) -> bool:
        node_baru = BSTNode(kode, nama, level, populasi, status)
        if self.root is None:
            self.root = node_baru
            self._size += 1
            return True
        return self._insert_rekursif(self.root, node_baru)

    def _insert_rekursif(self, cur, node_baru) -> bool:
        if node_baru.kode < cur.kode:
            if cur.left is None:
                cur.left = node_baru
                self._size += 1
                return True
            return self._insert_rekursif(cur.left, node_baru)
        elif node_baru.kode > cur.kode:
            if cur.right is None:
                cur.right = node_baru
                self._size += 1
                return True
            return self._insert_rekursif(cur.right, node_baru)
        return False

    def search(self, kode) -> BSTNode:
        return self._search_rekursif(self.root, kode)

    def _search_rekursif(self, cur, kode) -> BSTNode:
        if cur is None or cur.kode == kode:
            return cur
        if kode < cur.kode:
            return self._search_rekursif(cur.left, kode)
        return self._search_rekursif(cur.right, kode)

    def update_level(self, kode, level_baru) -> bool:
        node = self.search(kode)
        if node:
            node.level = int(level_baru)
            return True
        return False

    def inorder(self) -> list:
        hasil = []
        self._inorder_rekursif(self.root, hasil)
        return hasil

    def _inorder_rekursif(self, cur, hasil):
        if cur:
            self._inorder_rekursif(cur.left, hasil)
            hasil.append(cur)
            self._inorder_rekursif(cur.right, hasil)

    def __len__(self) -> int:
        return self._size


# ==============================================================================
# COMPACT UNIT TESTING
# ==============================================================================
class TestBSTRegistryMurni(unittest.TestCase):

    def setUp(self):
        self.bst = BSTRegistryLokasi()

    def test_bst_operations(self):
        # 1. Test Insert & Kaidah Pohon BST
        self.assertTrue(self.bst.insert("L002", "Kecamatan B", 2, 5000, "Siaga"))
        self.assertTrue(self.bst.insert("L001", "Kecamatan A", 1, 3500, "Kritis"))
        self.assertTrue(self.bst.insert("L003", "Kecamatan C", 3, 1200, "Aman"))
        self.assertFalse(self.bst.insert("L002", "Duplikat", 2, 100, "Siaga")) # Harus ditolak
        self.assertEqual(len(self.bst), 3)
        self.assertEqual(self.bst.root.kode, "L002")
        self.assertEqual(self.bst.root.left.kode, "L001")
        self.assertEqual(self.bst.root.right.kode, "L003")

        # 2. Test Search (Ketemu & Tidak Ketemu)
        node = self.bst.search("L001")
        self.assertIsNotNone(node)
        self.assertEqual(node.nama, "Kecamatan A")
        self.assertIsNone(self.bst.search("L999"))

        # 3. Test Update Level
        self.assertTrue(self.bst.update_level("L001", 3))
        self.assertEqual(self.bst.search("L001").level, 3)
        self.assertFalse(self.bst.update_level("L999", 1)) # Kode fiktif

        # 4. Test Inorder Traversal (Sorting Ascending Otomatis)
        self.bst.insert("L000", "Wilayah Baru", 2, 100, "Siaga")
        kunci_terurut = [n.kode for n in self.bst.inorder()]
        self.assertEqual(kunci_terurut, ["L000", "L001", "L002", "L003"])


if __name__ == "__main__":
    unittest.main(verbosity=1)