import pandas as pd
import matplotlib.pyplot as plt

def test_run():
    df = pd.read_csv("data/IBM.csv")
    print df['High']
    df['High'].plot()
    plt.show()

if __name__ == "__main__":
    test_run()