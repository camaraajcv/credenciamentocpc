import streamlit as st
import pandas as pd
import os
import re

# Função para carregar ou criar o DataFrame
def carregar_dataframe():
    # Verificar se o arquivo CSV existe
    if os.path.exists("dados.csv"):
        # Se o arquivo existir, carregue o DataFrame a partir dele
        return pd.read_csv("dados.csv")
    else:
        # Caso contrário, crie um DataFrame vazio com as colunas desejadas
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
            situacao_econsig = st.selectbox('Situação Econômica', options=['', 'Arquivado', 'Ativo', 'Bloqueado', 'Não Cadastrado'])
            localizacao = st.text_input('Localização')
            consignataria = st.text_input('Consignatária')
            bca_ou_dou = st.text_input('BCA ou DOU')
            situacao = st.text_input('Situação')
            data_expiracao_contratual = st.text_input('Data Expiração Contratual')
            categoria = st.selectbox('Categoria', options=['', 'I', 'II', 'III'])
            natureza_desconto = st.selectbox('Natureza de Desconto', options=['', 'MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA CARTÃO DE CRÉDITO', 'SEGURO DE VIDA'])
            cnpj = st.text_input('CNPJ')
            nro_contrato = st.text_input('Nro Contrato (Portaria ou Termo)')
        with col2:
           
            dias_para_fim_vigencia = st.text_input('Dias para Fim Vigência')
            nup = st.text_input('NUP')
            codigo = st.text_input('Código')
            status_credenciamento = st.text_input('Status Credenciamento')
            acao = st.text_input('Ação')
            oficio_para_ec = st.text_input('Ofício para EC')
            cpc_status = st.text_input('CPC Status')
            verificado = st.text_input('Verificado?')
            cpc_anual = st.text_input('CPC Anual')

        if st.button('Inserir'):
            # Validar CNPJ
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
                    'DATA EXPIRAÇÃO CONTRATUAL': data_expiracao_contratual,
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

    # Checkbox para exibir o formulário de exclusão
    exibir_formulario_exclusao = st.checkbox('Exibir Formulário de Exclusão')

    if exibir_formulario_exclusao:
        # Exibir formulário para exclusão de linha
        st.header('Excluir Dados')

        if not df.empty:
            indice_exclusao = st.number_input('Índice da Linha a ser Excluída', min_value=0, max_value=len(df)-1, step=1, value=0)

            if st.button('Excluir'):
                df = df.drop(index=indice_exclusao)
                st.success('Linha excluída com sucesso.')

    # Exibir DataFrame atualizado
    st.header('DataFrame Atualizado')
    st.write(df)

    # Salvar DataFrame em arquivo CSV
    salvar_dataframe(df)

if __name__ == '__main__':
    main()







