import unittest


# ── SOURCE CODE STACK ─────────────────────────────────────────
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def pop(self):
        if self.is_empty():
            print("Stack Underflow! Tumpukan kosong.")
            return None
        popped_data = self.top.data
        self.top = self.top.next
        self._size -= 1
        return popped_data

    def peek(self):
        if self.is_empty():
            return None
        return self.top.data

    def is_empty(self):
        return self.top is None

    def size(self):
        return self._size

    def display(self):
        if self.is_empty():
            print("Stack Kosong.")
            return
        current = self.top
        print("\n--- POSISI STACK (TOP -> BOTTOM) ---")
        while current:
            print(f"[ {current.data} ]")
            current = current.next
        print("------------------------------------")


# ── UNIT TEST ─────────────────────────────────────────────────
class TestStack(unittest.TestCase):

    def setUp(self):
        """Inisialisasi stack baru sebelum setiap test dijalankan."""
        self.stack = Stack()

    # ── TEST: is_empty() ──────────────────────────────────────
    def test_is_empty_on_new_stack(self):
        """Stack baru harus dalam keadaan kosong."""
        self.assertTrue(self.stack.is_empty())

    def test_is_empty_after_push(self):
        """Stack tidak boleh kosong setelah push."""
        self.stack.push(10)
        self.assertFalse(self.stack.is_empty())

    def test_is_empty_after_push_then_pop(self):
        """Stack harus kembali kosong setelah semua elemen di-pop."""
        self.stack.push(10)
        self.stack.pop()
        self.assertTrue(self.stack.is_empty())

    # ── TEST: size() ──────────────────────────────────────────
    def test_size_on_new_stack(self):
        """Ukuran stack baru harus 0."""
        self.assertEqual(self.stack.size(), 0)

    def test_size_after_multiple_push(self):
        """Ukuran stack harus bertambah setiap kali push."""
        self.stack.push("A")
        self.stack.push("B")
        self.stack.push("C")
        self.assertEqual(self.stack.size(), 3)

    def test_size_after_pop(self):
        """Ukuran stack harus berkurang setelah pop."""
        self.stack.push("A")
        self.stack.push("B")
        self.stack.pop()
        self.assertEqual(self.stack.size(), 1)

    def test_size_unchanged_after_peek(self):
        """Operasi peek tidak boleh mengubah ukuran stack."""
        self.stack.push(99)
        self.stack.peek()
        self.assertEqual(self.stack.size(), 1)

    # ── TEST: push() ──────────────────────────────────────────
    def test_push_single_element(self):
        """Push satu elemen, top harus menunjuk ke elemen tersebut."""
        self.stack.push(42)
        self.assertEqual(self.stack.peek(), 42)

    def test_push_multiple_elements_lifo_order(self):
        """Push banyak elemen, urutan LIFO harus terjaga."""
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        # Elemen terakhir push (3) harus berada di top
        self.assertEqual(self.stack.peek(), 3)

    def test_push_various_data_types(self):
        """Stack harus mampu menampung berbagai tipe data."""
        self.stack.push(100)
        self.stack.push("Halo")
        self.stack.push([1, 2, 3])
        self.stack.push({"key": "value"})
        self.assertEqual(self.stack.size(), 4)
        self.assertEqual(self.stack.peek(), {"key": "value"})

    def test_push_duplicate_values(self):
        """Stack harus bisa menyimpan nilai duplikat."""
        self.stack.push(5)
        self.stack.push(5)
        self.stack.push(5)
        self.assertEqual(self.stack.size(), 3)

    # ── TEST: pop() ───────────────────────────────────────────
    def test_pop_returns_correct_value(self):
        """Pop harus mengembalikan nilai yang ada di top."""
        self.stack.push("Pertama")
        self.stack.push("Kedua")
        result = self.stack.pop()
        self.assertEqual(result, "Kedua")

    def test_pop_follows_lifo_order(self):
        """Pop harus mengikuti urutan LIFO (Last In, First Out)."""
        items = [10, 20, 30, 40, 50]
        for item in items:
            self.stack.push(item)

        for expected in reversed(items):
            self.assertEqual(self.stack.pop(), expected)

    def test_pop_on_empty_stack_returns_none(self):
        """Pop pada stack kosong harus mengembalikan None (Stack Underflow)."""
        result = self.stack.pop()
        self.assertIsNone(result)

    def test_pop_until_empty(self):
        """Pop semua elemen hingga stack kosong."""
        self.stack.push("X")
        self.stack.push("Y")
        self.stack.pop()
        self.stack.pop()
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)

    def test_pop_does_not_affect_remaining_elements(self):
        """Pop hanya menghapus top, elemen lain harus tetap utuh."""
        self.stack.push("Bawah")
        self.stack.push("Tengah")
        self.stack.push("Atas")
        self.stack.pop()  # Hapus "Atas"
        self.assertEqual(self.stack.peek(), "Tengah")
        self.assertEqual(self.stack.size(), 2)

    # ── TEST: peek() ──────────────────────────────────────────
    def test_peek_returns_top_value(self):
        """Peek harus mengembalikan nilai top tanpa menghapusnya."""
        self.stack.push("Buku A")
        self.stack.push("Buku B")
        self.assertEqual(self.stack.peek(), "Buku B")

    def test_peek_does_not_remove_element(self):
        """Peek tidak boleh menghapus elemen dari stack."""
        self.stack.push(77)
        self.stack.peek()
        self.assertEqual(self.stack.size(), 1)
        self.assertFalse(self.stack.is_empty())

    def test_peek_on_empty_stack_returns_none(self):
        """Peek pada stack kosong harus mengembalikan None."""
        result = self.stack.peek()
        self.assertIsNone(result)

    def test_peek_updates_after_push(self):
        """Nilai peek harus diperbarui setelah push baru."""
        self.stack.push("Lama")
        self.assertEqual(self.stack.peek(), "Lama")
        self.stack.push("Baru")
        self.assertEqual(self.stack.peek(), "Baru")

    def test_peek_updates_after_pop(self):
        """Nilai peek harus diperbarui setelah pop."""
        self.stack.push("Bawah")
        self.stack.push("Atas")
        self.stack.pop()
        self.assertEqual(self.stack.peek(), "Bawah")

    # ── TEST: SKENARIO INTEGRASI ──────────────────────────────
    def test_push_pop_push_sequence(self):
        """Skenario: push → pop → push ulang harus tetap konsisten."""
        self.stack.push(1)
        self.stack.push(2)
        self.stack.pop()
        self.stack.push(3)
        self.assertEqual(self.stack.peek(), 3)
        self.assertEqual(self.stack.size(), 2)

    def test_full_stack_scenario(self):
        """Skenario lengkap: simulasi tumpukan buku seperti di drive code."""
        self.stack.push("Buku Struktur Data")
        self.stack.push("Buku Matematika Diskrit")
        self.stack.push("Buku Python Dasar")

        self.assertEqual(self.stack.size(), 3)
        self.assertEqual(self.stack.peek(), "Buku Python Dasar")

        self.assertEqual(self.stack.pop(), "Buku Python Dasar")
        self.assertEqual(self.stack.pop(), "Buku Matematika Diskrit")

        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.peek(), "Buku Struktur Data")
        self.assertFalse(self.stack.is_empty())

    def test_overflow_simulation_many_elements(self):
        """Stress test: push dan pop 1000 elemen."""
        n = 1000
        for i in range(n):
            self.stack.push(i)
        self.assertEqual(self.stack.size(), n)
        self.assertEqual(self.stack.peek(), n - 1)

        for i in range(n - 1, -1, -1):
            self.assertEqual(self.stack.pop(), i)

        self.assertTrue(self.stack.is_empty())


# ── RUNNER ────────────────────────────────────────────────────
if __name__ == "__main__":
    unittest.main(verbosity=2)