import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent

load_dotenv()

recharge_agent = LlmAgent(
  name="recharge_agent",
  model=f"bedrock/converse/{os.getenv('BEDROCK_MODEL_ID')}",
  description=(
    "Agente especializado no processamento e análise de recargas (Recharge), "
    "volume de recargas diárias, canais de distribuição e comportamento de recarga dos clientes."
  ),
  instruction="""
    Você é o especialista em recargas (Recharge) da Vodacom.
    Processe dados e consultas sobre valores e volumes de recargas realizadas pelos clientes.
    """,
  tools=[],
)
