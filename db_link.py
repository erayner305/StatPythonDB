import mysql.connector
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import json

MAX_WELLS = 20

with open('db_info.json') as f:
    db_info = json.load(f)

cnx = mysql.connector.connect(user=db_info['user'], password=db_info['password'],
                              host=db_info['host'], database=db_info['database'])

cursor = cnx.cursor()

query = "SELECT w.name, d.sampleDate, d.observed FROM data d JOIN well w ON d.wellID = w.wellID WHERE d.constituentID = 1 ORDER BY w.name DESC, d.sampleDate ASC"
cursor.execute(query)

dates = []
values = []
data = {}
maxVal = 0

for (wellName, sampleDate, observed) in cursor:
    if "n/a" in observed:
        continue

    observed = observed.replace('<', '').replace('*', '').replace('(J)', '')
    observedNum = float(observed)

    if observedNum > maxVal:
        maxVal = observedNum

    if not(wellName in data):
        data[wellName] = {}
        data[wellName]['dates'] = []
        data[wellName]['values'] = []

    data[wellName]['dates'].append(sampleDate)
    data[wellName]['values'].append(observedNum)

cursor.close()
cnx.close()

yAxisLimUp = maxVal
yAxisLimDown = 0

fig, axes = plt.subplots( int(np.ceil(np.ceil(len(data)/(MAX_WELLS))/2)) , 2, figsize=(12, 12), layout = 'none' )

breakOuter=False
dataSplits = 1

for i in range(len(axes)):
    if breakOuter:
        break

    for j in range(len(axes[i])):
        if breakOuter:
            break

        ax = axes[i][j]
        for k, well in enumerate(data):

                if k - (MAX_WELLS * dataSplits) == 0:
                    
                    if j == 1:
                        i = i + 1
                        j = 0
                    else:
                        j = 1

                    dataSplits = dataSplits + 1     
                    ax = axes[i][j]
                
                ax.plot(data[well]['dates'], data[well]['values'], 'o--', lw=0.7, ms=5, label=well)
                ax.set_xlabel('Date')
                ax.set_ylabel('Antimony (mg/L)')
                ax.grid(visible=True)
                ax.autoscale(enable=True, axis = 'x', tight = True)
                ax.autoscale(enable=True, axis = 'y')
                ax.set_title("Time Series", pad = 10.0)
                ax.legend(loc = 'right', bbox_to_anchor = (1.3, .5), frameon = False, handletextpad = 4)

                if k == len(data) - 1:
                    breakOuter = True
                    break


fig.subplots_adjust(hspace=.25, wspace=.55)
plt.show()