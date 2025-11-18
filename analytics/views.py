"""
Views para o sistema de análise de notas
Implementa endpoints para dashboard e geração de relatórios
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .data_processor import BigDataAnalytics
import json


# Instância global do processador de dados (em produção, usar cache/Redis)
analytics_engine = BigDataAnalytics()


def dashboard(request):
    """
    View principal do dashboard com filtros e visualização
    """
    # Obter valores únicos para os filtros
    unique_values = analytics_engine.get_unique_values()
    
    context = {
        'filiais': unique_values['filiais'],
        'series_turmas': unique_values['series_turmas'],
        'disciplinas': unique_values['disciplinas'],
        'tipos_nota': unique_values['tipos_nota'],
        'status_options': ['Aprovado', 'Recuperação', 'Reprovado']
    }
    
    return render(request, 'analytics/dashboard.html', context)


@require_http_methods(["POST"])
def get_chart_data(request):
    """
    API endpoint para obter dados do gráfico baseado nos filtros
    Retorna JSON com dados processados usando Big Data Analytics
    """
    try:
        # Obter filtros do request
        data = json.loads(request.body)
        filters = {
            'id_filial': data.get('id_filial', ''),
            'serie_turma': data.get('serie_turma', ''),
            'nome_disciplina': data.get('nome_disciplina', ''),
            'tipo_nota_aval': data.get('tipo_nota_aval', ''),
            'status': data.get('status', '')
        }
        
        # Remover filtros vazios
        filters = {k: v for k, v in filters.items() if v}
        
        # Tipo de gráfico solicitado
        chart_type = data.get('chart_type', 'distribuicao_notas')
        
        # Filtrar dados
        df_filtered = analytics_engine.filter_data(filters)
        
        # Agregar dados para o gráfico
        chart_data = analytics_engine.aggregate_data(df_filtered, chart_type)
        
        # Obter estatísticas
        statistics = analytics_engine.get_statistics(df_filtered)
        
        return JsonResponse({
            'success': True,
            'chart_data': chart_data,
            'statistics': statistics
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@require_http_methods(["POST"])
def generate_report(request):
    """
    Gera dados para relatório em formato JSON
    
    """
    try:
        data = json.loads(request.body)
        filters = {
            'id_filial': data.get('id_filial', ''),
            'serie_turma': data.get('serie_turma', ''),
            'nome_disciplina': data.get('nome_disciplina', ''),
            'tipo_nota_aval': data.get('tipo_nota_aval', ''),
            'status': data.get('status', '')
        }
        
        # Remover filtros vazios
        filters = {k: v for k, v in filters.items() if v}
        
        chart_type = data.get('chart_type', 'distribuicao_notas')
        
        # Filtrar e agregar dados
        df_filtered = analytics_engine.filter_data(filters)
        chart_data = analytics_engine.aggregate_data(df_filtered, chart_type)
        statistics = analytics_engine.get_statistics(df_filtered)
        
        # Criar relatório estruturado
        report = {
            'titulo': 'Relatório de Análise de Notas',
            'filtros_aplicados': filters,
            'grafico': chart_data,
            'estatisticas': statistics
        }
        
        return JsonResponse({
            'success': True,
            'report': report
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

