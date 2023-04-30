import csv

# Wipe the well list, data, constituents and facility clean
with open('wells.csv', 'w') as well_output:
    print('wellID, ' + 'name, ' + 'gradient', file=well_output)

with open('output.csv', 'w') as data_output:
    print('wellID, ' + 'constituentID, ' + 'mdl, ' + 'pql, ' + 'observed, ' + 'sampleDate', file=data_output)

with open('facility.csv', 'w') as facility_output:
    print('facility', file=facility_output)

with open('constituents.csv', 'w') as constituent_output:
    print('constituentID, ' + 'name, ' + 'units', file=constituent_output)

well_output.close() 
data_output.close()
facility_output.close()
constituent_output.close()

# This module reads the sanitas matrix (it hurts my brain, tab delimited to csv is a nightmare)
currentMax = 5
constituentID = 0
while constituentID < currentMax - 4:
    with open('sanitasMatrix.txt') as file:
        open('wells.csv', 'w').close()
        reader = csv.reader(file, delimiter='\t')
        facilityLine = True
        isFirstLine = True
        wellID = 0
        

        for line in file:
            line = line.split('\t')
            row = [element.strip() for element in line]
            if facilityLine: # This both wipes the well list, as well as provides the name of the facility
                with open('facility.csv', 'w', newline='') as facility_output:
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
                            print(units)
                            print(str(constituentID) + ',"' + units[0] + '",' + units[1], file=constituent_output)
                        constituent = str(constituentID) + ',' + 'NULL'+ ',' + 'NULL'
                        isFirstLine = False
                        file.readline()
                        continue

                    with open('output.csv', 'a', newline='') as data_output:
                            unformattedDate = row[1].split('/')
                            if len(unformattedDate[0]) == 1:
                                unformattedDate[0] = '0' + unformattedDate[0]

                            if len(unformattedDate[1]) == 1:
                                unformattedDate[1] = '0' + unformattedDate[1]
                            formattedDate = unformattedDate[2] + '-' + unformattedDate[0] + '-' + unformattedDate[1]
                            print(str(wellID) + ',' + constituent + ',' + row[4 + constituentID] + ',' + formattedDate, file=data_output)
        currentMax = max_length(row, currentMax)
        constituentID += 1



