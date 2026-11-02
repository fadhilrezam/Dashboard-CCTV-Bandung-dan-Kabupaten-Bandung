@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  start "" http://127.0.0.1:8765/dashboard_cctv_bandung.html
  py -3 server_cctv.py
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    start "" http://127.0.0.1:8765/dashboard_cctv_bandung.html
    python server_cctv.py
  ) else (
    echo Python 3 belum terpasang. Install dari https://www.python.org/downloads/ lalu jalankan file ini lagi.
    pause
  )
)
pause
