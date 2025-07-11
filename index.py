import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import streamlit as st

url = "https://www.noticiasagricolas.com.br/cotacoes/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

tabelas = soup.find_all('div', class_="tables")
graos = ["arroz", "café", "milho", "soja"]
with open("Graos.csv", "w", encoding="utf-8", newline='') as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(["Produto", " Data", " Preço por saca", " Variação"])
    for titulos in tabelas:
        h3s = titulos.find_all('h3')
        for h3 in h3s:
            links = h3.find_all('a')
            for produto in links:
                nome = produto.get_text(strip=True).lower()
                if nome in graos:
                    # Tenta encontrar o preço logo após o link
                    data_tag = produto.find_next('td')
                    preco_tag = data_tag.find_next('td')    
                    variacao_tag = preco_tag.find_next('td')
                    #escritor.writerow([nome, data])
                    data = data_tag.get_text(strip=True)
                    preco = preco_tag.get_text(strip=True)
                    variacao = variacao_tag.get_text(strip=True)
                    escritor.writerow([nome, data, preco, variacao])  
                    print(f"Produto: {nome}, Data: {data}, Preço: {preco}, Variação: {variacao}")

df_graos = pd.read_csv("graos.csv", sep=",")

boi = "Boi Gordo"
with open("boi.csv", "w", encoding="utf-8", newline='') as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(["estado", "Preço (R$/@)", "Variação(%)", "U$/@"])
    for titulos in tabelas:
        h3s = titulos.find_all('h3')
        for h3 in h3s:
            links = h3.find_all('a')
            for produto in links:
                nome = produto.get_text(strip=True).lower()
                if nome == boi.lower():
                    tabela = h3.find_next('table')
                    if tabela:
                        linhas = tabela.find_all('tr')[1:]
                        for linha in linhas:
                            colunas = linha.find_all('td')
                            if len(colunas) >= 4:
                                estado = colunas[0].get_text(strip=True)
                                preco = colunas[1].get_text(strip=True)
                                variacao = colunas[2].get_text(strip=True)
                                dolar = colunas[3].get_text(strip=True)
                                escritor.writerow([estado, preco, variacao, dolar])

df_boi = pd.read_csv("boi.csv", sep=",")

galinha = "frango"
with open("frango.csv", "w", encoding="utf-8", newline='') as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(["data", "a prazo R$", "Variação(%)"])
    for titulos in tabelas:
        h3s = titulos.find_all('h3')
        for h3 in h3s:
            nome = h3.get_text(strip=True).lower()
            if nome == galinha.lower():
                tabela = h3.find_next('table')
                if tabela:
                    linhas = tabela.find_all('tr')[1:]  # pula o cabeçalho
                    for linha in linhas:
                        colunas = linha.find_all('td')
                        if len(colunas) >= 3:
                            data = colunas[0].get_text(strip=True)
                            preco = colunas[1].get_text(strip=True)
                            variacao = colunas[2].get_text(strip=True)
                            escritor.writerow([data, preco, variacao])
df_frango = pd.read_csv("frango.csv", sep=",")

suinos = "Suínos"
with open("suino.csv", "w", encoding="utf-8", newline='') as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(["data", "a prazo R$", "Variação(%)"])
    for titulos in tabelas:
        h3s = titulos.find_all('h3')
        for h3 in h3s:
            nome = h3.get_text(strip=True).lower()
            if nome == suinos.lower():
                tabela = h3.find_next('table')
                if tabela:
                    linhas = tabela.find_all('tr')[1:]  # pula o cabeçalho
                    for linha in linhas:
                        colunas = linha.find_all('td')
                        if len(colunas) >= 3:
                            data = colunas[0].get_text(strip=True)
                            preco = colunas[1].get_text(strip=True)
                            variacao = colunas[2].get_text(strip=True)
                            escritor.writerow([data, preco, variacao])
df_suino = pd.read_csv("suino.csv", sep=",")



st.title("AgroBot - Cotações Agrícolas")
st.write("Bem-vindo ao AgroBot! Aqui você pode consultar as cotações de grãos, boi, frango e suíno.")
st.write("As cotações são atualizadas automaticamente a partir do site Notícias Agrícolas.")
st.header("Cotações de Grãos")
st.write("Aqui estão as cotações dos principais grãos:")
if st.checkbox("Exibir tabela de Grãos"):
    st.write(df_graos)
st.header("Cotações de animais")
if st.checkbox("Exibir tabelas de animais"):
    st.write("Clique nas opções abaixo para ver as cotações dos animais:")

    if st.checkbox("Cotações de Boi"):
        st.write("Aqui estão as cotações do Boi Gordo:")
        st.write(df_boi)
    if st.checkbox("Cotações de Frango"):
        st.write("Aqui estão as cotações do Frango:")
        st.write(df_frango)
    if st.checkbox("Cotações de Suínos"):
        st.image("https://www.petz.com.br/blog/wp-content/uploads/2022/10/quanto-tempo-vive-um-porco-2.jpg")
        st.write("Aqui estão as cotações dos Suínos:")
        st.write(df_suino)
    
