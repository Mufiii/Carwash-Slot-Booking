from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def place_order(request) :
    return render(request,'orders.html')

  