import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

load_dotenv()


# 

import json
from collections import defaultdict

with open("FINAL_V_DRA_DAILY_CUSTOMERS_SELECT.json", "r") as file:
    data = json.load(file)

total_revenue_users = []

for item in data:
    if item["EVENT_DESCRIPTION"] == "Voice Users" and item["DC_DATE"] == "2026-08-02 00:00:00.0":
        total_revenue_users.append(item)

# print(len(total_revenue_users))

total = 0
for active_gsm in total_revenue_users:
    total = float(active_gsm["DC_PREPAD"]) + total

print(total)



# grouped = defaultdict(list)

# # Chave composta: (EVENT_DESCRIPTION, DC_DATE)
# for item in customers_traffic:
#     chave_composta = (item["EVENT_DESCRIPTION"], item["DC_DATE"])
#     grouped[chave_composta].append(item)

# for (EVENT_DESCRIPTION, DC_DATE), itens in grouped.items():
#     total_prepad = sum(float(item["DC_PREPAD"]) for item in itens)
#     print(f"{DC_DATE} - {EVENT_DESCRIPTION} | DC_PREPAD: {total_prepad:.2f}")


# -----------------------------------------------------------------------------------------------------------------------------

# grouped = defaultdict(list)

# # Agrupa os itens percorrendo a lista
# for item in customers_traffic:
#     EVENT_DESCRIPTION = item["EVENT_DESCRIPTION"]
#     grouped[EVENT_DESCRIPTION].append(item)


# # Exibindo o resultado formatado
# # print(json.dumps(grouped, indent=4, ensure_ascii=False))
# print(json.dumps(customers_traffic, indent=4, ensure_ascii=False))

# for EVENT_DESCRIPTION, itens in grouped.items():
#     total_prepad = sum(float(item["DC_PREPAD"]) for item in itens)
#     total_hybrid = sum(float(item["DC_HYBRID"]) if item["DC_HYBRID"] is not None else 0.0 for item in itens)

#     print(f"{itens[0]["DC_DATE"]} - {EVENT_DESCRIPTION} | DC_PREPAD: {total_prepad:.2f}")
#     print(f"{itens[0]["DC_DATE"]} - {EVENT_DESCRIPTION} | DC_HYBRID: {total_hybrid:.2f}")




# -----------------------------------------------------------------------------------------------------------------------------



# # Chave composta: (EVENT_DESCRIPTION, DC_DATE, DC_PROVINCE, DC_SEGMENT)
# for item in customers_traffic:
#     chave_composta = (item["EVENT_DESCRIPTION"], item["DC_DATE"], item["DC_PROVINCE"], item["DC_SEGMENT"])
#     grouped[chave_composta].append(item)



# from collections import defaultdict
# import json

# # Seu array de objetos
# produtos = [
#     {"nome": "Teclado A", "categoria": "Eletrônicos", "marca": "Logitech", "preco": 150},
#     {"nome": "Mouse A", "categoria": "Eletrônicos", "marca": "Logitech", "preco": 80},
#     {"nome": "Teclado B", "categoria": "Eletrônicos", "marca": "Razer", "preco": 300},
#     {"nome": "Camiseta X", "categoria": "Vestuário", "marca": "Nike", "preco": 120},
#     {"nome": "Calça Y", "categoria": "Vestuário", "marca": "Nike", "preco": 200}
# ]

# # Inicializa o defaultdict passando a tupla (categoria, marca) como chave
# produtos_agrupados = defaultdict(list)

# for item in produtos:
#     # Cria a chave composta usando uma tupla
#     chave_composta = (item["categoria"], item["marca"])
#     produtos_agrupados[chave_composta].append(item)

# # Exibindo os grupos e calculando a soma com o tratamento para None/vazio
# for (categoria, marca), itens in produtos_agrupados.items():
#     total_grupo = sum(float(item["preco"]) if item["preco"] is not None else 0.0 for item in itens)
    
#     print(f"Categoria: {categoria} | Marca: {marca} | Itens: {len(itens)} | Total: R$ {total_grupo:.2f}")




















# Keys
# print("Keys:")
# for key in grouped.keys():
#     print(key)


# root_agent = LlmAgent(
#     model=f"bedrock/converse/{os.getenv('BEDROCK_MODEL_ID')}",
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
# )
