import StrategyLearner as sl
import datetime as dt
from ManualStrategy import ms



learner = sl.StrategyLearner(verbose = False, impact = 0.0) # constructor
learner.addEvidence("JPM", dt.datetime(2008,1,1), dt.datetime(2009,12,31), 100000)
