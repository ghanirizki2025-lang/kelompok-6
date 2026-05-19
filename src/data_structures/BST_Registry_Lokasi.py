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

    