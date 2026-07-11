import requests
import json
import os
from datetime import datetime, timedelta

# Tenta obter a chave do ambiente; se não existir, exibe erro claro
API_KEY = os.environ.get("API_FOOTBALL")
if not API_KEY:
    print("❌ ERRO: A variável de ambiente 'API_FOOTBALL' não foi definida.")
    print("Verifique se o segredo foi criado corretamente no repositório e se o workflow está configurado para injetá-lo.")
    exit(1)

COMPETICAO_ID = 2000  # Brasileirão Série A
DIAS_A_FRENTE = 10

headers = {"X-Auth-Token": API_KEY}
data_fim = (datetime.now() + timedelta(days=DIAS_A_FRENTE)).strftime("%Y-%m-%d")
data_inicio = datetime.now().strftime("%Y-%m-%d")

url = f"https://api.football-data.org/v4/competitions/{COMPETICAO_ID}/matches?dateFrom={data_inicio}&dateTo={data_fim}&status=SCHEDULED"

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    jogos = response.json()["matches"]

    palpites = []
    for jogo in jogos:
        casa = jogo["homeTeam"]["name"]
        fora = jogo["awayTeam"]["name"]
        data = jogo["utcDate"]

        # Algoritmo simples de palpite (exemplo)
        if "Flamengo" in casa or "Palmeiras" in casa:
            previsao = casa
        elif "Flamengo" in fora or "Palmeiras" in fora:
            previsao = fora
        else:
            previsao = "Empate" if hash(casa) % 2 == 0 else casa

        palpites.append({
            "casa": casa,
            "fora": fora,
            "data": data,
            "previsao": previsao
        })

    with open("palpites.json", "w", encoding="utf-8") as f:
        json.dump(palpites, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON gerado com {len(palpites)} jogos.")

except Exception as e:
    print(f"❌ Erro ao acessar a API: {e}")
    # Gera um JSON vazio para o site não quebrar
    with open("palpites.json", "w", encoding="utf-8") as f:
        json.dump([], f)
