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

#Código HTML e CSS para ajustar a largura da imagem para 20% da largura da coluna e centralizar
html_code = f'<div style="display: flex; justify-content: center;"><img src="{image_url}" alt="Imagem" style="width:8vw;"/></div>'
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
    # Save DataFrame as Excel file locally using openpyxl
    with pd.ExcelWriter("dados.xlsx", engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    # Information for GitHub repository
    usuario = "camaraajcv"
    repositorio = "credenciamentocpc"
    caminho_arquivo = "dados.xlsx"
    token = "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"

    # Read Excel file as binary
    with open(caminho_arquivo, "rb") as file:
        conteudo_xls = file.read()

    # Base64 encode the binary content
    conteudo_base64 = conteudo_xls.hex()

    # URL of the GitHub API to create or update a file
    url = f"https://api.github.com/repos/{usuario}/{repositorio}/contents/{caminho_arquivo}"

    # Headers for HTTP request
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Body of the request to create or update the file
    data = {
        "message": "Atualizando dados.xlsx",
        "content": conteudo_base64
    }

    # Send PUT request to create or update the file
    response = requests.put(url, headers=headers, json=data)

    # Check the result
    if response.status_code == 201:
        st.success("Arquivo dados.xlsx atualizado com sucesso no GitHub!")
    else:
        st.error("Falha ao atualizar o arquivo dados.xlsx no GitHub.")
        st.error(response.text)

# Função para carregar ou criar o DataFrame
def carregar_dataframe():
    # Check if the Excel file exists
    if not os.path.exists("dados.xlsx"):
        # If it doesn't exist, create a DataFrame with the required columns
        colunas = ['SITUAÇÃO ECONSIG', 'SUBPROCESSO SILOMS', 'CATEGORIA', 'NATUREZA DE DESCONTO', 
                   'CONSIGNATÁRIA', 'CNPJ', 'NRO CONTRATO', 
                   'BCA OU DOU', 'SITUAÇÃO', 'DATA EXPIRAÇÃO CONTRATUAL', 
                   'Dias para Fim Vigência', 'CÓDIGO', 'STATUS CREDENCIAMENTO', 
                   'CPC STATUS',  'CPC ANUAL', 'DATA DE ENTRADA']
        df = pd.DataFrame(columns=colunas)
        # Save the DataFrame to an Excel file
        salvar_dataframe(df)  # Adicionando chamada para salvar o DataFrame
        return df
    else:
        # If the Excel file exists, load the DataFrame from the file
        return pd.read_excel("dados.xlsx")

def validar_cnpj(cnpj):
    if not re.match(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', cnpj):
        st.error('O CNPJ deve ter o formato XX.XXX.XXX/XXXX-XX')
        return False
    return True

def main():
    st.title('Controle Processos CPC 2024')

    # Carregar ou criar o DataFrame
    df = carregar_dataframe()

    # Checkboxes para incluir, editar e excluir processos
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

    if opcao_selecionada == 'incluir':
        # Exibir formulário para inserir dados
        col1, col2 = st.columns(2)

        with col1:
            situacao_econsig = st.selectbox('Situação Econsig*', options=['', 'Sem Cadastro','Recredenciado', 'Credenciado', 'Aguardando Publicação', 'Arquivado','Bloqueado','Credenciamento Vencido'])
            subprocesso_siloms = st.text_input('Subprocesso Siloms*')
            subprocesso_siloms = subprocesso_siloms.replace(',', '')

            # Adicionar o valor convertido ao DataFrame
            df['SUBPROCESSO SILOMS'] = pd.to_numeric(subprocesso_siloms, errors='coerce')
            consignataria = st.text_input('Consignatária*')
            bca_ou_dou = st.text_input('BCA ou DOU')
            situacao = st.selectbox('Situação*', options=['', 'Ativo', 'Inativo'])
            dias_para_fim_vigencia = st.text_input('Dias para Fim Vigência*')

        with col2:
            cnpj = st.text_input('CNPJ*')
            validar_cnpj(cnpj)
            nro_contrato = st.text_input('Nro Contrato')
            codigo = st.text_input('Código')
            status_credenciamento = st.selectbox('Status Credenciamento*', options=['', 'Deferido', 'Indeferido', 'Aguardando Publicação'])
            data_expiracao_contratual = st.date_input('Data Expiração Contratual*', min_value=date.today())

        if st.button('Incluir'):
            # Adicionar uma nova linha ao DataFrame
            nova_linha = {'SITUAÇÃO ECONSIG': situacao_econsig,
                          'SUBPROCESSO SILOMS': subprocesso_siloms,
                          'CONSIGNATÁRIA': consignataria,
                          'CNPJ': cnpj,
                          'NRO CONTRATO': nro_contrato,
                          'BCA OU DOU': bca_ou_dou,
                          'SITUAÇÃO': situacao,
                          'Dias para Fim Vigência': dias_para_fim_vigencia,
                          'CÓDIGO': codigo,
                          'STATUS CREDENCIAMENTO': status_credenciamento,
                          'DATA EXPIRAÇÃO CONTRATUAL': data_expiracao_contratual}
            df = df.append(nova_linha, ignore_index=True)

            # Salvar o DataFrame atualizado
            salvar_dataframe(df)
            st.success('Processo incluído com sucesso!')

    elif opcao_selecionada == 'editar':
        # Exibir formulário para editar dados
        indice_selecionado = st.selectbox('Selecione o índice da linha para editar:', options=df.index.tolist(), index=0)
        linha_selecionada = df.loc[indice_selecionado]

        col1, col2 = st.columns(2)

        with col1:
            situacao_econsig = st.selectbox('Situação Econsig*', options=['', 'Sem Cadastro','Recredenciado', 'Credenciado', 'Aguardando Publicação', 'Arquivado','Bloqueado','Credenciamento Vencido'], index=df.index.tolist().index(indice_selecionado))
            subprocesso_siloms = st.text_input('Subprocesso Siloms*', value=str(linha_selecionada['SUBPROCESSO SILOMS']).replace(',', ''))

            # Atualizar o valor no DataFrame
            df.at[indice_selecionado, 'SITUAÇÃO ECONSIG'] = situacao_econsig
            df.at[indice_selecionado, 'SUBPROCESSO SILOMS'] = pd.to_numeric(subprocesso_siloms, errors='coerce')

            consignataria = st.text_input('Consignatária*', value=linha_selecionada['CONSIGNATÁRIA'])
            bca_ou_dou = st.text_input('BCA ou DOU', value=linha_selecionada['BCA OU DOU'])
            situacao = st.selectbox('Situação*', options=['', 'Ativo', 'Inativo'], index=0)
            dias_para_fim_vigencia = st.text_input('Dias para Fim Vigência*', value=linha_selecionada['Dias para Fim Vigência'])

        with col2:
            cnpj = st.text_input('CNPJ*', value=linha_selecionada['CNPJ'])
            validar_cnpj(cnpj)
            nro_contrato = st.text_input('Nro Contrato', value=linha_selecionada['NRO CONTRATO'])
            codigo = st.text_input('Código', value=linha_selecionada['CÓDIGO'])
            status_credenciamento = st.selectbox('Status Credenciamento*', options=['', 'Deferido', 'Indeferido', 'Aguardando Publicação'], index=df.index.tolist().index(indice_selecionado))
            data_expiracao_contratual = st.date_input('Data Expiração Contratual*', value=datetime.strptime(linha_selecionada['DATA EXPIRAÇÃO CONTRATUAL'], '%Y-%m-%d'))

        if st.button('Editar'):
            # Atualizar a linha no DataFrame
            df.at[indice_selecionado, 'CONSIGNATÁRIA'] = consignataria
            df.at[indice_selecionado, 'CNPJ'] = cnpj
            df.at[indice_selecionado, 'NRO CONTRATO'] = nro_contrato
            df.at[indice_selecionado, 'BCA OU DOU'] = bca_ou_dou
            df.at[indice_selecionado, 'SITUAÇÃO'] = situacao
            df.at[indice_selecionado, 'Dias para Fim Vigência'] = dias_para_fim_vigencia
            df.at[indice_selecionado, 'CÓDIGO'] = codigo
            df.at[indice_selecionado, 'STATUS CREDENCIAMENTO'] = status_credenciamento
            df.at[indice_selecionado, 'DATA EXPIRAÇÃO CONTRATUAL'] = data_expiracao_contratual.strftime('%Y-%m-%d')

            # Salvar o DataFrame atualizado
            salvar_dataframe(df)
            st.success('Processo editado com sucesso!')

    elif opcao_selecionada == 'excluir':
        # Exibir formulário para excluir linha
        indice_selecionado = st.selectbox('Selecione o índice da linha para excluir:', options=df.index.tolist(), index=0)
        linha_selecionada = df.loc[indice_selecionado]

        st.write('Tem certeza que deseja excluir o seguinte processo?')
        st.write(linha_selecionada)

        if st.button('Excluir'):
            # Excluir a linha do DataFrame
            df = df.drop(index=indice_selecionado)

            # Salvar o DataFrame atualizado
            salvar_dataframe(df)
            st.success('Processo excluído com sucesso!')

    # Exibir DataFrame
    st.write(df)

if __name__ == '__main__':
    main()
