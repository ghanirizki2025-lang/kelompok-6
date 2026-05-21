class Node:
    """Class untuk merepresentasikan setiap elemen (wadah data) di dalam Stack."""
    def __init__(self, data):
        self.data = data      # Menyimpan nilai/data
        self.next = None      # Pointer/penunjuk ke node di bawahnya


class Stack:
    """Class utama Struktur Data Stack menggunakan prinsip LIFO."""
    def __init__(self):
        self.top = None       # Menunjuk ke elemen paling atas (puncak tumpukan)
        self._size = 0        # Menyimpan jumlah elemen dalam tumpukan

    def push(self, data):
        """Memasukkan data baru ke bagian paling atas tumpukan (Top)."""
        new_node = Node(data)
        new_node.next = self.top  # Arahkan node baru ke top yang lama
        self.top = new_node       # Jauhkan node baru sebagai top yang baru
        self._size += 1

    def pop(self):
        """Mengambil dan menghapus data dari elemen paling atas (Top)."""
        if self.is_empty():
            print("Stack Underflow! Tumpukan kosong.")
            return None
        
        popped_data = self.top.data  # Ambil data yang ada di top
        self.top = self.top.next     # Geser posisi top ke node di bawahnya
        self._size -= 1
        return popped_data

    def peek(self):
        """Melihat data pada elemen paling atas (Top) tanpa menghapusnya."""
        if self.is_empty():
            return None
        return self.top.data

    def is_empty(self):
        """Memeriksa apakah tumpukan dalam keadaan kosong."""
        return self.top is None

    def size(self):
        """Mengembalikan jumlah total elemen di dalam tumpukan."""
        return self._size

    def display(self):
        """Menampilkan seluruh isi tumpukan dari Top ke Bottom."""
        if self.is_empty():
            print("Stack Kosong.")
            return
        
        current = self.top
        print("\n--- POSISI STACK (TOP -> BOTTOM) ---")
        while current:
            print(f"[ {current.data} ]")
            current = current.next
        print("------------------------------------")


# ── CONTOH PENGGUNAAN (DRIVE CODE) ────────────────────────────
if __name__ == "__main__":
    # 1. Inisialisasi Tumpukan Baru
    tumpukan_buku = Stack()

    # 2. Tambah Data (Push)
    print("Menambahkan buku ke tumpukan...")
    tumpukan_buku.push("Buku Struktur Data")
    tumpukan_buku.push("Buku Matematika Diskrit")
    tumpukan_buku.push("Buku Python Dasar")
    
    # Tampilkan Stack
    tumpukan_buku.display()
    print(f"Buku paling atas (Peek): {tumpukan_buku.peek()}")
    print(f"Total buku saat ini   : {tumpukan_buku.size()}")

    print("\n" + "="*40 + "\n")

    # 3. Ambil Data (Pop)
    print(f"Mengambil buku: {tumpukan_buku.pop()}")
    print(f"Mengambil buku: {tumpukan_buku.pop()}")

    # Tampilkan Stack Akhir
    tumpukan_buku.display()
    print(f"Buku paling atas sekarang: {tumpukan_buku.peek()}")
    print(f"Total buku tersisa       : {tumpukan_buku.size()}")