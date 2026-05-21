
class PriorityQueueBantuan:
    """
    Antrian berprioritas untuk pengiriman bantuan bencana.

    Aturan prioritas:
        1 = KRITIS  → dilayani PERTAMA
        2 = SEDANG  → dilayani setelah KRITIS
        3 = RINGAN  → dilayani terakhir

    Jika dua bantuan memiliki prioritas sama, bantuan yang lebih dulu
    masuk (FIFO) akan dilayani lebih dulu — sifat alami dari sisip di belakang
    node dengan prioritas yang sama.

    Atribut:
        head   : simpul pertama antrian (prioritas tertinggi)
        _size  : jumlah elemen saat ini
    """

    def __init__(self):
        self.head = None   # awal antrian (paling diprioritaskan)
        self._size = 0

    # ------------------------------------------------------------------
    # ENQUEUE — masukkan bantuan ke antrian dengan urutan prioritas
    # ------------------------------------------------------------------
    def enqueue(self, bantuan):
        """
        Sisipkan objek Bantuan ke posisi yang sesuai berdasarkan prioritas.
        Semakin kecil angka prioritas, semakin dekat ke head.
        Big-O: O(n).

        Parameter:
            bantuan : objek Bantuan (memiliki atribut .prioritas int)
        """
        node_baru = LLNode(bantuan)

        # Kasus 1: antrian kosong atau bantuan baru lebih prioritas dari head
        if self.head is None or bantuan.prioritas < self.head.data.prioritas:
            node_baru.next = self.head
            self.head = node_baru

        else:
            # Telusuri sampai menemukan posisi yang tepat
            # Berhenti di simpul yang prioritasnya SAMA ATAU LEBIH KECIL
            # supaya FIFO terjaga untuk bantuan setingkat
            saat_ini = self.head
            while (saat_ini.next is not None and
                   saat_ini.next.data.prioritas <= bantuan.prioritas):
                saat_ini = saat_ini.next

            # Sisipkan node baru setelah saat_ini
            node_baru.next = saat_ini.next
            saat_ini.next = node_baru

        self._size += 1

    # ------------------------------------------------------------------
    # DEQUEUE — ambil bantuan paling prioritas dari head
    # ------------------------------------------------------------------
    def dequeue(self):
        """
        Ambil dan hapus bantuan dengan prioritas tertinggi (head).
        Jika antrian kosong, kembalikan None.
        Big-O: O(1).

        Return:
            objek Bantuan dari head, atau None bila antrian kosong.
        """
        if self.head is None:
            return None  # antrian kosong

        data = self.head.data       # ambil objek Bantuan di head
        self.head = self.head.next  # geser head ke simpul berikutnya
        self._size -= 1
        return data

    # ------------------------------------------------------------------
    # TAMPILKAN — cetak isi antrian untuk debugging / CLI
    # ------------------------------------------------------------------
    def tampilkan(self):
        """
        Cetak seluruh isi antrian dari head ke tail.
        Berguna untuk verifikasi urutan prioritas.
        Big-O: O(n).
        """
        from src.models import LEVEL_BENCANA  # import lokal agar tidak sirkular

        if self.head is None:
            print("  [Antrian kosong]")
            return

        saat_ini = self.head
        urutan = 1
        while saat_ini is not None:
            b = saat_ini.data
            # Cari label teks dari angka prioritas
            label = next((k for k, v in LEVEL_BENCANA.items() if v == b.prioritas), str(b.prioritas))
            print(f"  {urutan:3}. ID={b.bantuan_id:4} | {b.jenis:<8} x{b.jumlah:<5} | "
                  f"{b.asal} → {b.tujuan:<8} | [{label}]")
            saat_ini = saat_ini.next
            urutan += 1

    # ------------------------------------------------------------------
    # UTILITAS
    # ------------------------------------------------------------------
    def kosong(self) -> bool:
        """Kembalikan True jika antrian tidak memiliki elemen."""
        return self.head is None

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        if self.head is None:
            return "PriorityQueue: [kosong]"
        items = []
        s = self.head
        while s:
            items.append(f"(ID={s.data.bantuan_id},P={s.data.prioritas})")
            s = s.next
        return "HEAD → " + " → ".join(items) + " → TAIL"
