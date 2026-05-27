import requests
import pandas as pd
import json

# --- CONFIGURAÇÃO DA API ---
# ATENÇÃO: Use a sua chave de API real aqui. 
# Ela deve ser incluída no cabeçalho 'X-Auth-Token'.
API_KEY = "732065ca7cc5407dbbc5d376eaac0ef3" 
BASE_URL = "https://api.football-data.org/v4"
COMPETITION_CODE = "BSA" # Código do Brasileirão Série A
ENDPOINT = f"/competitions/{COMPETITION_CODE}/standings"

# --- Cabeçalhos de Autenticação ---
headers = {
    'X-Auth-Token': API_KEY
}

def obter_tabela_brasileirao():
    """Faz a requisição à API football-data.org e retorna os dados JSON."""
    url = BASE_URL + ENDPOINT
    print(f"Buscando dados em: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Lança exceção para erros HTTP (4xx ou 5xx)
        
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar a API: {e}")
        # Informa sobre o status do erro (pode ser 403 Forbidden se a chave for inválida ou o plano não cobrir)
        if 'response' in locals() and response.status_code == 403:
            print("Verifique se sua chave (API Key) está correta e se o plano de acesso cobre o Brasileirão.")
        return None

def formatar_tabela(dados):
    """Extrai e formata a tabela de classificação em um DataFrame do Pandas."""
    if not dados or 'standings' not in dados:
        print("Estrutura de dados inválida ou vazia.")
        return None

    # O primeiro item da lista 'standings' contém a tabela geral (TOTAL)
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

    # Cria o DataFrame
    df = pd.DataFrame(tabela)
    # Define as colunas na ordem desejada
    df = df[['Pos', 'Time', 'P', 'J', 'V', 'E', 'D', 'GP', 'GC', 'SG']]
    return df

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    print("Iniciando busca da Tabela do Campeonato Brasileiro (football-data.org)...")
    dados_json = obter_tabela_brasileirao()

    if dados_json:
        tabela_df = formatar_tabela(dados_json)
        
        if tabela_df is not None:
            print("\n🏆 Tabela do Campeonato Brasileiro - Série A 🏆")
            # Imprime a tabela no console sem o índice do Pandas
            print(tabela_df.to_string(index=False)) 
        else:
            print("Não foi possível gerar a tabela.")
    else:
        print("Falha na obtenção dos dados da API.")
