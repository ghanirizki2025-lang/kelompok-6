import unittest

class TestLinkedListMurni(unittest.TestCase):
    def setUp(self):
        self.list = LinkedList()

    def test_operasi_linked_list(self):
        # 1. Pengujian Kondisi Awal
        self.assertTrue(self.list.kosong())
        self.assertEqual(len(self.list), 0)
        self.assertEqual(self.list.ke_list(), [])

        # 2. Pengujian Prepend (Tambah di Awal)
        self.list.prepend(20)
        self.list.prepend(10)
        self.assertFalse(self.list.kosong())
        self.assertEqual(len(self.list), 2)
        self.assertEqual(self.list.ke_list(), [10, 20])

        # 3. Pengujian Append (Tambah di Akhir)
        self.list.append(30)
        self.list.append(40)
        self.assertEqual(len(self.list), 4)
        self.assertEqual(self.list.ke_list(), [10, 20, 30, 40])

        # 4. Pengujian Cari Nilai
        self.assertTrue(self.list.cari(30))
        self.assertTrue(self.list.cari(10))
        self.assertFalse(self.list.cari(99))

        # 5. Pengujian Hapus Elemen Tengah
        self.assertTrue(self.list.hapus(20))
        self.assertEqual(self.list.ke_list(), [10, 30, 40])
        self.assertEqual(len(self.list), 3)

        # 6. Pengujian Hapus Elemen Head
        self.assertTrue(self.list.hapus(10))
        self.assertEqual(self.list.ke_list(), [30, 40])
        self.assertEqual(self.list.head.data, 30)

        # 7. Pengujian Hapus Elemen yang Tidak Ada
        self.assertFalse(self.list.hapus(99))
        self.assertEqual(len(self.list), 2)

        # 8. Pengujian Hapus Sisa Elemen Hingga Kosong
        self.assertTrue(self.list.hapus(40))
        self.assertTrue(self.list.hapus(30))
        self.assertTrue(self.list.kosong())
        self.assertEqual(len(self.list), 0)
        self.assertFalse(self.list.hapus(30))

if __name__ == "__main__":
    unittest.main()