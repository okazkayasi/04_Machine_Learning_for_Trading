import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data

print pd.__version__
end_date = "31-12-2009"
start_date = "01-01-2008"
stocks = ["JPM"]

adj_close = get_data(stocks, pd.date_range(start_date, end_date))

# print pd.rolling_mean(adj_close, window=50)
