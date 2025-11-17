# Big Data Analytics - Sistema de Análise de Notas Escolares

Sistema web para análise de notas de alunos usando princípios de Big Data com Django e Pandas.

## Tecnologias Utilizadas

- **Backend**: Django 5.x
- **Análise de Dados**: Pandas (otimizado com princípios de Big Data)
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualização**: Chart.js
- **Princípios**: MapReduce, Hadoop concepts, Big Data Analytics

## Estrutura do Projeto

```
bigdata/
├── bigdata_project/          # Configurações do Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── analytics/                # App principal
│   ├── data_processor.py    # Módulo de análise Big Data com Pandas
│   ├── views.py             # Views do Django
│   ├── urls.py              # Rotas do app
│   ├── apps.py              # Configuração do app
│   └── templates/
│       └── analytics/
│           ├── base.html
│           └── dashboard.html
├── data-1760299876054.csv   # Dados das notas
├── test_installation.py      # Script de verificação
└── manage.py
```

## Instalação

### 1. Instalar dependências

```bash
pip install django pandas
```

### 2. Executar migrações

```bash
python manage.py migrate
```

### 3. Iniciar o servidor

```bash
python manage.py runserver
```

### 4. Acessar o sistema

Abra o navegador em: `http://localhost:8000`

## Funcionalidades

### Filtros Disponíveis
- **ID Filial**: Filtrar por escola
- **Série e Turma**: Ex: "1ª Série - A"
- **Disciplina**: Matemática, Português, etc.
- **Tipo de Nota**: Mb1, Mb2, Mb3, Mb4, MA
- **Status**: Aprovado, Recuperação, Reprovado

### Tipos de Gráficos
1. **Distribuição de Notas**: Notas por faixa (0-2, 2-4, 4-6, 6-8, 8-10)
2. **Média por Disciplina**: Comparativo de desempenho
3. **Status dos Alunos**: Aprovados vs Recuperação vs Reprovados
4. **Média por Tipo de Avaliação**: Desempenho em Mb1, Mb2, Mb3, Mb4, MA
5. **Alunos por Faixa de Desempenho**: Distribuição qualitativa

### Estatísticas
- Total de registros
- Total de alunos
- Média geral
- Nota máxima e mínima
- Contadores de aprovados, recuperação e reprovados

### Funcionalidades Extras
- **Impressão de Relatório**: Imprime o gráfico atual
- **Design Responsivo**: Funciona em desktop, tablet e mobile
- **Processamento Otimizado**: Usa princípios de Big Data para grandes volumes

## Regras de Negócio

**IMPORTANTE**: O sistema tem 530.470 **registros** de notas, mas isso **NÃO** é o total de alunos. Cada aluno (identificado por `id_matricula`) possui múltiplas notas (Mb1, Mb2, Mb3, Mb4, MA).

### Cálculo de Status (por aluno único):
- **REPROVADO**: MA < 6.0 (independente das demais notas)
- **RECUPERAÇÃO**: MA >= 6.0, mas pelo menos uma nota Mb1-4 < 6.0
- **APROVADO**: Todas as notas >= 6.0

### Total de Alunos:
- Baseado em `id_matricula` único
- Um aluno = múltiplos registros no CSV (uma linha por nota)

## Princípios de Big Data Aplicados

1. **Operações Vetorizadas**: Processamento otimizado com Pandas
2. **MapReduce**: Operações de filtragem e agregação otimizadas
3. **Data Quality**: Limpeza e normalização de dados
4. **Analytics**: Estatísticas descritivas e visualização
5. **Escalabilidade**: Otimizações de memória e performance

## API Endpoints

- `GET /`: Dashboard principal
- `POST /api/chart-data/`: Obter dados do gráfico
- `POST /api/generate-report/`: Gerar relatório

## Observações

- O arquivo CSV deve estar na raiz do projeto
- O sistema usa processamento otimizado com Pandas
- Cache em memória para melhor performance
- Design limpo e moderno com gradientes

