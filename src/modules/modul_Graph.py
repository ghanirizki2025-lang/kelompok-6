# ============================================================
#  MODULE 1 : GRAPH JARINGAN RUTE
#  Graf berbobot tidak berarah menggunakan Adjacency List
#  berbasis Linked List.
#  Big-O: add O(1), BFS O(V+E)
# ============================================================


class GNode:
    """Simpul dalam adjacency list (merepresentasikan satu tetangga)."""
    def __init__(self, tujuan: str, jarak: float):
        self.tujuan = tujuan
        self.jarak  = jarak
        self.next   = None


class AdjList:
    """Linked list untuk menyimpan daftar tetangga satu node."""
    def __init__(self):
        self.head  = None
        self._size = 0

    def tambah(self, tujuan: str, jarak: float):
        node      = GNode(tujuan, jarak)
        node.next = self.head
        self.head = node
        self._size += 1

    def semua(self) -> list:
        hasil, cur = [], self.head
        while cur:
            hasil.append((cur.tujuan, cur.jarak))
            cur = cur.next
        return hasil

    def __len__(self):
        return self._size


class Graph:
    def __init__(self):
        self._adj   = {}
        self._nodes = set()
        self.depots = []

    def tambah_node(self, kode: str, adalah_depot: bool = False):
        if kode not in self._adj:
            self._adj[kode]  = AdjList()
            self._nodes.add(kode)
        if adalah_depot and kode not in self.depots:
            self.depots.append(kode)

    def tambah_rute(self, asal: str, tujuan: str, jarak: float):
        for k in (asal, tujuan):
            if k not in self._adj:
                self.tambah_node(k)
        self._adj[asal].tambah(tujuan, jarak)
        self._adj[tujuan].tambah(asal, jarak)

    def tetangga(self, kode: str) -> list:
        if kode not in self._adj:
            return []
        return self._adj[kode].semua()

    def bfs_dari_depot(self, depot: str) -> set:
        if depot not in self._adj:
            return set()
        dikunjungi = set()
        antrian    = [depot]
        dikunjungi.add(depot)
        while antrian:
            saat_ini = antrian.pop(0)
            for (tetangga, _) in self._adj[saat_ini].semua():
                if tetangga not in dikunjungi:
                    dikunjungi.add(tetangga)
                    antrian.append(tetangga)
        return dikunjungi

    def lokasi_tidak_terjangkau(self, depot: str) -> set:
        return self._nodes - self.bfs_dari_depot(depot)

    def dijkstra(self, asal: str) -> tuple:
        INF   = float('inf')
        jarak = {n: INF  for n in self._nodes}
        prev  = {n: None for n in self._nodes}
        jarak[asal]      = 0
        belum_dikunjungi = set(self._nodes)
        while belum_dikunjungi:
            u = min(belum_dikunjungi, key=lambda n: jarak[n])
            if jarak[u] == INF:
                break
            belum_dikunjungi.remove(u)
            for (v, bobot) in self._adj[u].semua():
                alt = jarak[u] + bobot
                if alt < jarak[v]:
                    jarak[v] = alt
                    prev[v]  = u
        return jarak, prev

    def rute_optimal(self, asal: str, tujuan: str) -> tuple:
        jarak, prev = self.dijkstra(asal)
        path, cur   = [], tujuan
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        if path and path[0] == asal:
            return jarak[tujuan], path
        return float('inf'), []

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


# ============================================================
#  DRIVER CODE — Jalankan langsung untuk melihat output
# ============================================================
if __name__ == "__main__":

    print("╔══════════════════════════════════════════════╗")
    print("║       SIMULASI GRAPH JARINGAN RUTE           ║")
    print("╚══════════════════════════════════════════════╝")

    # ── 1. INISIALISASI GRAF ────────────────────────────────
    g = Graph()

    for depot in ["DEPOT_0", "DEPOT_1", "DEPOT_2"]:
        g.tambah_node(depot, adalah_depot=True)

    rute_data = [
        ("DEPOT_0", "LOK_001", 12),
        ("DEPOT_0", "LOK_002",  8),
        ("DEPOT_0", "LOK_003", 25),
        ("DEPOT_1", "LOK_003",  5),
        ("DEPOT_1", "LOK_004", 15),
        ("DEPOT_2", "LOK_005", 20),
        ("DEPOT_2", "LOK_006", 10),
        ("LOK_001", "LOK_002",  6),
        ("LOK_003", "LOK_005",  9),
        ("LOK_004", "LOK_006",  7),
    ]
    for asal, tujuan, jarak in rute_data:
        g.tambah_rute(asal, tujuan, jarak)

    # ── 2. TAMPILKAN ADJACENCY LIST ─────────────────────────
    g.tampilkan()

    # ── 3. CEK TETANGGA ─────────────────────────────────────
    print(">>> Tetangga DEPOT_0:")
    for tujuan, jarak in g.tetangga("DEPOT_0"):
        print(f"    -> {tujuan}  ({jarak} km)")

    # ── 4. BFS DARI DEPOT ───────────────────────────────────
    print("\n>>> BFS dari DEPOT_1 (semua lokasi terjangkau):")
    terjangkau = g.bfs_dari_depot("DEPOT_1")
    for lok in sorted(terjangkau):
        print(f"    v {lok}")

    # ── 5. LOKASI TIDAK TERJANGKAU ──────────────────────────
    print("\n>>> Lokasi TIDAK terjangkau dari DEPOT_1:")
    tidak = g.lokasi_tidak_terjangkau("DEPOT_1")
    if tidak:
        for lok in sorted(tidak):
            print(f"    x {lok}")
    else:
        print("    Semua lokasi terjangkau.")

    # ── 6. RUTE OPTIMAL (DIJKSTRA) ──────────────────────────
    pasangan_rute = [
        ("DEPOT_0", "LOK_005"),
        ("DEPOT_1", "LOK_006"),
        ("DEPOT_2", "LOK_001"),
    ]
    print("\n>>> Rute Optimal (Dijkstra):")
    print(f"  {'ASAL':<12} {'TUJUAN':<12} {'JARAK':>8}   PATH")
    print(f"  {'-'*12} {'-'*12} {'-'*8}   {'-'*30}")
    for asal, tujuan in pasangan_rute:
        jarak, path = g.rute_optimal(asal, tujuan)
        jarak_str   = f"{jarak} km" if jarak != float('inf') else "tidak terjangkau"
        path_str    = " -> ".join(path) if path else "-"
        print(f"  {asal:<12} {tujuan:<12} {jarak_str:>8}   {path_str}")

    # ── 7. STATISTIK GRAF ───────────────────────────────────
    print(f"\n>>> Statistik Graf:")
    print(f"    Total node  : {g.jumlah_node()}")
    print(f"    Total depot : {len(g.depots)}  -> {g.depots}")
    print(f"    Semua node  : {sorted(g.semua_node())}")