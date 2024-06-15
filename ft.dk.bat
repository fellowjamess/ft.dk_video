@echo off
setlocal

REM Use PowerShell to get inputs with better pasting support
for /f "tokens=* delims=" %%i in ('powershell -Command "Read-Host 'URL of M3U8'"') do set m3u8_url=%%i
for /f "tokens=* delims=" %%i in ('powershell -Command "Read-Host 'Title of the file (default: ft_video.mp4)'"') do set output_file=%%i
for /f "tokens=* delims=" %%i in ('powershell -Command "Read-Host 'Start time (default: 00:00:00)'"') do set start_time=%%i
for /f "tokens=* delims=" %%i in ('powershell -Command "Read-Host 'End time (default: end of video)'"') do set end_time=%%i

REM Set default values if not provided
if "%output_file%"=="" set output_file=ft_video.mp4
if "%start_time%"=="" set start_time=00:00:00

REM Run the Python script with the provided inputs
python ft.dk_video.py "%m3u8_url%" "%output_file%" --start "%start_time%" --end "%end_time%"

endlocal
pause
