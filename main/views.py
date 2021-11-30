from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django import forms

def index(request):
    print("hello world")
    return render(request, "main/index.html")

def write(request):
    print(555555)
    if request.method == 'POST':
        add_code = request.POST.get('code', None)
        if add_code is not None:
            print(add_code)