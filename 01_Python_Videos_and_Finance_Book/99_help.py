import numpy as np
import pandas as pd
from scipy.stats import pearsonr

np.random.seed(10)
a = np.random.random(30).reshape(10,3)
b = np.random.random(30).reshape(10,3)

a_1 = pd.DataFrame(a)
b_1 = pd.DataFrame(b)

print pd.rolling_corr(arg1=a_1, arg2=b_1, window=5)

