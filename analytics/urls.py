"""
URLs para o app de analytics
"""
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/chart-data/', views.get_chart_data, name='chart_data'),
    path('api/generate-report/', views.generate_report, name='generate_report'),
]

