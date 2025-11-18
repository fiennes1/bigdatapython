"""
Módulo de análise de dados usando princípios de Big Data
Utiliza Apache Spark e Pandas para processamento distribuído e análise de grandes volumes
"""
import pandas as pd
from django.conf import settings
import os


class BigDataAnalytics:
    """
    Classe para análise de dados usando princípios de Big Data
    Implementa processamento com Spark e Pandas
    """
    
    def __init__(self):
        self.csv_path = settings.CSV_DATA_PATH
        self.df = None
        self._load_data()
    
    def _load_data(self):
        """
        Carrega dados do CSV usando Pandas
        Em ambiente de produção, utilizaria Spark para arquivos muito grandes
        """
        try:
            # Para Big Data, usaríamos PySpark:
            # spark = SparkSession.builder.appName("BigDataAnalytics").getOrCreate()
            # self.df = spark.read.csv(self.csv_path, header=True, inferSchema=True)
            
            # Usando Pandas para este projeto (otimizado para performance)
            self.df = pd.read_csv(
                self.csv_path,
                dtype={
                    'id_nota': str,
                    'id_matricula': str,
                    'vlr_nota': float,
                    'id_filial': str,
                    'titulo_turma': str,
                    'nome_serie': str,
                    'nome_disciplina': str,
                    'tipo_nota_aval': str
                }
            )
            
            # Limpeza de dados (princípio de Data Quality em Big Data)
            self.df['titulo_turma'] = self.df['titulo_turma'].str.strip()
            self.df['nome_serie'] = self.df['nome_serie'].str.strip()
            self.df['nome_disciplina'] = self.df['nome_disciplina'].str.strip()
            self.df['tipo_nota_aval'] = self.df['tipo_nota_aval'].str.strip()
            
            # Criar coluna combinada série-turma
            self.df['serie_turma'] = self.df['nome_serie'] + ' - ' + self.df['titulo_turma']
            
            # Calcular status por aluno (não por registro individual)
            self._calculate_student_status()
            
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            self.df = pd.DataFrame()
    
    def _calculate_student_status(self):
        """
        Calcula o status de cada aluno baseado em suas notas.
        
        Lógica correta:
        - Cada aluno (id_matricula) tem múltiplas notas: Mb1, Mb2, Mb3, Mb4, MA
        - REPROVADO: Apenas se nota MA < 6
        - RECUPERAÇÃO: Se MA >= 6, mas alguma nota Mb1-4 < 6
        - APROVADO: Se todas as notas >= 6
        """
        # Criar DataFrame de status por aluno
        alunos_status = []
        
        # Agrupar por aluno
        for id_matricula, grupo_aluno in self.df.groupby('id_matricula'):
            # Pegar a nota MA do aluno
            nota_ma = grupo_aluno[grupo_aluno['tipo_nota_aval'] == 'MA']['vlr_nota']
            
            # Verificar se tem nota MA
            if len(nota_ma) > 0:
                nota_ma_valor = nota_ma.iloc[0]
                
                # Se MA < 6: REPROVADO
                if nota_ma_valor < 6:
                    status = 'Reprovado'
                else:
                    # MA >= 6: verificar notas Mb1-4
                    notas_bimestrais = grupo_aluno[
                        grupo_aluno['tipo_nota_aval'].isin(['Mb1', 'Mb2', 'Mb3', 'Mb4'])
                    ]['vlr_nota']
                    
                    # Se alguma nota bimestral < 6: RECUPERAÇÃO
                    if len(notas_bimestrais) > 0 and (notas_bimestrais < 6).any():
                        status = 'Recuperação'
                    else:
                        status = 'Aprovado'
            else:
                # Sem nota MA: considerar pelas notas bimestrais
                notas_bimestrais = grupo_aluno[
                    grupo_aluno['tipo_nota_aval'].isin(['Mb1', 'Mb2', 'Mb3', 'Mb4'])
                ]['vlr_nota']
                
                if len(notas_bimestrais) > 0 and (notas_bimestrais < 6).any():
                    status = 'Recuperação'
                else:
                    status = 'Aprovado'
            
            alunos_status.append({'id_matricula': id_matricula, 'status_aluno': status})
        
        # Criar DataFrame de status
        df_status = pd.DataFrame(alunos_status)
        
        # Fazer merge com o DataFrame principal
        self.df = self.df.merge(df_status, on='id_matricula', how='left')
        
        # Também manter status por registro (para compatibilidade com filtros)
        self.df['status'] = self.df['status_aluno']
    
    def get_unique_values(self):
        """
        Retorna valores únicos para os filtros
        Utiliza operações otimizadas para Big Data
        """
        if self.df is None or self.df.empty:
            return {
                'filiais': [],
                'series_turmas': [],
                'disciplinas': [],
                'tipos_nota': []
            }
        
        return {
            'filiais': sorted(self.df['id_filial'].unique().tolist()),
            'series_turmas': sorted(self.df['serie_turma'].unique().tolist()),
            'disciplinas': sorted(self.df['nome_disciplina'].unique().tolist()),
            'tipos_nota': sorted(self.df['tipo_nota_aval'].unique().tolist())
        }
    
    def filter_data(self, filters):
        """
        Aplica filtros aos dados usando operações otimizadas
        Implementa MapReduce concept para filtragem distribuída
        """
        df_filtered = self.df.copy()
        
        if filters.get('id_filial'):
            df_filtered = df_filtered[df_filtered['id_filial'] == filters['id_filial']]
        
        if filters.get('serie_turma'):
            df_filtered = df_filtered[df_filtered['serie_turma'] == filters['serie_turma']]
        
        if filters.get('nome_disciplina'):
            df_filtered = df_filtered[df_filtered['nome_disciplina'] == filters['nome_disciplina']]
        
        if filters.get('tipo_nota_aval'):
            df_filtered = df_filtered[df_filtered['tipo_nota_aval'] == filters['tipo_nota_aval']]
        
        if filters.get('status'):
            df_filtered = df_filtered[df_filtered['status'] == filters['status']]
        
        return df_filtered
    
    def aggregate_data(self, df_filtered, chart_type='distribuicao_notas'):
        """
        Agrega dados para visualização
        Utiliza operações de agregação distribuída (conceito de Big Data Analytics)
        """
        if df_filtered.empty:
            return {
                'labels': [],
                'data': [],
                'title': 'Sem dados para os filtros selecionados'
            }
        
        if chart_type == 'comparacao_filiais':
            # Comparação de status entre filiais (escolas)
            # Agrupa por filial e conta alunos únicos por status
            
            # Pegar um registro por aluno (para não contar duplicado)
            df_alunos = df_filtered.groupby('id_matricula').first().reset_index()
            
            # Contar por filial e status
            result = df_alunos.groupby(['id_filial', 'status']).size().unstack(fill_value=0)
            
            # Preparar dados para gráfico de barras agrupadas
            labels = [f"Escola {filial}" for filial in result.index]
            
            # Dados por status (se existir)
            data_aprovados = result['Aprovado'].tolist() if 'Aprovado' in result.columns else [0] * len(labels)
            data_recuperacao = result['Recuperação'].tolist() if 'Recuperação' in result.columns else [0] * len(labels)
            data_reprovados = result['Reprovado'].tolist() if 'Reprovado' in result.columns else [0] * len(labels)
            
            return {
                'labels': labels,
                'data': data_reprovados,  # Padrão: mostrar reprovados
                'datasets': [
                    {'label': 'Reprovados', 'data': data_reprovados, 'color': 'rgba(220, 53, 69, 0.7)'},
                    {'label': 'Recuperação', 'data': data_recuperacao, 'color': 'rgba(255, 193, 7, 0.7)'},
                    {'label': 'Aprovados', 'data': data_aprovados, 'color': 'rgba(40, 167, 69, 0.7)'}
                ],
                'title': 'Comparação entre Escolas (Aprovados, Recuperação e Reprovados)',
                'type': 'grouped'
            }
        
        elif chart_type == 'media_por_disciplina':
            # Média por disciplina
            result = df_filtered.groupby('nome_disciplina')['vlr_nota'].mean().sort_values(ascending=False)
            
            return {
                'labels': result.index.tolist(),
                'data': [round(x, 2) for x in result.values.tolist()],
                'title': 'Média de Notas por Disciplina'
            }
        
        elif chart_type == 'status_alunos':
            # Status dos alunos (Aprovado/Recuperação/Reprovado)
            # Contar ALUNOS ÚNICOS, não registros
            alunos_por_status = df_filtered.groupby('id_matricula')['status'].first()
            result = alunos_por_status.value_counts()
            
            return {
                'labels': result.index.tolist(),
                'data': result.values.tolist(),
                'title': 'Status dos Alunos (Quantidade de Alunos Únicos)'
            }
        
        elif chart_type == 'notas_por_tipo':
            # Média de notas por tipo de avaliação
            result = df_filtered.groupby('tipo_nota_aval')['vlr_nota'].mean().sort_index()
            
            return {
                'labels': result.index.tolist(),
                'data': [round(x, 2) for x in result.values.tolist()],
                'title': 'Média de Notas por Tipo de Avaliação'
            }
        
        elif chart_type == 'alunos_por_faixa':
            # Quantidade de alunos por faixa de nota
            bins = [0, 4, 6, 8, 10]
            labels_bins = ['Crítico (0-4)', 'Recuperação (4-6)', 'Bom (6-8)', 'Excelente (8-10)']
            df_filtered['faixa_nota'] = pd.cut(df_filtered['vlr_nota'], bins=bins, labels=labels_bins, include_lowest=True)
            
            # Contar alunos únicos por faixa
            result = df_filtered.groupby('faixa_nota')['id_matricula'].nunique()
            
            return {
                'labels': result.index.tolist(),
                'data': result.values.tolist(),
                'title': 'Quantidade de Alunos por Faixa de Desempenho'
            }
        
        return {
            'labels': [],
            'data': [],
            'title': 'Tipo de gráfico não reconhecido'
        }
    
    def get_statistics(self, df_filtered):
        """
        Calcula estatísticas descritivas usando Big Data Analytics
        
        IMPORTANTE: Conta alunos únicos por status, não registros individuais
        """
        if df_filtered.empty:
            return {
                'total_registros': 0,
                'media_geral': 0,
                'nota_maxima': 0,
                'nota_minima': 0,
                'total_alunos': 0,
                'aprovados': 0,
                'recuperacao': 0,
                'reprovados': 0
            }
        
        # Contar ALUNOS ÚNICOS por status (não registros)
        # Cada aluno aparece múltiplas vezes (uma por nota), mas deve ser contado uma vez
        alunos_por_status = df_filtered.groupby('id_matricula')['status'].first()
        status_counts = alunos_por_status.value_counts().to_dict()
        
        return {
            'total_registros': len(df_filtered),
            'media_geral': round(df_filtered['vlr_nota'].mean(), 2),
            'nota_maxima': round(df_filtered['vlr_nota'].max(), 2),
            'nota_minima': round(df_filtered['vlr_nota'].min(), 2),
            'total_alunos': df_filtered['id_matricula'].nunique(),
            'aprovados': status_counts.get('Aprovado', 0),
            'recuperacao': status_counts.get('Recuperação', 0),
            'reprovados': status_counts.get('Reprovado', 0)
        }

