import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

data = pd.read_csv('pre_code_change_data.csv')
data.drop(columns=['Year','Month','Week'], inplace = True)
data.drop(axis = 0, index = 1062, inplace = True)
data['Date'] = data['Date'].map(lambda x: x.replace('00:00:00','').strip())
data['SQ meter SMA20'] = data['kWh per SQ meter'].rolling(window = 20).mean()
data['kWh/Throughput SMA20'] = data['KWh/Throughput'].rolling(window = 20).mean()
data['kWh per Operational Hour SMA20'] = data['kWh per Operational Hour'].rolling(window = 20).mean()
print(data.tail(10))
print(data)

fig, (ax1,ax2,ax3) = plt.subplots(3,1,sharex=True)

ax1.plot(data['Date'], data['kWh per Operational Hour'],label = 'kWh per Operational Hour')
ax1.plot(data['Date'], data['kWh per Operational Hour SMA20'],label = 'kWh per Operational Hour SMA20')
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.legend(loc="upper right")
ax1.grid()

ax2.plot(data['Date'], data['KWh/Throughput'],label = 'KWh/Throughput')
ax2.plot(data['Date'], data['kWh/Throughput SMA20'],label = 'kWh/Throughput SMA20')
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.legend(loc="upper right")
ax2.grid()

ax3.plot(data['Date'], data['kWh per SQ meter'],label = 'kWh per SQ meter')
ax3.plot(data['Date'], data['SQ meter SMA20'],label = 'kWh per SQ meter SMA20')
ax3.xaxis.set_major_locator(mdates.MonthLocator())
ax3.legend(loc="upper right")
ax3.grid()

_ = plt.xticks(rotation=45)
plt.show()
