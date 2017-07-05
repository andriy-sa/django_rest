from django.http import JsonResponse


def error404(request):
    return JsonResponse({}, status=404)
