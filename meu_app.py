###########################################
#  Site de Floricultura Rosas & Espinhos
#  RA: 2102144  Fernando Dias
#  RA: 2009640  Felipe Sousa Chagas
#  PJI 310 - Turma 004 Grupo 005
#  Ultima atualização 12/04/2024 as 20:00 hs
#  #########################################


import requests


import streamlit as st


import pandas as pd


from pandas import read_csv

def pega_cotacoes():
    requisicao = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL")
    requisicao_dic = requisicao.json()
    cotacao_dolar = requisicao_dic["USDBRL"]["bid"]
    cotacao_euro = requisicao_dic["EURBRL"]["bid"]
    cotacao_btc = requisicao_dic["BTCBRL"]["bid"]
    with st.container(border=True, height=150):
        st.write("Cotação Dolar R$", float(cotacao_dolar))
        st.write("Cotação Euro. R$", float(cotacao_euro))
        st.write("Cotação Btc.. R$", float(cotacao_btc))
    return


st.set_page_config(page_title="Floricultura Rosas & Espinhos",
        page_icon="🧊", layout="wide")


with st.sidebar:
    # "Floricultura Rosas & Espinhos."   # Nome acima da imagem
    opcoes = st.sidebar.selectbox(
    "Escolha uma opção",
    ("        ","Pedidos", "Cotações", "Tabela preços", "Relatórios"),  # Menu de opções
    )
    if opcoes == "Cotações":
        pega_cotacoes()  # pega a cotação das moedas dolar, euro e bitcoin e exib

    if opcoes == "Pedidos":
        st.write("Em programação -> aguarde")

    if opcoes == "Tabela preços":
        st.write("Em programação -> aguarde")

    if opcoes == "Relatórios":
        st.write("Em programação -> aguarde")

    st.image("flower.png", width=270)  # Imagem da Flor


with st.container(border=True, height=170):
    st.subheader("Floricultura Rosas & Espinhos - 30 anos no mercado.", divider="rainbow")  # Linha colorida Rainbow
    st.title("Tabela das Ultimas Vendas")

@st.cache_data
def carregar_vendas():
    tabela = pd.read_csv("resultados.csv")  # carrega a tabela resultados da vendas nos dias
    return tabela

@st.cache_data
def carregar_produtos():
    produto  = read_csv("produtos.csv")
    return produto


with st.container(border=True, height=400):
    qtde_dias = st.selectbox("Selecione o período", ["7D", "15D", "21D", "30D"])
    num_dias = int(qtde_dias.replace("D", ""))
    dados = carregar_vendas()
    dados = dados[-num_dias:]
    st.area_chart(dados, x="Data", y="Vendas", width=180, height=300)  # apresenta os ultimos vendas do arquivo resultados


with st.container(border=True, height=400):  # Tabela de Produtos
    st.title("Produtos da Floricultura")
    pro = carregar_produtos()
    st.dataframe(pro)  # Tabela de Produtos


#  with st.container(border=True, height=400):  # Calendario
#      date = st.date_input("Escolha um dia", format="DD/MM/YYYY", label_visibility="visible")


with st.container(border=True, height=200):  # Rodapé da Pagina
    st.write("Patrocinio [Clique aqui] (https://www.hashtagtreinamentos.com/curso-python)")
    st.write("Copyright(C) 2024 - Direitos Reservados - Versão 1.01")
    with st.container(border=True, height=100):  # Rodapé da Pagina (2)
        st.write("Desenvolvido pela Turma 004 Grupo 005")
        st.write("Linguagem utilizada Python 3.12.2 + Stremlit + Pandas")


# Fim deste Módulo