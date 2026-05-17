kelompok-6-Disaster-Response-Logistick-Sistem
Topik Disaster Response Logistick Sistem
Team
Ghani Rizki Putri (25051030110)
Abdurohman Sahid (25051030108)
Mumtajz Zahra Anisa Asikin (25051030125)
Muhammad Abdul Aziz (25051930107)
Mata Kuliah 
Algoritma dan Setruktur Data 
S1 Teknik Elektro 
Universitas Negri Yogyakarta 
Deskripsi Project
Project ini merupakan implementasi sistem manajemen logistik respons bencana (Disaster Response Logistics) menggunakan bahasa Python dan konsep Algoritma Struktur Data. Sistem dirancang untuk membantu mengoptimalkan distribusi bantuan/logistik dari gudang pusat (depot) menuju wilayah terdampak bencana secara cepat dan efisien dengan mempertimbangkan:

Tingkat urgensi atau level bencana di tiap lokasi (Kritis, Sedang, Ringan)
Jumlah populasi terdampak
Keterjangkauan wilayah distribusi
Jarak rute pengiriman terpendek
Struktur Data yang Digunakan
Project ini menggunakan beberapa struktur data utama yang dibangun secara manual (from scratch), yaitu:

Binary Search Tree (BST) : Mengelola registrasi data lokasi desa/kelurahan terdampak dan melakukan pencarian serta pembaruan level bencana secara efisien.
Priority Queue : Mengatur urutan antrean bantuan logistik menggunakan Singly Linked List terurut, di mana wilayah dengan level bencana KRITIS otomatis dilayani paling depan.
Stack : Menyimpan log riwayat transaksi pengiriman sukses yang bersifat LIFO untuk mendukung fitur pembatalan distribusi (ROLLBACK).
Graph (Adjacency List) : Merepresentasikan jaringan jalur transportasi antar depot logistik dan lokasi pengiriman, dilengkapi dengan fungsi penelusuran struktur Linked List.
BFS (Breadth-First Search) : Mendeteksi dan memfilter lokasi-lokasi terisolasi yang tidak dapat dijangkau dari depot tertentu.
Algoritma Dijkstra : Menentukan rute atau jalur distribusi logistik dengan jarak terpendek dari depot ke lokasi target.
Quick Sort : Melakukan pengurutan data lokasi terdampak berdasarkan skor urgensi tertinggi untuk pembuatan laporan kebencanaan.
Fitur Program
KIRIM : Memasukkan permintaan bantuan logistik ke dalam antrean Priority Queue.
PROSES BANTUAN : Mendistribusikan bantuan berdasarkan prioritas tertinggi dan mencatatnya ke dalam Stack Log.
STATUS ANTRIAN : Menampilkan daftar bantuan yang sedang menunggu dalam antrean.
RUTE OPTIMAL : Mencari dan menampilkan jalur terpendek menggunakan algoritma Dijkstra.
TIDAK TERJANGKAU : Melakukan audit aksesibilitas menggunakan BFS untuk melihat desa yang terisolasi.
UPDATE LEVEL : Memperbarui tingkat keparahan bencana suatu lokasi langsung pada pohon BST.
LAPORAN BENCANA : Menampilkan laporan wilayah yang diurutkan berdasarkan skor urgensi menggunakan Quick Sort.
LOG PENGIRIMAN : Menampilkan riwayat transaksi distribusi logistik yang telah berhasil diproses.
ROLLBACK : Membatalkan transaksi pengiriman terakhir dan mengembalikan datanya ke dalam Priority Queue.
Struktur Folder
docs/ -> laporan proyek dan slide presentasi
src/ -> source code utama program
structures/ -> modul struktur data kustom (graph, bst, priority queue, stack)
tests/ -> pengujian keandalan program
