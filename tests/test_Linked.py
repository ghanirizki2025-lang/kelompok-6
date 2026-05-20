import unittest


# ── SOURCE CODE LINKED LIST ───────────────────────────────────
class LLNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, data):
        node_baru = LLNode(data)
        if self.head is None:
            self.head = node_baru
        else:
            saat_ini = self.head
            while saat_ini.next is not None:
                saat_ini = saat_ini.next
            saat_ini.next = node_baru
        self._size += 1

    def prepend(self, data):
        node_baru = LLNode(data)
        node_baru.next = self.head
        self.head = node_baru
        self._size += 1

    def hapus(self, data) -> bool:
        if self.head is None:
            return False
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True
        saat_ini = self.head
        while saat_ini.next is not None:
            if saat_ini.next.data == data:
                saat_ini.next = saat_ini.next.next
                self._size -= 1
                return True
            saat_ini = saat_ini.next
        return False

    def cari(self, data) -> bool:
        saat_ini = self.head
        while saat_ini is not None:
            if saat_ini.data == data:
                return True
            saat_ini = saat_ini.next
        return False

    def ke_list(self) -> list:
        hasil = []
        saat_ini = self.head
        while saat_ini is not None:
            hasil.append(saat_ini.data)
            saat_ini = saat_ini.next
        return hasil

    def kosong(self) -> bool:
        return self.head is None

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return " -> ".join(str(x) for x in self.ke_list()) + " -> NULL"


# ── UNIT TEST ─────────────────────────────────────────────────
class TestLLNode(unittest.TestCase):
    """Test unit untuk class LLNode (struktur dasar simpul)."""

    def test_node_default_data_none(self):
        """Node tanpa argumen harus menyimpan data None."""
        node = LLNode()
        self.assertIsNone(node.data)

    def test_node_stores_data(self):
        """Node harus menyimpan data yang diberikan dengan benar."""
        node = LLNode(42)
        self.assertEqual(node.data, 42)

    def test_node_next_default_none(self):
        """Atribut next pada node baru harus None secara default."""
        node = LLNode(10)
        self.assertIsNone(node.next)

    def test_node_next_can_be_linked(self):
        """Dua node harus bisa saling terhubung melalui atribut next."""
        node1 = LLNode(1)
        node2 = LLNode(2)
        node1.next = node2
        self.assertEqual(node1.next.data, 2)


# ─────────────────────────────────────────────────────────────
class TestLinkedListInisialisasi(unittest.TestCase):
    """Test kondisi awal LinkedList saat baru dibuat."""

    def setUp(self):
        self.ll = LinkedList()

    def test_head_awal_none(self):
        """Head pada list baru harus None."""
        self.assertIsNone(self.ll.head)

    def test_size_awal_nol(self):
        """Ukuran list baru harus 0."""
        self.assertEqual(len(self.ll), 0)

    def test_kosong_pada_list_baru(self):
        """List baru harus dalam keadaan kosong."""
        self.assertTrue(self.ll.kosong())

    def test_ke_list_pada_list_kosong(self):
        """ke_list pada list kosong harus mengembalikan list Python kosong."""
        self.assertEqual(self.ll.ke_list(), [])

    def test_repr_list_kosong(self):
        """
        ⚠️  BUG DITEMUKAN di source code:
        __repr__ memanggil " -> ".join([]) yang menghasilkan string kosong "",
        lalu ditambah " -> NULL" sehingga output-nya adalah " -> NULL" (ada spasi di depan).
        Perilaku yang diharapkan seharusnya "-> NULL" atau "NULL" (tanpa spasi).

        Test ini sengaja memverifikasi perilaku aktual source code saat ini.
        Untuk memperbaiki bug, ubah __repr__ agar menangani list kosong secara khusus:
            if self.head is None:
                return "NULL"
        """
        self.assertEqual(repr(self.ll), " -> NULL")


# ─────────────────────────────────────────────────────────────
class TestAppend(unittest.TestCase):
    """Test operasi append (tambah di akhir)."""

    def setUp(self):
        self.ll = LinkedList()

    def test_append_elemen_pertama_jadi_head(self):
        """Elemen pertama yang di-append harus menjadi head."""
        self.ll.append(10)
        self.assertEqual(self.ll.head.data, 10)

    def test_append_urutan_terjaga(self):
        """Elemen harus tersusun sesuai urutan append (FIFO)."""
        self.ll.append(1)
        self.ll.append(2)
        self.ll.append(3)
        self.assertEqual(self.ll.ke_list(), [1, 2, 3])

    def test_append_menambah_size(self):
        """Setiap append harus menambah ukuran list sebesar 1."""
        for i in range(5):
            self.ll.append(i)
        self.assertEqual(len(self.ll), 5)

    def test_append_berbagai_tipe_data(self):
        """Append harus mendukung berbagai tipe data."""
        self.ll.append(100)
        self.ll.append("teks")
        self.ll.append([1, 2])
        self.ll.append({"k": "v"})
        self.assertEqual(len(self.ll), 4)
        self.assertEqual(self.ll.ke_list(), [100, "teks", [1, 2], {"k": "v"}])

    def test_append_nilai_duplikat(self):
        """Append harus bisa menyimpan nilai yang sama lebih dari sekali."""
        self.ll.append(7)
        self.ll.append(7)
        self.ll.append(7)
        self.assertEqual(self.ll.ke_list(), [7, 7, 7])

    def test_append_list_tidak_lagi_kosong(self):
        """Setelah append, list tidak boleh dianggap kosong."""
        self.ll.append(99)
        self.assertFalse(self.ll.kosong())


# ─────────────────────────────────────────────────────────────
class TestPrepend(unittest.TestCase):
    """Test operasi prepend (tambah di awal)."""

    def setUp(self):
        self.ll = LinkedList()

    def test_prepend_pada_list_kosong(self):
        """Prepend pada list kosong harus menjadi head."""
        self.ll.prepend(5)
        self.assertEqual(self.ll.head.data, 5)

    def test_prepend_selalu_jadi_head_baru(self):
        """Setiap prepend harus menggantikan head dengan node baru."""
        self.ll.prepend(1)
        self.ll.prepend(2)
        self.ll.prepend(3)
        self.assertEqual(self.ll.head.data, 3)

    def test_prepend_urutan_terbalik(self):
        """Urutan hasil prepend harus kebalikan dari urutan pemanggilan."""
        self.ll.prepend("A")
        self.ll.prepend("B")
        self.ll.prepend("C")
        self.assertEqual(self.ll.ke_list(), ["C", "B", "A"])

    def test_prepend_menambah_size(self):
        """Setiap prepend harus menambah ukuran list sebesar 1."""
        self.ll.prepend(10)
        self.ll.prepend(20)
        self.assertEqual(len(self.ll), 2)

    def test_prepend_dan_append_kombinasi(self):
        """Kombinasi prepend dan append harus menghasilkan urutan yang benar."""
        self.ll.append(2)    # [2]
        self.ll.append(3)    # [2, 3]
        self.ll.prepend(1)   # [1, 2, 3]
        self.ll.prepend(0)   # [0, 1, 2, 3]
        self.assertEqual(self.ll.ke_list(), [0, 1, 2, 3])


# ─────────────────────────────────────────────────────────────
class TestHapus(unittest.TestCase):
    """Test operasi hapus (hapus node berdasarkan nilai)."""

    def setUp(self):
        self.ll = LinkedList()
        for val in [10, 20, 30, 40, 50]:
            self.ll.append(val)
        # Kondisi awal: [10, 20, 30, 40, 50]

    def test_hapus_elemen_tengah(self):
        """Hapus elemen di tengah list harus berhasil."""
        hasil = self.ll.hapus(30)
        self.assertTrue(hasil)
        self.assertEqual(self.ll.ke_list(), [10, 20, 40, 50])

    def test_hapus_elemen_head(self):
        """Hapus head harus memindahkan head ke node berikutnya."""
        hasil = self.ll.hapus(10)
        self.assertTrue(hasil)
        self.assertEqual(self.ll.head.data, 20)
        self.assertEqual(self.ll.ke_list(), [20, 30, 40, 50])

    def test_hapus_elemen_tail(self):
        """Hapus elemen di akhir (tail) harus berhasil."""
        hasil = self.ll.hapus(50)
        self.assertTrue(hasil)
        self.assertEqual(self.ll.ke_list(), [10, 20, 30, 40])

    def test_hapus_nilai_tidak_ada_return_false(self):
        """Hapus nilai yang tidak ada harus mengembalikan False."""
        hasil = self.ll.hapus(999)
        self.assertFalse(hasil)

    def test_hapus_pada_list_kosong_return_false(self):
        """Hapus pada list kosong harus mengembalikan False."""
        ll_kosong = LinkedList()
        self.assertFalse(ll_kosong.hapus(1))

    def test_hapus_mengurangi_size(self):
        """Hapus yang berhasil harus mengurangi ukuran list sebesar 1."""
        ukuran_awal = len(self.ll)
        self.ll.hapus(20)
        self.assertEqual(len(self.ll), ukuran_awal - 1)

    def test_hapus_hanya_pertama_jika_duplikat(self):
        """Hapus hanya boleh menghapus kemunculan pertama dari nilai duplikat."""
        ll_dup = LinkedList()
        for v in [5, 5, 5]:
            ll_dup.append(v)
        ll_dup.hapus(5)
        self.assertEqual(ll_dup.ke_list(), [5, 5])
        self.assertEqual(len(ll_dup), 2)

    def test_hapus_semua_elemen_hingga_kosong(self):
        """Hapus semua elemen satu per satu hingga list benar-benar kosong."""
        for val in [10, 20, 30, 40, 50]:
            self.ll.hapus(val)
        self.assertTrue(self.ll.kosong())
        self.assertEqual(len(self.ll), 0)

    def test_hapus_tidak_ubah_elemen_lain(self):
        """Elemen yang tidak dihapus harus tetap utuh dan berurutan."""
        self.ll.hapus(30)
        self.assertIn(10, self.ll.ke_list())
        self.assertIn(20, self.ll.ke_list())
        self.assertIn(40, self.ll.ke_list())
        self.assertIn(50, self.ll.ke_list())


# ─────────────────────────────────────────────────────────────
class TestCari(unittest.TestCase):
    """Test operasi cari (pencarian nilai dalam list)."""

    def setUp(self):
        self.ll = LinkedList()
        for val in ["apel", "mangga", "jeruk"]:
            self.ll.append(val)

    def test_cari_nilai_yang_ada(self):
        """Cari nilai yang ada dalam list harus mengembalikan True."""
        self.assertTrue(self.ll.cari("mangga"))

    def test_cari_nilai_di_head(self):
        """Cari nilai yang ada di head harus mengembalikan True."""
        self.assertTrue(self.ll.cari("apel"))

    def test_cari_nilai_di_tail(self):
        """Cari nilai yang ada di tail harus mengembalikan True."""
        self.assertTrue(self.ll.cari("jeruk"))

    def test_cari_nilai_tidak_ada(self):
        """Cari nilai yang tidak ada harus mengembalikan False."""
        self.assertFalse(self.ll.cari("durian"))

    def test_cari_pada_list_kosong(self):
        """Cari pada list kosong harus mengembalikan False."""
        ll_kosong = LinkedList()
        self.assertFalse(ll_kosong.cari("apapun"))

    def test_cari_setelah_hapus(self):
        """Nilai yang sudah dihapus tidak boleh ditemukan lagi."""
        self.ll.hapus("mangga")
        self.assertFalse(self.ll.cari("mangga"))

    def test_cari_setelah_append(self):
        """Nilai yang baru di-append harus langsung bisa ditemukan."""
        self.ll.append("semangka")
        self.assertTrue(self.ll.cari("semangka"))


# ─────────────────────────────────────────────────────────────
class TestKosongDanLen(unittest.TestCase):
    """Test method kosong() dan __len__() (dunder method)."""

    def setUp(self):
        self.ll = LinkedList()

    def test_kosong_true_pada_list_baru(self):
        """List baru harus kosong."""
        self.assertTrue(self.ll.kosong())

    def test_kosong_false_setelah_append(self):
        """List tidak boleh kosong setelah ada elemen."""
        self.ll.append(1)
        self.assertFalse(self.ll.kosong())

    def test_kosong_true_setelah_hapus_semua(self):
        """List harus kembali kosong setelah semua elemen dihapus."""
        self.ll.append(1)
        self.ll.hapus(1)
        self.assertTrue(self.ll.kosong())

    def test_len_sesuai_jumlah_elemen(self):
        """len() harus mencerminkan jumlah elemen yang tepat."""
        for i in range(1, 6):
            self.ll.append(i)
            self.assertEqual(len(self.ll), i)

    def test_len_berkurang_setelah_hapus(self):
        """len() harus berkurang setelah hapus berhasil."""
        self.ll.append(10)
        self.ll.append(20)
        self.ll.hapus(10)
        self.assertEqual(len(self.ll), 1)

    def test_len_tidak_berubah_setelah_hapus_gagal(self):
        """len() tidak boleh berubah jika hapus gagal (nilai tidak ada)."""
        self.ll.append(10)
        self.ll.hapus(999)
        self.assertEqual(len(self.ll), 1)


# ─────────────────────────────────────────────────────────────
class TestKeListDanRepr(unittest.TestCase):
    """Test konversi ke_list() dan representasi __repr__()."""

    def setUp(self):
        self.ll = LinkedList()

    def test_ke_list_urutan_benar(self):
        """ke_list harus mengembalikan elemen dari head ke tail."""
        for v in [1, 2, 3]:
            self.ll.append(v)
        self.assertEqual(self.ll.ke_list(), [1, 2, 3])

    def test_ke_list_tidak_ubah_list_asli(self):
        """Memanggil ke_list berkali-kali harus menghasilkan hasil yang sama."""
        for v in [4, 5, 6]:
            self.ll.append(v)
        hasil1 = self.ll.ke_list()
        hasil2 = self.ll.ke_list()
        self.assertEqual(hasil1, hasil2)

    def test_repr_format_benar(self):
        """Format __repr__ harus: val1 -> val2 -> NULL."""
        self.ll.append(1)
        self.ll.append(2)
        self.ll.append(3)
        self.assertEqual(repr(self.ll), "1 -> 2 -> 3 -> NULL")

    def test_repr_satu_elemen(self):
        """__repr__ dengan satu elemen harus: val -> NULL."""
        self.ll.append(99)
        self.assertEqual(repr(self.ll), "99 -> NULL")


# ─────────────────────────────────────────────────────────────
class TestIntegrasi(unittest.TestCase):
    """Test skenario integrasi lintas operasi."""

    def test_append_cari_hapus_cari(self):
        """Skenario: append → cari (ada) → hapus → cari (tidak ada)."""
        ll = LinkedList()
        ll.append("buku")
        ll.append("pena")
        ll.append("penggaris")

        self.assertTrue(ll.cari("pena"))
        ll.hapus("pena")
        self.assertFalse(ll.cari("pena"))
        self.assertEqual(ll.ke_list(), ["buku", "penggaris"])

    def test_prepend_append_campuran(self):
        """Skenario: gabungan prepend dan append menghasilkan urutan yang benar."""
        ll = LinkedList()
        ll.append(3)     # [3]
        ll.prepend(2)    # [2, 3]
        ll.prepend(1)    # [1, 2, 3]
        ll.append(4)     # [1, 2, 3, 4]
        self.assertEqual(ll.ke_list(), [1, 2, 3, 4])
        self.assertEqual(len(ll), 4)

    def test_hapus_head_berulang(self):
        """Skenario: hapus head berulang kali hingga list kosong."""
        ll = LinkedList()
        for v in [10, 20, 30]:
            ll.append(v)
        ll.hapus(10)
        self.assertEqual(ll.head.data, 20)
        ll.hapus(20)
        self.assertEqual(ll.head.data, 30)
        ll.hapus(30)
        self.assertTrue(ll.kosong())

    def test_stress_1000_elemen(self):
        """Stress test: append dan hapus 1000 elemen harus konsisten."""
        ll = LinkedList()
        n = 1000
        for i in range(n):
            ll.append(i)

        self.assertEqual(len(ll), n)
        self.assertEqual(ll.ke_list()[0], 0)
        self.assertEqual(ll.ke_list()[-1], n - 1)

        # Hapus semua elemen
        for i in range(n):
            ll.hapus(i)

        self.assertTrue(ll.kosong())
        self.assertEqual(len(ll), 0)

    def test_prepend_ke_list_kosong_lalu_hapus(self):
        """Skenario: prepend ke list kosong, lalu hapus, list harus kembali kosong."""
        ll = LinkedList()
        ll.prepend(42)
        self.assertFalse(ll.kosong())
        ll.hapus(42)
        self.assertTrue(ll.kosong())
        self.assertIsNone(ll.head)


# ── RUNNER ────────────────────────────────────────────────────
if __name__ == "__main__":
    unittest.main(verbosity=2)