import pandas as pd

def getlist():
    df = pd.read_csv("../NYSEcut.csv")
    print(df.to_dict("records")[0])
    return(df.to_dict("records"))
