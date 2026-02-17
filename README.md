# Solusi Permainan N-Queens dengan Metode Brute Force

**Dibuat oleh:** Kurt Mikhael Purba
**NIM:** 13524065

## Deskripsi Proyek

Program ini adalah implementasi solusi permainan N-Queens menggunakan metode Brute Force dengan antarmuka grafis (GUI). N-Queens adalah permasalahan klasik dalam ilmu komputer yang bertujuan menempatkan N buah ratu pada papan catur berukuran N×N sedemikian rupa sehingga tidak ada ratu yang saling menyerang.

### Fitur Utama

1. **Dua Mode Algoritma:**

   - **Optimal**: Menggunakan pendekatan permutasi kolom yang lebih efisien
   - **Brute Force**: Menghasilkan semua kombinasi posisi ratu yang mungkin
2. **Interface Grafis:**

   - Visualisasi papan permainan dengan warna
   - Animasi pencarian solusi secara real-time
   - Kontrol kecepatan animasi (Speed Up / Speed Down)
   - Timer untuk mengukur waktu eksekusi
3. **Fitur Input/Output:**

   - Load papan dari file teks
   - Simpan solusi sebagai file teks
   - Simpan visualisasi solusi sebagai gambar PNG
4. **Validasi:**

   - Pengecekan papan harus berbentuk persegi
   - Validasi jumlah warna unik pada papan
   - Validasi posisi ratu (tidak boleh diagonal, horizontal, atau vertikal berdekatan)
   - Setiap ratu harus berada pada warna yang berbeda

## Struktur Proyek

```
tucil-1/
│
├── src/
│   ├── main.py          # Entry point aplikasi
│   ├── GUI.py           # Interface grafis
│   └── model.py         # Logika algoritma dan validasi
│
├── test/
│   ├── test1.txt        # File input contoh 1
│   ├── test2.txt        # File input contoh 2
│   └── ...              # File-file test lainnya
│
└── README.md            # Dokumentasi proyek
```

## Cara Install Library yang Dibutuhkan

### Prasyarat

- Python 3.7 atau lebih baru
- pip (Python package manager)

### Langkah Instalasi

1. **Clone atau Download Repository**

   ```bash
   git clone https://github.com/Kurt-Mikhael/Tucil1_13524065
   ```
2. **Buat Virtual Environment (Opsional)**

   ```bash
   python -m venv .venv
   ```
3. **Aktifkan Virtual Environment**

   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```
4. **Install Dependencies**

   Program ini menggunakan library berikut:

   - `tkinter` (built in Python)
   - `Pillow` (PIL) untuk manipulasi gambar

   Instalasi Pillow:

   ```bash
   pip install Pillow
   ```

## Cara Menjalankan Program

### Menjalankan dengan GUI

```bash
python src/main.py
```

atau

```bash
cd src
python main.py
```

### Langkah-Langkah Penggunaan

1. **Start Program**: Jalankan `python src/main.py`
2. **Load File Input**:

   - Klik tombol "Load File"
   - Pilih file papan (contoh: `test/test1.txt`)
   - File harus berformat teks dengan huruf kapital (A-Z) yang merepresentasikan warna
3. **Pilih Mode Algoritma**:

   - **Optimal**: Untuk solusi yang lebih cepat (permutasi kolom)
   - **Brute Force**: Untuk pencarian menyeluruh (semua kombinasi)
4. **Kontrol Kecepatan**:

   - **Speed Up**: Mempercepat animasi pencarian
   - **Speed Down**: Memperlambat animasi pencarian
5. **Simpan Solusi**:

   - **Simpan As text**: Menyimpan solusi ke file teks (folder `test/`)
   - **Simpan As Image**: Menyimpan visualisasi sebagai PNG (folder `test/`)

## Format File Input

File input harus berformat text (.txt) dengan ketentuan:

- Setiap baris merepresentasikan satu baris papan
- Setiap karakter merepresentasikan satu sel dengan warna tertentu
- Gunakan huruf kapital A-Z untuk warna yang berbeda
- Papan harus berbentuk persegi (jumlah baris = jumlah kolom)

**Contoh:**

```
AAABBCCCD
ABBBBCECD
ABBBDCECD
AAABDCCCD
BBBBDDDDD
FGGGDDHDD
FGIGDDHDD
FGIGDDHDD
FGGGDDHHH
```

## Algoritma

### Mode Optimal

- Menggunakan permutasi kolom (setiap baris pasti ada satu ratu)
- Kompleksitas: O(n!)
- Lebih cepat karena mengurangi ruang pencarian

### Mode Brute Force

- Menghasilkan semua kemungkinan kombinasi n ratu dari n×n posisi
- Kompleksitas: O(C(n², n) × n)
- Lebih lambat tetapi menyeluruh

### Validasi

Solusi dianggap valid jika:

1. Setiap ratu berada pada warna yang berbeda
2. Tidak ada dua ratu yang bersebelahan secara diagonal
3. Tidak ada dua ratu dalam baris atau kolom yang sama (mode Brute Force)

## Troubleshooting

### Error: "Papan harus berbentuk persegi!"

- Pastikan jumlah baris dan kolom dalam file input sama

### Error: "Jumlah warna unik pada papan melebihi jumlah ratu!"

- Jumlah warna berbeda dalam papan tidak boleh lebih dari ukuran papan (n)

### tkinter tidak ditemukan

- Install tkinter:
  - Windows: Biasanya sudah terinstall
  - Ubuntu/Debian: `sudo apt-get install python3-tk`
  - Mac: Biasanya sudah terinstall dengan Python

## Lisensi

Proyek ini dibuat untuk keperluan akademis (Tugas Kecil 1 - Strategi Algoritma).

## Kontak

Kurt Mikhael Purba - NIM 13524065
