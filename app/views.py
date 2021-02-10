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
# Main Home View Function
# Pagination Available
def index(request):
    page_number = request.GET.get('page')
    data = get_data(True, page_number)

    context = {'page_obj': data}
    return render(request, 'index.html', context)

# after call details of perticular company
# request type: GET
# params : code <Company Code>
def details_page(request, code):
    data = get_details(code)
    
    # If code filtered from cache then return directly
    if cache.get(code):
        print("==============FROM CASHE==============")
        json_Data = cache.get(code)

    else:
        print("==============FROM DB==============")
        json_Data = {'code': data.CODE, 'name': data.NAME.strip(), 'open': data.OPEN, 'high': data.HIGH,
                     'low': data.LOW,
                     'close': data.CLOSE}
        # Set code and data to cache memory 
        cache.set(code, json_Data)

    return render(request, 'details.html', json_Data)


# Download CSV file of perticular company
# Request Type: GET
# params: Code
def download_csv(request, code):
    dir_name, filename = create_cv(code)

    # Open CSV file and send to client side
    with open(dir_name, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = f'inline; filename={filename}.csv'
        return response

    
# Autofile view, for better user exprience
# Can establish better and easy acess for user
# request Type: Get
# Pagination not available
def auto_fill(request):
    datas = get_data(False)
    all_data = []

    for data in datas:
        json_Data = {'code': data.CODE, 'name': data.NAME.strip()}

        all_data.append(json_Data)

    return JsonResponse(all_data, safe=False)
