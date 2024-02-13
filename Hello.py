import streamlit as st
import pandas as pd

def main():
    st.title('Inserindo Dados em DataFrame')

    # Criar DataFrame vazio com as colunas desejadas
    colunas = ['SITUAÇÃO ECONSIG', 'LOCALIZAÇÃO', 'CATEGORIA', 'NATUREZA DE DESCONTO', 
               'CONSIGNATÁRIA', 'CNPJ', 'NRO CONTRATO (PORTARIA OU TERMO)', 
               'BCA OU DOU', 'SITUAÇÃO', 'DATA EXPIRAÇÃO CONTRATUAL', 
               'Dias para Fim Vigência', 'NUP', 'CÓDIGO', 'STATUS CREDENCIAMENTO', 
               'AÇÃO', 'OFÍCIO PARA EC', 'CPC STATUS', 'Verificado ?', 'CPC ANUAL']

    df = pd.DataFrame(columns=colunas)

    # Exibir formulário para inserir dados
    st.header('Inserir Novos Dados')

    situacao_econsig = st.text_input('Situação Econômica')
    localizacao = st.text_input('Localização')
    categoria = st.text_input('Categoria')
    natureza_desconto = st.text_input('Natureza de Desconto')
    consignataria = st.text_input('Consignatária')
    cnpj = st.text_input('CNPJ')
    nro_contrato = st.text_input('Nro Contrato (Portaria ou Termo)')
    bca_ou_dou = st.text_input('BCA ou DOU')
    situacao = st.text_input('Situação')
    data_expiracao_contratual = st.text_input('Data Expiração Contratual')
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

        df = df.append(novo_dado, ignore_index=True)

        st.success('Dados inseridos com sucesso.')

    # Exibir DataFrame atualizado
    st.header('DataFrame Atualizado')
    st.write(df)

if __name__ == '__main__':
    main()



