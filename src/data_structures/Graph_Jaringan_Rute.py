# ============================================================
#  PURE DATA STRUCTURE : GRAPH
#  Graf Berbobot Tidak Berarah
#  Menggunakan Adjacency List berbasis Linked List murni
# ============================================================


# ── NODE LINKED LIST (untuk adjacency list) ────────────────
class EdgeNode:
    """Satu edge dalam adjacency list."""
    def __init__(self, vertex: str, bobot: float = 1.0):
        self.vertex = vertex
        self.bobot  = bobot
        self.next   = None


class EdgeList:
    """Linked List untuk menyimpan daftar edge dari satu vertex."""
    def __init__(self):
        self.head  = None
        self._size = 0

    def tambah(self, vertex: str, bobot: float = 1.0):
        node       = EdgeNode(vertex, bobot)
        node.next  = self.head
        self.head  = node
        self._size += 1

    def hapus(self, vertex: str) -> bool:
        if self.head is None:
            return False
        if self.head.vertex == vertex:
            self.head  = self.head.next
            self._size -= 1
            return True
        cur = self.head
        while cur.next:
            if cur.next.vertex == vertex:
                cur.next   = cur.next.next
                self._size -= 1
                return True
            cur = cur.next
        return False

    def ada(self, vertex: str) -> bool:
        cur = self.head
        while cur:
            if cur.vertex == vertex:
                return True
            cur = cur.next
        return False

    def semua(self) -> list:
        hasil, cur = [], self.head
        while cur:
            hasil.append((cur.vertex, cur.bobot))
            cur = cur.next
        return hasil

    def __len__(self):
        return self._size

    def __repr__(self):
        bagian = [f"{v}({b})" for v, b in self.semua()]
        return " -> ".join(bagian) + " -> NULL"


# ── GRAPH UTAMA ────────────────────────────────────────────
class Graph:
    """
    Graf Berbobot Tidak Berarah (Undirected Weighted Graph).

    Representasi : Adjacency List (dict of EdgeList)
    Tipe Graf    : Tidak berarah — setiap edge disimpan 2 arah

    Operasi              Big-O
    ─────────────────────────────────
    tambah_vertex        O(1)
    hapus_vertex         O(V + E)
    tambah_edge          O(1)
    hapus_edge           O(degree)
    ada_edge             O(degree)
    tetangga             O(degree)
    bfs                  O(V + E)
    dfs                  O(V + E)
    dijkstra             O(V²)      ← list-based
    ada_siklus           O(V + E)
    terhubung            O(V + E)
    komponen_terhubung   O(V + E)
    """

    def __init__(self, berarah: bool = False):
        self._adj     = {}         # {vertex -> EdgeList}
        self._berarah = berarah    # False = undirected

    # ── VERTEX ──────────────────────────────────────────────
    def tambah_vertex(self, v: str):
        """Tambah vertex baru. Abaikan jika sudah ada. O(1)"""
        if v not in self._adj:
            self._adj[v] = EdgeList()

    def hapus_vertex(self, v: str) -> bool:
        """
        Hapus vertex beserta semua edge yang terhubung dengannya.
        O(V + E)
        """
        if v not in self._adj:
            return False
        del self._adj[v]
        # Hapus semua edge yang menuju v dari vertex lain
        for u in self._adj:
            self._adj[u].hapus(v)
        return True

    def semua_vertex(self) -> list:
        return list(self._adj.keys())

    def jumlah_vertex(self) -> int:
        return len(self._adj)

    # ── EDGE ────────────────────────────────────────────────
    def tambah_edge(self, u: str, v: str, bobot: float = 1.0):
        """
        Tambah edge antara u dan v (dua arah jika undirected).
        Vertex yang belum ada dibuat otomatis. O(1)
        """
        for vertex in (u, v):
            self.tambah_vertex(vertex)

        self._adj[u].tambah(v, bobot)
        if not self._berarah:
            self._adj[v].tambah(u, bobot)

    def hapus_edge(self, u: str, v: str) -> bool:
        """Hapus edge u–v. O(degree)"""
        if u not in self._adj or v not in self._adj:
            return False
        ok = self._adj[u].hapus(v)
        if not self._berarah:
            self._adj[v].hapus(u)
        return ok

    def ada_edge(self, u: str, v: str) -> bool:
        """Cek apakah edge u–v ada. O(degree)"""
        if u not in self._adj:
            return False
        return self._adj[u].ada(v)

    def tetangga(self, v: str) -> list:
        """Kembalikan list (vertex, bobot) tetangga v. O(degree)"""
        if v not in self._adj:
            return []
        return self._adj[v].semua()

    def jumlah_edge(self) -> int:
        total = sum(len(self._adj[v]) for v in self._adj)
        return total if self._berarah else total // 2

    # ── BFS ─────────────────────────────────────────────────
    def bfs(self, start: str) -> list:
        """
        Breadth-First Search dari 'start'.
        Kembalikan urutan vertex yang dikunjungi. O(V+E)
        """
        if start not in self._adj:
            return []

        dikunjungi = set()
        urutan     = []
        antrian    = [start]
        dikunjungi.add(start)

        while antrian:
            v = antrian.pop(0)
            urutan.append(v)
            for (tetangga, _) in self._adj[v].semua():
                if tetangga not in dikunjungi:
                    dikunjungi.add(tetangga)
                    antrian.append(tetangga)

        return urutan

    # ── DFS ─────────────────────────────────────────────────
    def dfs(self, start: str) -> list:
        """
        Depth-First Search dari 'start' (iteratif dengan stack).
        Kembalikan urutan vertex yang dikunjungi. O(V+E)
        """
        if start not in self._adj:
            return []

        dikunjungi = set()
        urutan     = []
        stack      = [start]

        while stack:
            v = stack.pop()
            if v not in dikunjungi:
                dikunjungi.add(v)
                urutan.append(v)
                for (tetangga, _) in self._adj[v].semua():
                    if tetangga not in dikunjungi:
                        stack.append(tetangga)

        return urutan

    # ── DIJKSTRA ────────────────────────────────────────────
    def dijkstra(self, sumber: str) -> tuple:
        """
        Algoritma Dijkstra — jarak terpendek dari sumber ke semua vertex.
        Kembalikan (jarak_dict, prev_dict). O(V²) dengan list sederhana.
        """
        INF    = float('inf')
        jarak  = {v: INF  for v in self._adj}
        prev   = {v: None for v in self._adj}
        jarak[sumber] = 0
        belum  = set(self._adj.keys())

        while belum:
            u = min(belum, key=lambda x: jarak[x])
            if jarak[u] == INF:
                break
            belum.remove(u)
            for (v, w) in self._adj[u].semua():
                alt = jarak[u] + w
                if alt < jarak[v]:
                    jarak[v] = alt
                    prev[v]  = u

        return jarak, prev

    def jalur_terpendek(self, sumber: str, tujuan: str) -> tuple:
        """
        Rekonstruksi jalur terpendek dari sumber ke tujuan.
        Kembalikan (total_bobot, [path]).
        """
        jarak, prev = self.dijkstra(sumber)
        path, cur   = [], tujuan

        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()

        if path and path[0] == sumber:
            return jarak[tujuan], path
        return float('inf'), []

    # ── CEK SIKLUS ──────────────────────────────────────────
    def ada_siklus(self) -> bool:
        """
        Deteksi siklus menggunakan DFS + parent tracking.
        O(V+E). Hanya akurat untuk graf tidak berarah.
        """
        dikunjungi = set()

        def dfs_siklus(v, parent):
            dikunjungi.add(v)
            for (tetangga, _) in self._adj[v].semua():
                if tetangga not in dikunjungi:
                    if dfs_siklus(tetangga, v):
                        return True
                elif tetangga != parent:
                    return True
            return False

        for v in self._adj:
            if v not in dikunjungi:
                if dfs_siklus(v, None):
                    return True
        return False

    # ── KONEKTIVITAS ────────────────────────────────────────
    def terhubung(self) -> bool:
        """Cek apakah seluruh graf terhubung. O(V+E)"""
        if not self._adj:
            return True
        start  = next(iter(self._adj))
        return len(self.bfs(start)) == len(self._adj)

    def komponen_terhubung(self) -> list:
        """
        Kembalikan list of list — setiap sub-list adalah
        satu komponen terhubung. O(V+E)
        """
        dikunjungi = set()
        komponen   = []
        for v in self._adj:
            if v not in dikunjungi:
                komp = self.bfs(v)
                dikunjungi.update(komp)
                komponen.append(komp)
        return komponen

    # ── UTILITAS ────────────────────────────────────────────
    def derajat(self, v: str) -> int:
        """Kembalikan jumlah edge yang terhubung ke v."""
        if v not in self._adj:
            return 0
        return len(self._adj[v])

    def tampilkan(self):
        tipe = "Berarah" if self._berarah else "Tidak Berarah"
        print(f"\n{'='*50}")
        print(f"  GRAPH ({tipe})")
        print(f"  Vertex: {self.jumlah_vertex()}  |  Edge: {self.jumlah_edge()}")
        print(f"{'='*50}")
        for v in sorted(self._adj):
            print(f"  {v:10} -> {self._adj[v]}")
        print(f"{'='*50}\n")