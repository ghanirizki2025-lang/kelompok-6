import math

class NodeJarak:
    def __init__(self, kode_lokasi, jarak):
        self.kode_lokasi = kode_lokasi
        self.jarak = jarak
        self.next = None


class LinkedListJarak:
    def __init__(self):
        self.head = None

    def append(self, kode_lokasi, jarak):
        new_node = NodeJarak(kode_lokasi, jarak)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def selection_sort(self):
        if not self.head or not self.head.next:
            return
        curr_i = self.head
        while curr_i:
            min_node = curr_i
            curr_j = curr_i.next
            while curr_j:
                if curr_j.jarak < min_node.jarak:
                    min_node = curr_j
                curr_j = curr_j.next
            if min_node != curr_i:
                curr_i.kode_lokasi, min_node.kode_lokasi = min_node.kode_lokasi, curr_i.kode_lokasi
                curr_i.jarak, min_node.jarak = min_node.jarak, curr_i.jarak
            curr_i = curr_i.next

    def tampilkan_list(self):
        curr = self.head
        while curr:
            jarak_str = f"{curr.jarak} km" if curr.jarak != math.inf else "TIDAK TERJANGKAU"
            print(f"- Lokasi: {curr.kode_lokasi} | Jarak: {jarak_str}")
            curr = curr.next


class DijkstraAuditJarak:
    def __init__(self, graph_modul):
        self.graph = graph_modul

    def hitung_dijkstra(self, asal):
        jarak = {node: math.inf for node in self.graph.get_all_nodes()}
        jarak[asal] = 0
        dikunjungi = set()
        semua_node = self.graph.get_all_nodes()

        for _ in range(len(semua_node)):
            min_jarak = math.inf
            u = None
            for node in semua_node:
                if node not in dikunjungi and jarak[node] < min_jarak:
                    min_jarak = jarak[node]
                    u = node
            if u is None:
                break
            dikunjungi.add(u)
            for tetangga, bobot in self.graph.get_tetangga(u):
                if tetangga not in dikunjungi:
                    jarak_baru = jarak[u] + bobot
                    if jarak_baru < jarak[tetangga]:
                        jarak[tetangga] = jarak_baru
        return jarak

    def audit_jarak(self, daftar_depot, daftar_lokasi_bencana):
        jarak_terdekat_global = {lokasi: math.inf for lokasi in daftar_lokasi_bencana}

        for depot in daftar_depot:
            if depot in self.graph.get_all_nodes():
                hasil_dijkstra = self.hitung_dijkstra(depot)
                for lokasi in daftar_lokasi_bencana:
                    if hasil_dijkstra[lokasi] < jarak_terdekat_global[lokasi]:
                        jarak_terdekat_global[lokasi] = hasil_dijkstra[lokasi]

        list_audit = LinkedListJarak()
        for lokasi, jarak in jarak_terdekat_global.items():
            list_audit.append(lokasi, jarak)

        list_audit.selection_sort()

        curr = list_audit.head
        paling_sulit = None
        jarak_maks = -1

        while curr:
            if curr.jarak != math.inf and curr.jarak > jarak_maks:
                jarak_maks = curr.jarak
                paling_sulit = curr.kode_lokasi
            elif curr.jarak == math.inf and paling_sulit is None:
                paling_sulit = curr.kode_lokasi
                jarak_maks = math.inf
            curr = curr.next

        print("=== HASIL AUDIT JARAK LOGISTIK (TERURUT KELUAR SECARA SELECTION SORT) ===")
        list_audit.tampilkan_list()
        print("-------------------------------------------------------------------------")
        if jarak_maks == math.inf:
            print(f"Lokasi Paling Sulit Dijangkau: {paling_sulit} (TIDAK TERKONEKSI JALAN)")
        else:
            print(f"Lokasi Paling Sulit Dijangkau: {paling_sulit} (Jarak Terjauh: {jarak_maks} km)")
        print("=========================================================================\n")

        return list_audit, paling_sulit