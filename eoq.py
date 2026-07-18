import math

def calculate_eoq(annual_demand, order_cost, holding_cost):
    """Calculate the Economic Order Quantity (EOQ).

    annual_demand: units per year (D)
    order_cost: fixed cost per order (S)
    holding_cost: holding cost per unit per year (H)
    """
    eoq = math.sqrt(2 * annual_demand * order_cost / holding_cost)
    return eoq


# --- Example usage ---
if __name__ == "__main__":
    demand = 12000      # units/year
    order_cost = 150    # EUR per order
    holding = 4         # EUR per unit per year

    result = calculate_eoq(demand, order_cost, holding)
    orders_per_year = demand / result

    print(f"EOQ: {result:.0f} units per order")
    print(f"Orders per year: {orders_per_year:.1f}")