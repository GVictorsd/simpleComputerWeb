####################
# Python script to parse the output of the verilog code from
# the console (linux pipeline) and process it to output a JSON
# file for the frontend to render.
####################

import sys

def main():

    outfile = "process.json"                    # output JSON file
    counter = 0                                 # index variable for JSON indexes

    with open(outfile, "w") as file:

        file.write('{\n"process":[\n')          # boilerplate header
        data = sys.stdin.read()                 # get data from the commandline

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



if __name__ == '__main__':
    main()