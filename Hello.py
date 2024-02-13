import streamlit as st
import pandas as pd

# Função para adicionar dados à planilha
def adicionar_dados(file_path, dados):
    df = pd.read_excel(file_path)
    novo_registro = pd.DataFrame([dados], columns=df.columns)
    df = pd.concat([df, novo_registro], ignore_index=True)
    df.to_excel(file_path, index=False)

def main():
    st.title('Inserindo Dados em Planilha Excel')

    # Caminho da planilha
    file_path = 'cpc.xls'

    # Checkbox para exibir o formulário
    exibir_formulario = st.checkbox('Exibir Formulário')

    # Exibir formulário se a opção estiver selecionada
    if exibir_formulario:
        # Formulário para inserir dados
        st.header('Inserir Novos Dados')

        situacao_econsig = st.text_input('Situação Econômica')
        localizacao = st.text_input('Localização')
        categoria = st.text_input('Categoria')
        natureza_desconto = st.text_input('Natureza de Desconto')
        consignataria = st.text_input('Consignatária')
        cnpj = st.text_input('CNPJ')
        nro_contrato = st.text_input('Nro Contrato (Portaria ou Termo)')
        bca_ou_dou = st.text_input('BCA ou DOU')
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
            # Adiciona os dados à planilha
            dados = {'SITUAÇÃO ECONSIG': situacao_econsig, 'LOCALIZAÇÃO': localizacao, 
                     'CATEGORIA': categoria, 'NATUREZA DE DESCONTO': natureza_desconto, 
                     'CONSIGNATÁRIA': consignataria, 'CNPJ': cnpj, 'NRO CONTRATO (PORTARIA OU TERMO)': nro_contrato, 
                     'BCA OU DOU': bca_ou_dou, 'DATA EXPIRAÇÃO CONTRATUAL': data_expiracao_contratual, 
                     'Dias para Fim Vigência': dias_para_fim_vigencia, 'NUP': nup, 'CÓDIGO': codigo, 
                     'STATUS CREDENCIAMENTO': status_credenciamento, 'AÇÃO': acao, 'OFÍCIO PARA EC': oficio_para_ec, 
                     'CPC STATUS': cpc_status, 'Verificado ?': verificado, 'CPC ANUAL': cpc_anual}
            adicionar_dados(file_path, dados)
            st.success('Dados inseridos com sucesso.')

    # Exibe os dados da planilha atualizada
    st.header('Planilha Atualizada')
    df = pd.read_excel(file_path)
    st.write(df)

if __name__ == '__main__':
    main()

