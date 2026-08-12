import csv
import json
from datetime import UTC, datetime
from typing import Literal

from dateutil.relativedelta import relativedelta

# Load the recharge dataset from a CSV file
with open("recharge_dataset.csv", mode="r", encoding="iso-8859-1", newline="") as file:
  records = list(csv.DictReader(file))

BillingType = Literal["prepaid", "hybrid", "total"]
RechargeGroup = Literal["mpesa", "other", "all"]

MPESA_KPI_LIST = [
  "MPesa Bundles",
  "So-Prati",
  "My Vodacom",
  "Super Agent",
  "Baza Baza",
  "M-Pesa Recharge",
]

OTHER_KPI_LIST = [
  "Electronic - Others",
  "Electronic - Bank",
  "Physical",
]

RECHARGE_KPI_LIST = MPESA_KPI_LIST + OTHER_KPI_LIST


RECHARGE_BILLING_MAP = {
  "prepaid": "REV_PREPAID",
  "hybrid": "REV_HYBRID",
  "total": "BPM_REVENUE",
}

RECHARGE_GROUP_MAP = {
  "mpesa": MPESA_KPI_LIST,
  "other": OTHER_KPI_LIST,
  "all": RECHARGE_KPI_LIST,
}


# Function to get total recharge per day for a specific KPI and date
def get_total_recharge_per_day(
  kpi: str,
  date: str,
  billing_type: BillingType = "prepaid",
) -> dict:
  try:
    target_column = RECHARGE_BILLING_MAP.get(billing_type.lower(), billing_type)

    total = sum(
      float(item[target_column])
      for item in records
      if item.get("CHANNEL") == kpi and item.get("BPM_START_DATE") == date
    )

    return {
      "date": date,
      "kpi": kpi,
      "billing_type": billing_type,
      "total_recharge": f"{round(total):,}",
    }
  except (KeyError, ValueError) as e:
    return {"error": f"get_total_recharge_per_day failed due to invalid data: {e}"}


# Function to get total M-Pesa recharge per day for a specific date
def get_total_mpesa_recharge_per_day(
  date: str,
  billing_type: BillingType = "prepaid",
) -> dict:
  try:
    target_column = RECHARGE_BILLING_MAP.get(billing_type.lower(), billing_type)

    total_mpesa_recharge = sum(
      float(item[target_column])
      for item in records
      if item.get("CHANNEL") in MPESA_KPI_LIST and item.get("BPM_START_DATE") == date
    )

    return {
      "date": date,
      "billing_type": billing_type,
      "total_mpesa_recharge": f"{round(total_mpesa_recharge):,}",
    }
  except (KeyError, ValueError) as e:
    return {
      "error": f"get_total_mpesa_recharge_per_day failed due to invalid data: {e}"
    }


# Function to get total other recharge per day for a specific date
def get_total_other_recharge_per_day(
  date: str,
  billing_type: BillingType = "prepaid",
) -> dict:
  try:
    target_column = RECHARGE_BILLING_MAP.get(billing_type.lower(), billing_type)

    total_other_recharge = sum(
      float(item[target_column])
      for item in records
      if item.get("CHANNEL") in OTHER_KPI_LIST and item.get("BPM_START_DATE") == date
    )

    return {
      "date": date,
      "billing_type": billing_type,
      "total_other_recharge": f"{round(total_other_recharge):,}",
    }
  except (KeyError, ValueError) as e:
    return {
      "error": f"get_total_other_recharge_per_day failed due to invalid data: {e}"
    }


# Function to get total recharge per day for all KPIs and a specific date
def get_total_recharge_per_day_all_kpis(
  date: str,
  billing_type: BillingType = "prepaid",
) -> dict:
  try:
    target_column = RECHARGE_BILLING_MAP.get(billing_type.lower(), billing_type)

    total_recharge_all_kpis = sum(
      float(item[target_column])
      for item in records
      if item.get("BPM_START_DATE") == date and item.get("CHANNEL") in RECHARGE_KPI_LIST
    )

    return {
      "date": date,
      "billing_type": billing_type,
      "total_recharge_all_kpis": f"{round(total_recharge_all_kpis):,}",
    }
  except (KeyError, ValueError) as e:
    return {
      "error": f"get_total_recharge_per_day_all_kpis failed due to invalid data: {e}"
    }


# Function to get the total revenue for a specific KPI and date range
def get_kpi_month_to_date_total(
  kpi: str,
  target_date: str,
  billing_type: BillingType = "prepaid",
) -> dict:
  try:
    target_column = RECHARGE_BILLING_MAP.get(billing_type.lower(), billing_type)

    parsed_dt = datetime.strptime(target_date, "%d-%b-%y").replace(tzinfo=UTC)
    target_date_obj = parsed_dt.date()
    month_start_date = target_date_obj.replace(day=1)
    month_to_date_total = 0.0

    for record in records:
      if record["CHANNEL"] != kpi:
        continue

      record_date = (
        datetime.strptime(record["BPM_START_DATE"], "%d-%b-%y")
        .replace(tzinfo=UTC)
        .date()
      )

      if month_start_date <= record_date <= target_date_obj:
        month_to_date_total += float(record.get(target_column))

    return {
      "date": target_date,
      "kpi": kpi,
      "billing_type": billing_type,
      "month_to_date_total": f"{round(month_to_date_total):,}",
    }

  except (KeyError, ValueError, TypeError, AttributeError) as e:
    return {"error": f"get_kpi_month_to_date_total failed: {e}"}


# Function to get the total recharge for a specific group and date range
def get_grouped_recharge_month_to_date_total(
  target_date: str,
  group: RechargeGroup = "mpesa",
  billing_type: BillingType = "prepaid",
) -> dict:
  try:
    target_column = RECHARGE_BILLING_MAP.get(billing_type.lower(), billing_type)
    target_kpis = RECHARGE_GROUP_MAP.get(group.lower(), MPESA_KPI_LIST)

    parsed_dt = datetime.strptime(target_date, "%d-%b-%y").replace(tzinfo=UTC)
    target_date_obj = parsed_dt.date()
    month_start_date = target_date_obj.replace(day=1)
    month_to_date_total = 0.0

    for record in records:
      if record["CHANNEL"] not in target_kpis:
        continue

      record_date = (
        datetime.strptime(record["BPM_START_DATE"], "%d-%b-%y")
        .replace(tzinfo=UTC)
        .date()
      )

      if month_start_date <= record_date <= target_date_obj:
        month_to_date_total += float(record.get(target_column))

    return {
      "date": target_date,
      "group": group,
      "billing_type": billing_type,
      "month_to_date_total": f"{round(month_to_date_total):,}",
    }
  except (KeyError, ValueError, TypeError, AttributeError) as e:
    return {"error": f"get_grouped_recharge_month_to_date_total failed: {e}"}


# Function to get month-on-month metrics for a specific group and date
def get_grouped_recharge_month_on_month_metrics(
  target_date: str,
  group: RechargeGroup,
  billing_type: BillingType = "prepaid",
) -> dict:
  try:
    previous_month_date = get_previous_month_same_day(target_date)

    current_data = get_grouped_recharge_month_to_date_total(
      target_date, group, billing_type
    )
    previous_data = get_grouped_recharge_month_to_date_total(
      previous_month_date, group, billing_type
    )

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
      "group": group,
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
      "error": (
        f"get_grouped_recharge_month_on_month_metrics failed due to invalid data: {e}"
      )
    }


# Function to get year-on-year metrics for a specific group and date
def get_grouped_recharge_year_on_year_metrics(
  target_date: str,
  group: RechargeGroup,
  billing_type: BillingType = "prepaid",
) -> dict:
  try:
    previous_year_date = get_previous_year_same_day(target_date)

    current_data = get_grouped_recharge_month_to_date_total(
      target_date, group, billing_type
    )
    previous_data = get_grouped_recharge_month_to_date_total(
      previous_year_date, group, billing_type
    )

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
      "group": group,
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
      "error": (
        f"get_grouped_recharge_year_on_year_metrics failed due to invalid data: {e}"
      )
    }


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
def get_recharge_month_on_month_metrics(
  kpi: str,
  target_date: str,
  billing_type: BillingType = "prepaid",
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
      "error": (f"get_recharge_month_on_month_metrics failed due to invalid data: {e}")
    }


# Function to get year-on-year metrics for a specific KPI and date
def get_recharge_year_on_year_metrics(
  kpi: str,
  target_date: str,
  billing_type: BillingType = "prepaid",
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
      "error": (f"get_recharge_year_on_year_metrics failed due to invalid data: {e}")
    }


# test cases for the function, for each KPI and date combination, including different billing types.
if __name__ == "__main__":
  # # Test case for total recharge per day
  # kpi = "MPesa Bundles"  # MPesa Bundles
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_recharge_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "So-Prati"  # So-Prati
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_recharge_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "My Vodacom"  # My Vodacom
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_recharge_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Super Agent"  # Super Agent
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_recharge_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Baza Baza"  # Baza Baza
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_recharge_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "M-Pesa Recharge"  # M-Pesa Recharge
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_recharge_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Others"  # Others ------ Soma dos outros ---------
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_recharge_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Electronic - Others"  # Electronic - Others
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_recharge_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Electronic - Bank"  # Electronic - Bank
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_recharge_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Physical"  # Physical
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_recharge_per_day(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Physical"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Physical"
  # date = "06-JUL-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_kpi_month_to_date_total(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Physical"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_recharge_month_on_month_metrics(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # kpi = "Physical"
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_recharge_year_on_year_metrics(kpi, date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # # Test case for total M-Pesa recharge per day
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_mpesa_recharge_per_day(date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # # Test case for total other recharge per day
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_other_recharge_per_day(date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # # Test case for total recharge per day for all KPIs
  # date = "06-AUG-26"
  # for billing_type in ["prepaid", "hybrid", "total"]:
  #   result = get_total_recharge_per_day_all_kpis(date, billing_type=billing_type)
  #   print(json.dumps(result, indent=2))

  # # Test case for grouped recharge month-to-date total
  # date = "06-AUG-26"
  # for group in ["mpesa", "other", "all"]:
  #   for billing_type in ["prepaid", "hybrid", "total"]:
  #     result = get_grouped_recharge_month_to_date_total(
  #       date, group=group, billing_type=billing_type
  #     )
  #     print(json.dumps(result, indent=2))

  # # Test case for grouped recharge month-on-month metrics
  # date = "06-AUG-26"
  # for group in ["mpesa", "other", "all"]:
  #   for billing_type in ["prepaid", "hybrid", "total"]:
  #     result = get_grouped_recharge_month_on_month_metrics(
  #       date, group=group, billing_type=billing_type
  #     )
  #     print(json.dumps(result, indent=2))

  # Test case for grouped recharge year-on-year metrics
  date = "06-AUG-26"
  for group in ["mpesa", "other", "all"]:
    for billing_type in ["prepaid", "hybrid", "total"]:
      result = get_grouped_recharge_year_on_year_metrics(
        date, group=group, billing_type=billing_type
      )
      print(json.dumps(result, indent=2))
