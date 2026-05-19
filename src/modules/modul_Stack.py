# test_Stack.py (Standalone Unit Test - Stack Log Pengiriman)

# ── STACK IMPLEMENTATION ──────────────────────────────────────
class _StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, data):
        node = _StackNode(data)
        node.next = self.top
        self.top = node
        self._size += 1

    def push_many(self, items):
        """Helper untuk memasukkan banyak item sekaligus dari sebuah list."""
        for item in items:
            self.push(item)

    def pop(self):
        if self.top is None:
            return None
        data = self.top.data
        self.top = self.top.next
        self._size -= 1
        return data

    def peek(self):
        return self.top.data if self.top else None

    def to_list(self):
        hasil, curr = [], self.top
        while curr:
            hasil.append(curr.data)
            curr = curr.next
        return hasil

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size


# ── DUMMY DATA FOR LOGISTIK ───────────────────────────────────
class _Item:
    def __init__(self, id_, jenis, jumlah, asal, tujuan, prioritas=2):
        self.bantuan_id = id_
        self.jenis      = jenis
        self.jumlah     = jumlah
        self.asal       = asal
        self.tujuan     = tujuan
        self.prioritas  = prioritas

def create_dummy_item(id_=1):
    """Factory function untuk membuat object item logistik."""
    return _Item(id_, "MAKANAN", 10, "DEPOT_0", f"L00{id_}")


# ── PERFECTED TEST CASES ──────────────────────────────────────
def test_tc01():
    s = Stack()
    s.push(create_dummy_item(1))
    assert s.peek() is not None, "Peek mengembalikan None padahal stack terisi"
    print("  [TC-01 PASS] push + peek sukses")

def test_tc02():
    s = Stack()
    b1, b2, b3 = create_dummy_item(1), create_dummy_item(2), create_dummy_item(3)
    s.push(b1); s.push(b2); s.push(b3)
    
    assert s.pop() is b3, "Gagal: Elemen terakhir masuk (b3) harus keluar pertama"
    assert s.pop() is b2, "Gagal: Elemen kedua (b2) tidak berurutan"
    assert s.pop() is b1, "Gagal: Elemen pertama masuk (b1) harus keluar terakhir"
    print("  [TC-02 PASS] Urutan LIFO (Last In, First Out) akurat")

def test_tc03():
    s = Stack()
    assert s.pop() is None, "Pop pada stack kosong seharusnya mengembalikan None"
    print("  [TC-03 PASS] Pop stack kosong aman (mengembalikan None)")

def test_tc04():
    s = Stack()
    s.push(create_dummy_item(1))
    s.push(create_dummy_item(2))
    p1 = s.peek()
    p2 = s.peek()
    assert p1 is p2, "Mengakses peek berkali-kali mengubah hasil objek"
    assert len(s) == 2, "Fungsi peek secara tidak sengaja mengubah ukuran stack"
    print("  [TC-04 PASS] Peek bersifat non-destructive (tidak mengubah stack)")

def test_tc05():
    s = Stack()
    b1, b2, b3 = create_dummy_item(1), create_dummy_item(2), create_dummy_item(3)
    s.push(b1); s.push(b2); s.push(b3)
    lst = s.to_list()
    
    assert len(lst) == 3, "Ukuran list hasil konversi tidak sesuai"
    assert lst[0] is b3, "Elemen pertama di list harus berupa Top Stack (b3)"
    assert lst[-1] is b1, "Elemen terakhir di list harus berupa Bottom Stack (b1)"
    print("  [TC-05 PASS] Konversi ke list mempertahankan urutan top ke bottom")

def test_tc06():
    s = Stack()
    assert s.is_empty() is True, "Status awal stack harusnya kosong (True)"
    s.push(create_dummy_item())
    assert s.is_empty() is False, "Stack terisi tapi is_empty() mengembalikan True"
    s.pop()
    assert s.is_empty() is True, "Stack dikosongkan tapi is_empty() mengembalikan False"
    print("  [TC-06 PASS] Method is_empty mendeteksi kekosongan dengan akurat")

def test_tc07():
    s = Stack()
    for i in range(5): 
        s.push(create_dummy_item(i))
    assert len(s) == 5, f"Ekspektasi ukuran 5, tapi terbaca {len(s)}"
    s.pop(); s.pop()
    assert len(s) == 3, f"Ekspektasi ukuran 3 setelah 2x pop, tapi terbaca {len(s)}"
    print("  [TC-07 PASS] Penghitungan dunder len(stack) akurat")

def test_tc08():
    s = Stack()
    # Mengetes ketahanan stack dengan data yang lebih banyak (Stress Test skala kecil)
    for i in range(50): 
        s.push(create_dummy_item(i))
    for _ in range(50): 
        s.pop()
    assert s.is_empty() and len(s) == 0, "Stack gagal kembali bersih setelah push-pop seimbang"
    print("  [TC-08 PASS] Operasi massal (Push/Pop berulang) kembali bersih total")


# ── RUNNER ────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [test_tc01, test_tc02, test_tc03, test_tc04,
             test_tc05, test_tc06, test_tc07, test_tc08]

    print("\n" + "="*55)
    print("   AUTOMATED UNIT TEST – Stack Log Pengiriman")
    print("="*55)

    lulus = gagal = 0
    for fn in tests:
        try:
            fn()
            lulus += 1
        except AssertionError as e:
            print(f"  [GAGAL] {fn.__name__}: {e}")
            gagal += 1
        except Exception as general_error:
            print(f"  [CRASH] {fn.__name__} Mengalami error sistem: {general_error}")
            gagal += 1

    print("─"*55)
    print(f"  HASIL AKHIR: {lulus} LULUS | {gagal} GAGAL dari {len(tests)} Test Cases")
    print("="*55)