from django.http import response
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# imports
from django import forms
import json
from main.helpers import assemble, outToJson
import os
import subprocess

def index(request):
    '''
    main route
    code to send json data to the frontend
    '''

    return render(request, "main/index.html",{
        "codein" : 1
    })

def write(request):
    '''
    route to get code, process and run it with in the verilog module
    '''

    if request.method == 'POST':
        filename = "assemblycode.asm"       # auxilary file to store instructions
        outfilepath = "simpleComputer/program.v"
        add_code = request.POST.get('code', None)   # get form data
        if add_code is not None:                    # and write it to the auxilary file
            with open(filename, 'w') as file:
                file.write(add_code)

            # convert the instructions to verilog module form to run it
            # returns -1 if instructions are invalid
            if assemble(filename, outfilepath) == -1:
                return HttpResponse('<a href="/main/"> <h1>Oops!! something went wrong with the code</h1> </a>')
        
        # os.system(cmd)
        os.system(f'iverilog -I simpleComputer -o simpleComputer/a.out simpleComputer/program.v')
        # os.system(f'vvp simpleComputer/a.out | python3 simpleComputer/processop.py')


        returnfile = 'process.json'     # file which will hold resulting json data which will be sent back to the interface

        # run the out file from previous step using vvp and write the result to a file for next step
        os.system(f'vvp simpleComputer/a.out > jsoninput.txt')
        # convert the raw data from previous step to json format.
        outToJson('jsoninput.txt', returnfile)


        # read the json file and convert the data to json object
        jsondata = ""
        with open(returnfile, "r") as file:
            jsondata = file.read()

        jsondata = json.loads(jsondata)
        jsondata = str(jsondata)

        # assembly code entered by the user...
        asmcode = ""
        with open("assemblycode.asm", "r") as file:
            asmcode = file.read()
        
        asmcode = json.dumps({
            "asmcode": asmcode
        })

        return render(request, "main/index.html", {
            "codein" : 0,               # set state(not taking any input, displaying the output)
            "jsondata": jsondata,           # json data containing execution sequence
            "asmcode": asmcode              # code entered by the user
        })
        