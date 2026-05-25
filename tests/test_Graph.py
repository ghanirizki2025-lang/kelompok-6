import unittest

class GraphNodeData:
    def __init__(self, tujuan, bobot):
        self.tujuan = tujuan
        self.bobot = bobot

class GraphJaringanRute:
    def __init__(self):
        self.adj_list = {}

    def tambah_node(self, kode_lokasi):
        if kode_lokasi not in self.adj_list:
            self.adj_list[kode_lokasi] = LinkedList()

    def tambah_rute(self, asal, tujuan, bobot):
        self.tambah_node(asal)
        self.tambah_node(tujuan)
        self.adj_list[asal].prepend(GraphNodeData(tujuan, bobot))
        self.adj_list[tujuan].prepend(GraphNodeData(asal, bobot))

    def get_tetangga(self, kode_lokasi):
        hasil = []
        if kode_lokasi in self.adj_list:
            saat_ini = self.adj_list[kode_lokasi].head
            while saat_ini is not None:
                hasil.append((saat_ini.data.tujuan, saat_ini.data.bobot))
                saat_ini = saat_ini.next
        return hasil

    def get_all_nodes(self):
        return list(self.adj_list.keys())

    def bfs_deteksi_terjangkau(self, depot_asal):
        if depot_asal not in self.adj_list:
            return set()
        
        dikunjungi = set()
        queue = [depot_asal]
        dikunjungi.add(depot_asal)

        while len(queue) > 0:
            node_sekarang = queue.pop(0)
            saat_ini = self.adj_list[node_sekarang].head
            while saat_ini is not None:
                tetangga = saat_ini.data.tujuan
                if tetangga not in dikunjungi:
                    dikunjungi.add(tetangga)
                    queue.append(tetangga)
                saat_ini = saat_ini.next
        return dikunjungi

    def tampilkan_graf(self):
        print("\n=== REPRESENTASI ADJACENCY LIST GRAPH ===")
        for node, linked_list in self.adj_list.items():
            cetak_tetangga = []
            saat_ini = linked_list.head
            while saat_ini is not None:
                cetak_tetangga.append(f"{saat_ini.data.tujuan}({saat_ini.data.bobot}km)")
                saat_ini = saat_ini.next
            str_tetangga = " -> ".join(cetak_tetangga) if cetak_tetangga else "Tidak ada tetangga"
            print(f"[Node {node}] : {str_tetangga}")
        print("===========================================")

class TestGraphDenganLinkedList(unittest.TestCase):
    def setUp(self):
        self.graph = GraphJaringanRute()

    def test_graph_operations(self):
        self.graph.tambah_node("DEPOT_0")
        self.graph.tambah_node("LOK_01")
        self.assertIn("DEPOT_0", self.graph.get_all_nodes())
        self.assertIn("LOK_01", self.graph.get_all_nodes())

        self.graph.tambah_rute("DEPOT_0", "LOK_01", 15)
        self.graph.tambah_rute("LOK_01", "LOK_02", 10)
        self.graph.tambah_node("LOK_TERISOLASI")

        tetangga_depot = self.graph.get_tetangga("DEPOT_0")
        self.assertEqual(len(tetangga_depot), 1)
        self.assertEqual(tetangga_depot[0][0], "LOK_01")
        self.assertEqual(tetangga_depot[0][1], 15)

        tetangga_lok01 = self.graph.get_tetangga("LOK_01")
        self.assertEqual(len(tetangga_lok01), 2)

        self.graph.tampilkan_graf()

        terjangkau = self.graph.bfs_deteksi_terjangkau("DEPOT_0")
        self.assertIn("DEPOT_0", terjangkau)
        self.assertIn("LOK_01", terjangkau)
        self.assertIn("LOK_02", terjangkau)
        self.assertNotIn("LOK_TERISOLASI", terjangkau)

if __name__ == "__main__":
    unittest.main()