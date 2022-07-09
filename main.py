import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


pd.options.mode.chained_assignment = None  # default='warn'


def f(x):
    _f = lambda x: "/".join(x)
    return pd.Series(
        dict(Weight=_f(x.Weight), Reps=_f(x.Reps), Volume=x["Volume"].sum())
    )


if __name__ == "__main__":

    df = pd.read_csv("strong.csv", delimiter=";")
    df['Date'] = pd.to_datetime(df.Date, errors='coerce')
    df =  df[df.Date > '2021-09-01']
    df = df[["Date", "Exercise Name", "Weight", "Reps"]].dropna(axis=0)
    default_exercise = "Deadlift (Barbell)"
    exercises = list(df['Exercise Name'].unique())
    exercises.sort()

    fig = go.Figure()
    exercise_plot_names = []
    buttons = []

    # del exercises[-2]

    for exercise_name in exercises:
        exercise = df[
            (df["Exercise Name"] == exercise_name)
        ]

        exercise["Weight"] = exercise.Weight.str.replace(",", ".").astype(float)

        # Compute volume load for each set
        exercise["Volume"] = exercise.Weight * exercise.Reps

        # Reps as str to enable concatenation
        exercise["Weight"] = exercise.Weight.astype(str)
        exercise["Reps"] = exercise.Reps.astype(int).astype(str)

        # Combine rows
        exercise = exercise.groupby(["Date"]).apply(f).reset_index()
        custom_data = np.dstack((exercise.Weight, exercise.Reps))[0]

        # We have two traces we're plotting per state: a boxplot of the submission quartiles, and a line with the current data to-date
        fig.add_trace(
            go.Bar(
                x=exercise["Date"],
                y=exercise["Volume"],
                customdata=custom_data,
                # title=exercise, 
                # hover_data=["Weight", "Reps"],
                hovertemplate="<br>".join([
                            "Volume: %{y}",
                            "Date: %{x}",
                            "Weight: %{customdata[0]}",
                            "Reps: %{customdata[1]}",
                        ]) + "<extra></extra>",
                visible=(exercise_name == default_exercise),
            )
        )
        exercise_plot_names.extend([exercise_name])

    for exercise_name in exercises:
        buttons.append(
            dict(
                method="update",
                label=exercise_name,
                args=[{"visible": [exercise_name == r for r in exercise_plot_names]}],
            )
        )

    # Add dropdown menus to the figure
    fig.update_layout(
        showlegend=False,
        updatemenus=[
            {
                "buttons": buttons,
                "direction": "down",
                "active": exercises.index(default_exercise),
                "showactive": True,
                "x": 0.15,
                "y": 1.05,
            }
        ],
    )
    # Write fig as html to deploy
    fig.write_html("index.html")
