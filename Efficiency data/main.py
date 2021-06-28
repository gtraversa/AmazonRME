import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

data = pd.read_csv('pre_code_change_data.csv')

grouped = data.groupby('Year')
data_2021 = grouped.get_group(2021)
data_2020 = grouped.get_group(2020)
data_2019 = grouped.get_group(2019)
data_2018 = grouped.get_group(2018)
merged = pd.concat([data_2018,data_2019,data_2020,data_2021], ignore_index=True)

merged.drop(columns=['Year','Month','Week'], inplace = True)
merged['Date'] = merged['Date'].map(lambda x: x.replace('00:00:00','').strip())
merged['KWh/Throughput'].where(merged['KWh/Throughput']<3, np.nan , inplace=True)

merged.interpolate(method ='linear', limit_direction ='forward',inplace = True)

merged['SQ meter SMA20'] = merged['kWh per SQ meter'].rolling(window = 20).mean()
merged['kWh/Throughput SMA20'] = merged['KWh/Throughput'].rolling(window = 20).mean()
merged['kWh per Operational Hour SMA20'] = merged['kWh per Operational Hour'].rolling(window = 20).mean()

merged.interpolate(method ='linear', limit_direction ='forward',inplace = True)

fig, (ax1,ax2,ax3) = plt.subplots(3,1,sharex=True)

ax1.plot(merged['Date'], merged['kWh per Operational Hour'],label = 'kWh per Operational Hour')
ax1.plot(merged['Date'], merged['kWh per Operational Hour SMA20'],label = 'kWh per Operational Hour SMA20')
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.legend(loc="upper right")
ax1.grid()

ax2.plot(merged['Date'], merged['KWh/Throughput'],label = 'KWh/Throughput')
ax2.plot(merged['Date'], merged['kWh/Throughput SMA20'],label = 'kWh/Throughput SMA20')
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.legend(loc="upper right")
ax2.grid()

ax3.plot(merged['Date'], merged['kWh per SQ meter'],label = 'kWh per SQ meter')
ax3.plot(merged['Date'], merged['SQ meter SMA20'],label = 'kWh per SQ meter SMA20')
ax3.xaxis.set_major_locator(mdates.MonthLocator())
ax3.legend(loc="upper right")
ax3.grid()

_ = plt.xticks(rotation=45)
plt.show()
