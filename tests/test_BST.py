# test_BST.py
# unit test untuk BST_Registry_Lokasi.py
# jalankan: pytest tests/test_BST.py -v

import sys
import os
import pytest

# naik dua level: tests/ -> KELOMPOK-6/ (root project)
# biar bisa import data_structures dan modules dari mana pun
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from data_structures.BST_Registry_Lokasi import BSTLokasi, BSTNodeLok
from dataclasses import dataclass


# class Lokasi mini buat keperluan test, biar ga perlu import dari models
@dataclass
class Lokasi:
    kode: str
    nama: str
    level: int
    populasi: int
    status: int = 0


# helper buat bikin lokasi dummy cepet
def buat_lok(kode, level=2, populasi=500):
    return Lokasi(kode, f'Desa-{kode}', level, populasi)


# fixture: BST kosong
@pytest.fixture
def bst_kosong():
    return BSTLokasi()


# fixture: BST yang udah ada isinya
@pytest.fixture
def bst_isi():
    bst = BSTLokasi()
    # insert urutan acak biar pohonnya ga jadi linked list
    for kode in ['L010', 'L005', 'L020', 'L003', 'L007', 'L015', 'L025']:
        bst.insert(buat_lok(kode))
    return bst


# -------------------------------------------------------
# TEST INSERT
# -------------------------------------------------------

class TestInsert:

    def test_insert_pertama_jadi_root(self, bst_kosong):
        # node pertama harus langsung masuk jadi root
        bst_kosong.insert(buat_lok('L001'))
        assert bst_kosong.root is not None
        assert bst_kosong.root.lokasi.kode == 'L001'

    def test_insert_nambah_jumlah_node(self, bst_kosong):
        # tiap insert harus nambah jumlah node
        bst_kosong.insert(buat_lok('L001'))
        bst_kosong.insert(buat_lok('L002'))
        bst_kosong.insert(buat_lok('L003'))
        assert bst_kosong.jumlah_node() == 3

    def test_insert_posisi_kiri_kanan(self, bst_kosong):
        # kode lebih kecil harus ke kiri, lebih besar ke kanan
        bst_kosong.insert(buat_lok('L010'))  # root
        bst_kosong.insert(buat_lok('L005'))  # kiri karena L005 < L010
        bst_kosong.insert(buat_lok('L015'))  # kanan karena L015 > L010
        assert bst_kosong.root.left.lokasi.kode == 'L005'
        assert bst_kosong.root.right.lokasi.kode == 'L015'

    def test_insert_duplikat_diabaikan(self, bst_kosong):
        # kalau kode sama, node kedua ga boleh masuk
        bst_kosong.insert(buat_lok('L001'))
        bst_kosong.insert(buat_lok('L001'))  # duplikat
        assert bst_kosong.jumlah_node() == 1

    def test_insert_depot_dan_lokasi(self, bst_kosong):
        # BST harus bisa nyimpen kode DEPOT juga
        bst_kosong.insert(Lokasi('DEPOT_0', 'Gudang 0', 3, 0))
        bst_kosong.insert(buat_lok('L001'))
        assert bst_kosong.jumlah_node() == 2

    def test_insert_banyak_node(self, bst_kosong):
        # coba insert 20 node sekaligus
        for i in range(20):
            bst_kosong.insert(buat_lok(f'L{i:03d}'))
        assert bst_kosong.jumlah_node() == 20


# -------------------------------------------------------
# TEST SEARCH
# -------------------------------------------------------

class TestSearch:

    def test_search_ketemu(self, bst_isi):
        # search kode yang ada harus return objek Lokasi
        hasil = bst_isi.search('L007')
        assert hasil is not None
        assert hasil.kode == 'L007'

    def test_search_tidak_ketemu(self, bst_isi):
        # search kode yang ga ada harus return None
        assert bst_isi.search('L999') is None

    def test_search_bst_kosong(self, bst_kosong):
        # search di BST kosong jangan error, return None aja
        assert bst_kosong.search('L001') is None

    def test_search_root(self, bst_isi):
        # search root node (L010 di fixture ini)
        hasil = bst_isi.search('L010')
        assert hasil is not None
        assert hasil.kode == 'L010'

    def test_search_node_daun(self, bst_isi):
        # L003 itu daun (node paling bawah di kiri), harus tetap ketemu
        hasil = bst_isi.search('L003')
        assert hasil is not None

    def test_search_return_referensi_asli(self, bst_kosong):
        # objek yang dikembalikan harus referensi ke objek aslinya
        # bukan salinan baru, ini penting buat update_level
        lok_asli = buat_lok('L050')
        bst_kosong.insert(lok_asli)
        hasil = bst_kosong.search('L050')
        assert hasil is lok_asli  # harus object yang persis sama


# -------------------------------------------------------
# TEST UPDATE LEVEL
# -------------------------------------------------------

class TestUpdateLevel:

    def test_update_berhasil(self, bst_isi):
        # update level lokasi yang ada harus berhasil
        ok = bst_isi.update_level('L005', 1)
        assert ok is True

    def test_update_nilai_berubah(self, bst_isi):
        # cek levelnya beneran berubah setelah update
        bst_isi.update_level('L005', 1)
        assert bst_isi.search('L005').level == 1

    def test_update_kode_ga_ada(self, bst_isi):
        # update kode yang ga ada harus return False
        ok = bst_isi.update_level('L999', 1)
        assert ok is False

    def test_update_bst_kosong(self, bst_kosong):
        # update di BST kosong jangan error
        assert bst_kosong.update_level('L001', 1) is False

    def test_update_berkali_kali(self, bst_isi):
        # update boleh dilakukan berkali-kali ke node yang sama
        bst_isi.update_level('L010', 1)
        bst_isi.update_level('L010', 3)
        bst_isi.update_level('L010', 2)
        assert bst_isi.search('L010').level == 2

    def test_update_tidak_merusak_struktur(self, bst_isi):
        # setelah update, jumlah node ga boleh berubah
        sebelum = bst_isi.jumlah_node()
        bst_isi.update_level('L015', 1)
        assert bst_isi.jumlah_node() == sebelum


# -------------------------------------------------------
# TEST INORDER TRAVERSAL
# -------------------------------------------------------

class TestInorder:

    def test_inorder_terurut(self, bst_isi):
        # hasil inorder harus urut ascending by kode
        hasil = [lok.kode for lok in bst_isi.inorder()]
        assert hasil == sorted(hasil)

    def test_inorder_jumlah_sama(self, bst_isi):
        # jumlah hasil inorder harus sama dengan jumlah node
        assert len(bst_isi.inorder()) == bst_isi.jumlah_node()

    def test_inorder_bst_kosong(self, bst_kosong):
        # inorder di BST kosong harus return list kosong
        assert bst_kosong.inorder() == []

    def test_inorder_satu_node(self, bst_kosong):
        # BST dengan satu node, inorder harus return list satu elemen
        bst_kosong.insert(buat_lok('L001'))
        hasil = bst_kosong.inorder()
        assert len(hasil) == 1
        assert hasil[0].kode == 'L001'

    def test_inorder_semua_kode_ada(self, bst_isi):
        # semua kode yang diinsert harus muncul di inorder
        kode_diinsert = {'L010', 'L005', 'L020', 'L003', 'L007', 'L015', 'L025'}
        kode_inorder  = {lok.kode for lok in bst_isi.inorder()}
        assert kode_diinsert == kode_inorder

    def test_inorder_insert_urutan_terbalik(self, bst_kosong):
        # insert dari besar ke kecil, inorder tetap harus urut abjad
        for kode in ['L030', 'L020', 'L010', 'L005']:
            bst_kosong.insert(buat_lok(kode))
        hasil = [lok.kode for lok in bst_kosong.inorder()]
        assert hasil == sorted(hasil)


# -------------------------------------------------------
# TEST JUMLAH NODE & TINGGI
# -------------------------------------------------------

class TestUtilitas:

    def test_jumlah_node_kosong(self, bst_kosong):
        assert bst_kosong.jumlah_node() == 0

    def test_jumlah_node_setelah_insert(self, bst_kosong):
        bst_kosong.insert(buat_lok('L001'))
        bst_kosong.insert(buat_lok('L002'))
        assert bst_kosong.jumlah_node() == 2

    def test_tinggi_kosong(self, bst_kosong):
        # pohon kosong tingginya 0
        assert bst_kosong.tinggi() == 0

    def test_tinggi_satu_node(self, bst_kosong):
        # satu node tingginya 1
        bst_kosong.insert(buat_lok('L001'))
        assert bst_kosong.tinggi() == 1

    def test_tinggi_bertambah(self, bst_kosong):
        # rantai kiri L010->L005->L003 harusnya tinggi minimal 3
        bst_kosong.insert(buat_lok('L010'))
        bst_kosong.insert(buat_lok('L005'))
        bst_kosong.insert(buat_lok('L003'))
        assert bst_kosong.tinggi() >= 3

    def test_repr_tidak_error(self, bst_isi):
        # __repr__ jangan error
        hasil = repr(bst_isi)
        assert 'BSTLokasi' in hasil


# -------------------------------------------------------
# TEST SKENARIO LENGKAP (mirip pemakaian di sistem nyata)
# -------------------------------------------------------

class TestSkenario:

    def test_skenario_init_sistem(self):
        # simulasi inisialisasi sistem: generate lokasi, insert semua, cek
        bst = BSTLokasi()
        lokasi_list = [buat_lok(f'L{i:03d}', level=(i % 3) + 1) for i in range(10)]
        lokasi_list.append(Lokasi('DEPOT_0', 'Gudang 0', 3, 0))

        for lok in lokasi_list:
            bst.insert(lok)

        assert bst.jumlah_node() == 11

        # cek depot bisa dicari
        assert bst.search('DEPOT_0') is not None

        # cek inorder urut
        kode_list = [l.kode for l in bst.inorder()]
        assert kode_list == sorted(kode_list)

    def test_skenario_update_lalu_cek(self):
        # update level terus cek hasilnya
        bst = BSTLokasi()
        bst.insert(buat_lok('L001', level=3))

        # awalnya level 3 (RINGAN)
        assert bst.search('L001').level == 3

        # update ke KRITIS
        bst.update_level('L001', 1)
        assert bst.search('L001').level == 1

    def test_skenario_cari_setelah_banyak_insert(self):
        # insert banyak data terus cari yang ada di tengah-tengah
        bst = BSTLokasi()
        kode_target = 'L017'

        for i in range(35):
            bst.insert(buat_lok(f'L{i:03d}'))

        hasil = bst.search(kode_target)
        assert hasil is not None
        assert hasil.kode == kode_target
