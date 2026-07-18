from eoq import calculate_eoq
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

# --- Order policy for A-class items ---
    # Realistic per-item data: annual demand, order cost, holding cost
    item_data = {
        "Motor":   {"demand": 2400, "order_cost": 200, "holding": 12.0},
        "Gehäuse": {"demand": 3600, "order_cost": 180, "holding": 6.5},
    }

    print()
    print("--- A-class order policy ---")
    a_items = result[result["class"] == "A"]

    for item in a_items["item"]:
        d = item_data[item]
        eoq = calculate_eoq(d["demand"], d["order_cost"], d["holding"])
        orders = d["demand"] / eoq
        print(f"{item}: order {eoq:.0f} units per batch "
              f"({orders:.1f} orders/year)")

    # --- Pareto chart ---
    fig, ax1 = plt.subplots()

    ax1.bar(result["item"], result["annual_value"], color="steelblue")
    ax1.set_ylabel("Annual value (EUR)")
    ax1.tick_params(axis="x", rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(result["item"], result["cum_share"] * 100,
             color="darkred", marker="o")
    ax2.set_ylabel("Cumulative share (%)")
    ax2.axhline(y=80, color="gray", linestyle="--", alpha=0.5)

    plt.title("Pareto Analysis of Inventory Items")
    plt.tight_layout()
    plt.savefig("pareto_chart.png")
    plt.show()