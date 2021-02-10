import csv

from django.core.cache import cache
from django.shortcuts import render
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.http import JsonResponse, HttpResponse

from .utils import get_data, get_details, create_cv

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# Create your views here.
def index(request):
    page_number = request.GET.get('page')
    data = get_data(True, page_number)

    context = {'page_obj': data}
    return render(request, 'index.html', context)


def details_page(request, code):
    data = get_details(code)
    if cache.get(code):
        print("==============FROM CASHE==============")
        json_Data = cache.get(code)

    else:
        print("==============FROM DB==============")
        json_Data = {'code': data.CODE, 'name': data.NAME.strip(), 'open': data.OPEN, 'high': data.HIGH,
                     'low': data.LOW,
                     'close': data.CLOSE}
        cache.set(code, json_Data)

    return render(request, 'details.html', json_Data)


def download_csv(request, code):
    dir_name, filename = create_cv(code)

    with open(dir_name, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = f'inline; filename={filename}.csv'
        return response


def auto_fill(request):
    datas = get_data(False)
    all_data = []

    for data in datas:
        json_Data = {'code': data.CODE, 'name': data.NAME.strip()}

        all_data.append(json_Data)

    return JsonResponse(all_data, safe=False)