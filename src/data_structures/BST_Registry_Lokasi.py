# ================================================================
# bst_lokasi.py
# MODUL 3 — BST Registry Lokasi Bencana
# Topik 9: Disaster Response Logistics System
# ELT60213 Algoritma dan Struktur Data | TA 2025/2026
#
# Spesifikasi (sesuai dokumen):
#   - Kunci BST   : kode_lokasi (string)
#   - Data simpan : kode, nama, level, populasi, status
#   - Operasi     : insert, search, update_level, inorder
#   - Big-O       : O(log n) rata-rata
# ================================================================
#
# KONSEP BST — UNTUK PEMULA
# ─────────────────────────────────────────────────────────────────
#
#  Bayangkan BST seperti permainan tebak angka:
#  "Angkanya lebih besar atau lebih kecil dari 50?"
#  → Lebih kecil : cari di KIRI
#  → Lebih besar : cari di KANAN
#  → Tepat       : KETEMU!
#
#  Contoh BST dengan 7 lokasi (dimasukkan secara acak):
#
#                  [L010]          ← ROOT (pertama dimasukkan)
#                 /       \
#            [L005]       [L020]
#            /    \       /    \
#         [L002] [L007] [L015] [L025]
#
#  Aturan BST (selalu terjaga):
#    node.kiri  < node  (semua di kiri lebih kecil)
#    node.kanan > node  (semua di kanan lebih besar)
#
#  Cari "L007":
#    Mulai L010 → L007 < L010 → ke KIRI
#    Sampai L005 → L007 > L005 → ke KANAN
#    Sampai L007 → KETEMU! ✓  (hanya 3 langkah dari 7 data)
#
#  Bandingkan dengan Linked List:
#    L002 → L005 → L007 → ... harus scan 1 per 1 → O(n)
#
#  BST jauh lebih cepat: O(log n) vs O(n)
# ─────────────────────────────────────────────────────────────────


# ================================================================
# BAGIAN 1: DATA CLASS LOKASI
# ================================================================

class Lokasi:
    """
    Menyimpan data satu lokasi bencana.
    Atribut 'kode' digunakan sebagai KUNCI BST.

    Contoh kode: 'DEPOT_0', 'L000', 'L001', ..., 'L034'
    Perbandingan kode menggunakan urutan string (leksikografis),
    seperti urutan kata di kamus.
    """
    def __init__(self, kode, nama, level, populasi, status=0):
        self.kode     = kode      # ← KUNCI BST (string)
        self.nama     = nama      # nama desa/kelurahan/depot
        self.level    = level     # 1=KRITIS, 2=SEDANG, 3=RINGAN
        self.populasi = populasi  # jumlah jiwa terdampak
        self.status   = status    # 0=menunggu, 1=dalam_penanganan, 2=selesai

    def __str__(self):
        level_label  = {1: 'KRITIS', 2: 'SEDANG', 3: 'RINGAN'}
        status_label = {0: 'Menunggu', 1: 'Dalam Penanganan', 2: 'Selesai'}
        return (f"[{self.kode}] {self.nama} | "
                f"Level: {level_label.get(self.level, '?')} | "
                f"Populasi: {self.populasi:,} jiwa | "
                f"Status: {status_label.get(self.status, '?')}")


# ================================================================
# BAGIAN 2: BST NODE
# ================================================================

class BSTNode:
    """
    Satu 'kotak' dalam pohon BST.

    Setiap BSTNode menyimpan:
      - lokasi : data Lokasi
      - left   : referensi ke anak kiri (kode lebih kecil)
      - right  : referensi ke anak kanan (kode lebih besar)

    Visualisasi satu node:
        ┌─────────────────┐
        │  lokasi: Lokasi │
        ├────────┬────────┤
        │  left  │ right  │
        └───┬────┴────┬───┘
            ↓         ↓
         (kecil)   (besar)
    """
    def __init__(self, lokasi):
        self.lokasi = lokasi   # data yang disimpan
        self.left   = None     # anak kiri
        self.right  = None     # anak kanan


# ================================================================
# BAGIAN 3: BST REGISTRY LOKASI
# ================================================================

class BSTLokasi:
    """
    Binary Search Tree untuk Registry Lokasi Bencana.

    Kunci BST : lokasi.kode (string)
    Operasi   : insert, search, update_level, update_status, inorder
    Big-O     : O(log n) rata-rata untuk insert/search/update
                O(n) untuk inorder (kunjungi semua node)
    """

    def __init__(self):
        self.root    = None   # akar pohon, awalnya kosong
        self._jumlah = 0      # counter jumlah node


    # ──────────────────────────────────────────────────────────────
    # OPERASI 1: INSERT
    # Sisipkan lokasi baru ke dalam BST
    # ──────────────────────────────────────────────────────────────

    def insert(self, lokasi):
        """
        Masukkan lokasi baru ke BST berdasarkan lokasi.kode.

        Big-O waktu : O(log n) rata-rata
                      O(n) worst-case (jika data dimasukkan terurut)
        Big-O ruang : O(log n) karena rekursi menggunakan call stack

        Langkah-langkah:
          1. Jika pohon kosong → lokasi langsung jadi root
          2. Bandingkan kode lokasi baru dengan node saat ini
          3. Kode lebih kecil → cari posisi di KIRI
          4. Kode lebih besar → cari posisi di KANAN
          5. Jika posisi kosong (None) → sisipkan di sini
          6. Jika kode sama → duplikat, abaikan
        """
        if self.root is None:
            # Pohon masih kosong, lokasi ini menjadi root
            self.root = BSTNode(lokasi)
            self._jumlah += 1
        else:
            # Pohon sudah ada, cari posisi yang tepat
            berhasil = self._insert_rekursif(self.root, lokasi)
            if berhasil:
                self._jumlah += 1

    def _insert_rekursif(self, node, lokasi):
        """
        Fungsi pembantu (helper) untuk insert secara rekursif.
        Kembalikan True jika berhasil disisipkan, False jika duplikat.
        """
        if lokasi.kode < node.lokasi.kode:
            # ── Kode lebih kecil → pergi ke KIRI ─────────────────
            if node.left is None:
                # Posisi kiri kosong → sisipkan di sini!
                node.left = BSTNode(lokasi)
                return True
            else:
                # Posisi kiri sudah ada → terus ke bawah
                return self._insert_rekursif(node.left, lokasi)

        elif lokasi.kode > node.lokasi.kode:
            # ── Kode lebih besar → pergi ke KANAN ────────────────
            if node.right is None:
                # Posisi kanan kosong → sisipkan di sini!
                node.right = BSTNode(lokasi)
                return True
            else:
                # Posisi kanan sudah ada → terus ke bawah
                return self._insert_rekursif(node.right, lokasi)

        else:
            # ── Kode sama persis → DUPLIKAT, tolak ───────────────
            return False


    # ──────────────────────────────────────────────────────────────
    # OPERASI 2: SEARCH
    # Cari lokasi berdasarkan kode
    # ──────────────────────────────────────────────────────────────

    def search(self, kode):
        """
        Cari dan kembalikan objek Lokasi berdasarkan kode.

        Big-O waktu : O(log n) rata-rata
                      O(n) worst-case

        Kembalikan : objek Lokasi jika ditemukan
                     None jika tidak ditemukan

        Cara kerja (seperti mencari kata di kamus):
          - Mulai dari root (halaman tengah)
          - Kode dicari < kode node saat ini → buka halaman sebelumnya (kiri)
          - Kode dicari > kode node saat ini → buka halaman sesudahnya (kanan)
          - Ulangi sampai ketemu atau ujung pohon (None)
        """
        node = self._search_rekursif(self.root, kode)
        return node.lokasi if node is not None else None

    def _search_rekursif(self, node, kode):
        """
        Fungsi pembantu (helper) untuk search secara rekursif.
        Kembalikan BSTNode yang cocok, atau None jika tidak ada.
        """
        # BASIS: sampai ujung pohon → tidak ditemukan
        if node is None:
            return None

        if kode == node.lokasi.kode:
            # KETEMU! Kembalikan node ini
            return node

        elif kode < node.lokasi.kode:
            # Kode yang dicari lebih kecil → cari di KIRI
            return self._search_rekursif(node.left, kode)

        else:
            # Kode yang dicari lebih besar → cari di KANAN
            return self._search_rekursif(node.right, kode)


    # ──────────────────────────────────────────────────────────────
    # OPERASI 3: UPDATE LEVEL
    # Perbarui level bencana suatu lokasi
    # ──────────────────────────────────────────────────────────────

    def update_level(self, kode, level_baru):
        """
        Perbarui level bencana lokasi dengan kode tertentu.

        Big-O waktu : O(log n) rata-rata (search dulu, lalu update)

        Parameter:
          kode      : kode lokasi yang ingin diupdate
          level_baru: 1=KRITIS, 2=SEDANG, 3=RINGAN

        Kembalikan:
          True  jika berhasil diupdate
          False jika kode tidak ditemukan
        """
        level_label = {1: 'KRITIS', 2: 'SEDANG', 3: 'RINGAN'}

        if level_baru not in level_label:
            print(f"  [!] Level tidak valid. Gunakan 1 (KRITIS), 2 (SEDANG), atau 3 (RINGAN)")
            return False

        # Cari node terlebih dahulu
        node = self._search_rekursif(self.root, kode)

        if node is not None:
            level_lama        = node.lokasi.level
            node.lokasi.level = level_baru
            print(f"  [✓] {kode}: level diperbarui "
                  f"{level_label[level_lama]} → {level_label[level_baru]}")
            print(f"      Big-O: O(log n), n = {self._jumlah} lokasi")
            return True
        else:
            print(f"  [!] Lokasi '{kode}' tidak ditemukan dalam BST")
            return False


    # ──────────────────────────────────────────────────────────────
    # OPERASI 4: UPDATE STATUS
    # Perbarui status penanganan suatu lokasi
    # ──────────────────────────────────────────────────────────────

    def update_status(self, kode, status_baru):
        """
        Perbarui status penanganan lokasi.

        Big-O waktu : O(log n) rata-rata

        Parameter status_baru:
          0 = Menunggu
          1 = Dalam Penanganan
          2 = Selesai

        Kembalikan True jika berhasil, False jika tidak ditemukan.
        """
        status_label = {0: 'Menunggu', 1: 'Dalam Penanganan', 2: 'Selesai'}

        if status_baru not in status_label:
            print(f"  [!] Status tidak valid. Gunakan 0, 1, atau 2")
            return False

        node = self._search_rekursif(self.root, kode)

        if node is not None:
            node.lokasi.status = status_baru
            return True

        return False


    # ──────────────────────────────────────────────────────────────
    # OPERASI 5: INORDER TRAVERSAL
    # Daftar semua lokasi terurut berdasarkan kode
    # ──────────────────────────────────────────────────────────────

    def inorder(self):
        """
        Kembalikan semua lokasi dalam urutan KODE TERURUT (A → Z).

        Big-O waktu : O(n) — kunjungi semua node tepat 1 kali
        Big-O ruang : O(n) — menyimpan semua lokasi dalam list

        Mengapa inorder = terurut?
        ─────────────────────────
        Pola traversal INORDER: KIRI → ROOT → KANAN
        Karena properti BST: kiri < root < kanan
        → Urutan kunjungan otomatis dari kecil ke besar!

        Contoh pohon:
                [L010]
               /       \\
           [L005]     [L020]
           /    \\
         [L002] [L007]

        Inorder: L002 → L005 → L007 → L010 → L020  ✓ (terurut!)
        """
        hasil = []
        self._inorder_rekursif(self.root, hasil)
        return hasil

    def _inorder_rekursif(self, node, hasil):
        """
        Fungsi pembantu inorder.
        Pola: kiri dulu → catat node ini → kanan
        """
        if node is None:
            return
        self._inorder_rekursif(node.left,  hasil)   # 1. kunjungi KIRI
        hasil.append(node.lokasi)                    # 2. catat node ini
        self._inorder_rekursif(node.right, hasil)   # 3. kunjungi KANAN


    # ──────────────────────────────────────────────────────────────
    # OPERASI TAMBAHAN: FILTER BERDASARKAN LEVEL
    # ──────────────────────────────────────────────────────────────

    def filter_level(self, level):
        """
        Kembalikan semua lokasi dengan level bencana tertentu.

        Big-O waktu : O(n)
        Alasan O(n): BST diindeks berdasarkan 'kode', bukan 'level'.
        Jadi harus scan semua node untuk mencari yang levelnya cocok.
        Tidak bisa O(log n) seperti search berdasarkan kode.
        """
        semua = self.inorder()
        return [lok for lok in semua if lok.level == level]


    # ──────────────────────────────────────────────────────────────
    # FUNGSI STATISTIK & ANALISIS POHON
    # ──────────────────────────────────────────────────────────────

    def jumlah_node(self):
        """Total lokasi tersimpan. Big-O: O(1)"""
        return self._jumlah

    def tinggi(self):
        """
        Tinggi pohon = panjang jalur terpanjang dari root ke daun.

        Big-O: O(n)

        Penting untuk analisis laporan:
          - BST SEIMBANG (data acak)  : tinggi ≈ log₂(n)
          - BST MIRING (data terurut) : tinggi = n  [WORST CASE!]

          Contoh 38 lokasi:
            Data acak   → tinggi ≈ log₂(38) ≈ 6  (efisien!)
            Data terurut → tinggi = 38           (sama seperti Linked List)
        """
        return self._tinggi_rekursif(self.root)

    def _tinggi_rekursif(self, node):
        if node is None:
            return 0
        kiri  = self._tinggi_rekursif(node.left)
        kanan = self._tinggi_rekursif(node.right)
        return 1 + max(kiri, kanan)

    def distribusi_level(self):
        """
        Hitung jumlah lokasi per level bencana.
        Big-O: O(n)
        """
        semua  = self.inorder()
        dist   = {1: 0, 2: 0, 3: 0}
        for lok in semua:
            if lok.level in dist:
                dist[lok.level] += 1
        return dist


    # ──────────────────────────────────────────────────────────────
    # VISUALISASI POHON (untuk demo presentasi)
    # ──────────────────────────────────────────────────────────────

    def tampilkan_pohon(self):
        """
        Cetak struktur pohon BST ke terminal.
        Berguna saat demo presentasi kepada dosen!

        Contoh output:
          L010 [SEDANG]
          ├── L005 [KRITIS]
          │   ├── L002 [KRITIS]
          │   └── L007 [SEDANG]
          └── L020 [RINGAN]
              ├── L015 [RINGAN]
              └── L025 [KRITIS]
        """
        level_label = {1: 'KRITIS', 2: 'SEDANG', 3: 'RINGAN'}

        if self.root is None:
            print("  (Pohon BST kosong)")
            return

        print(f"  {self.root.lokasi.kode} [{level_label.get(self.root.lokasi.level,'?')}]")
        self._cetak_rekursif(self.root.left,  "  ", True)
        self._cetak_rekursif(self.root.right, "  ", False)

    def _cetak_rekursif(self, node, prefix, is_left):
        if node is None:
            return
        level_label = {1: 'KRITIS', 2: 'SEDANG', 3: 'RINGAN'}
        connector   = "├── " if is_left else "└── "
        print(f"{prefix}{connector}{node.lokasi.kode} "
              f"[{level_label.get(node.lokasi.level,'?')}]")
        extension = "│   " if is_left else "    "
        self._cetak_rekursif(node.left,  prefix + extension, True)
        self._cetak_rekursif(node.right, prefix + extension, False)

    def __repr__(self):
        return (f"BSTLokasi("
                f"n={self._jumlah}, "
                f"tinggi={self.tinggi()}, "
                f"root='{self.root.lokasi.kode if self.root else None}')")


# ================================================================
# BAGIAN 4: DEMO & UJI COBA
# ================================================================

def demo_bst():
    """
    Demo lengkap semua operasi BST.
    Jalankan file ini langsung: python bst_lokasi.py
    """

    GARIS = "─" * 55

    print("\n" + "=" * 55)
    print("  DEMO BST REGISTRY LOKASI BENCANA")
    print("  Modul 3 | Topik 9 | ELT60213")
    print("=" * 55)

    # ── Buat BST ──────────────────────────────────────────────────
    bst = BSTLokasi()

    # Data lokasi (sengaja TIDAK dimasukkan berurutan
    # agar pohon relatif seimbang)
    data_lokasi = [
        Lokasi('L010', 'Desa Makmur Jaya',    2, 1200),
        Lokasi('L005', 'Desa Sukajadi',        1, 3000),
        Lokasi('L020', 'Desa Cempaka Indah',   3,  800),
        Lokasi('L002', 'Desa Harapan Baru',    1, 4500),
        Lokasi('L007', 'Desa Mekar Sari',      2, 2100),
        Lokasi('L015', 'Desa Sejahtera',       3, 1500),
        Lokasi('L025', 'Desa Berkah Abadi',    1, 5000),
        Lokasi('DEPOT_0', 'Gudang Logistik 0', 3,    0),
    ]

    # ── Demo INSERT ───────────────────────────────────────────────
    print(f"\n{'INSERT — Memasukkan 8 lokasi ke BST':^55}")
    print(GARIS)
    for lok in data_lokasi:
        bst.insert(lok)
        print(f"  insert('{lok.kode}') → "
              f"jumlah={bst.jumlah_node()}, tinggi={bst.tinggi()}")

    print(f"\n  Total node : {bst.jumlah_node()}")
    print(f"  Tinggi BST : {bst.tinggi()} (log₂8 = 3.0, ideal)")

    # ── Visualisasi Pohon ─────────────────────────────────────────
    print(f"\n{'STRUKTUR POHON BST':^55}")
    print(GARIS)
    bst.tampilkan_pohon()

    # ── Demo SEARCH ───────────────────────────────────────────────
    print(f"\n{'SEARCH — Mencari lokasi berdasarkan kode':^55}")
    print(GARIS)

    kode_cari_list = ['L007', 'DEPOT_0', 'L999']
    for kode in kode_cari_list:
        hasil = bst.search(kode)
        if hasil:
            print(f"  search('{kode}') → DITEMUKAN: {hasil}")
        else:
            print(f"  search('{kode}') → TIDAK DITEMUKAN (None)")
    print(f"  Big-O: O(log n), n={bst.jumlah_node()}, tinggi={bst.tinggi()}")

    # ── Demo UPDATE LEVEL ─────────────────────────────────────────
    print(f"\n{'UPDATE LEVEL — Memperbarui level bencana':^55}")
    print(GARIS)

    print("  Situasi: kondisi L020 memburuk, dari RINGAN → KRITIS")
    bst.update_level('L020', 1)

    print("\n  Situasi: L010 berhasil ditangani, SEDANG → RINGAN")
    bst.update_level('L010', 3)

    print("\n  Coba update kode yang tidak ada:")
    bst.update_level('L999', 1)

    # ── Demo INORDER ──────────────────────────────────────────────
    print(f"\n{'INORDER — Daftar lokasi terurut berdasarkan kode':^55}")
    print(GARIS)

    semua = bst.inorder()
    print(f"  {len(semua)} lokasi terurut (Big-O: O(n)):\n")
    for i, lok in enumerate(semua, 1):
        level_label  = {1:'KRITIS', 2:'SEDANG', 3:'RINGAN'}
        print(f"  {i:2}. {lok.kode:<12} {lok.nama:<25} "
              f"[{level_label.get(lok.level,'?')}]")

    # ── Demo FILTER LEVEL ─────────────────────────────────────────
    print(f"\n{'FILTER LEVEL — Lokasi KRITIS saja':^55}")
    print(GARIS)

    kritis = bst.filter_level(1)
    print(f"  Ditemukan {len(kritis)} lokasi KRITIS (Big-O: O(n)):")
    for lok in kritis:
        print(f"    → {lok.kode}: {lok.nama} | Populasi: {lok.populasi:,}")

    # ── Distribusi Level ──────────────────────────────────────────
    print(f"\n{'DISTRIBUSI LEVEL BENCANA':^55}")
    print(GARIS)

    dist = bst.distribusi_level()
    print(f"  KRITIS  (level 1) : {dist[1]} lokasi")
    print(f"  SEDANG  (level 2) : {dist[2]} lokasi")
    print(f"  RINGAN  (level 3) : {dist[3]} lokasi")

    # ── Demo Worst-Case ───────────────────────────────────────────
    print(f"\n{'ANALISIS WORST-CASE: Data Terurut':^55}")
    print(GARIS)

    bst_miring = BSTLokasi()
    kode_terurut = ['L001','L002','L003','L004','L005']
    print("  Insert berurutan: L001, L002, L003, L004, L005")
    for k in kode_terurut:
        bst_miring.insert(Lokasi(k, f'Desa {k}', 1, 100))
    print(f"  Tinggi BST miring   = {bst_miring.tinggi()} (= n, worst-case!)")
    print(f"  Tinggi BST seimbang = {bst.tinggi()} (≈ log₂n, rata-rata)")
    print(f"\n  → Kesimpulan: data terurut membuat BST seperti Linked List!")
    print(f"    Solusi: acak (shuffle) data sebelum dimasukkan ke BST")

    print("\n" + "=" * 55)
    print("  Demo selesai.")
    print("=" * 55)


# ── Jalankan demo jika file ini dieksekusi langsung ──────────────
if __name__ == '__main__':
    demo_bst()
