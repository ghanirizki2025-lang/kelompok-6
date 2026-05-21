# ============================================================
#  MODULE 1 : GRAPH JARINGAN RUTE
#  Graf berbobot tidak berarah menggunakan Adjacency List
#  berbasis Linked List.
#  Big-O: add O(1), BFS O(V+E)
# ============================================================


class GNode:
    """Simpul dalam adjacency list (merepresentasikan satu tetangga)."""
    def __init__(self, tujuan: str, jarak: float):
        self.tujuan = tujuan    # kode lokasi tujuan
        self.jarak  = jarak     # bobot edge (km)
        self.next   = None


class AdjList:
    """Linked list untuk menyimpan daftar tetangga satu node."""
    def __init__(self):
        self.head  = None
        self._size = 0

    def tambah(self, tujuan: str, jarak: float):
        node = GNode(tujuan, jarak)
        node.next  = self.head
        self.head  = node
        self._size += 1

    def semua(self) -> list:
        """Kembalikan list of (tujuan, jarak)."""
        hasil, cur = [], self.head
        while cur:
            hasil.append((cur.tujuan, cur.jarak))
            cur = cur.next
        return hasil

    def __len__(self):
        return self._size


class Graph:
    """
    Graf berbobot tidak berarah untuk jaringan rute logistik.

    Atribut:
        _adj   : dict {kode_lokasi -> AdjList}
        _nodes : set semua kode lokasi
        depots : list kode depot (DEPOT_0, DEPOT_1, DEPOT_2)
    """

    def __init__(self):
        self._adj   = {}          # adjacency list
        self._nodes = set()       # semua node
        self.depots = []          # daftar depot terdaftar

    # ----------------------------------------------------------
    # MANAJEMEN NODE
    # ----------------------------------------------------------
    def tambah_node(self, kode: str, adalah_depot: bool = False):
        """
        Daftarkan lokasi baru ke dalam graf.
        Jika adalah_depot=True, kode juga masuk ke self.depots.
        Big-O: O(1)
        """
        if kode not in self._adj:
            self._adj[kode]  = AdjList()
            self._nodes.add(kode)
        if adalah_depot and kode not in self.depots:
            self.depots.append(kode)

    # ----------------------------------------------------------
    # MANAJEMEN RUTE (EDGE)
    # ----------------------------------------------------------
    def tambah_rute(self, asal: str, tujuan: str, jarak: float):
        """
        Tambahkan edge dua arah antara asal dan tujuan.
        Node yang belum ada akan dibuat otomatis.
        Big-O: O(1)
        """
        for k in (asal, tujuan):
            if k not in self._adj:
                self.tambah_node(k)

        self._adj[asal].tambah(tujuan, jarak)
        self._adj[tujuan].tambah(asal, jarak)

    # ----------------------------------------------------------
    # TETANGGA
    # ----------------------------------------------------------
    def tetangga(self, kode: str) -> list:
        """
        Kembalikan list of (tujuan, jarak) tetangga sebuah node.
        Big-O: O(degree(v))
        """
        if kode not in self._adj:
            return []
        return self._adj[kode].semua()

    # ----------------------------------------------------------
    # BFS DARI DEPOT (deteksi lokasi terjangkau)
    # ----------------------------------------------------------
    def bfs_dari_depot(self, depot: str) -> set:
        """
        BFS mulai dari sebuah depot — kembalikan set semua node
        yang dapat dijangkau.
        Big-O: O(V+E)
        """
        if depot not in self._adj:
            return set()

        dikunjungi = set()
        antrian    = [depot]           # queue sederhana (list)
        dikunjungi.add(depot)

        while antrian:
            saat_ini = antrian.pop(0)
            for (tetangga, _) in self._adj[saat_ini].semua():
                if tetangga not in dikunjungi:
                    dikunjungi.add(tetangga)
                    antrian.append(tetangga)

        return dikunjungi

    def lokasi_tidak_terjangkau(self, depot: str) -> set:
        """
        Kembalikan set lokasi yang TIDAK bisa dijangkau dari depot.
        """
        terjangkau = self.bfs_dari_depot(depot)
        return self._nodes - terjangkau

    # ----------------------------------------------------------
    # DIJKSTRA (rute optimal)
    # ----------------------------------------------------------
    def dijkstra(self, asal: str) -> tuple:
        """
        Cari jarak terpendek dari 'asal' ke semua node lain.
        Kembalikan (jarak_dict, prev_dict).
        Big-O: O(V^2) dengan implementasi list sederhana.
        """
        INF   = float('inf')
        jarak = {n: INF for n in self._nodes}
        prev  = {n: None for n in self._nodes}
        jarak[asal] = 0
        belum_dikunjungi = set(self._nodes)

        while belum_dikunjungi:
            # Ambil node dengan jarak terkecil (O(V))
            u = min(belum_dikunjungi, key=lambda n: jarak[n])
            if jarak[u] == INF:
                break
            belum_dikunjungi.remove(u)

            for (v, bobot) in self._adj[u].semua():
                alternatif = jarak[u] + bobot
                if alternatif < jarak[v]:
                    jarak[v] = alternatif
                    prev[v]  = u

        return jarak, prev

    def rute_optimal(self, asal: str, tujuan: str) -> tuple:
        """
        Kembalikan (total_jarak, [path]) dari asal ke tujuan.
        """
        jarak, prev = self.dijkstra(asal)
        path, cur   = [], tujuan

        while cur is not None:
            path.append(cur)
            cur = prev[cur]

        path.reverse()

        if path and path[0] == asal:
            return jarak[tujuan], path
        return float('inf'), []

    # ----------------------------------------------------------
    # UTILITAS
    # ----------------------------------------------------------
    def jumlah_node(self) -> int:
        return len(self._nodes)

    def semua_node(self) -> set:
        return set(self._nodes)

    def tampilkan(self):
        print("\n=== ADJACENCY LIST GRAF ===")
        for kode in sorted(self._adj):
            label  = " [DEPOT]" if kode in self.depots else ""
            tetang = self._adj[kode].semua()
            print(f"  {kode}{label} -> {tetang}")
        print(f"Total node: {self.jumlah_node()}")
        print("===========================\n")