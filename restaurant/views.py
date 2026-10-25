import json
from datetime import datetime
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .forms import BookingForm
from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer


def index(request):
    return render(request, 'index.html', {})


def menu(request):
    return render(request, 'menu.html', {'menu': Menu.objects.all()})


class MenuItemsView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


def book(request):
    form = BookingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
    return render(request, 'book.html', {'form': form})


def about(request):
    return render(request, 'about.html')


@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            booking_date = data['booking_date']
            no_of_guests = int(data['no_of_guests'])
            if Booking.objects.filter(booking_date=booking_date, no_of_guests=no_of_guests).exists():
                return JsonResponse({'error': 'A booking with these details already exists.'}, status=409)
            Booking.objects.create(name=data['name'], booking_date=booking_date, no_of_guests=no_of_guests)
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid booking payload.'}, status=400)
    date = request.GET.get('date', datetime.today().date())
    data = serializers.serialize('json', Booking.objects.filter(booking_date=date))
    return HttpResponse(data, content_type='application/json')


def reservations(request):
    date = request.GET.get('date', datetime.today().date())
    bookings_data = serializers.serialize('json', Booking.objects.filter(booking_date=date))
    return render(request, 'bookings.html', {'bookings': bookings_data})
