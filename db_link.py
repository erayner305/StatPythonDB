import mysql.connector
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import re

cnx = mysql.connector.connect(user='root', password='Wekljor#1',
                              host='104.222.17.66', database='gwstats')

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
        data[wellName][0] = []
        data[wellName][1] = []

    data[wellName][0].append(sampleDate)
    data[wellName][1].append(observedNum)

cursor.close()
cnx.close()

yAxisLimUp = maxVal
yAxisLimDown = 0

for well in data:
    plt.plot(data[well][0], data[well][1], label=well)

plt.yticks([yAxisLimDown, (yAxisLimUp - yAxisLimDown) * 1/4 , (yAxisLimUp - yAxisLimDown) * 1/2  , (yAxisLimUp - yAxisLimDown) * 3/4 , yAxisLimUp])
plt.xlabel('Date')
plt.ylabel('Antimony')
plt.title('Antimony levels by well')
plt.legend()
plt.show()