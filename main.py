import numpy as np
import pandas as pd
import plotly.express as px

def f(x):
    _f = lambda x: "/".join(x)
    return pd.Series(
        dict(Weight=_f(x.Weight), Reps=_f(x.Reps), Volume=x["Volume"].sum())
    )

if __name__ == "__main__":
    # df = pd.read_csv("strong.csv", delimiter=";")
    # exercises = exercises[2:-1]
    # for exercise in exercises:
    #     ex_df = df[df["Exercise Name"] == exercise][["Date", "Weight", "Reps"]]
    #     ex_df["Reps"] = ex_df.Reps.astype(int)
    #     ex_df["volume"] = ex_df.Weight.str.replace(",", ".").astype(float) * ex_df.Reps

    df = pd.read_csv("strong.csv", delimiter=";")
    exercise = "Deadlift (Barbell)"

    df = df[df["Exercise Name"] == exercise][["Date", "Weight", "Reps"]]
    # Compute volume load for each set
    df["Volume"] = df.Weight.str.replace(",", ".").astype(float) * df.Reps
    # Reps as str to enable concatenation
    df["Reps"] = df.Reps.astype(int).astype(str)
    # Combine rows
    df = df.groupby(["Date"]).apply(f).reset_index()

    # Create fig
    fig = px.bar(
        df, x="Date", y="Volume", title=exercise, hover_data=["Weight", "Reps"]
    )
    # Write fig as html to deploy
    fig.write_html("index.html")
