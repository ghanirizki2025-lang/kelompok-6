# =============================================================================
# linked_list.py
# Implementasi dasar Node dan LinkedList yang dipakai oleh semua modul lain.
# Struktur ini menjadi fondasi untuk Stack, Queue, Graph, dan BST.
#
# Mata Kuliah : ELT60213 Algoritma dan Struktur Data
# Topik       : 9 — Disaster Response Logistics System
# =============================================================================


class LLNode:
    """
    Satu unit simpul (node) dalam Linked List.

    Atribut:
        data : nilai yang disimpan (bisa apa saja — objek, int, string, dll.)
        next  : referensi ke simpul berikutnya, None jika ini adalah ekor.
    """

    def __init__(self, data=None):
        self.data = data
        self.next = None  # default: belum terhubung ke simpul manapun


class LinkedList:
    """
    Singly Linked List generik.
    Digunakan sebagai struktur pendukung di modul lain (bukan untuk dipakai
    langsung oleh pengguna CLI).

    Operasi utama:
        append   — tambah di akhir, O(n)
        prepend  — tambah di awal, O(1)
        hapus    — hapus node pertama yang nilainya cocok, O(n)
        cari     — cek apakah nilai ada, O(n)
        ke_list  — konversi ke Python list, O(n)
    """

    def __init__(self):
        self.head = None   # simpul pertama
        self._size = 0     # panjang saat ini

    # ------------------------------------------------------------------
    # TAMBAH DI AKHIR
    # ------------------------------------------------------------------
    def append(self, data):
        """
        Tambahkan simpul baru di posisi paling akhir.
        Big-O: O(n) karena harus traversal ke ekor.
        """
        node_baru = LLNode(data)

        if self.head is None:
            # List masih kosong — node baru langsung jadi head
            self.head = node_baru
        else:
            # Jalan sampai ke simpul terakhir
            saat_ini = self.head
            while saat_ini.next is not None:
                saat_ini = saat_ini.next
            saat_ini.next = node_baru

        self._size += 1

    # ------------------------------------------------------------------
    # TAMBAH DI AWAL
    # ------------------------------------------------------------------
    def prepend(self, data):
        """
        Tambahkan simpul baru di posisi paling awal (head).
        Big-O: O(1) karena langsung ganti head.
        """
        node_baru = LLNode(data)
        node_baru.next = self.head
        self.head = node_baru
        self._size += 1

    # ------------------------------------------------------------------
    # HAPUS NILAI
    # ------------------------------------------------------------------
    def hapus(self, data) -> bool:
        """
        Hapus simpul pertama yang menyimpan nilai 'data'.
        Kembalikan True jika berhasil, False jika tidak ditemukan.
        Big-O: O(n).
        """
        if self.head is None:
            return False

        # Kasus khusus: node yang dihapus adalah head
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True

        # Cari simpul sebelum target
        saat_ini = self.head
        while saat_ini.next is not None:
            if saat_ini.next.data == data:
                saat_ini.next = saat_ini.next.next  # lewati node target
                self._size -= 1
                return True
            saat_ini = saat_ini.next

        return False  # data tidak ditemukan

    # ------------------------------------------------------------------
    # CARI NILAI
    # ------------------------------------------------------------------
    def cari(self, data) -> bool:
        """
        Periksa apakah 'data' ada dalam list.
        Big-O: O(n).
        """
        saat_ini = self.head
        while saat_ini is not None:
            if saat_ini.data == data:
                return True
            saat_ini = saat_ini.next
        return False

    # ------------------------------------------------------------------
    # KONVERSI KE PYTHON LIST
    # ------------------------------------------------------------------
    def ke_list(self) -> list:
        """
        Kembalikan semua nilai sebagai Python list (head → tail).
        Big-O: O(n).
        """
        hasil = []
        saat_ini = self.head
        while saat_ini is not None:
            hasil.append(saat_ini.data)
            saat_ini = saat_ini.next
        return hasil

    # ------------------------------------------------------------------
    # UTILITAS
    # ------------------------------------------------------------------
    def kosong(self) -> bool:
        """Kembalikan True jika list tidak memiliki elemen."""
        return self.head is None

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return " -> ".join(str(x) for x in self.ke_list()) + " -> NULL"