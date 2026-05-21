import unittest

# ==============================================================================
# STRUKTUR DATA QUEUE MURNI YANG DI-TEST
# ==============================================================================
class NodeQueue:
    def __init__(self, data):
        self.data = data
        self.next = None

class QueueStrukturData:
    def __init__(self):
        self.front = None
        self.rear = None
        self._ukuran = 0

    def is_empty(self):
        return self.front is None

    def ukuran(self):
        return self._ukuran

    def enqueue(self, data):
        node_baru = NodeQueue(data)
        if self.is_empty():
            self.front = node_baru
            self.rear = node_baru
        else:
            self.rear.next = node_baru
            self.rear = node_baru
        self._ukuran += 1

    def dequeue(self):
        if self.is_empty():
            return None
        node_diambil = self.front
        data_diambil = node_diambil.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self._ukuran -= 1
        return data_diambil

    def peek(self):
        if self.is_empty():
            return None
        return self.front.data


# ==============================================================================
# SEKENARIO UNIT TESTING MURNI
# ==============================================================================
class TestQueueMurni(unittest.TestCase):

    def setUp(self):
        """Dijalankan otomatis sebelum setiap fungsi test dimulai."""
        self.queue = QueueStrukturData()

    def test_inisialisasi_awal(self):
        """Memastikan queue baru dalam kondisi kosong dan ukuran = 0."""
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.ukuran(), 0)
        self.assertIsNone(self.queue.peek())
        self.assertIsNone(self.queue.dequeue())

    def test_single_enqueue(self):
        """Memastikan proses memasukkan 1 elemen mengubah pointer front & rear dengan benar."""
        self.queue.enqueue("Mobil_A")
        self.assertFalse(self.queue.is_empty())
        self.assertEqual(self.queue.ukuran(), 1)
        self.assertEqual(self.queue.peek(), "Mobil_A")

    def test_multiple_enqueue_fifo(self):
        """Memastikan urutan masuk (FIFO) terjaga saat memasukkan banyak elemen."""
        self.queue.enqueue("Mobil_A")
        self.queue.enqueue("Mobil_B")
        self.queue.enqueue("Mobil_C")
        
        self.assertEqual(self.queue.ukuran(), 3)
        # Elemen terdepan (front) harus tetap Mobil_A
        self.assertEqual(self.queue.peek(), "Mobil_A")

    def test_dequeue_dan_pergeseran_front(self):
        """Memastikan dequeue mengambil data terdepan dan menggeser pointer dengan benar."""
        self.queue.enqueue("Mobil_A")
        self.queue.enqueue("Mobil_B")
        
        # Dequeue pertama harus keluar Mobil_A
        data1 = self.queue.dequeue()
        self.assertEqual(data1, "Mobil_A")
        self.assertEqual(self.queue.ukuran(), 1)
        
        # Sekarang front harus bergeser ke Mobil_B
        self.assertEqual(self.queue.peek(), "Mobil_B")
        
        # Dequeue kedua harus keluar Mobil_B
        data2 = self.queue.dequeue()
        self.assertEqual(data2, "Mobil_B")
        
        # Queue harus kosong kembali setelah semua diambil
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.ukuran(), 0)

    def test_reset_rear_saat_kosong(self):
        """Memastikan pointer rear ikut menjadi None saat semua elemen habis di-dequeue."""
        self.queue.enqueue("Mobil_A")
        self.queue.dequeue()
        
        # Validasi internal struktur data murni
        self.assertIsNone(self.queue.front)
        self.assertIsNone(self.queue.rear)


# ==============================================================================
# CARA MENJALANKAN TEST AUTOMATION
# ==============================================================================
if __name__ == "__main__":
    unittest.main()