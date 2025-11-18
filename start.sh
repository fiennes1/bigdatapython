#!/bin/bash

echo "========================================"
echo "Big Data Analytics - Sistema de Notas"
echo "========================================"
echo ""

echo "Verificando instalação..."
python3 test_installation.py

echo ""
echo "========================================"
echo "Executando migrações..."
python3 manage.py migrate

echo ""
echo "========================================"
echo "Iniciando servidor..."
echo ""
echo "Acesse: http://localhost:8000"
echo "Pressione CTRL+C para parar o servidor"
echo "========================================"
echo ""

python3 manage.py runserver

