# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cTdbAzD7WKqbgDIPg6kKtDlhkmBFjEYY
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


try:
    dados = pd.read_csv("compras.csv")
except FileNotFoundError:
    dados = pd.DataFrame({"produto": [], "preço": []})
    dados.to_csv("compras.csv", index=False)


st.title("Controle de compras")


orcamento = st.number_input("Orçamento:", min_value=0.0)
total = dados["preço"].sum() if not dados.empty else 0


with st.form("nova_compra"):
    produto = st.text_input("Adicione aqui o seu produto")
    preco = st.number_input("Indique o preço", min_value=0.0)
    submit = st.form_submit_button("Adicionar")

    if submit:
        if preco <= (orcamento - total):
            nova_linha = pd.DataFrame({"produto": [produto], "preço": [preco]})
            dados = pd.concat([dados, nova_linha], ignore_index=True)
            dados.to_csv("compras.csv", index=False)
            st.success("Produto adicionado")
        else:
            st.error("Não tem orçamento suficiente")


if orcamento > 0:

    fig, ax = plt.subplots(figsize=(8, 8))
    if not dados.empty:
        produtos = dados["produto"].tolist()
        valores = dados["preço"].tolist()
        restante = orcamento - total
        if restante > 0:
            produtos.append("Disponível")
            valores.append(restante)

        plt.pie(
            valores,
            labels=produtos,
            autopct='%1.1f%%',
            pctdistance=0.85,
        )
        plt.title(f"Orçamento: {orcamento}€")

        centro = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centro)

    st.pyplot(fig)
    st.dataframe(dados)
    st.write(f"Total gasto: {total}€")
    st.write(f"Resta: {orcamento - total}€")