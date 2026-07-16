from csv import DictReader

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator

from pagination import settings

def index(request):
    return redirect(reverse('bus_stations'))

def get_station_list():
    csv_file = settings.BUS_STATION_CSV

    station_list = []
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        stations = DictReader(csvfile)

        for station in stations:
            station_list.append({
                'Name': station['Name'],
                'Street': station['Street'],
                'District': station['District']
            })

    return station_list

def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    station_list = get_station_list()
    paginator = Paginator(station_list, 10)
    current_page = request.GET.get('page', 1)
    page = paginator.get_page(current_page)

    context = {
         'bus_stations': page.object_list,
         'page': page,
    }
    return render(request, 'stations/index.html', context)
