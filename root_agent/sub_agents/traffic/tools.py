import csv
import json
from datetime import UTC, datetime
from typing import Literal

from dateutil.relativedelta import relativedelta

# Load the traffic dataset from a CSV file
with open("traffic_dataset.csv", mode="r", encoding="iso-8859-1", newline="") as file:
  records = list(csv.DictReader(file))

TrafficMetric = Literal["DC_TOTAL", "DC_PREPAD", "DC_HYBRID"]


# Function to get total traffic per day for a specific KPI and date
def get_total_traffic_per_day(
  kpi: str, date: str, billing_type: TrafficMetric = "DC_TOTAL"
) -> dict:
  try:
    total = sum(
      float(item[billing_type])
      for item in records
      if item.get("EVENT_DESCRIPTION") == kpi and item.get("DC_DATE") == date
    )

    return {
      "date": date,
      "kpi": kpi,
      "billing_type": billing_type,
      "total_traffic": f"{round(total):,}",
    }
  except (KeyError, ValueError) as e:
    return {"error": f"get_total_traffic_per_day failed due to invalid data: {e}"}


# Function to get the total traffic for a specific KPI and date range
def get_kpi_month_to_date_total(
  kpi: str, target_date: str, billing_type: TrafficMetric = "DC_TOTAL"
) -> dict:
  try:
    parsed_dt = datetime.strptime(target_date, "%d-%b-%y").replace(tzinfo=UTC)
    target_date_obj = parsed_dt.date()
    month_start_date = target_date_obj.replace(day=1)
    month_to_date_total = 0.0

    for record in records:
      if record["EVENT_DESCRIPTION"] != kpi:
        continue

      record_date = (
        datetime.strptime(record["DC_DATE"], "%d-%b-%y").replace(tzinfo=UTC).date()
      )

      if month_start_date <= record_date <= target_date_obj:
        month_to_date_total += float(record.get(billing_type))

    return {
      "date": target_date,
      "kpi": kpi,
      "billing_type": billing_type,
      "month_to_date_total": f"{round(month_to_date_total):,}",
    }

  except (KeyError, ValueError) as e:
    return {"error": f"get_kpi_month_to_date_total failed due to invalid data: {e}"}


# Function to get the same day of the previous month for a given date
def get_previous_month_same_day(target_date: str) -> str:
  try:
    target_date_obj = (
      datetime.strptime(target_date, "%d-%b-%y").replace(tzinfo=UTC).date()
    )
    prev_month_date = target_date_obj - relativedelta(months=1)
    return prev_month_date.strftime("%d-%b-%y").upper()
  except ValueError as e:
    raise ValueError(
      f"Data inválida '{target_date}'. O formato esperado é 'DD-MMM-YY' (ex: '22-OCT-25')."
    ) from e


# Function to get the same day of the previous year for a given date
def get_previous_year_same_day(target_date: str) -> str:
  try:
    target_date_obj = (
      datetime.strptime(target_date, "%d-%b-%y").replace(tzinfo=UTC).date()
    )
    prev_year_date = target_date_obj - relativedelta(years=1)
    return prev_year_date.strftime("%d-%b-%y").upper()
  except ValueError as e:
    raise ValueError(
      f"Data inválida '{target_date}'. O formato esperado é 'DD-MMM-YY' (ex: '22-OCT-25')."
    ) from e


# Function to get month-on-month metrics for a specific KPI and date
def get_traffic_month_on_month_metrics(
  kpi: str, target_date: str, billing_type: TrafficMetric = "DC_TOTAL"
) -> dict:
  try:
    previous_month_date = get_previous_month_same_day(target_date)

    current_data = get_kpi_month_to_date_total(kpi, target_date, billing_type)
    previous_data = get_kpi_month_to_date_total(kpi, previous_month_date, billing_type)

    current_month_total = float(
      current_data.get("month_to_date_total", 0).replace(",", "")
    )
    previous_month_total = float(
      previous_data.get("month_to_date_total", 0).replace(",", "")
    )

    difference = current_month_total - previous_month_total

    percentage_change = (
      (difference / previous_month_total) * 100 if previous_month_total != 0 else None
    )

    return {
      "target_date": target_date,
      "previous_month_date": previous_month_date,
      "kpi": kpi,
      "billing_type": billing_type,
      "current_month_total": f"{round(current_month_total):,}",
      "previous_month_total": f"{round(previous_month_total):,}",
      "difference": f"{round(difference):,}",
      "percentage_change": (
        round(percentage_change, 1) if percentage_change is not None else None
      ),
    }
  except (KeyError, ValueError, TypeError) as e:
    return {
      "error": (f"get_traffic_month_on_month_metrics failed due to invalid data: {e}")
    }


# Function to get year-on-year metrics for a specific KPI and date
def get_traffic_year_on_year_metrics(
  kpi: str, target_date: str, billing_type: TrafficMetric = "DC_TOTAL"
) -> dict:
  try:
    previous_year_date = get_previous_year_same_day(target_date)
    current_data = get_kpi_month_to_date_total(kpi, target_date, billing_type)
    previous_data = get_kpi_month_to_date_total(kpi, previous_year_date, billing_type)

    current_year_total = float(
      current_data.get("month_to_date_total", 0).replace(",", "")
    )
    previous_year_total = float(
      previous_data.get("month_to_date_total", 0).replace(",", "")
    )

    difference = current_year_total - previous_year_total
    percentage_change = (
      (difference / previous_year_total) * 100 if previous_year_total != 0 else None
    )

    return {
      "target_date": target_date,
      "previous_year_date": previous_year_date,
      "kpi": kpi,
      "billing_type": billing_type,
      "current_year_total": f"{round(current_year_total):,}",
      "previous_year_total": f"{round(previous_year_total):,}",
      "difference": f"{round(difference):,}",
      "percentage_change": (
        round(percentage_change, 1) if percentage_change is not None else None
      ),
    }
  except (KeyError, ValueError, TypeError) as e:
    return {
      "error": (f"get_traffic_year_on_year_metrics failed due to invalid data: {e}")
    }


# Test cases for the function, for each KPI and date combination, including different billing types.
if __name__ == "__main__":
  # Test case for total traffic per day
  kpi = "Voice Traffic - Billed"
  date = "06-AUG-26"
  for billing_type in ["DC_TOTAL", "DC_PREPAD", "DC_HYBRID"]:
    result = get_total_traffic_per_day(kpi, date, billing_type=billing_type)
    print(json.dumps(result, indent=2))

  # Test case for month-to-date total traffic
  kpi = "Voice Traffic - Billed"
  target_date = "06-AUG-26"
  for billing_type in ["DC_TOTAL", "DC_PREPAD", "DC_HYBRID"]:
    result = get_kpi_month_to_date_total(kpi, target_date, billing_type=billing_type)
    print(json.dumps(result, indent=2))

  # Test case for month-on-month metrics
  kpi = "Voice Traffic - Billed"
  target_date = "06-AUG-26"
  for billing_type in ["DC_TOTAL", "DC_PREPAD", "DC_HYBRID"]:
    result = get_traffic_month_on_month_metrics(
      kpi, target_date, billing_type=billing_type
    )
    print(json.dumps(result, indent=2))

  # Test case for year-on-year metrics
  kpi = "Outflows"
  target_date = "06-AUG-26"
  for billing_type in ["DC_TOTAL", "DC_PREPAD", "DC_HYBRID"]:
    result = get_traffic_year_on_year_metrics(
      kpi, target_date, billing_type=billing_type
    )
    print(json.dumps(result, indent=2))
