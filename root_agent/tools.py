import csv

records = []

with open(
    "FINAL_V_DRA_DAILY_CUSTOMERS_SELECT.csv",
    mode="r",
    encoding="iso-8859-1",
    newline=""
) as file:
    for row in csv.DictReader(file):
        records.append(row)

# ---

def get_total_custumers_per_day(kpi: str, date: str) -> dict:
    try:
        total = 0
        for item in records:
            if item['EVENT_DESCRIPTION'] == kpi and  item['DC_DATE'] == date:
                total =  float(item['DC_TOTAL']) + total

        return {
            "date":             date,
            "kpi":              kpi,
            "total_customers": total,
        }
    except Exception as e:
        return {"error": f"get_total_custumers_per_day failed: {e}"}

# print(get_total_custumers_per_day('30 Days Data Users SUBID', "06-AUG-26"))
# print(get_total_custumers_per_day('Voice Users', "05-AUG-26"))


from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_kpi_month_to_date_total(kpi_name: str, target_date: str) -> dict:
    try:
        target_date_obj = datetime.strptime(target_date, "%d-%b-%y").date()
        month_start_date = target_date_obj.replace(day=1)
        month_to_date_total = 0.0

        for record in records:
            if record["EVENT_DESCRIPTION"] != kpi_name:
                continue

            record_date = datetime.strptime(record["DC_DATE"], "%d-%b-%y").date()

            if month_start_date <= record_date <= target_date_obj:
                month_to_date_total += float(record["DC_TOTAL"])
        return {
            "date": target_date,
            "kpi": kpi_name,
            "total": month_to_date_total
        }
    except Exception as e:
        return {
            "error": f"get_kpi_month_to_date_total failed: {e}"
        }


def get_previous_month_same_day(target_date: str) -> str:
    target_date_obj = datetime.strptime(target_date, "%d-%b-%y").date()
    return (target_date_obj - relativedelta(months=1)).strftime("%d-%b-%y")

def get_previous_year_same_day(target_date: str) -> str:
    target_date_obj = datetime.strptime(target_date, "%d-%b-%y").date()
    return (target_date_obj - relativedelta(years=1)).strftime("%d-%b-%y")


def get_customers_month_on_month_metrics(kpi_name: str, target_date: str) -> dict:
    try:
        previous_month_date = get_previous_month_same_day(target_date)
        current_month_total = get_kpi_month_to_date_total(kpi_name, target_date)["total"]
        previous_month_total = get_kpi_month_to_date_total(kpi_name, previous_month_date)["total"]

        difference = current_month_total - previous_month_total
        percentage_change = (
            (difference / previous_month_total) * 100
            if previous_month_total != 0
            else None
        )

        return {
            "date": target_date,
            "kpi": kpi_name,
            "current_month_total": round(current_month_total),
            "previous_month_total": round(previous_month_total),
            "difference": round(difference),
            "percentage_change": (
                round(percentage_change, 1)
                if percentage_change is not None
                else None
            )
        }
    except Exception as e:
        return {
            "error": f"calculate_kpis failed: {e}"
        }

# print(get_customers_month_on_month_metrics(kpi_name="Voice Traffic - Free", target_date="06-AUG-26"))
# print(get_customers_month_on_month_metrics(kpi_name="Voice Traffic - OOB", target_date="06-AUG-26"))



# ---


# print(get_kpi_month_to_date_total('Voice Traffic - Free',"06-AUG-25"))

def get_kpi_year_on_year_metrics(kpi_name: str, target_date: str) -> dict:
    try:
        previous_year_date = get_previous_year_same_day(target_date)

        current_year_total = get_kpi_month_to_date_total(kpi_name, target_date)["total"]
        previous_year_total = get_kpi_month_to_date_total(kpi_name, previous_year_date)["total"]
        absolute_change = (current_year_total - previous_year_total)
        percentage_change = (
            (absolute_change / previous_year_total) * 100
            if previous_year_total != 0
            else None
        )

        return {
            "kpi": kpi_name,
            "current_period_date": target_date,
            "previous_period_date": previous_year_date,
            "current_mtd_total": round(current_year_total),
            "previous_year_mtd_total": round(previous_year_total),
            "absolute_change": round(absolute_change),
            "percentage_change": (
                round(percentage_change, 1)
                if percentage_change is not None
                else None
            )
        }

    except Exception as e:
        return {
            "error": f"get_kpi_year_on_year_metrics failed: {e}"
        }


# print(get_kpi_year_on_year_metrics('Voice Traffic - Free',"06-AUG-26"))






