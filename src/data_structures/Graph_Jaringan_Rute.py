class LLNode:
    """
    Satu unit simpul (node) dalam Linked List.
    """
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    """
    Singly Linked List yang dimodifikasi khusus sebagai 
    pendukung struktur Adjacency List pada Graph.
    """
    def __init__(self):
        self.head = None
        self._size = 0

    def prepend(self, data):
        """
        Menambahkan simpul di awal (head) agar kompleksitas O(1),
        sehingga memenuhi spesifikasi add rute/edge O(1).
        """
        node_baru = LLNode(data)
        node_baru.next = self.head
        self.head = node_baru
        self._size += 1

    def append(self, data):
        """
        Menambahkan simpul di akhir list.
        Kompleksitas: O(n)
        """
        node_baru = LLNode(data)
        if self.head is None:
            self.head = node_baru
        else:
            saat_ini = self.head
            while saat_ini.next is not None:
                saat_ini = saat_ini.next
            saat_ini.next = node_baru
        self._size += 1

    def kosong(self) -> bool:
        return self.head is None

    def __len__(self) -> int:
        return self._size