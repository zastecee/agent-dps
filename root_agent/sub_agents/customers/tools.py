import csv
import json
from datetime import UTC, datetime
from typing import Literal

from dateutil.relativedelta import relativedelta

# Load the customers dataset from a CSV file
with open("customers_dataset.csv", mode="r", encoding="iso-8859-1", newline="") as file:
  records = list(csv.DictReader(file))


CUSTOMER_BILLING_MAP = {
  "prepaid": "DC_PREPAD",
  "hybrid": "DC_HYBRID",
  "total": "DC_TOTAL",
}

BillingType = Literal["prepaid", "hybrid", "total"]


total = 0
for item in records:
  if item["EVENT_DESCRIPTION"] == "MTD Active GSM" and item["DC_DATE"] == "06-AUG-26":
    total = float(item["DC_PREPAD"]) + total


# Function to get total customers per day for a specific KPI and date
def get_total_customers_per_day(
  kpi: str,
  date: str,
  billing_type: BillingType = "prepaid",
) -> dict:
  try:
    target_column = CUSTOMER_BILLING_MAP.get(billing_type.lower(), billing_type)

    total = sum(
      int(item[target_column])
      for item in records
      if item.get("EVENT_DESCRIPTION") == kpi and item.get("DC_DATE") == date
    )

    return {
      "date": date,
      "kpi": kpi,
      "billing_type": billing_type,
      "total_customers": f"{round(total):,}",
    }
  except (KeyError, ValueError) as e:
    return {"error": f"get_total_customers_per_day failed due to invalid data: {e}"}


# # Function to get the total revenue for a specific KPI and date range
# def get_kpi_month_to_date_total(
#   kpi: str,
#   target_date: str,
#   billing_type: BillingType = "prepaid",
# ) -> dict:
#   try:
#     target_column = RECHARGE_BILLING_MAP.get(billing_type.lower(), billing_type)

#     parsed_dt = datetime.strptime(target_date, "%d-%b-%y").replace(tzinfo=UTC)
#     target_date_obj = parsed_dt.date()
#     month_start_date = target_date_obj.replace(day=1)
#     month_to_date_total = 0.0

#     for record in records:
#       if record["CHANNEL"] != kpi:
#         continue

#       record_date = (
#         datetime.strptime(record["BPM_START_DATE"], "%d-%b-%y")
#         .replace(tzinfo=UTC)
#         .date()
#       )

#       if month_start_date <= record_date <= target_date_obj:
#         month_to_date_total += float(record.get(target_column))

#     return {
#       "date": target_date,
#       "kpi": kpi,
#       "billing_type": billing_type,
#       "month_to_date_total": f"{round(month_to_date_total):,}",
#     }

#   except (KeyError, ValueError, TypeError, AttributeError) as e:
#     return {"error": f"get_kpi_month_to_date_total failed: {e}"}


# # Test cases for the function, for each KPI and date combination, including different billing types.
if __name__ == "__main__":
  # Test case for total customers per day
  kpi = "Voice Users"
  date = "06-AUG-26"
  for billing_type in ["prepaid", "hybrid", "total"]:
    result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
    print(json.dumps(result, indent=2))
