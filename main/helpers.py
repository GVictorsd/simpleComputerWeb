##########################
#
# Some helper functions for the main program
##############

def assemble(infile:str, outfile:str):
    '''
    function takes input a file containing raw assembly text from the interface
    and outputs a valid verilog file as output which can then be run by iverilog
    '''

    # dict to map mnenomics to opcodes
    opcode = {
        "nop": "4'h0",
        "lda": "4'h1",
        "add": "4'h2",
        "sub": "4'h3",
        "sta": "4'h4",
        "ldi": "4'h5",
        "jmp": "4'h6",
        "jc": "4'h7",
        "jz": "4'h8",
        "out": "4'he",
        "hlt": "4'hf"
    }
    
    code = []
    ipcount = 0             # current memory address to load the inst into memory
    
    # some useful strings
    startstr = '`timescale 10ns/1ns\n`include "board.v"\nmodule program;\nboard bord();\nreg[7:0] Buss;\nreg[3:0] addr;\nreg clr,ramoa,ramwa;\n'
    resetstr = 'assign bord.hlt=0;\ninitial\nbegin\nbord.clr <= 1;\n#4 bord.clr <= 0;\n'
    endstr = 'end\ninitial\nbegin\n#300 $finish;\nend\nendmodule'

    with open(outfile, "w") as outfl:
        # boilerplate code...
        outfl.write(startstr)
        outfl.write(resetstr)

        # read the auxilary instructions file
        with open(infile, "r") as infl:
            for line in infl:
                code.append(line.split())

        # convert to verilog module form and write to the output file
        for inst in code:
            if inst[0] == "ram" :
                outfl.write(f"bord.rm.mem[4'h{inst[2]}] <= 8'h{inst[1]};\n")
            else:
                try:
                    outfl.write(f"bord.rm.mem[4'h{'{:x}'.format(ipcount)}] <= {{{opcode[inst[0]]}, 4'h{inst[1]}}};\n")
                    ipcount += 1            # increment the address to load next
                except:
                    # not a valid instruction!!
                    return -1   # unsuccessful transform (wrong syntax)

        # boilerplate ending code
        outfl.write(endstr)

    return 1    # successful execution



def outToJson(datafile:str, outfile:str):
    '''
    function which takes input a vvp output from a file(datafile) and converts the data
    to a json file(outfile) containing the sequence of events
    '''

    # outfile = "process.json"                    # output JSON file
    counter = 0                                 # index variable for JSON indexes
    data = ""
    with open(datafile, "r") as file:           # read data from the input file
        data = file.read()

    with open(outfile, "w") as file:

        file.write('{\n"process":[\n')          # boilerplate header
        # data = sys.stdin.read()                 # get data from the commandline

        data = data.split('#')                  # get individual blocks

        for index, elem in enumerate(data):     # get individual lines(sequences) of the block
            data[index] = elem.split('\n')

        for i, elem in enumerate(data):         # get rid of empty strings in the data
            data[i] = list(filter(lambda x:x!="", elem))

        for I, block in enumerate(data):        # conversion to JSON format
            counter = 0
            file.write('{\n')
            for index, line in enumerate(block):
                file.write(f'"{counter}": "{line}"')
                if(index != len(block)-1):
                    file.write(',\n')
                else:
                    file.write('\n')
                counter += 1
            if(I != len(data)-1):
                file.write('},\n')
            else:
                file.write('}\n')
        
        file.write(']\n}')      # boilerplate code (footer)
