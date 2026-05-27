import requests
import pandas as pd
import streamlit as st

# Configurações visuais da página web
st.set_page_config(page_title="Tabela do Brasileirão", page_icon="🏆", layout="centered")

# --- CONFIGURAÇÃO DA API ---
API_KEY = "732065ca7cc5407dbbc5d376eaac0ef3" 
BASE_URL = "https://api.football-data.org/v4"
COMPETITION_CODE = "BSA" 
ENDPOINT = f"/competitions/{COMPETITION_CODE}/standings"

headers = {'X-Auth-Token': API_KEY}

def obter_tabela_brasileirao():
    url = BASE_URL + ENDPOINT
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro ao acessar a API: {e}")
        return None

def formatar_tabela(dados):
    if not dados or 'standings' not in dados:
        return None
    
    tabela_standings = dados['standings'][0]['table']
    tabela = []
    for linha in tabela_standings:
        clube = {
            'Pos': linha.get('position'),
            'Time': linha.get('team', {}).get('name'),
            'P': linha.get('points'),
            'J': linha.get('playedGames'),
            'V': linha.get('won'),
            'E': linha.get('draw'),
            'D': linha.get('lost'),
            'GP': linha.get('goalsFor'),
            'GC': linha.get('goalsAgainst'),
            'SG': linha.get('goalDifference')
        }
        tabela.append(clube)

    df = pd.DataFrame(tabela)
    return df[['Pos', 'Time', 'P', 'J', 'V', 'E', 'D', 'GP', 'GC', 'SG']]

# --- CORPO PRINCIPAL DO SITE (O que aparece na tela) ---
st.title("🏆 Tabela do Campeonato Brasileiro - Série A")
st.write("Dados atualizados em tempo real via API.")

dados_json = obter_tabela_brasileirao()

if dados_json:
    tabela_df = formatar_tabela(dados_json)
    
    if tabela_df is not None:
        # Mostra a tabela de forma linda e interativa na página
        st.dataframe(tabela_df, use_container_width=True, hide_index=True)
    else:
        st.error("Não foi possível formatar os dados da tabela.")
else:
    st.error("Falha ao obter dados da API. Verifique sua chave ou permissões do plano.")
