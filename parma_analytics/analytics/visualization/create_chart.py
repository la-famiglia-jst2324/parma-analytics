import pandas as pd
import matplotlib.pyplot as plt


def create_time_series_chart(df_pandas, title, x_label, y_label):
    plt.figure(figsize=(6, 4))
    plt.plot(df_pandas["modified_at"], df_pandas["value"], marker="o")
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt
