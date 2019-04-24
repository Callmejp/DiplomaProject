from django.urls import path
from . import views

urlpatterns = [
    path('result/', views.queryResult, name='query'),
    path('analyze/', views.analyzeResult, name='analyze'),
    path('query/', views.test, name='test'),
    path('twocharts/', views.twoCharts, name='twocharts'), 
]

