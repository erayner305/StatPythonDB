import csv
import time

start = time.perf_counter() #for recording how fast this takes

# This is particularly useful for iterating through exactly the right amount of constituents. It could be four, it could be 300, who knows!? (max_length knows.)

def max_length(array, currentMax) :
    if len(array) > currentMax:
        return len(array)
    else:
        return currentMax
    
# This is intended to clear the data output file as well as the constituent file before assigning their column headers. You'll see this kind of thing
# below but only because this program loops through each of those several times. Maybe I could optimize that........

with open('output.csv', 'w') as data_output:
    print('wellID,constituentID,mdl,pql,observed,sampleDate', file=data_output)

with open('constituents.csv', 'w') as constituent_output:
    print('constituentID,name,units', file=constituent_output)

data_output.close()
constituent_output.close()

# This module reads the sanitas matrix (it hurts my brain, tab delimited to csv is a nightmare). I've realized I should really be using constants 
# instead of arbitrarily referencing [0] or [1]. Can be improved, but I did replace all strings using + with fstrings! Progress. - Easton
currentMax = 5
constituentID = 0
while constituentID < currentMax - 4:
    with open('sanitasMatrix.txt') as file:

        with open('wells.csv', 'w') as well_output:
            print('wellID,name,gradient', file=well_output)
        well_output.close()

        reader = csv.reader(file, delimiter='\t')
        facilityLine = True
        isFirstLine = True
        wellID = 0
        

        for line in file:

            line = line.split('\t')
            row = [element.strip() for element in line]

            if facilityLine: # This both wipes the well list, as well as provides the name of the facility

                with open('facility.csv', 'w', newline='') as facility_output:

                    print('facility', file=facility_output)

                    print(row[0].replace('[', '"').replace(']', '"'), file=facility_output)

                facilityLine = False

            else:
                if len(row) < 4:

                    with open('wells.csv', 'a', newline='') as well_output:

                        print(str(wellID) + ',' + row[0] + ',' + row[1], file=well_output)

                        wellID += 1

                else:
                    if isFirstLine:

                        with open('constituents.csv', 'a', newline='') as constituent_output:

                            units = row[constituentID + 4].split('(')

                            units[0] = units[0][:-1]
                            units[1] = units[1].replace(")", "")
                            
                            print(f'{constituentID},"{units[0]}",{units[1]}', file=constituent_output)

                        constituent = f'{str(constituentID)},NULL,NULL'

                        isFirstLine = False

                        file.readline()

                        continue

                    with open('output.csv', 'a', newline='') as data_output:
                            
                            unformattedDate = row[1].split('/')

                            if len(unformattedDate[0]) == 1:
                    
                                unformattedDate[0] = '0' + unformattedDate[0]

                            if len(unformattedDate[1]) == 1:

                                unformattedDate[1] = '0' + unformattedDate[1]

                            formattedDate = f'{unformattedDate[2]}-{unformattedDate[0]}-{unformattedDate[1]}'

                            print(f'{wellID},{constituent},{row[4 + constituentID]},{formattedDate}', file=data_output)
                            
                            
        currentMax = max_length(row, currentMax)
        constituentID += 1

end = time.perf_counter()

print(f'\nCompleted in {round(end-start, 3)} seconds!\n')

