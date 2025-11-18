#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de teste para verificar a instalação do sistema
"""

import os
import sys

def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    print(f"[OK] Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[AVISO] Python 3.8+ e recomendado")
        return False
    return True

def check_dependencies():
    """Verifica dependências instaladas"""
    dependencies = {
        'django': 'Django',
        'pandas': 'Pandas',
    }
    
    optional = {
        'pyspark': 'PySpark (Opcional para Big Data)'
    }
    
    print("\n[PACOTES] Verificando dependencias obrigatorias:")
    all_ok = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"[OK] {name}")
        except ImportError:
            print(f"[ERRO] {name} - FALTANDO")
            print(f"  Instale com: pip install {module}")
            all_ok = False
    
    print("\n[PACOTES] Verificando dependencias opcionais:")
    for module, name in optional.items():
        try:
            __import__(module)
            print(f"[OK] {name}")
        except ImportError:
            print(f"[INFO] {name} - Nao instalado (opcional)")
    
    return all_ok

def check_csv_file():
    """Verifica se o arquivo CSV existe"""
    csv_path = 'data-1760299876054.csv'
    print(f"\n[ARQUIVO] Verificando arquivo de dados:")
    if os.path.exists(csv_path):
        size = os.path.getsize(csv_path)
        size_mb = size / (1024 * 1024)
        print(f"[OK] {csv_path} encontrado ({size_mb:.2f} MB)")
        return True
    else:
        print(f"[ERRO] {csv_path} NAO ENCONTRADO")
        print("  O arquivo CSV deve estar na raiz do projeto")
        return False

def check_structure():
    """Verifica estrutura de diretórios"""
    print("\n[ESTRUTURA] Verificando estrutura do projeto:")
    
    required_dirs = [
        'bigdata_project',
        'analytics',
        'analytics/templates',
        'analytics/templates/analytics'
    ]
    
    all_ok = True
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"[OK] {directory}/")
        else:
            print(f"[ERRO] {directory}/ - FALTANDO")
            all_ok = False
    
    required_files = [
        'manage.py',
        'bigdata_project/settings.py',
        'analytics/views.py',
        'analytics/data_processor.py',
        'analytics/urls.py',
        'analytics/templates/analytics/dashboard.html'
    ]
    
    for file in required_files:
        if os.path.isfile(file):
            print(f"[OK] {file}")
        else:
            print(f"[ERRO] {file} - FALTANDO")
            all_ok = False
    
    return all_ok

def test_data_loading():
    """Testa carregamento dos dados"""
    print("\n[TESTE] Testando carregamento de dados:")
    try:
        import pandas as pd
        df = pd.read_csv('data-1760299876054.csv', nrows=100)
        print(f"[OK] CSV carregado com sucesso")
        print(f"  Colunas encontradas: {', '.join(df.columns.tolist())}")
        print(f"  Total de linhas (amostra): {len(df)}")
        return True
    except Exception as e:
        print(f"[ERRO] Erro ao carregar CSV: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("  BIG DATA ANALYTICS - Teste de Instalação")
    print("=" * 60)
    
    results = []
    
    results.append(check_python_version())
    results.append(check_dependencies())
    results.append(check_csv_file())
    results.append(check_structure())
    
    if results[1] and results[2]:  # Se pandas e CSV estão OK
        results.append(test_data_loading())
    
    print("\n" + "=" * 60)
    if all(results):
        print("[SUCESSO] TODOS OS TESTES PASSARAM!")
        print("\nVoce pode executar o servidor com:")
        print("  python manage.py migrate")
        print("  python manage.py runserver")
        print("\nAcesse: http://localhost:8000")
    else:
        print("[FALHA] ALGUNS TESTES FALHARAM")
        print("\nCorreja os problemas acima antes de continuar.")
    print("=" * 60)

if __name__ == "__main__":
    main()

