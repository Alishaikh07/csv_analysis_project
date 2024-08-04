from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CSVFile
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def upload_csv(request):
    if request.method == 'POST':
        file = request.FILES['file']
        csv_data = CSVFile(upload=file)
        csv_data.save()
        return redirect('data_analysis', pk=csv_data.pk)
    return render(request, 'upload_csv.html')

def plot_histogram_base64(csv_path):
    df = pd.read_csv(csv_path)
    numerical_cols = df.select_dtypes(include=['int', 'float']).columns
    if not numerical_cols.any():
        return None

    buffer = BytesIO()
    plt.figure()
    for col in numerical_cols:
        sns.histplot(df[col], kde=False)
        plt.title(f'Histogram of {col}')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.savefig(buffer, format='png')
        plt.close()
        break

    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    image_base64 = base64.b64encode(image_png).decode('utf-8')
    return image_base64

def data_analysis(request, pk):
    csv_data = CSVFile.objects.get(pk=pk)
    csv_path = csv_data.upload.path
    df = pd.read_csv(csv_path)

    summary_stats = df.describe()
    missing_values = df.isnull().sum()

    histogram_base64 = plot_histogram_base64(csv_path)

    context = {
        'csv_data': csv_data,
        'summary_stats': summary_stats.to_html(classes="table table-bordered"),
        'missing_values': missing_values.to_frame(name='Missing Values').to_html(classes="table table-bordered"),
        'histogram_base64': histogram_base64,
    }
    return render(request, 'data_analysis.html', context)
