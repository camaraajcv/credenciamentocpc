import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime, date
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests 
import openpyxl

# URL da imagem
image_url = "https://www.fab.mil.br/om/logo/mini/dirad2.jpg"

# Código HTML e CSS para ajustar a largura da imagem para 20% da largura da coluna e centralizar
html_code = f'<div style="display: flex; justify-content: center;"><img src="{image_url}" alt="Imagem" style="width:20vw;"/></div>'
# Exibir a imagem usando HTML
st.markdown(html_code, unsafe_allow_html=True)

# Centralizar o texto abaixo da imagem
st.markdown("<h1 style='text-align: center; font-size: 1.5em;'>DIRETORIA DE ADMINISTRAÇÃO DA AERONÁUTICA</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-size: 1.2em;'>SUBDIRETORIA DE PAGAMENTO DE PESSOAL</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 1em; text-decoration: underline;'>PP1 - DIVISÃO DE DESCONTOS</h3>", unsafe_allow_html=True)

# Texto explicativo
st.write("CPC - Comissão Permanente de Credenciamento")

# Função para salvar o DataFrame em um arquivo CSV e no GitHub
def salvar_dataframe(df):
    # Salvar DataFrame como arquivo Excel localmente usando openpyxl
    with pd.ExcelWriter("dados.xlsx", engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    # Informações para o repositório do GitHub
    usuario = "camaraajcv"
    repositorio = "credenciamentocpc"
    caminho_arquivo = "dados.xlsx"
    token = "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"

    # Ler o arquivo Excel como binário
    with open(caminho_arquivo, "rb") as file:
        conteudo_xls = file.read()

    # Codificar o conteúdo binário em base64
    conteudo_base64 = conteudo_xls.hex()

    # URL da API do GitHub para criar ou atualizar um arquivo
    url = f"https://api.github.com/repos/{usuario}/{repositorio}/contents/{caminho_arquivo}"

    # Cabeçalhos para a solicitação HTTP
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Corpo da solicitação para criar ou atualizar o arquivo
    data = {
        "message": "Atualizando dados.xlsx",
        "content": conteudo_base64
    }

    # Enviar solicitação PUT para criar ou atualizar o arquivo
    response = requests.put(url, headers=headers, json=data)

    # Verificar o resultado
    if response.status_code == 201:
        st.success("Arquivo dados.xlsx atualizado com sucesso no GitHub!")
    else:
        st.error("Falha ao atualizar o arquivo dados.xlsx no GitHub.")
        st.error(response.text)

# Função para carregar ou criar o DataFrame
def carregar_dataframe():
    if os.path.exists("dados.xlsx"):
        print("Arquivo 'dados.csv' encontrado.")
        try:
            df = pd.read_excel("dados.xlsx", encoding='utf-8')
            print("Arquivo 'dados.xlsx' lido com sucesso.")
            return df
        except Exception as e:
            print(f"Erro ao ler o arquivo CSV: {e}")
            print("Não foi possível ler o arquivo 'dados.csv'. Criando novo DataFrame vazio.")
            return pd.DataFrame(columns=['SITUAÇÃO ECONSIG', 'SUBPROCESSO SILOMS', 'CATEGORIA', 'NATUREZA DE DESCONTO', 
                                         'CONSIGNATÁRIA', 'CNPJ', 'NRO CONTRATO', 'BCA OU DOU', 'SITUAÇÃO', 
                                         'DATA EXPIRAÇÃO CONTRATUAL', 'Dias para Fim Vigência', 'CÓDIGO', 
                                         'STATUS CREDENCIAMENTO', 'CPC STATUS',  'CPC ANUAL', 'DATA DE ENTRADA'])
    else:
        print("Arquivo 'dados.csv' não encontrado. Criando novo arquivo.")
        colunas = ['SITUAÇÃO ECONSIG', 'SUBPROCESSO SILOMS', 'CATEGORIA', 'NATUREZA DE DESCONTO', 
                   'CONSIGNATÁRIA', 'CNPJ', 'NRO CONTRATO', 'BCA OU DOU', 'SITUAÇÃO', 'DATA EXPIRAÇÃO CONTRATUAL', 
                   'Dias para Fim Vigência', 'CÓDIGO', 'STATUS CREDENCIAMENTO', 'CPC STATUS',  'CPC ANUAL', 
                   'DATA DE ENTRADA']
        df = pd.DataFrame(columns=colunas)
        salvar_dataframe(df)  # Adicionando chamada para salvar o DataFrame
        return df

# Checkboxes para incluir, editar e excluir processos
def mostrar_opcoes():
    col1, col2, col3 = st.columns(3)

    # Variável para armazenar o valor do checkbox selecionado
    opcao_selecionada = st.session_state.get('opcao_selecionada', None)

    # Lógica para garantir apenas um checkbox selecionado
    with col1:
        inserir_checked = st.checkbox('Incluir Novo Processo', key='inserir')
        if inserir_checked:
            opcao_selecionada = 'incluir'
    with col2:
        editar_checked = st.checkbox('Alterar Processo', key='alterar')
        if editar_checked:
            opcao_selecionada = 'editar'
    with col3:
        excluir_checked = st.checkbox('Excluir Processo', key='excluir')
        if excluir_checked:
            opcao_selecionada = 'excluir'

    return opcao_selecionada

# Função principal
def main():
    st.title('Controle Processos CPC 2024')

    # Carregar ou criar o DataFrame
    df = carregar_dataframe()

    # Opções de inclusão, edição ou exclusão
    opcao_selecionada = mostrar_opcoes()

    if opcao_selecionada == 'incluir':
        # Lógica para inclusão de processo
        pass
    elif opcao_selecionada == 'excluir':
        # Lógica para exclusão de processo
        pass
    elif opcao_selecionada == 'editar':
        # Lógica para edição de processo
        pass

    # Exibir DataFrame atualizado
    st.header('Processos CPC')
    st.dataframe(df)

    # Botão para salvar o DataFrame
    if st.button('Salvar Alterações'):
        salvar_dataframe(df)

# Executar a função principal
if __name__ == '__main__':
    main()