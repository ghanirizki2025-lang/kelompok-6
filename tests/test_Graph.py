import unittest

# ============================================================
# 1. PURE DATA STRUCTURE : GRAPH (Salin ulang kode murni kamu)
# ============================================================
class EdgeNode:
    def __init__(self, vertex: str, bobot: float = 1.0):
        self.vertex = vertex
        self.bobot  = bobot
        self.next   = None

class EdgeList:
    def __init__(self):
        self.head  = None
        self._size = 0

    def tambah(self, vertex: str, bobot: float = 1.0):
        node       = EdgeNode(vertex, bobot)
        node.next  = self.head
        self.head  = node
        self._size += 1

    def hapus(self, vertex: str) -> bool:
        if self.head is None: return False
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
            if cur.vertex == vertex: return True
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

class Graph:
    def __init__(self, berarah: bool = False):
        self._adj     = {}         # {vertex -> EdgeList}
        self._berarah = berarah    # False = undirected

    def tambah_vertex(self, v: str):
        if v not in self._adj:
            self._adj[v] = EdgeList()

    def hapus_vertex(self, v: str) -> bool:
        if v not in self._adj: return False
        del self._adj[v]
        for u in self._adj:
            self._adj[u].hapus(v)
        return True

    def semua_vertex(self) -> list:
        return list(self._adj.keys())

    def jumlah_vertex(self) -> int:
        return len(self._adj)

    def tambah_edge(self, u: str, v: str, bobot: float = 1.0):
        for vertex in (u, v):
            self.tambah_vertex(vertex)
        self._adj[u].tambah(v, bobot)
        if not self._berarah:
            self._adj[v].tambah(u, bobot)

    def ada_edge(self, u: str, v: str) -> bool:
        if u not in self._adj: return False
        return self._adj[u].ada(v)

    def derajat(self, v: str) -> int:
        if v not in self._adj: return 0
        return len(self._adj[v])

    def jumlah_edge(self) -> int:
        total = sum(len(self._adj[v]) for v in self._adj)
        return total if self._berarah else total // 2

    def bfs(self, start: str) -> list:
        if start not in self._adj: return []
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

    def dijkstra(self, sumber: str) -> tuple:
        INF    = float('inf')
        jarak  = {v: INF  for v in self._adj}
        prev   = {v: None for v in self._adj}
        jarak[sumber] = 0
        belum  = set(self._adj.keys())
        while belum:
            u = min(belum, key=lambda x: jarak[x])
            if jarak[u] == INF: break
            belum.remove(u)
            for (v, w) in self._adj[u].semua():
                alt = jarak[u] + w
                if alt < jarak[v]:
                    jarak[v] = alt
                    prev[v]  = u
        return jarak, prev

    def jalur_terpendek(self, sumber: str, tujuan: str) -> tuple:
        jarak, prev = self.dijkstra(sumber)
        path, cur   = [], tujuan
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        if path and path[0] == sumber:
            return jarak[tujuan], path
        return float('inf'), []

    def ada_siklus(self) -> bool:
        dikunjungi = set()
        def dfs_siklus(v, parent):
            dikunjungi.add(v)
            for (tetangga, _) in self._adj[v].semua():
                if tetangga not in dikunjungi:
                    if dfs_siklus(tetangga, v): return True
                elif tetangga != parent: return True
            return False
        for v in self._adj:
            if v not in dikunjungi:
                if dfs_siklus(v, None): return True
        return False

    def terhubung(self) -> bool:
        if not self._adj: return True
        start  = next(iter(self._adj))
        return len(self.bfs(start)) == len(self._adj)


# ============================================================
# 2. SEKENARIO UNIT TESTING (Bagian yang tadinya Error)
# ============================================================
class TestGraphMurni(unittest.TestCase):

    def setUp(self):
        """Sekarang kelas Graph di atas sudah pasti terbaca!"""
        self.g = Graph(berarah=False)

    def test_tambah_and_jumlah_vertex(self):
        self.g.tambah_vertex("DEPOT_A")
        self.g.tambah_vertex("L001")
        self.assertEqual(self.g.jumlah_vertex(), 2)

    def test_tambah_edge_undirected_dua_arah(self):
        self.g.tambah_edge("DEPOT_A", "L001", 5.0)
        self.assertEqual(self.g.jumlah_edge(), 1)
        self.assertTrue(self.g.ada_edge("DEPOT_A", "L001"))
        self.assertTrue(self.g.ada_edge("L001", "DEPOT_A"))

    def test_hapus_vertex_dan_pembersihan_edge(self):
        self.g.tambah_edge("DEPOT_A", "L001", 5.0)
        self.g.tambah_edge("L001", "L002", 7.0)
        self.g.hapus_vertex("L001")
        self.assertEqual(self.g.jumlah_vertex(), 2)
        self.assertFalse(self.g.ada_edge("DEPOT_A", "L001"))

    def test_dijkstra_jalur_terpendek(self):
        self.g.tambah_edge("A", "B", 5.0)
        self.g.tambah_edge("B", "C", 2.0)
        self.g.tambah_edge("A", "C", 12.0)
        total_bobot, rute = self.g.jalur_terpendek("A", "C")
        self.assertEqual(total_bobot, 7.0)
        self.assertEqual(rute, ["A", "B", "C"])

    def test_deteksi_siklus_dan_konektivitas(self):
        self.g.tambah_edge("A", "B")
        self.g.tambah_edge("B", "C")
        self.assertFalse(self.g.ada_siklus())
        self.g.tambah_edge("C", "A")
        self.assertTrue(self.g.ada_siklus())


if __name__ == "__main__":
    unittest.main()