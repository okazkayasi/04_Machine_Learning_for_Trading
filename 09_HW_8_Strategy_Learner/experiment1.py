import StrategyLearner as sl
import datetime as dt
from ManualStrategy import ms


learner = sl.StrategyLearner(verbose = False, impact = 0.00) # constructor
learner.addEvidence("IBM", dt.datetime(2008,1,1), dt.datetime(2009,12,31), 100000)



ms.test_policy(['IBM'], dt.datetime(2009,1,1), dt.datetime(2010,12,31), sv=100000)
