import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime, date

# Função para carregar ou criar o DataFrame
def carregar_dataframe():
    if os.path.exists("dados.csv"):
        return pd.read_csv("dados.csv")
    else:
        colunas = ['SITUAÇÃO ECONSIG', 'LOCALIZAÇÃO', 'CATEGORIA', 'NATUREZA DE DESCONTO', 
                   'CONSIGNATÁRIA', 'CNPJ', 'NRO CONTRATO (PORTARIA OU TERMO)', 
                   'BCA OU DOU', 'SITUAÇÃO', 'DATA EXPIRAÇÃO CONTRATUAL', 
                   'Dias para Fim Vigência', 'NUP', 'CÓDIGO', 'STATUS CREDENCIAMENTO', 
                   'AÇÃO', 'OFÍCIO PARA EC', 'CPC STATUS', 'Verificado ?', 'CPC ANUAL']
        return pd.DataFrame(columns=colunas)

# Função para salvar o DataFrame em um arquivo CSV
def salvar_dataframe(df):
    df.to_csv("dados.csv", index=False)

# Função para validar o formato do CNPJ
def validar_cnpj(cnpj):
    if not re.match(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', cnpj):
        st.error('O CNPJ deve ter o formato XX.XXX.XXX/XXXX-XX')
        return False
    return True

def main():
    st.title('Inserindo e Excluindo Dados em DataFrame')

    # Carregar ou criar o DataFrame
    df = carregar_dataframe()

    # Checkbox para exibir o formulário de inserção
    exibir_formulario_insercao = st.checkbox('Exibir Formulário de Inserção')

    if exibir_formulario_insercao:
        # Exibir formulário para inserir dados
        st.header('Inserir Novos Dados')

        col1, col2 = st.columns(2)

        with col1:
            situacao_econsig = st.selectbox('Situação Econômica*', options=['', 'Recredenciado', 'Credenciado', 'Aguardando Publicação', 'Arquivado'])
            localizacao = st.text_input('Localização', required=False)
            consignataria = st.text_input('Consignatária*', required=True)
            bca_ou_dou = st.text_input('BCA ou DOU', required=False)
            situacao = st.text_input('Situação*', required=True)
            data_expiracao_contratual = st.date_input('Data Expiração Contratual*', format='DD/MM/YYYY')
            categoria = st.selectbox('Categoria*', options=['', 'I', 'II', 'III'])
            natureza_desconto = st.selectbox('Natureza de Desconto*', options=['', 'MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA','CARTÃO DE CRÉDITO', 'SEGURO DE VIDA'])
            cnpj = st.text_input('CNPJ*', placeholder='XX.XXX.XXX/XXXX-XX')
            nro_contrato = st.text_input('Nro Contrato (Portaria ou Termo)', required=False)
            verificado = st.selectbox('Verificado?*', options=['', 'Sim', 'Não'])
        with col2:
            data_atual = date.today()  # Obtém a data atual
            dias_para_fim_vigencia = (data_expiracao_contratual - data_atual).days
            if dias_para_fim_vigencia < 0:
                dias_para_fim_vigencia = 'Expirado'
            else:
                dias_para_fim_vigencia = str(dias_para_fim_vigencia) + ' dias'
           
            dias_para_fim_vigencia = st.text_input('Dias para Fim Vigência', value=dias_para_fim_vigencia, disabled=True)
            nup = st.text_input('NUP')
            codigo = st.text_input('Código', required=False)
            status_credenciamento = st.text_input('Status Credenciamento')
            acao = st.text_input('Ação', required=False)
            oficio_para_ec = st.text_input('Ofício para EC', required=False)
            cpc_status = st.selectbox('CPC Status', options=['','EM ANÁLISE', 'CONCLUÍDO', 'ENTREGUE', 'REJEITADO'])
            cpc_anual = st.selectbox('CPC Anual', options=['', 'CPC 2021', 'CPC 2022', 'CPC 2023', 'CPC 2024', 'CPC 2025', 'CPC 2026'])

        if st.button('Inserir'):
            if validar_cnpj(cnpj):
                novo_dado = {
                    'SITUAÇÃO ECONSIG': situacao_econsig,
                    'LOCALIZAÇÃO': localizacao,
                    'CATEGORIA': categoria,
                    'NATUREZA DE DESCONTO': natureza_desconto,
                    'CONSIGNATÁRIA': consignataria,
                    'CNPJ': cnpj,
                    'NRO CONTRATO (PORTARIA OU TERMO)': nro_contrato,
                    'BCA OU DOU': bca_ou_dou,
                    'SITUAÇÃO': situacao,
                    'DATA EXPIRAÇÃO CONTRATUAL': data_expiracao_contratual.strftime('%d/%m/%Y'),
                    'Dias para Fim Vigência': dias_para_fim_vigencia,
                    'NUP': nup,
                    'CÓDIGO': codigo,
                    'STATUS CREDENCIAMENTO': status_credenciamento,
                    'AÇÃO': acao,
                    'OFÍCIO PARA EC': oficio_para_ec,
                    'CPC STATUS': cpc_status,
                    'Verificado ?': verificado,
                    'CPC ANUAL': cpc_anual
                }

                novo_df = pd.DataFrame([novo_dado])
                df = pd.concat([df, novo_df], ignore_index=True)

                st.success('Dados inseridos com sucesso.')

    # Exibir DataFrame atualizado
    st.header('DataFrame Atualizado')
    st.write(df)

    # Salvar DataFrame em arquivo CSV
    salvar_dataframe(df)

if __name__ == '__main__':
    main()

