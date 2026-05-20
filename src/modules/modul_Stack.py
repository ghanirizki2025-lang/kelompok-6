# =============================================================================
# modul_4.py
# Modul 4 — Stack Log Pengiriman
#
# Tanggung jawab modul ini:
#   - Mencatat setiap transaksi pengiriman yang sudah diproses (push)
#   - Menampilkan riwayat pengiriman dari yang terbaru (LOG_PENGIRIMAN)
#   - Membatalkan pengiriman terakhir dan mengembalikan ke antrian (ROLLBACK)
#
# Mata Kuliah : ELT60213 Algoritma dan Struktur Data
# Topik       : 9 — Disaster Response Logistics System
# =============================================================================

import time
from src.data_structures.Stack_Log_Pengiriman import Stack
from src.data_structures.queue_ll import PriorityQueueBantuan
from src.models import Bantuan, LABEL_LEVEL


def catat_pengiriman(stack: Stack, bantuan: Bantuan):
    """
    Simpan transaksi pengiriman yang berhasil ke dalam Stack log.
    Setiap entri menyimpan objek Bantuan beserta timestamp pengiriman.

    Parameter:
        stack   : objek Stack sebagai log
        bantuan : objek Bantuan yang baru selesai diproses
    """
    entri = {
        'bantuan': bantuan,
        'waktu': time.strftime('%H:%M:%S'),   # waktu saat dicatat
        'tanggal': time.strftime('%Y-%m-%d'),
    }
    stack.push(entri)


def tampilkan_log(stack: Stack):
    """
    Tampilkan seluruh riwayat pengiriman dari yang paling baru (top) ke lama.
    Memanfaatkan to_list() agar stack tidak berubah.

    Parameter:
        stack : objek Stack berisi riwayat pengiriman
    """
    riwayat = stack.to_list()   # top → bottom, tidak merusak stack

    if not riwayat:
        print("  Belum ada pengiriman yang tercatat.")
        return

    print(f"\n  {'─'*60}")
    print(f"  RIWAYAT PENGIRIMAN — {len(riwayat)} transaksi (terbaru di atas)")
    print(f"  {'─'*60}")
    print(f"  {'No':<5} {'Waktu':<10} {'ID':<6} {'Jenis':<10} {'Jml':<6} {'Rute':<22} {'Level'}")
    print(f"  {'─'*60}")

    for i, item in enumerate(riwayat, 1):
        b = item['bantuan']
        label = LABEL_LEVEL.get(b.prioritas, str(b.prioritas))
        rute = f"{b.asal} → {b.tujuan}"
        print(f"  {i:<5} {item['waktu']:<10} {b.bantuan_id:<6} "
              f"{b.jenis:<10} {b.jumlah:<6} {rute:<22} {label}")

    print(f"  {'─'*60}\n")


def rollback_pengiriman(stack: Stack, antrian: PriorityQueueBantuan) -> bool:
    """
    Batalkan pengiriman terakhir:
        1. Pop entri teratas dari stack log.
        2. Kembalikan objek Bantuan ke antrian berprioritas.

    Jika stack kosong, tidak ada yang dibatalkan.

    Parameter:
        stack   : objek Stack log pengiriman
        antrian : objek PriorityQueueBantuan untuk menerima bantuan kembali

    Return:
        True jika rollback berhasil, False jika stack kosong.
    """
    entri = stack.pop()

    if entri is None:
        print("  Tidak ada pengiriman untuk di-rollback.")
        return False

    bantuan = entri['bantuan']
    # Kembalikan bantuan ke antrian dengan prioritas semula
    antrian.enqueue(bantuan)

    label = LABEL_LEVEL.get(bantuan.prioritas, str(bantuan.prioritas))
    print(f"  ✓ ROLLBACK: ID={bantuan.bantuan_id} ({bantuan.jenis} x{bantuan.jumlah} "
          f"ke {bantuan.tujuan}) dibatalkan.")
    print(f"  Bantuan dikembalikan ke antrian [{label}].")
    print(f"  Sisa log: {len(stack)} transaksi | Antrian: {len(antrian)} item")
    return True
