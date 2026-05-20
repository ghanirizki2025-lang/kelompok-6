# =============================================================================
# bst.py
# Implementasi Binary Search Tree (BST) untuk Registry Lokasi Bencana.
#
# Setiap node menyimpan satu objek Lokasi. Kunci pencarian adalah lokasi.kode
# (string), misalnya 'L001', 'DEPOT_0', dsb.
#
# Operasi:
#   insert       — tambah lokasi baru, O(log n) rata-rata
#   search       — cari lokasi by kode, O(log n)
#   update_level — perbarui level bencana, O(log n)
#   inorder      — daftar semua lokasi terurut by kode, O(n)
#
# Catatan BST tidak self-balancing — worst case O(n) jika data masuk terurut.
#
# Mata Kuliah : ELT60213 Algoritma dan Struktur Data
# Topik       : 9 — Disaster Response Logistics System
# =============================================================================

from typing import Optional, List


class BSTNodeLok:
    """
    Satu simpul dalam BST Lokasi.

    Atribut:
        lokasi : objek Lokasi yang disimpan
        left   : anak kiri  (kode lebih kecil secara leksikografis)
        right  : anak kanan (kode lebih besar)
    """

    def __init__(self, lokasi):
        self.lokasi = lokasi
        self.left = None   # sub-pohon kiri
        self.right = None  # sub-pohon kanan


class BSTLokasi:
    """
    Binary Search Tree untuk menyimpan dan mengelola data lokasi bencana.

    Kunci   : lokasi.kode (string), perbandingan leksikografis
    Nilai   : objek Lokasi lengkap

    Contoh urutan kode: DEPOT_0 < DEPOT_1 < L000 < L001 < ... < L034
    """

    def __init__(self):
        self.root = None   # akar pohon, awalnya kosong

    # ------------------------------------------------------------------
    # INSERT
    # ------------------------------------------------------------------
    def insert(self, lokasi):
        """
        Masukkan lokasi baru ke BST.
        Jika kode sudah ada, operasi diabaikan (tidak ada duplikat).
        Big-O: O(log n) rata-rata, O(n) worst case (pohon tidak seimbang).

        Parameter:
            lokasi : objek Lokasi dengan atribut .kode (str)
        """
        if self.root is None:
            self.root = BSTNodeLok(lokasi)
        else:
            self._insert_rekursif(self.root, lokasi)

    def _insert_rekursif(self, node: BSTNodeLok, lokasi):
        """Helper rekursif untuk insert. Bandingkan kode secara leksikografis."""
        if lokasi.kode < node.lokasi.kode:
            # Masuk sub-pohon kiri
            if node.left is None:
                node.left = BSTNodeLok(lokasi)   # temukan slot kosong
            else:
                self._insert_rekursif(node.left, lokasi)  # terus ke bawah

        elif lokasi.kode > node.lokasi.kode:
            # Masuk sub-pohon kanan
            if node.right is None:
                node.right = BSTNodeLok(lokasi)
            else:
                self._insert_rekursif(node.right, lokasi)

        # lokasi.kode == node.lokasi.kode → duplikat, abaikan

    # ------------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------------
    def search(self, kode: str) -> Optional[object]:
        """
        Cari dan kembalikan objek Lokasi berdasarkan kode.
        Kembalikan None jika tidak ditemukan.
        Big-O: O(log n) rata-rata.

        Parameter:
            kode : string kode lokasi, mis. 'L010' atau 'DEPOT_1'

        Return:
            objek Lokasi jika ditemukan, None jika tidak.
        """
        return self._search_rekursif(self.root, kode)

    def _search_rekursif(self, node: Optional[BSTNodeLok], kode: str):
        """Helper rekursif untuk search."""
        if node is None:
            return None   # kode tidak ada dalam pohon

        if kode == node.lokasi.kode:
            return node.lokasi   # ketemu!

        elif kode < node.lokasi.kode:
            # Kode yang dicari lebih kecil → pergi ke kiri
            return self._search_rekursif(node.left, kode)

        else:
            # Kode yang dicari lebih besar → pergi ke kanan
            return self._search_rekursif(node.right, kode)
        
    # ------------------------------------------------------------------
    # UPDATE LEVEL
    # ------------------------------------------------------------------
    def update_level(self, kode: str, level: int) -> bool:
        """
        Perbarui level bencana lokasi yang memiliki kode tertentu.
        Big-O: O(log n) — cukup lakukan search lalu ubah atribut.

        Parameter:
            kode  : kode lokasi yang akan diperbarui
            level : int baru (1=KRITIS, 2=SEDANG, 3=RINGAN)

        Return:
            True jika berhasil, False jika kode tidak ditemukan.
        """
        lok = self.search(kode)
        if lok is not None:
            lok.level = level   # langsung ubah karena objek adalah referensi
            return True
        return False
    
    # ------------------------------------------------------------------
    # INORDER TRAVERSAL
    # ------------------------------------------------------------------
    def inorder(self) -> List:
        """
        Kembalikan semua lokasi dalam urutan terurut by kode (ascending).
        Traversal: kiri → akar → kanan.
        Big-O: O(n) — setiap node dikunjungi tepat satu kali.

        Return:
            list objek Lokasi terurut leksikografis by kode.
        """
        hasil = []
        self._inorder_rekursif(self.root, hasil)
        return hasil

    def _inorder_rekursif(self, node: Optional[BSTNodeLok], hasil: list):
        """Helper rekursif untuk inorder traversal."""
        if node is None:
            return
        self._inorder_rekursif(node.left, hasil)    # kunjungi kiri dulu
        hasil.append(node.lokasi)                    # simpan akar
        self._inorder_rekursif(node.right, hasil)   # kunjungi kanan