from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# imports
from django import forms
import json
from main.helpers import assemble

def index(request):
    # main route
    # code to send json data to the frontend
    data = ""
    with open("main/seq.json", "r") as file:
        data = file.read()
    data = json.loads(data)
    data = str(data)
    return render(request, "main/index.html", {
        "str": data
    })

def write(request):
    # route to get code, process and run it with in the verilog module
    if request.method == 'POST':
        filename = "assemblycode.asm"       # auxilary file to store instructions
        add_code = request.POST.get('code', None)   # get form data
        if add_code is not None:                    # and write it to the auxilary file
            with open(filename, 'w') as file:
                file.write(add_code)

            # convert the instructions to verilog module form to run it
            # returns -1 if instructions are invalid
            if assemble(filename) == -1:
                return HttpResponse('<a href="/main/"> <h1>Oops!! somethings wrong with the code</h1> </a>')
        return HttpResponseRedirect("/main/")
    else:
        return Http404