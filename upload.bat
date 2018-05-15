@echo off
for /f "tokens=3" %%a in ('wmic os get Caption') do if /i "%%a" neq "" set Win=%%a
if /i %Win%==xp chcp 936
if /i %Win%==7 chcp 936
python upload.py
pause