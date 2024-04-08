#######################################
# Site de Floricultura Rosas & Espinhos
# Alberto Dias 07/04/2024 as 22:45 hs
# Python 3.12
#######################################


import streamlit as st


import pandas as pd


st.set_page_config(page_title="Floricultura Rosas & Espinhos")


with st.container():
    st.subheader("Floricultura Rosas & Espinhos - 30 anos no mercado.")
    st.title("Tabela das Ultimas Vendas")
    st.write("Informações sobre as ultimas vendas efetuadas")
    st.write("Patrocinio: Aprenda Python! [Clique aqui] (https://www.hashtagtreinamentos.com/curso-python)")


@st.cache_data
def carregar_dados():
    tabela = pd.read_csv("resultados.csv")
    return tabela


with st.container():
    st.write("---")
    qtde_dias = st.selectbox("Selecione o período", ["7D", "15D", "21D", "30D"])
    num_dias = int(qtde_dias.replace("D", ""))
    dados = carregar_dados()
    dados = dados[-num_dias:]
    st.area_chart(dados, x="Data", y="Contratos")


# Fim deste Módulo