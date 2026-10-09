import pandas as pd
import numpy as np
import json

# Generate simulated venue ticket sales & sponsorship exposure dataset
np.random.seed(42)
events = [f"Game_{i:02d}" for i in range(1, 21)]
zones = ["VIP Courtside", "Lower Bowl", "Upper Deck", "Suites"]

data = []
for event in events:
    for zone in zones:
        capacity = 500 if zone == "Lower Bowl" else (100 if zone == "VIP Courtside" else 1000)
        tickets_sold = np.random.randint(int(capacity * 0.6), capacity + 1)
        base_price = 150 if zone == "VIP Courtside" else (80 if zone == "Lower Bowl" else 30)
        actual_price = base_price * np.random.uniform(0.9, 1.3)
        sponsorship_impressions = tickets_sold * np.random.randint(5, 12)
        
        data.append({
            "event_id": event,
            "seating_zone": zone,
            "capacity": capacity,
            "tickets_sold": tickets_sold,
            "avg_ticket_price": round(actual_price, 2),
            "sponsorship_impressions": sponsorship_impressions
        })

df = pd.DataFrame(data)

# Analytics Calculations
df["total_revenue"] = df["tickets_sold"] * df["avg_ticket_price"]
df["occupancy_pct"] = round((df["tickets_sold"] / df["capacity"]) * 100, 2)
df["rev_per_available_seat"] = round(df["total_revenue"] / df["capacity"], 2)

# Dynamic Pricing Strategy Flag
df["yield_status"] = np.where(
    (df["occupancy_pct"] > 90) & (df["avg_ticket_price"] < 100),
    "Underpriced (High Demand)",
    np.where(df["occupancy_pct"] < 70, "Low Yield (Price Adjustment Recommended)", "Optimal")
)

# Export processed datasets for Power BI / Excel visualization
df.to_csv("outputs/sports_insights_summary.csv", index=False)

summary_metrics = {
    "total_revenue_generated": round(df["total_revenue"].sum(), 2),
    "overall_occupancy_rate": round(df["occupancy_pct"].mean(), 2),
    "underpriced_zones_identified": int((df["yield_status"] == "Underpriced (High Demand)").sum()),
    "total_sponsorship_impressions": int(df["sponsorship_impressions"].sum())
}

with open("outputs/sports_analytics_metrics.json", "w") as f:
    json.dump(summary_metrics, f, indent=4)

print("Analytics pipeline executed successfully. Output files saved to outputs/")