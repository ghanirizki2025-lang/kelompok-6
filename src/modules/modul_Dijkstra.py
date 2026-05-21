class NodeLokasiJarak:
    """Node Linked List untuk menyimpan data hasil audit jarak lokasi dari depot."""
    def __init__(self, kode, jarak):
        self.kode = kode        # Kode lokasi (misal: "L001")
        self.jarak = jarak      # Jarak dari depot dalam km
        self.next = None


class LinkedListAudit:
    """Struktur data Linked List untuk menampung dan mengurutkan data audit jarak."""
    def __init__(self):
        self.head = None

    def append(self, kode, jarak):
        """Menambahkan data audit lokasi baru ke akhir linked list."""
        node_baru = NodeLokasiJarak(kode, jarak)
        if not self.head:
            self.head = node_baru
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = node_baru

    def selection_sort(self):
        """
        Mengurutkan Linked List berdasarkan jarak terdekat (Ascending)
        menggunakan algoritma Selection Sort sesuai spesifikasi Big-O: O(V^2).
        """
        if not self.head:
            return

        start = self.head
        while start:
            min_node = start
            current = start.next
            
            # Cari node dengan jarak terkecil di sisa list
            while current:
                if current.jarak < min_node.jarak:
                    min_node = current
                current = current.next
            
            # Tukar data jika ditemukan jarak yang lebih kecil
            if min_node != start:
                start.kode, min_node.kode = min_node.kode, start.kode
                start.jarak, min_node.jarak = min_node.jarak, start.jarak
                
            start = start.next

    def tampilkan_audit(self):
        """Mencetak daftar audit jarak yang telah diurutkan."""
        current = self.head
        no = 1
        while current:
            # Jika nilai jarak adalah infinity, berarti lokasi terisolasi
            jarak_str = f"{current.jarak} km" if current.jarak != float('inf') else "TIDAK TERJANGKAU"
            print(f"   {no}. {current.kode} -> Jarak: {jarak_str}")
            current = current.next
            no += 1


class ModuleDijkstra:
    def __init__(self, graph_adjacency_list):
        """
        Menerima graph_adjacency_list dari Module 1 (Graph Jaringan Rute).
        Format graph diharapkan: { "NODE_A": [("NODE_B", jarak_int), ...], ... }
        """
        self.graph = graph_adjacency_list

    # 1. ALGORITMA DIJKSTRA
    def cari_rute_optimal(self, start, target):
        """
        Mencari rute terpendek dari start ke target menggunakan algoritma Dijkstra.
        Returns: tuple (jalur_list, total_jarak)
        """
        # Inisialisasi jarak ke semua node dengan tak hingga (infinity)
        jarak = {node: float('inf') for node in self.graph}
        jarak[start] = 0
        
        # Menyimpan rute pendahulu untuk rekonstruksi jalur
        parent = {node: None for node in self.graph}
        
        # Daftar node yang belum dikunjungi (simulasi priority queue sederhana)
        unvisited = list(self.graph.keys())

        while unvisited:
            # Cari node dengan jarak terkecil di daftar unvisited
            current_node = min(unvisited, key=lambda node: jarak[node])
            
            # Jika jarak terkecil adalah tak hingga, sisa node tidak dapat dijangkau
            if jarak[current_node] == float('inf'):
                break
                
            unvisited.remove(current_node)

            # Jika sudah mencapai target, hentikan pencarian lebih awal
            if current_node == target:
                break

            # Evaluasi tetangga dari node saat ini
            for tetangga, bobot in self.graph.get(current_node, []):
                if tetangga in unvisited:
                    jarak_baru = jarak[current_node] + bobot
                    if jarak_baru < jarak[tetangga]:
                        jarak[tetangga] = jarak_baru
                        parent[tetangga] = current_node

        # Rekonstruksi jalur dari target ke start
        jalur = []
        node_sekarang = target
        while node_sekarang is not None:
            jalur.insert(0, node_sekarang)
            node_sekarang = parent[node_sekarang]

        # Validasi apakah rute benar-benar ditemukan
        if jarak[target] == float('inf'):
            return [], float('inf')
            
        return jalur, jarak[target]

    # 2. AUDIT JARAK (MENGGUNAKAN SELECTION SORT LINKED LIST)
    def audit_seluruh_jarak(self, depot_asal):
        """
        Mengaudit dan mengurutkan seluruh lokasi berdasarkan jarak terdekat dari depot asal.
        Mengidentifikasi lokasi yang paling sulit dijangkau.
        """
        list_audit = LinkedListAudit()
        
        # Hitung jarak dari depot ke setiap node di dalam graph menggunakan Dijkstra
        for node in self.graph.keys():
            if node != depot_asal:
                _, total_jarak = self.cari_rute_optimal(depot_asal, node)
                list_audit.append(node, total_jarak)
        
        # Urutkan menggunakan Selection Sort berbasis Linked List (O(V^2))
        list_audit.selection_sort()
        return list_audit


# ==============================================================================
# PENGUJIAN MANDIRI MODULE DIJKSTRA & AUDIT JARAK
# ==============================================================================
if __name__ == "__main__":
    print("=== TESTING MODULE DIJKSTRA & AUDIT JARAK ===")
    
    # Mock data graph adjacency list dari Module 1 Graph (35 lokasi + 3 depot)
    # Diperkecil untuk contoh pengujian fungsionalitas
    mock_graph = {
        "DEPOT_0": [("L001", 5), ("L002", 12)],
        "L001": [("DEPOT_0", 5), ("L003", 7)],
        "L002": [("DEPOT_0", 12)],
        "L003": [("L001", 7)],
        "L004": []  # Lokasi terisolasi / tidak memiliki edge
    }

    dijkstra_sys = ModuleDijkstra(mock_graph)

    # 1. Test Rute Terpendek (Perintah: RUTE OPTIMAL DEPOT_0 L003)
    print("\n📍 Menghitung Rute Optimal dari DEPOT_0 ke L003...")
    jalur, jarak = dijkstra_sys.cari_rute_optimal("DEPOT_0", "L003")
    if jarak != float('inf'):
        print(f"✔️ Rute Terpendek : {' -> '.join(jalur)}")
        print(f"📏 Total Jarak    : {jarak} km")
    else:
        print("❌ Rute tidak ditemukan atau lokasi terisolasi!")

    # 2. Test Audit Jarak (Mengurutkan lokasi terdekat -> tersulit dijangkau)
    print("\n📊 Menjalankan Audit Jarak dari DEPOT_0 (Selection Sort Linked List):")
    hasil_audit = dijkstra_sys.audit_seluruh_jarak("DEPOT_0")
    hasil_audit.tampilkan_audit()