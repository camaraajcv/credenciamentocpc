import streamlit as st
from streamlit_pydantic import st_pydantic
import pandas as pd
import os
import re
from datetime import datetime, date

class DadosInsercao:
    situacao_econsig: str
    localizacao: str
    consignataria: str
    bca_ou_dou: str
    situacao: str
    data_expiracao_contratual: str
    categoria: str
    natureza_desconto: str
    cnpj: str
    nro_contrato: str
    nup: str
    codigo: str
    status_credenciamento: str
    acao: str
    oficio_para_ec: str
    cpc_status: str
    verificado: str
    cpc_anual: str

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

        # Criar um objeto para inserção de dados
        dados = DadosInsercao()

        # Definir a máscara para o CNPJ
        cnpj_mask = '99.999.999/9999-99'

        # Exibir o formulário de inserção de dados
        with col1:
            st.write('Coluna 1')
            st_pydantic(dados, fields={'situacao_econsig': {'label': 'Situação Econômica', 'options': ['Arquivado', 'Ativo', 'Bloqueado', 'Não Cadastrado']},
                                       'localizacao': 'Localização',
                                       'consignataria': 'Consignatária',
                                       'bca_ou_dou': 'BCA ou DOU',
                                       'situacao': 'Situação',
                                       'data_expiracao_contratual': 'Data Expiração Contratual',
                                       'categoria': {'label': 'Categoria', 'options': ['I', 'II', 'III']},
                                       'natureza_desconto': {'label': 'Natureza de Desconto', 'options': ['MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA','CARTÃO DE CRÉDITO', 'SEGURO DE VIDA']},
                                       'cnpj': {'input_type': 'text', 'placeholder': cnpj_mask},
                                       'nro_contrato': 'Nro Contrato (Portaria ou Termo)'})
        with col2:
            st.write('Coluna 2')
            st_pydantic(dados, fields={'nup': 'NUP',
                                       'codigo': 'Código',
                                       'status_credenciamento': 'Status Credenciamento',
                                       'acao': 'Ação',
                                       'oficio_para_ec': 'Ofício para EC',
                                       'cpc_status': {'label': 'CPC Status', 'options': ['EM ANÁLISE', 'CONCLUÍDO', 'ENTREGUE', 'REJEITADO']},
                                       'verificado': 'Verificado?',
                                       'cpc_anual': 'CPC Anual'})

        if st.button('Inserir'):
            if validar_cnpj(dados.cnpj):
                novo_dado = {
                    'SITUAÇÃO ECONSIG': dados.situacao_econsig,
                    'LOCALIZAÇÃO': dados.localizacao,
                    'CATEGORIA': dados.categoria,
                    'NATUREZA DE DESCONTO': dados.natureza_desconto,
                    'CONSIGNATÁRIA': dados.consignataria,
                    'CNPJ': dados.cnpj,
                    'NRO CONTRATO (PORTARIA OU TERMO)': dados.nro_contrato,
                    'BCA OU DOU': dados.bca_ou_dou,
                    'SITUAÇÃO': dados.situacao,
                    'DATA EXPIRAÇÃO CONTRATUAL': dados.data_expiracao_contratual,
                    'Dias para Fim Vigência': dados.dias_para_fim_vigencia,
                    'NUP': dados.nup,
                    'CÓDIGO': dados.codigo,
                    'STATUS CREDENCIAMENTO': dados.status_credenciamento,
                    'AÇÃO': dados.acao,
                    'OFÍCIO PARA EC': dados.oficio_para_ec,
                    'CPC STATUS': dados.cpc_status,
                    'Verificado ?': dados.verificado,
                    'CPC ANUAL': dados.cpc_anual
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
