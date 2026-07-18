import pandas as pd
import matplotlib.pyplot as plt

def abc_analysis(df, value_column):
    """Classify items into A/B/C classes by cumulative value share.

    A: top items up to 80% of total value
    B: next items up to 95%
    C: the rest
    """
    df = df.sort_values(value_column, ascending=False).copy()
    df["share"] = df[value_column] / df[value_column].sum()
    df["cum_share"] = df["share"].cumsum()
    df["class"] = df["cum_share"].apply(
        lambda x: "A" if x <= 0.80 else ("B" if x <= 0.95 else "C")
    )
    return df


if __name__ == "__main__":
    items = pd.DataFrame({
        "item": ["Motor", "Gehäuse", "Sensor", "Kabel", "Schraube",
                 "Dichtung", "Lager", "Feder", "Stecker", "Clip"],
        "annual_value": [420000, 260000, 180000, 90000, 40000,
                         25000, 15000, 9000, 6000, 3000]
    })

    result = abc_analysis(items, "annual_value")
    print(result[["item", "annual_value", "cum_share", "class"]].round(3))
    print()
    print(result["class"].value_counts())