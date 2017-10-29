import pandas as pd

def getlist():
    df = pd.read_csv("../NYSEcut.csv")
    return(df.to_dict("records"))
