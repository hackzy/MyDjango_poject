@echo off
call my_venv\Scripts\activate
set base_dir=%~dp0
set nginx_path=%base_dir%nginx-1.26.1
echo ���� Nginx ...
cd /d %nginx_path%
start %base_dir%nginx-1.26.1\nginx

echo ���� waitress ...
cd /d %base_dir%
start /B py run.py

echo ���������ɹ���
echo ���������־...
