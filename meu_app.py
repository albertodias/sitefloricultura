#######################################
# Site de Floricultura Rosas & Espinhos
# Alberto Dias 09/04/2024 as 22:45 hs
# Python 3.12 + Pandas + Streamlit
#######################################


import streamlit as st


import pandas as pd


from pandas import read_csv


import time


st.set_page_config(page_title="Floricultura Rosas & Espinhos")

with st.sidebar:
    "Floricultura Rosas & Espinhos."
    st.image("flower.png", width=270)
    opcoes = st.sidebar.selectbox(
        "Escolha uma opção",
        ("Pedidos", "Contatos", "Tabela preços", "Relatórios"),
    )
    with st.spinner("Carregando..."):
        time.sleep(4)
    st.success("Carregamento Concluido !!!")


with st.container(border=True, height=110):
    st.subheader("Floricultura Rosas & Espinhos - 30 anos no mercado.", divider="rainbow")
    st.title("Tabela das Ultimas Vendas")

@st.cache_data
def carregar_vendas():
    tabela = pd.read_csv("resultados.csv")  # carrega a tabela resultados da vendas nos dias
    return tabela

@st.cache_data
def carregar_produtos():
    produto  = read_csv("produtos.csv")
    # produto = pd.read_csv("produtos.csv") # carrega a tabela de produtos da Floricultura
    return produto


with st.container(border=True, height=560):
    st.title("Relatório: Ultimas Vendas")
    qtde_dias = st.selectbox("Selecione o período", ["7D", "15D", "21D", "30D"])
    num_dias = int(qtde_dias.replace("D", ""))
    dados = carregar_vendas()
    dados = dados[-num_dias:]
    st.area_chart(dados, x="Data", y="Vendas", width=180, height=300)  # apresenta os ultimos vendas do arquivo resultados


with st.container(border=True, height=400):
    st.title("Produtos da Floricultura")
    pro = carregar_produtos()
    # st.table(pro) # apresenta a tabela de produtos
    st.dataframe(pro)  # troquei por esta com mais opcoes


with st.container(border=True, height=110):  # Rodapé da Pagina
    st.write("Patrocinio [Clique aqui] (https://www.hashtagtreinamentos.com/curso-python)")
    st.write("Copyright(C) 2024 - Direitos Reservados - Linguagem Python + Stremlit + Pandas")


# Fim deste Módulo