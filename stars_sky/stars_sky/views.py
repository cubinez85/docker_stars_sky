from django.shortcuts import render
from django.http import JsonResponse


def sky_view(request):
    """Отображение интерактивной модели звёздного неба."""
    return render(request, 'sky_standalone.html')


def api_root(request):
    """Корневой URL — красивая HTML-страница с информацией об API."""
    return render(request, 'api_root.html')


def health_check(request):
    """Health check endpoint для мониторинга."""
    return JsonResponse({'status': 'ok'})
