#######################################
# Site de Floricultura Rosas & Espinhos
# Alberto Dias 08/04/2024 as 21:45 hs
# Python 3.12 + Pandas + Streamlit
#######################################

import streamlit as st

import pandas as pd

st.set_page_config(page_title="Floricultura Rosas & Espinhos")

with st.container():
    st.subheader("Floricultura Rosas & Espinhos - 30 anos no mercado.", divider="rainbow")
    st.title("Tabela das Ultimas Vendas")

@st.cache_data
def carregar_vendas():
    tabela = pd.read_csv("resultados.csv") # carrega a tabela resultados da vendas nos dias
    return tabela

@st.cache_data
def carregar_produtos():
    produto = pd.read_csv("produtos.csv") # carrega a tabela de produtos da Floricultura
    return produto

with st.container():
    st.write("---")
    qtde_dias = st.selectbox("Selecione o período", ["7D", "15D", "21D", "30D"])
    num_dias = int(qtde_dias.replace("D", ""))
    dados = carregar_vendas()
    dados = dados[-num_dias:]
    st.area_chart(dados, x="Data", y="Vendas") # apresenta os ultimos vendas do arquivo resultados


with st.container():
    st.write("---")
    st.title("Tabela de Produtos da Floricultura")
    pro = carregar_produtos()
    st.table(pro) # apresenta a tabela de produtos


with st.container():  # Rodapé da Pagina
    st.write("---")
    st.write("Patrocinador: Aprenda Python! [Clique aqui] (https://www.hashtagtreinamentos.com/curso-python)")
    st.write("Copyright(C) 2024 - Todos os Direitos Reservados - Linguagem Python + Stremlit + Pandas")


# Fim deste Módulo