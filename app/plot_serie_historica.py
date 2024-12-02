from app import app
import plotly.express as px
import os
import json
import pandas as pd
import plotly.express as px

current_dir = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(current_dir, 'tabela_geral.xlsx'))

def load_data(file_path):
    data = pd.read_excel(file_path)
    return data

def carregar_dados_json(arquivo):
    caminho_arquivo = os.path.join(app.root_path, 'static', 'JSON', f'{arquivo}.json')
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        dados = json.load(file)
    return dados

def plotar_serie_historica(tipoDado, produto, tipo):
    displayProdutos = carregar_dados_json(tipo)
    dados = load_data(file_path)
    dados.drop(dados.tail(1).index, inplace=True)

    dados = dados[dados['Classe'] == 1]
    dados = dados[dados['Produto'] == produto]

    fig = px.line(
        dados, 
        x=dados['Data'], 
        y=[tipoDado], 
        template = 'plotly_white', 
        title=f'{displayProdutos[produto]} (Classe 1) - {tipoDado}'
    )

    fig.update_layout(
        xaxis_title='Data',
        yaxis_title=tipoDado,
        xaxis=dict(
            tickformat='%d-%m-%Y',  # Formato de data
        ),
        showlegend=False,
    )

    fig.update_traces(
        hovertemplate=(
            f'<b>{displayProdutos[produto]}</b><br>'
            f'Data: %{{x}}<br>'
            f'{tipoDado}: %{{y:.2f}}<extra></extra>'
        ),
        name=f'{tipoDado}'
    )

    fig = fig.to_html(full_html=False)
    return fig