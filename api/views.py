from django.http import JsonResponse

from api.apimanager import ApiManager


def index(request):
    api = ApiManager()
    data = api.get(request.GET)
    return JsonResponse(data, safe=False)
