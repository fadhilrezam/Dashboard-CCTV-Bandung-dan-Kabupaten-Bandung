# CCTV Bandung — Integrated Monitoring Dashboard

**Integrated CCTV Monitoring Dashboard for Kabupaten Bandung and Kota Bandung**

Dashboard berbasis web untuk mengintegrasikan titik kamera CCTV dari dua sumber berbeda ke dalam satu peta interaktif. Proyek ini bertujuan mempermudah pencarian lokasi kamera, pemantauan persebaran CCTV, dan akses langsung ke live stream melalui satu antarmuka.

## 1. Project Overview

Saat ini, data dan akses CCTV Kabupaten Bandung dan Kota Bandung tersedia melalui platform yang berbeda. Hal tersebut membuat pencarian kamera dan pemantauan lokasi harus dilakukan secara terpisah.

Proyek ini menggabungkan kedua sumber tersebut ke dalam satu dashboard dengan pendekatan visualisasi geografis menggunakan peta interaktif.

Dashboard mengintegrasikan:

- **Dishub Kabupaten Bandung** — CCTV dari platform CCTV Dinas Perhubungan Kabupaten Bandung.
- **PELINDUNG Kota Bandung** — CCTV dari platform PELINDUNG Kota Bandung.

Total terdapat **440 titik kamera CCTV** berdasarkan data yang digunakan dalam proyek ini:

| Sumber | Jumlah Kamera |
|---|---:|
| PELINDUNG Kota Bandung | 433 |
| Dishub Kabupaten Bandung | 7 |
| **Total** | **440** |

*Jumlah tersebut merupakan jumlah data kamera dengan koordinat valid yang dimasukkan ke dashboard, bukan jaminan seluruh kamera sedang online.*

## 2. Key Features

### Interactive CCTV Map
- Menampilkan persebaran kamera CCTV dalam satu peta.
- Menggunakan OpenStreetMap sebagai basemap.
- Marker kamera dapat dipilih untuk melihat informasi kamera.
- Peta mendukung navigasi, zoom, dan eksplorasi lokasi.

### Live CCTV Streaming
- Menampilkan live stream ketika kamera dipilih.
- Mendukung format video HLS (`.m3u8`).
- Menggunakan HLS.js untuk pemutaran stream pada browser yang kompatibel.
- Menggunakan local proxy untuk meneruskan playlist dan segmen video agar dapat mengatasi pembatasan CORS pada sumber tertentu.

### Camera Search & Filtering
- Pencarian kamera berdasarkan nama atau lokasi.
- Filter kamera berdasarkan sumber platform.
- Filter berdasarkan instansi atau dinas yang tersedia pada data.
- Daftar kamera terhubung dengan marker pada peta.

### Integrated Data
- Menggabungkan data dari dua platform CCTV.
- Mempertahankan identitas, nama, koordinat, sumber, dan URL stream kamera.
- Memungkinkan kamera dengan koordinat berdekatan tetap ditampilkan sebagai entri kamera yang berbeda.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| HTML | Dashboard structure |
| CSS | User interface and styling |
| JavaScript | Dashboard logic and interaction |
| Leaflet.js | Interactive map |
| OpenStreetMap | Map tiles / basemap |
| HLS.js | HLS video playback |
| Python 3 | Local web server and stream proxy |

Proyek menggunakan Python standard library untuk menjalankan server lokal dan proxy, sehingga tidak memerlukan instalasi framework backend tambahan.

## 4. Project Structure

```text
CCTV-Bandung/
│
├── dashboard_cctv_bandung.html
│   └── Main dashboard interface
│
├── server_cctv.py
│   └── Local HTTP server and HLS proxy
│
├── JALANKAN_DASHBOARD.bat
│   └── Windows launcher
│
└── README.md
    └── Project documentation
```

## 5. Installation & Setup

### Requirements

- Windows 10 atau Windows 11
- Python 3
- Internet connection
- Web browser modern (Chrome, Edge, Firefox, atau browser berbasis Chromium)

### How to Run

1. Download atau clone repository ini.
2. Ekstrak seluruh file ke dalam satu folder.
3. Pastikan Python 3 sudah terpasang.
4. Jalankan file `JALANKAN_DASHBOARD.bat`.
5. Browser akan membuka dashboard melalui alamat:

   `http://127.0.0.1:8765/dashboard_cctv_bandung.html`

6. Biarkan jendela terminal/server tetap berjalan selama dashboard digunakan.

**Important:** Jangan membuka file HTML secara langsung menggunakan `file://`. Dashboard harus dijalankan melalui launcher agar local proxy dapat berfungsi.

## 6. How It Works

Sistem bekerja melalui tiga komponen utama:

1. **Data Layer**  
   Data kamera dari kedua platform dikumpulkan dan digabungkan, termasuk nama kamera, koordinat geografis, instansi, dan URL stream.

2. **Visualization Layer**  
   Leaflet.js menampilkan lokasi kamera pada peta OpenStreetMap. Pengguna dapat mencari kamera, menerapkan filter, dan memilih marker untuk membuka informasi kamera.

3. **Streaming Layer**  
   HLS.js menangani pemutaran video. Permintaan playlist (`.m3u8`) dan segmen video diteruskan melalui Python local proxy agar browser dapat mengakses stream melalui origin lokal yang sama.

Alur sederhananya:

```text
PELINDUNG CCTV ─────┐
                    ├── Integrated Camera Data
Dishub CCTV ────────┘
                           │
                           ▼
                    CCTV Dashboard
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
        Interactive Map            Camera List
              │                         │
              └────────────┬────────────┘
                           ▼
                     Camera Selected
                           │
                           ▼
                       HLS.js
                           │
                           ▼
                     Local Proxy
                           │
                           ▼
                  Original CCTV Stream
```

## 7. Limitations & Notes

- Dashboard membutuhkan koneksi internet untuk memuat OpenStreetMap, library eksternal, dan stream CCTV.
- Ketersediaan live stream bergantung pada kondisi server sumber dan status kamera.
- Kamera yang offline, URL stream yang berubah, atau token akses yang kedaluwarsa tidak dapat diputar.
- Local proxy membantu menangani pembatasan CORS, tetapi tidak dapat mengatasi pembatasan autentikasi atau gangguan pada server sumber.
- Jumlah kamera pada dashboard mengikuti data yang dikumpulkan dan dapat berubah apabila platform sumber memperbarui datanya.
- Dashboard berjalan secara lokal pada komputer pengguna dan belum merupakan layanan hosting publik.

## 8. Data Sources & Credits

Data kamera berasal dari platform resmi berikut:

- **Dishub Kabupaten Bandung:** https://dishub.bandungkab.go.id/cctv/
- **PELINDUNG Kota Bandung:** https://pelindung.bandung.go.id/

Teknologi dan layanan yang digunakan:

- [Leaflet.js](https://leafletjs.com/)
- [OpenStreetMap](https://www.openstreetmap.org/)
- [HLS.js](https://github.com/video-dev/hls.js)

## 9. Future Improvements

Pengembangan berikutnya yang berpotensi meningkatkan fungsionalitas dashboard:

- Automatic camera status monitoring (online/offline).
- Periodic data synchronization dari platform sumber.
- Camera availability indicator.
- Advanced filtering berdasarkan wilayah dan instansi.
- Camera clustering untuk area dengan kepadatan kamera tinggi.
- Deployment ke server agar dashboard dapat diakses oleh beberapa pengguna.

---

**Project:** CCTV Bandung — Integrated Monitoring Dashboard  
**Version:** 1.0  
**Platform:** Windows / Local Web Application  
**Purpose:** Unified CCTV visualization and monitoring
