import math

# ==========================================
# STRUKTUR DATA UTAMA (LINKED LIST)
# ==========================================

class NodeJarak:
    """Node Linked List untuk menyimpan hasil audit jarak lokasi"""
    def __init__(self, kode_lokasi, jarak):
        self.kode_lokasi = kode_lokasi
        self.jarak = jarak
        self.next = None


class LinkedListJarak:
    """Linked List untuk menampung data lokasi dan jaraknya"""
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
        """
        Mengurutkan Linked List berdasarkan jarak terkecil ke terbesar
        menggunakan algoritma Selection Sort (Sesuai Spesifikasi)
        """
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
            
            # Tukar data jika ditemukan yang lebih kecil
            if min_node != curr_i:
                curr_i.kode_lokasi, min_node.kode_lokasi = min_node.kode_lokasi, curr_i.kode_lokasi
                curr_i.jarak, min_node.jarak = min_node.jarak, curr_i.jarak
                
            curr_i = curr_i.next

    def tampilkan_list(self):
        """Helper untuk mencetak isi list hasil audit"""
        curr = self.head
        while curr:
            jarak_str = f"{curr.jarak} km" if curr.jarak != math.inf else "TIDAK TERJANGKAU"
            print(f"- Lokasi: {curr.kode_lokasi} | Jarak: {jarak_str}")
            curr = curr.next


# ==========================================
# MODUL 5: DIJKSTRA & AUDIT JARAK
# ==========================================

class DijkstraAuditJarak:
    def __init__(self, graph_modul):
        """
        Menerima parameter object graph_modul (Modul 1) 
        yang memiliki representasi adjacency list.
        """
        self.graph = graph_modul

    def hitung_dijkstra(self, asal):
        """
        Menghitung jarak minimum dari satu titik asal (depot) ke semua lokasi.
        Kompleksitas: O(V^2 + E) jika menggunakan array/adjacency list standar.
        """
        # Inisialisasi jarak ke semua node dengan tak hingga (infinity)
        jarak = {node: math.inf for node in self.graph.get_all_nodes()}
        jarak[asal] = 0
        
        dikunjungi = set()
        semua_node = self.graph.get_all_nodes()

        for _ in range(len(semua_node)):
            # Cari node dengan jarak minimum yang belum dikunjungi
            min_jarak = math.inf
            u = None
            for node in semua_node:
                if node not in dikunjungi and jarak[node] < min_jarak:
                    min_jarak = jarak[node]
                    u = node
            
            # Jika tidak ada node lagi yang bisa dijangkau
            if u is None:
                break
                
            dikunjungi.add(u)
            
            # Update jarak tetangga dari node u
            # Mengasumsikan graph.get_tetangga(u) mengembalikan list tuple (tetangga, bobot)
            for tetangga, bobot in self.graph.get_tetangga(u):
                if tetangga not in dikunjungi:
                    jarak_baru = jarak[u] + bobot
                    if jarak_baru < jarak[tetangga]:
                        jarak[tetangga] = jarak_baru
                        
        return jarak

    def audit_jarak(self, daftar_depot, daftar_lokasi_bencana):
        """
        1. Menghitung rute jarak minimum dari setiap depot menggunakan Dijkstra.
        2. Mencari jarak terdekat dari kombinasi depot ke suatu lokasi bencana.
        3. Mengurutkan hasil menggunakan Selection Sort berbasis Linked List.
        4. Mengidentifikasi lokasi paling sulit dijangkau.
        """
        # Menyimpan hasil jarak minimum final ke masing-masing lokasi bencana
        jarak_terdekat_global = {lokasi: math.inf for lokasi in daftar_lokasi_bencana}
        
        # Jalankan Dijkstra dari SETIAP depot
        for depot in daftar_depot:
            if depot in self.graph.get_all_nodes():
                hasil_dijkstra = self.hitung_dijkstra(depot)
                
                # Bandingkan dan ambil yang paling minimum/dekat dari depot manapun
                for lokasi in daftar_lokasi_bencana:
                    if hasil_dijkstra[lokasi] < jarak_terdekat_global[lokasi]:
                        jarak_terdekat_global[lokasi] = hasil_dijkstra[lokasi]

        # Masukkan hasil ke dalam struktur Linked List (Sesuai Spesifikasi)
        list_audit = LinkedListJarak()
        for lokasi, jarak in jarak_terdekat_global.items():
            list_audit.append(lokasi, jarak)

        # Urutkan menggunakan Selection Sort berbasis Linked List
        list_audit.selection_sort()

        # Identifikasi lokasi paling sulit dijangkau (Jarak terjauh setelah diurutkan)
        # Karena sudah diurutkan, kita cari node paling terakhir yang bukan infinity,
        # atau jika ada infinity berarti node tersebut benar-benar terisolasi.
        curr = list_audit.head
        paling_sulit = None
        jarak_maks = -1
        
        while curr:
            if curr.jarak != math.inf and curr.jarak > jarak_maks:
                jarak_maks = curr.jarak
                paling_sulit = curr.kode_lokasi
            elif curr.jarak == math.inf and paling_sulit is None:
                # Jika ada yang tidak terjangkau sama sekali, langsung jadi prioritas paling sulit
                paling_sulit = curr.kode_lokasi
                jarak_maks = math.inf
            curr = curr.next

        # Output Hasil Akhir Audit
        print("=== HASIL AUDIT JARAK LOGISTIK (TERURUT KELUAR SECARA SELECTION SORT) ===")
        list_audit.tampilkan_list()
        print("-------------------------------------------------------------------------")
        if jarak_maks == math.inf:
            print(f"Lokasi Paling Sulit Dijangkau: {paling_sulit} (TIDAK TERKONEKSI JALAN)")
        else:
            print(f"Lokasi Paling Sulit Dijangkau: {paling_sulit} (Jarak Terjauh: {jarak_maks} km)")
        print("=========================================================================\n")
        
        return list_audit, paling_sulit