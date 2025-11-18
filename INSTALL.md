# Guia de Instalação - Big Data Analytics

## Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Passo a Passo

### 1. Instalar Dependências Básicas

```bash
pip install django pandas
```

### 2. Configurar o Banco de Dados

```bash
python manage.py migrate
```

### 3. Executar o Servidor

```bash
python manage.py runserver
```

### 4. Acessar o Sistema

Abra seu navegador em: **http://localhost:8000**

## Solução de Problemas

### Erro: "No module named 'django'"

```bash
pip install django
```

### Erro: "No module named 'pandas'"

```bash
pip install pandas
```

### Erro ao carregar CSV

Verifique se o arquivo `data-1760299876054.csv` está na raiz do projeto.

### Porta 8000 em uso

Execute em outra porta:
```bash
python manage.py runserver 8080
```

## Verificar Instalação

Execute os testes:

```bash
python manage.py check
```

## Performance

Para melhor performance com grandes volumes:

1. Configure cache no Django (Redis/Memcached)
2. Use banco de dados PostgreSQL ao invés de SQLite
3. Otimize os tipos de dados no Pandas

## Ambiente de Produção

Para produção, instale adicionalmente:

```bash
pip install gunicorn whitenoise psycopg2-binary
```

Configure:
- DEBUG = False no settings.py
- ALLOWED_HOSTS com seu domínio
- Colete arquivos estáticos: `python manage.py collectstatic`

## Suporte

Para problemas, verifique:
- Python version: `python --version`
- Django version: `python manage.py --version`
- Logs: `tail -f django.log`

