import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent

load_dotenv()

customers_agent = LlmAgent(
  name="customers_agent",
  model=f"bedrock/converse/{os.getenv('BEDROCK_MODEL_ID')}",
  description=(
    "Agente especializado na análise da base de clientes (Customers), "
    "incluindo contagem de subs ativos (1D, 30D, 90D), adições brutas (Gross Adds), "
    "churn e comportamento da base de clientes CBU Pré-pago."
  ),
  instruction="""
    Você é o especialista na base de clientes (Customers) da Vodacom.
    Processe métricas relativas a subscritores, adições de base, desativações e churn.
    """,
  tools=[],
)
