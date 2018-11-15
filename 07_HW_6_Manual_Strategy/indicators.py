import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data
import matplotlib.pyplot as plt

end_date = "31-12-2009"
start_date = "01-01-2007"
stocks = ["JPM"]

adj_close = get_data(stocks, pd.date_range(start_date, end_date))
adj_close.fillna(method='ffill', inplace=True)
adj_close.fillna(method='bfill', inplace=True)

jpm = adj_close.ix[:, ["JPM"]]
rm_jpm = pd.rolling_mean(adj_close["JPM"], window=20)
rm_150_jpm = pd.rolling_mean(adj_close["JPM"], window=150)
rstd_jpm = pd.rolling_std(adj_close["JPM"], window=20)

def get_bollinger_bands(rm, rstd):
    upper_band = rm + 2*rstd
    lower_band = rm - 2*rstd

    return upper_band, lower_band

upper_band, lower_band = get_bollinger_bands(rm_jpm, rstd_jpm)
jp = adj_close["JPM"]['2008-01-01':]
up = upper_band['2008-01-01':]
low = lower_band['2008-01-01':]
ax = jp.plot()
plt.title("Bollinger Bands", fontsize = 20)
plt.ylabel("JPM", fontsize = 20)
plt.rcParams["figure.figsize"] = (16,12)
up.plot(label='upper band', ax=ax)
low.plot(label='lower band', ax=ax)
plt.legend(fontsize=14)
plt.savefig('Bollinger Bands.png', dpi=100)
plt.clf()
# plt.show()

# stochastic
jpm['highest 14'] = pd.rolling_max(jpm["JPM"], window=14)
jpm['lowest 14'] = pd.rolling_min(jpm["JPM"], window=14)
K = (jpm["JPM"] - jpm["lowest 14"])/ (jpm['highest 14'] - jpm['lowest 14']) * 100
slow_stoch = pd.rolling_mean(K, window=3)

slow_stoch_2008 = slow_stoch['2008-01-01':]

fig,ax1 = plt.subplots()
# ax1.plot(slow_stoch)
# ax1.title('Slow Stochastic', fontsize=20)
ax1.set_xlabel('Date', fontsize=20)
ax1.set_ylabel('Slow Stochastic)', fontsize=20)
ax1.plot(slow_stoch_2008)
plt.axhline(20, color='tab:red')
plt.axhline(80, color='tab:green')
fig.savefig('Slow Stochastic.png', dpi=100)
plt.clf()

JP = jpm[['JPM']]
JP['150-SMA'] = rm_150_jpm
JP['20-SMA'] = rm_jpm


JP_2008 = JP['2008-01-01':]
plt.title('150 and 20 Days Simple Moving Average', fontsize=20)
plt.xlabel('Date', fontsize=20)
plt.ylabel('JPM value', fontsize=20)
plt.plot(JP_2008['JPM'], label='JPM')
plt.plot(JP_2008['150-SMA'], label='150-SMA')
plt.plot(JP_2008['20-SMA'], label='20-SMA')
plt.legend()
plt.savefig('Moving Averages.png', dpi=100)
plt.clf()


e = 12
rm_jpm_1 = pd.rolling_mean(adj_close["JPM"], window=e)
ema_12 = np.zeros(len(rm_jpm_1.index))
multiplier = 2./(e+1)
ema_12[e-1] = rm_jpm_1[e-1]
for i in range(e, len(jpm.index)):
    close = jpm["JPM"].values[i]
    em = ema_12[i-1]
    ema_12[i] = (close - em) * multiplier + em


e = 26
rm_jpm_1 = pd.rolling_mean(adj_close["JPM"], window=e)
ema_26 = np.zeros(len(rm_jpm_1.index))
multiplier = 2./(e+1)
ema_26[e-1] = rm_jpm_1[e-1]
for i in range(e, len(jpm.index)):
    close = jpm["JPM"].values[i]
    em = ema_26[i-1]
    ema_26[i] = (close - em) * multiplier + em


df_macd = pd.DataFrame(rm_jpm_1)
df_macd['ema_12'] = ema_12
df_macd['ema_26'] = ema_26
df_macd['MACD'] = df_macd['ema_12'] - df_macd['ema_26']


MACD = ema_12 - ema_26
MACD[:25] = 0




# signal_line
e = 9
rm_macd = pd.rolling_mean(MACD, window=e)
sig = np.zeros(len(MACD))
multiplier = 2./(e+1)
sig[e-1] = rm_macd[e-1]
for i in range(e, len(MACD)):
    close = MACD[i]
    em = sig[i-1]
    sig[i] = (close - em) * multiplier + em

df_macd['signal'] = sig
df_macd['hist'] = df_macd['MACD'] - df_macd['signal']



hist = df_macd['hist']
hist = hist['2008-01-01':]

plt.title('Standart MACD', fontsize=20)
plt.xlabel('Date', fontsize=20)
plt.ylabel('MACD Value', fontsize=20)
plt.plot(hist)
plt.axhline(0)

# plt.plot(hist)
plt.savefig('MACD Histogram.png', dpi=100)
plt.clf()