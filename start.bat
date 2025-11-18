@echo off
echo ========================================
echo Big Data Analytics - Sistema de Notas
echo ========================================
echo.

echo Verificando instalacao...
python test_installation.py

echo.
echo ========================================
echo Executando migracoes...
python manage.py migrate

echo.
echo ========================================
echo Iniciando servidor...
echo.
echo Acesse: http://localhost:8000
echo Pressione CTRL+C para parar o servidor
echo ========================================
echo.

python manage.py runserver

