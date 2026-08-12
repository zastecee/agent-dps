import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent

from .tools import (
  get_customers_month_on_month_metrics,
  get_customers_year_on_year_metrics,
  get_kpi_month_to_date_total,
  get_total_customers_per_day,
)

load_dotenv()

root_agent = LlmAgent(
  model=f"bedrock/converse/{os.getenv('BEDROCK_MODEL_ID')}",
  name="first_agent",
  description="A Vodacom customer analytics assistant.",
  instruction="""
        You are a helpful assistant specializing in Vodacom customer analytics.
        Your role is to provide accurate information about our prepaid segments.
        When asked about topics outside your knowledge, clearly state that you don't have that information.
        Maintain a professional and helpful tone at all times.
    """,
  tools=[
    get_customers_month_on_month_metrics,
    get_customers_year_on_year_metrics,
    get_kpi_month_to_date_total,
    get_total_customers_per_day,
  ],
)
