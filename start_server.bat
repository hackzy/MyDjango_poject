@echo off
call my_venv\Scripts\activate
set base_dir=%~dp0
set nginx_path=%base_dir%nginx-1.26.1
echo 启动 Nginx ...
cd /d %nginx_path%
start %base_dir%nginx-1.26.1\nginx

echo 启动 waitress ...
cd /d %base_dir%
start /B py run.py

echo 服务启动成功！
echo 正在输出日志...
