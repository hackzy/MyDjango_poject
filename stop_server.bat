@echo off

set base_dir=%~dp0
set nginx_path=%base_dir%nginx-1.26.1
echo 停止 Nginx ...
cd /d %nginx_path%
start %base_dir%nginx-1.26.1\nginx -s quit

echo 停止 waitress ...
cd /d %base_dir%
for /f "tokens=5 delims= " %%a in ('netstat -ano ^| findstr :8080') do taskkill /F /PID %%a

call my_venv\Scripts\deactivate
echo 停止服务成功！
pause