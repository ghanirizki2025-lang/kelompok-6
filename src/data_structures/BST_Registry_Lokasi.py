# BST_Registry_Lokasi.py
# implementasi Binary Search Tree buat nyimpen data lokasi bencana
# kunci pencariannya pake kode lokasi (string), contoh: 'L001', 'DEPOT_0'
# urutan: kode lebih kecil ke kiri, lebih besar ke kanan


# --- node untuk tiap lokasi di pohon ---
class BSTNodeLok:

    def __init__(self, lokasi):
        self.lokasi = lokasi   # objek Lokasi yang disimpan di node ini
        self.left   = None     # anak kiri
        self.right  = None     # anak kanan


# --- pohon BST-nya sendiri ---
class BSTLokasi:

    def __init__(self):
        self.root = None   # mulai kosong

    # --- INSERT ---
    def insert(self, lokasi):
        # kalau pohon masih kosong, langsung jadi root
        if self.root is None:
            self.root = BSTNodeLok(lokasi)
            return

        # kalau udah ada isinya, cari posisi yang bener
        self._insert_rekursif(self.root, lokasi)

    def _insert_rekursif(self, node, lokasi):
        # bandingkan kode baru sama kode node sekarang
        if lokasi.kode < node.lokasi.kode:
            # kode lebih kecil -> harusnya di kiri
            if node.left is None:
                node.left = BSTNodeLok(lokasi)
            else:
                self._insert_rekursif(node.left, lokasi)

        elif lokasi.kode > node.lokasi.kode:
            # kode lebih besar -> harusnya di kanan
            if node.right is None:
                node.right = BSTNodeLok(lokasi)
            else:
                self._insert_rekursif(node.right, lokasi)

        # kalau kodenya sama persis, skip aja (ga boleh duplikat)

    # --- SEARCH ---
    def search(self, kode):
        # cari lokasi berdasarkan kodenya
        # return objek Lokasi kalau ketemu, None kalau tidak
        return self._search_rekursif(self.root, kode)

    def _search_rekursif(self, node, kode):
        # kalau node kosong berarti kode ga ada di pohon
        if node is None:
            return None

        if kode == node.lokasi.kode:
            return node.lokasi   # ketemu

        if kode < node.lokasi.kode:
            # cari ke kiri
            return self._search_rekursif(node.left, kode)
        else:
            # cari ke kanan
            return self._search_rekursif(node.right, kode)

    # --- UPDATE LEVEL ---
    def update_level(self, kode, level_baru):
        # cari lokasinya dulu, terus ganti levelnya
        # return True kalau berhasil, False kalau kode ga ketemu
        lok = self.search(kode)
        if lok is None:
            return False

        lok.level = level_baru   # objek lokasi langsung keubah karena reference
        return True

    # --- INORDER TRAVERSAL ---
    def inorder(self):
        # kembalikan semua lokasi dalam urutan terurut by kode (kiri->akar->kanan)
        # karena BST, hasil inorder otomatis dari kode terkecil ke terbesar
        hasil = []
        self._inorder_rekursif(self.root, hasil)
        return hasil

    def _inorder_rekursif(self, node, hasil):
        if node is None:
            return
        self._inorder_rekursif(node.left, hasil)    # kiri dulu
        hasil.append(node.lokasi)                    # baru ambil isinya
        self._inorder_rekursif(node.right, hasil)   # terus ke kanan

    # --- UTILITAS ---
    def jumlah_node(self):
        # hitung total node yang ada di pohon
        return self._hitung(self.root)

    def _hitung(self, node):
        if node is None:
            return 0
        # 1 (node ini) + semua node di kiri + semua node di kanan
        return 1 + self._hitung(node.left) + self._hitung(node.right)

    def tinggi(self):
        # hitung tinggi pohon, berguna buat ngecek seberapa seimbang BST kita
        return self._tinggi_rekursif(self.root)

    def _tinggi_rekursif(self, node):
        if node is None:
            return 0
        tinggi_kiri   = self._tinggi_rekursif(node.left)
        tinggi_kanan  = self._tinggi_rekursif(node.right)
        # ambil yang lebih tinggi, tambah 1 buat node sekarang
        return 1 + max(tinggi_kiri, tinggi_kanan)

    def __repr__(self):
        return f"BSTLokasi(node={self.jumlah_node()}, tinggi={self.tinggi()})"


# testing langsung kalau file ini dijalankan sendiri
if __name__ == '__main__':

    from dataclasses import dataclass

    @dataclass
    class Lokasi:
        kode: str
        nama: str
        level: int
        populasi: int

    print("test BST_Registry_Lokasi.py")
    print("-" * 35)

    bst = BSTLokasi()

    # insert beberapa data
    data = [
        Lokasi('L010', 'Desa Sumber',   2, 1200),
        Lokasi('L003', 'Kel. Maju',     1,  500),
        Lokasi('L020', 'Desa Harapan',  3, 2000),
        Lokasi('L007', 'Dusun Melati',  1,  300),
        Lokasi('L015', 'Desa Damai',    2,  800),
    ]

    for d in data:
        bst.insert(d)
        print(f"  insert {d.kode}")

    print(f"\nhasil: {bst}")

    # test search
    print("\ncari L007:", bst.search('L007'))
    print("cari L999:", bst.search('L999'))

    # test inorder (harusnya urut)
    print("\ninorder traversal:")
    for lok in bst.inorder():
        print(f"  {lok.kode} - {lok.nama}")

    # test update
    print("\nupdate level L020 ke 1")
    bst.update_level('L020', 1)
    print("cek L020:", bst.search('L020').level)

    # test duplikat
    print("\ncoba insert L010 lagi (harus diabaikan)")
    sebelum = bst.jumlah_node()
    bst.insert(Lokasi('L010', 'duplikat', 3, 0))
    sesudah = bst.jumlah_node()
    print(f"  node sebelum: {sebelum}, sesudah: {sesudah} -> {'ok, ga berubah' if sebelum == sesudah else 'ERROR duplikat masuk'}")