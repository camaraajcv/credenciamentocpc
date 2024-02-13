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
        colunas = ['SITUAÇÃO ECONSIG', 'SUBOPROCESSO SILOMS', 'CATEGORIA', 'NATUREZA DE DESCONTO', 
                   'CONSIGNATÁRIA', 'CNPJ', 'NRO CONTRATO (PORTARIA OU TERMO)', 
                   'BCA OU DOU', 'SITUAÇÃO', 'DATA EXPIRAÇÃO CONTRATUAL', 
                   'Dias para Fim Vigência', 'NUP', 'CÓDIGO', 'STATUS CREDENCIAMENTO', 
                   'AÇÃO', 'OFÍCIO PARA EC', 'CPC STATUS', 'Verificado ?', 'CPC ANUAL',
                   'Data de Entrada']  # Adiciona a coluna 'Data de Entrada'
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
    st.title('Inserindo, Editando e Excluindo Dados em DataFrame')

    # Carregar ou criar o DataFrame
    df = carregar_dataframe()

    # Checkbox para exibir o formulário de inserção
    exibir_formulario_insercao = st.checkbox('Exibir Formulário de Inserção')

    if exibir_formulario_insercao:
        # Exibir formulário para inserir dados
        st.header('Inserir Novos Dados')

        col1, col2 = st.columns(2)

        with col1:
            situacao_econsig = st.selectbox('Situação Econsig*', options=['', 'Sem Cadastro','Recredenciado', 'Credenciado', 'Aguardando Publicação', 'Arquivado'])
            subprocesso_siloms = st.text_input('SUBOPROCESSO SILOMS*')
            consignataria = st.text_input('Consignatária*')
            bca_ou_dou = st.text_input('BCA ou DOU')
            situacao = st.selectbox('Situação*', options=['', 'Encaminhado para Secretária da CPC', 'Análise Equipe 1', 'Análise Equipe 2', 'Análise Equipe 3', 'Análise Equipe 4', 'Aguardando Assinaturas', 'Encaminhado para a PP1'])
            data_expiracao_contratual = st.date_input('Data Expiração Contratual*', format='DD/MM/YYYY')
            categoria = st.selectbox('Categoria*', options=['', 'I', 'II', 'III'])
            natureza_desconto = st.selectbox('Natureza de Desconto*', options=['', 'MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA','CARTÃO DE CRÉDITO', 'SEGURO DE VIDA'])
            cnpj = st.text_input('CNPJ*', placeholder='XX.XXX.XXX/XXXX-XX')
            data_entrada = st.date_input('Data de Entrada*', format='DD/MM/YYYY')  # Adiciona o campo de Data de Entrada
        with col2:
            data_atual = date.today()  # Obtém a data atual
            dias_para_fim_vigencia = (data_expiracao_contratual - data_atual).days
            if dias_para_fim_vigencia < 0:
                dias_para_fim_vigencia = 'Expirado'
            else:
                dias_para_fim_vigencia = str(dias_para_fim_vigencia) + ' dias'
           
            dias_para_fim_vigencia = st.text_input('Dias para Fim Vigência', value=dias_para_fim_vigencia, disabled=True)
            nup = st.text_input('NUP')
            codigo = st.text_input('Código Caixa')
            status_credenciamento = st.text_input('Status Credenciamento -  Observações')
            acao = st.text_input('Ação')
            oficio_para_ec = st.text_input('Ofício para EC')
            cpc_status = st.selectbox('CPC Status', options=['','EM ANÁLISE', 'CONCLUÍDO', 'ENTREGUE', 'REJEITADO'])
            cpc_anual = st.selectbox('CPC Anual', options=['', 'CPC 2021', 'CPC 2022', 'CPC 2023', 'CPC 2024', 'CPC 2025', 'CPC 2026'])
            verificado = st.selectbox('Verificado?*', options=['', 'Sim', 'Não'])

        if st.button('Inserir'):
            if validar_cnpj(cnpj):
                if consignataria.strip() == '' or situacao.strip() == '' or situacao_econsig.strip() == '' or verificado.strip() == '' or data_entrada is None:
                    st.error('Os campos marcados com * são obrigatórios.')
                else:
                    novo_dado = {
                        'SITUAÇÃO ECONSIG': situacao_econsig,
                        'SUBOPROCESSO SILOMS': subprocesso_siloms,
                        'CATEGORIA': categoria,
                        'NATUREZA DE DESCONTO': natureza_desconto,
                        'CONSIGNATÁRIA': consignataria,
                        'CNPJ': cnpj,
                        'NRO CONTRATO (PORTARIA OU TERMO)': '',
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
                        'CPC ANUAL': cpc_anual,
                        'Data de Entrada': data_entrada.strftime('%d/%m/%Y')  # Adiciona a data de entrada ao DataFrame
                    }

                    novo_df = pd.DataFrame([novo_dado])
                    df = pd.concat([df, novo_df], ignore_index=True)

                    st.success('Dados inseridos com sucesso.')

    # Checkbox para exibir o formulário de edição
    exibir_formulario_edicao = st.checkbox('Exibir Formulário de Edição')

    if exibir_formulario_edicao:
        # Exibir formulário para edição de linha
        st.header('Editar Dados')

        if not df.empty:
            indice_edicao = st.number_input('Índice da Linha a ser Editada', min_value=0, max_value=len(df)-1, step=1, value=0)

            if st.button('Editar'):
                # Preencher o formulário de inserção com os dados da linha selecionada para edição
                linha_selecionada = df.iloc[indice_edicao]
                situacao_econsig = st.selectbox('Situação Econsig*', options=['', 'Sem Cadastro','Recredenciado', 'Credenciado', 'Aguardando Publicação', 'Arquivado'], index=df.columns.get_loc('SITUAÇÃO ECONSIG'))
                subprocesso_siloms = st.text_input('SUBOPROCESSO SILOMS*', value=linha_selecionada['SUBOPROCESSO SILOMS'])
                consignataria = st.text_input('Consignatária*', value=linha_selecionada['CONSIGNATÁRIA'])
                bca_ou_dou = st.text_input('BCA ou DOU', value=linha_selecionada['BCA OU DOU'])
                situacao = st.selectbox('Situação*', options=['', 'Encaminhado para Secretária da CPC', 'Análise Equipe 1', 'Análise Equipe 2', 'Análise Equipe 3', 'Análise Equipe 4', 'Aguardando Assinaturas', 'Encaminhado para a PP1'], index=df.columns.get_loc('SITUAÇÃO'))
                data_expiracao_contratual = st.date_input('Data Expiração Contratual*', format='DD/MM/YYYY', value=datetime.strptime(linha_selecionada['DATA EXPIRAÇÃO CONTRATUAL'], '%d/%m/%Y'))
                categoria = st.selectbox('Categoria*', options=['', 'I', 'II', 'III'], index=df.columns.get_loc('CATEGORIA'))
                natureza_desconto = st.selectbox('Natureza de Desconto*', options=['', 'MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA','CARTÃO DE CRÉDITO', 'SEGURO DE VIDA'], index=df.columns.get_loc('NATUREZA DE DESCONTO'))
                cnpj = st.text_input('CNPJ*', placeholder='XX.XXX.XXX/XXXX-XX', value=linha_selecionada['CNPJ'])
                data_entrada = st.date_input('Data de Entrada*', format='DD/MM/YYYY', value=datetime.strptime(linha_selecionada['Data de Entrada'], '%d/%m/%Y'))  # Adiciona o campo de Data de Entrada
                dias_para_fim_vigencia = st.text_input('Dias para Fim Vigência', value=linha_selecionada['Dias para Fim Vigência'], disabled=True)
                nup = st.text_input('NUP', value=linha_selecionada['NUP'])
                codigo = st.text_input('Código Caixa', value=linha_selecionada['CÓDIGO'])
                status_credenciamento = st.text_input('Status Credenciamento -  Observações', value=linha_selecionada['STATUS CREDENCIAMENTO'])
                acao = st.text_input('Ação', value=linha_selecionada['AÇÃO'])
                oficio_para_ec = st.text_input('Ofício para EC', value=linha_selecionada['OFÍCIO PARA EC'])
                cpc_status = st.selectbox('CPC Status', options=['','EM ANÁLISE', 'CONCLUÍDO', 'ENTREGUE', 'REJEITADO'], index=df.columns.get_loc('CPC STATUS'), value=linha_selecionada['CPC STATUS'])
                cpc_anual = st.selectbox('CPC Anual', options=['', 'CPC 2021', 'CPC 2022', 'CPC 2023', 'CPC 2024', 'CPC 2025', 'CPC 2026'], index=df.columns.get_loc('CPC ANUAL'), value=linha_selecionada['CPC ANUAL'])
                verificado = st.selectbox('Verificado?*', options=['', 'Sim', 'Não'], index=df.columns.get_loc('Verificado ?'), value=linha_selecionada['Verificado ?'])

                if st.button('Alterar'):
                    df.loc[indice_edicao] = {
                        'SITUAÇÃO ECONSIG': situacao_econsig,
                        'SUBOPROCESSO SILOMS': subprocesso_siloms,
                        'CATEGORIA': categoria,
                        'NATUREZA DE DESCONTO': natureza_desconto,
                        'CONSIGNATÁRIA': consignataria,
                        'CNPJ': cnpj,
                        'NRO CONTRATO (PORTARIA OU TERMO)': '',
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
                        'CPC ANUAL': cpc_anual,
                        'Data de Entrada': data_entrada.strftime('%d/%m/%Y')  # Adiciona a data de entrada ao DataFrame
                    }

                    st.success('Dados alterados com sucesso.')

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


