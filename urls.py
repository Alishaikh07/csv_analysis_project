from django.urls import path
from csv_analysis_app import views

urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),
    path('analysis/<int:pk>/', views.data_analysis, name='data_analysis'),
    path('plot/<int:pk>/', views.plot_histogram_base64, name='plot_histogram_base64'),
]
