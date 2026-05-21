# modul_BST.py
# Modul 3 - BST Registry Lokasi
# berisi fungsi-fungsi untuk ngelola data lokasi pake BST
# dipanggil dari main.py / CLI

import sys
import os
import math

# biar bisa import dari folder data_structures
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_structures.BST_Registry_Lokasi import BSTLokasi

# konstanta level bencana, angka kecil = lebih darurat
LEVEL_BENCANA = {
    'KRITIS': 1,
    'SEDANG': 2,
    'RINGAN': 3,
}

# buat balik dari angka ke nama, kepake buat print output
LABEL_LEVEL = {1: 'KRITIS', 2: 'SEDANG', 3: 'RINGAN'}


def isi_bst(bst, lokasi_list):
    # masukin semua lokasi ke BST satu-satu
    # dipanggil sekali pas program pertama jalan
    for lok in lokasi_list:
        bst.insert(lok)


def cari_lokasi(bst, kode):
    # cari lokasi berdasarkan kodenya, misal 'L010' atau 'DEPOT_1'
    # kalau ga ketemu langsung print pesan error
    hasil = bst.search(kode)
    if hasil is None:
        print(f"  lokasi '{kode}' tidak ada di registry")
    return hasil


def perbarui_level(bst, kode, level_baru):
    # update level bencana suatu lokasi
    # level_baru berupa string: 'KRITIS', 'SEDANG', atau 'RINGAN'
    # return True kalau berhasil, False kalau gagal

    lvl = level_baru.upper()

    # cek dulu levelnya valid ga
    if lvl not in LEVEL_BENCANA:
        print(f"  level '{level_baru}' tidak dikenal")
        print(f"  pilihan: {', '.join(LEVEL_BENCANA.keys())}")
        return False

    angka = LEVEL_BENCANA[lvl]
    ok = bst.update_level(kode, angka)

    if ok:
        print(f"  {kode} sekarang jadi {lvl} (level {angka})")
    else:
        print(f"  lokasi '{kode}' tidak ditemukan, tidak ada yang diubah")

    return ok


def daftar_semua_lokasi(bst):
    # kembalikan semua lokasi urut abjad berdasarkan kode
    # hasil inorder traversal BST secara otomatis sudah terurut
    return bst.inorder()


def rekap_per_level(bst):
    # kelompokkan lokasi bencana berdasarkan levelnya
    # depot dilewati karena bukan lokasi terdampak

    hasil = {1: [], 2: [], 3: []}

    for lok in bst.inorder():
        if 'DEPOT' in lok.kode:
            continue
        if lok.level in hasil:
            hasil[lok.level].append(lok)

    return hasil


def tampilkan_semua_lokasi(bst, skip_depot=False):
    # print tabel lokasi ke terminal
    # kalau skip_depot=True maka depot ga ditampilin

    data = bst.inorder()

    if skip_depot:
        data = [x for x in data if 'DEPOT' not in x.kode]

    if len(data) == 0:
        print("  tidak ada data lokasi")
        return

    print(f"\n  {'No':<5} {'Kode':<10} {'Nama':<25} {'Level':<8} {'Populasi':>9}")
    print(f"  {'-'*60}")

    for i, lok in enumerate(data, 1):
        label = LABEL_LEVEL.get(lok.level, '-')
        print(f"  {i:<5} {lok.kode:<10} {lok.nama:<25} {label:<8} {lok.populasi:>9}")

    print(f"  {'-'*60}")
    print(f"  total {len(data)} lokasi\n")


def tampilkan_rekap_level(bst):
    # print ringkasan jumlah lokasi per level bencana

    data = rekap_per_level(bst)
    total = sum(len(v) for v in data.values())

    print("\n  rekap level bencana:")
    print(f"  {'-'*30}")
    for lvl in [1, 2, 3]:
        nama  = LABEL_LEVEL[lvl]
        n     = len(data[lvl])
        bar   = '|' * n   # bar sederhana biar keliatan proporsinya
        print(f"  {nama:<7}: {n:>3} lokasi  {bar}")
    print(f"  {'-'*30}")
    print(f"  total  : {total:>3} lokasi\n")


def tampilkan_info_bst(bst):
    # print info teknis BST: jumlah node, tinggi pohon, dll
    # berguna buat laporan / debugging

    n      = bst.jumlah_node()
    tinggi = bst.tinggi()
    ideal  = round(math.log2(n + 1), 1) if n > 0 else 0

    print(f"\n  info BST:")
    print(f"  jumlah node  : {n}")
    print(f"  tinggi pohon : {tinggi}")
    print(f"  search ideal : ~{ideal} langkah (log2 {n})")
    print(f"  search worst : {n} langkah\n")


# jalankan file ini langsung buat demo/testing
# python modules/modul_BST.py

if __name__ == '__main__':

    from dataclasses import dataclass

    # buat class Lokasi sederhana buat testing tanpa import main
    @dataclass
    class Lokasi:
        kode: str
        nama: str
        level: int
        populasi: int
        status: int = 0

    print("=== TEST modul_BST.py ===\n")

    # data contoh buat testing
    contoh = [
        Lokasi('DEPOT_0', 'Gudang Utara',    3,    0),
        Lokasi('DEPOT_1', 'Gudang Selatan',  3,    0),
        Lokasi('L010',    'Desa Sumber Rejo', 2, 1500),
        Lokasi('L003',    'Kel. Maju',        1,  800),
        Lokasi('L025',    'Desa Harapan',     3, 2200),
        Lokasi('L007',    'Dusun Melati',     1,  430),
        Lokasi('L018',    'Kel. Damai',       2,  990),
        Lokasi('L001',    'Desa Sejahtera',   3,  670),
        Lokasi('L033',    'Kampung Baru',     2, 1100),
    ]

    # init BST
    bst = BSTLokasi()
    isi_bst(bst, contoh)

    # cek info pohon
    tampilkan_info_bst(bst)

    # lihat semua lokasi
    print("semua lokasi (urut kode):")
    tampilkan_semua_lokasi(bst)

    # coba cari
    print("cari L007:")
    lok = cari_lokasi(bst, 'L007')
    if lok:
        print(f"  ketemu -> {lok.nama}, level {LABEL_LEVEL[lok.level]}\n")

    print("cari L099 (tidak ada):")
    cari_lokasi(bst, 'L099')

    # update level
    print("\nupdate level:")
    perbarui_level(bst, 'L025', 'KRITIS')
    perbarui_level(bst, 'L003', 'SEDANG')
    perbarui_level(bst, 'L099', 'KRITIS')  # ga ada
    perbarui_level(bst, 'L010', 'PARAH')   # level salah

    # rekap setelah update
    print("\nrekap setelah update:")
    tampilkan_rekap_level(bst)

    # lokasi bencana saja
    print("lokasi bencana (tanpa depot):")
    tampilkan_semua_lokasi(bst, skip_depot=True)

    print("=== selesai ===")
