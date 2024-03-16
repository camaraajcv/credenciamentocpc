import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime, date
import matplotlib.pyplot as plt

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
    df.to_excel("dados.xlsx", index=False)

# Função para carregar o DataFrame a partir de um arquivo Excel
def carregar_dataframe():
    if os.path.exists("dados.xlsx"):
        print("Arquivo 'dados.xlsx' encontrado.")
        try:
            df = pd.read_excel("dados.xlsx", engine='openpyxl')
            print("Arquivo 'dados.xlsx' lido com sucesso.")
            return df
        except Exception as e:
            print(f"Erro ao ler o arquivo Excel: {e}")
            print("Criando novo DataFrame vazio.")
            return pd.DataFrame(columns=['SITUAÇÃO ECONSIG', 'SUBPROCESSO SILOMS', 'CATEGORIA', 'NATUREZA DE DESCONTO', 
                                          'CONSIGNATÁRIA', 'CNPJ', 'NRO CONTRATO', 
                                          'BCA OU DOU', 'SITUAÇÃO', 'DATA EXPIRAÇÃO CONTRATUAL', 
                                          'Dias para Fim Vigência', 'CÓDIGO', 'STATUS CREDENCIAMENTO', 
                                          'CPC STATUS',  'CPC ANUAL', 'DATA DE ENTRADA'])
    else:
        print("Arquivo 'dados.xlsx' não encontrado. Criando novo arquivo.")
        colunas = ['SITUAÇÃO ECONSIG', 'SUBPROCESSO SILOMS', 'CATEGORIA', 'NATUREZA DE DESCONTO', 
                   'CONSIGNATÁRIA', 'CNPJ', 'NRO CONTRATO', 
                   'BCA OU DOU', 'SITUAÇÃO', 'DATA EXPIRAÇÃO CONTRATUAL', 
                   'Dias para Fim Vigência', 'CÓDIGO', 'STATUS CREDENCIAMENTO', 
                   'CPC STATUS',  'CPC ANUAL', 'DATA DE ENTRADA']
        df = pd.DataFrame(columns=colunas)
        salvar_dataframe(df)  # Adicionando chamada para salvar o DataFrame
        return df

# Função para validar o formato do CNPJ
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
            subprocesso_siloms = st.text_input('Subprocesso Siloms*', value='')
            consignataria = st.text_input('Consignatária*', value='')
            bca_ou_dou = st.text_input('BCA ou DOU', value='')
            situacao = st.selectbox('Situação*', options=['', 'Encaminhado para Secretário(a) da CPC', 'Análise Equipe A', 'Análise Equipe B', 'Análise Equipe C', 'Análise Equipe D', 'Análise Equipe E' ,'Aguardando Assinaturas', 'encaminhado para a PP1 (conclusão/arquivamento)','encaminhado para a PP1 para análise'], index=0)
            categoria = st.selectbox('Categoria*', options=['', 'I', 'II', 'III'], index=0)
            natureza_desconto = st.selectbox('Natureza de Desconto*', options=['', 'MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA','CARTÃO DE CRÉDITO', 'SEGURO DE VIDA'], index=0)
            cnpj = st.text_input('CNPJ*', placeholder='XX.XXX.XXX/XXXX-XX', value='')
            numero_contrato = st.text_input('NRO CONTRATO', value='')

        with col2:
            data_entrada = st.date_input('Data de Entrada*', format='DD/MM/YYYY', value=date.today())
            data_expiracao_contratual = st.date_input('Data Expiração Contratual*', format='DD/MM/YYYY')
            codigo = st.text_input('CÓDIGO', value='')
            status_credenciamento = st.selectbox('Status Credenciamento*', options=['', 'Vencido', 'Ativo', 'Inativo'], index=0)
            cpc_status = st.selectbox('CPC STATUS*', options=['', 'Aguardando Publicação', 'Ativo', 'Credenciado', 'Bloqueado', 'Recredenciado'], index=0)
            cpc_anual = st.number_input('CPC ANUAL*', value=0)

        # Botão para adicionar novo processo
        if st.button('Adicionar Processo'):
            if validar_cnpj(cnpj):
                novo_processo = {
                    'SITUAÇÃO ECONSIG': situacao_econsig,
                    'SUBPROCESSO SILOMS': subprocesso_siloms,
                    'CATEGORIA': categoria,
                    'NATUREZA DE DESCONTO': natureza_desconto,
                    'CONSIGNATÁRIA': consignataria,
                    'CNPJ': cnpj,
                    'NRO CONTRATO': numero_contrato,
                    'BCA OU DOU': bca_ou_dou,
                    'SITUAÇÃO': situacao,
                    'DATA EXPIRAÇÃO CONTRATUAL': data_expiracao_contratual,
                    'Dias para Fim Vigência': (data_expiracao_contratual - date.today()).days,
                    'CÓDIGO': codigo,
                    'STATUS CREDENCIAMENTO': status_credenciamento,
                    'CPC STATUS': cpc_status,
                    'CPC ANUAL': cpc_anual,
                    'DATA DE ENTRADA': data_entrada
                }
                df = df.append(novo_processo, ignore_index=True)
                salvar_dataframe(df)
                st.success('Processo adicionado com sucesso!')

    elif opcao_selecionada == 'editar':
        st.warning('Funcionalidade de edição ainda não implementada.')

    elif opcao_selecionada == 'excluir':
        st.warning('Funcionalidade de exclusão ainda não implementada.')

    # Exibir DataFrame
    st.dataframe(df)

    # Botão para exportar os dados
    if st.button('Exportar dados'):
        st.markdown(get_table_download_link(df), unsafe_allow_html=True)

# Função para criar link de download do DataFrame
def get_table_download_link(df):
    # Cria um link para download do DataFrame como CSV
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # codifica em bytes para base64
    href = f'<a href="data:file/csv;base64,{b64}" download="dados.csv">Baixar arquivo CSV</a>'
    return href

if __name__ == '__main__':
    main()
