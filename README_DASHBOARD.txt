DASHBOARD CCTV BANDUNG - VERSI PERBAIKAN

CARA MENJALANKAN (Windows):
1. Ekstrak semua isi ZIP ke satu folder.
2. Pastikan Python 3 terpasang.
3. Klik dua kali JALANKAN_DASHBOARD.bat.
4. Browser akan membuka http://127.0.0.1:8765/dashboard_cctv_bandung.html
5. Biarkan jendela hitam/server tetap terbuka selama dashboard dipakai.

Mengapa perlu dijalankan seperti ini?
Browser membatasi stream HLS lintas-domain (CORS). Server lokal meneruskan playlist dan segmen video melalui alamat localhost, lalu menulis ulang URL segmen agar pemutar dapat mengaksesnya. Ini juga menghindari pembukaan file langsung dengan file://.

Kebutuhan internet: tetap diperlukan untuk peta OpenStreetMap, library Leaflet/HLS.js, dan server CCTV.

Catatan: akses kamera bergantung pada server sumber, token Dishub, dan izin jaringan. Kamera yang sedang offline atau token yang dicabut tetap tidak dapat diputar oleh dashboard.
