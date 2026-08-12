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


MONTH_TO_DATE_KPIS_MAP = {
  # Case 1: usa formula 1
  "Active GSM": "MTD Active GSM",
  "Voice Users": "MTD Voice Users",
  "Data Users": "MTD Data Users",
  "Sms Users": "MTD Sms Users",
  "Active Mpesa base": "Active Mpesa base - 30 Days",
  "Total Revenue Users": "MTD Total Revenue Users",
  "Voice Revenue Users": "MTD Voice Revenue Users",
  "Data Revenue Users": "MTD Data Revenue Users",
  "Sms Revenue Users": "MTD Sms Revenue Users",
  "Total Buyers": "MTD Total Buyers",
  "Voice Buyers": "MTD Voice Buyers",
  "Data Buyers": "MTD Data Buyers",
  "Sms Buyers": "MTD Sms Buyers",
  "30 Days Active SUBID": "30 Days Active SUBID",
  "30 Days Active GSM SUBID": "30 Days Active GSM SUBID",
  "30 Days Voice Users SUBID": "30 Days Voice Users SUBID",
  "30 Days Data Users SUBID": "30 Days Data Users SUBID",
  "30 Days Sms Users SUBID": "30 Days Sms Users SUBID",
  "30 Days Total Revenue Users": "30 Days Total Revenue Users",
  "30 Days Voice Revenue Users": "30 Days Voice Revenue Users",
  "30 Days Data Revenue Users": "30 Days Data Revenue Users",
  "30 Days Sms Revenue Users": "30 Days Sms Revenue Users",
  "30 Days Total Buyers": "30 Days Total Buyers",
  "30 Days Voice Buyers": "30 Days Voice Buyers",
  "30 Days Data Buyers": "30 Days Data Buyers",
  "30 Days Sms Buyers": "30 Days Sms Buyers",
  "Gross Adds Mpesa": "M Gross Adds Mpesa",
  # Case 2: usa formula 2
  "Gross Adds - GSM": "Gross Adds - GSM",
}


# total = 0
# DESCRIPTION_SET = set(item["EVENT_DESCRIPTION"] for item in records)
# for description in DESCRIPTION_SET:
#   if description == "30 Days Total Buyers":
#     print(description)


# for item in records:
#   if item["EVENT_DESCRIPTION"] == "MTD Active GSM" and item["DC_DATE"] == "06-AUG-26":
#     total = float(item["DC_PREPAD"]) + total


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


# for key, value in MONTH_TO_DATE_KPIS_MAP.items():
#   kpi = key
#   date = "06-AUG-26"
#   for billing_type in ["prepaid", "hybrid", "total"]:
#     result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
#     print(json.dumps(result, indent=2))


# Function to get the total customers for a specific KPI and date range
def get_kpi_month_to_date_total(
  kpi: str,
  target_date: str,
  billing_type: BillingType = "prepaid",
) -> dict:
  try:
    # Case 1: Formula 2
    target_column = CUSTOMER_BILLING_MAP.get(billing_type.lower(), billing_type)
    month_to_date_total = 0.0
    target_kpi = MONTH_TO_DATE_KPIS_MAP.get(kpi, kpi)

    for item in records:
      if item["EVENT_DESCRIPTION"] == target_kpi and item["DC_DATE"] == target_date:
        month_to_date_total = float(item[target_column]) + month_to_date_total

    # # Case 2: Formula 2
    # target_column = CUSTOMER_BILLING_MAP.get(billing_type.lower(), billing_type)
    # parsed_dt = datetime.strptime(target_date, "%d-%b-%y").replace(tzinfo=UTC)
    # target_date_obj = parsed_dt.date()
    # month_start_date = target_date_obj.replace(day=1)
    # month_to_date_total = 0.0

    # for record in records:
    #   if record["EVENT_DESCRIPTION"] != kpi:
    #     continue

    #   record_date = (
    #     datetime.strptime(record["DC_DATE"], "%d-%b-%y").replace(tzinfo=UTC).date()
    #   )

    #   if month_start_date <= record_date <= target_date_obj:
    #     month_to_date_total += float(record.get(target_column))

    return {
      "date": target_date,
      "kpi": kpi,
      "billing_type": billing_type,
      "month_to_date_total": f"{round(month_to_date_total):,}",
    }

  except (KeyError, ValueError, TypeError, AttributeError) as e:
    return {"error": f"get_kpi_month_to_date_total failed: {e}"}


# # Test cases for the function, for each KPI and date combination, including different billing types.
if __name__ == "__main__":
  # # Test case for total customers per
  # kpi = "Active GSM"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Voice Users"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Data Users"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Sms Users"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Active Mpesa base"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Total Revenue Users"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Voice Revenue Users"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Data Revenue Users"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Sms Revenue Users"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Total Buyers"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Voice Buyers"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Data Buyers"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Sms Buyers"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Active SUBID"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Active GSM SUBID"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Voice Users SUBID"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Data Users SUBID"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Sms Users SUBID"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Total Revenue Users"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Voice Revenue Users"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Data Revenue Users"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Sms Revenue Users"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Total Buyers"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Voice Buyers"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Data Buyers"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Sms Buyers"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Gross Adds - GSM"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Gross Adds Mpesa"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_customers_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # Test case for month-to-date total customers
  # kpi = "Active GSM"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Voice Users"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Data Users"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Sms Users"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Active Mpesa base"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Total Revenue Users"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Voice Revenue Users"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Data Revenue Users"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Sms Revenue Users"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Total Buyers"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Voice Buyers"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Data Buyers"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Sms Buyers"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Active SUBID"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Active GSM SUBID"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Voice Users SUBID"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Data Users SUBID"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Sms Users SUBID"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Total Revenue Users"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Voice Revenue Users"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Data Revenue Users"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Sms Revenue Users"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Total Buyers"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Voice Buyers"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Data Buyers"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "30 Days Sms Buyers"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Gross Adds - GSM"
  # target_date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  kpi = "Gross Adds Mpesa"
  target_date = "06-AUG-26"
  for billing_type in ["prepaid", "hybrid", "total"]:
    result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
    print(json.dumps(result, indent=2))
