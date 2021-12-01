from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django import forms
import json

def index(request):
    data = ""
    with open("main/seq.json", "r") as file:
        data = file.read()
    data = json.loads(data)
    data = str(data)
    return render(request, "main/index.html", {
        "str": data
    })

def write(request):
    if request.method == 'POST':
        filename = "assemblycode.asm"
        add_code = request.POST.get('code', None)
        if add_code is not None:
            with open(filename, 'w') as file:
                file.write(add_code)
        return HttpResponseRedirect("/main/")
    else:
        return Http404