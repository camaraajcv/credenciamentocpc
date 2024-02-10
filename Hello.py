import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Função para criar o DataFrame inicial
def create_dataframe():
    data = {
        'SITUAÇÃO ECONSIG': ['Arquivado pela PP1', 'Ativo', 'Bloqueado', 'Arquivado pela CPC'],
        'SUBPROCESSO': ['AQV 16', 'MENS 4', 'MENS 11', 'AQV 22'],
        'CATEGORIA': ['II', 'II', 'II', 'II'],
        'NATUREZA DE DESCONTO': ['MENSALIDADE ASSOCIATIVA', 'MENSALIDADE ASSOCIATIVA', 'MENSALIDADE ASSOCIATIVA', 'MENSALIDADE ASSOCIATIVA'],
        'CONSIGNATÁRIA': ['ASSOCIAÇÃO CENTRO SOCIAL CASSINO DOS SUBOFICIAIS E SARGENTOS - CASUSA GUARATINGUETÁ', 'ASSOCIAÇÃO CENTRO SOCIAL CASSINO DOS SUBOFICIAIS E SARGENTOS - CASUSA GUARATINGUETÁ', 'ADMINISTRAÇÃO DE COMPOSSUIDORES DO BLOCO C DA SQN 204', 'ADMINISTRAÇÃO DE COMPOSSUIDORES DO BLOCO C DA SQN 204'],
        'CNPJ': ['24.119.252/0001-00', '24.119.252/0001-00', '28.440.479/0001-04', '28.440.479/0001-04'],
        'NRO CONTRATO (PORTARIA OU TERMO)': ['PORT DIRAD Nº 17/CPC, DE 09/01/2019', 'PORT DIRAD Nº 99/CPC, DE 19/01/2022', 'PORT DIRAD 410/CPC, DE 14/12/2018', 'PROCESSO REJEITADO, CONFORM DECLARAÇÃO DO PRESIDENTE DA CPC'],
        'BCA OU DOU': ['BCA 018, 31/01/2019', 'BCA 029, DE 10/02/2022', 'BCA 005, DE 09/01/2019', ''],
        'SITUAÇÃO': ['Recredenciado', 'Vigente', '', 'expirado'],
        'DATA EXPIRAÇÃO CONTRATUAL': ['09/01/2023', '19/01/2025', '14/12/2021', '01/01/2023'],
        'NUP': ['67542.010756/2017-67', '67420.015270/2021-88', '67420.023801/2018-19', '67420.015238/2021-01'],
        'CÓDIGO': ['Q2N', 'Q2N', 'Q2W', 'Q2W'],
        'STATUS CREDENCIAMENTO': ['1-Na CPC com pendência da empresa (Ten Aretha). PC ENCAMINHADA PARA A CPC – 23/01/17 2-CREDENCIAMENTO FINALIZADO. PAG ENCONTRA-SE NO ARQUIVO DA PP1.', '1- Encaminhado para CPC em 19/10/2021 (SIGAD 440415), 2- Doc complementar SIGAD 450171.', '1- Encaminhado para CPC,via Chefia imediata, em 13/11/2018; 2 - Retornou para PP1 em 23/04/2019, 3- Solicitação de Inclusão de Elemento de Ligação (documentação INCOMPLETA) -SIGAD 451423.', '1- Encaminhado para CPC em 19/10/2021 (SIGAD 440309)']
    }
    df2 = pd.DataFrame(data)
    return df2

# Função para carregar ou criar o DataFrame
def load_or_create_dataframe():
    if os.path.exists("data.csv"):
        return pd.read_csv("data.csv")
    else:
        df2 = create_dataframe()
        df2.to_csv("data.csv", index=False)
        return df2

def main():
    st.title('CPC - Controle processos')

    # Carregar ou criar o DataFrame
    df2 = load_or_create_dataframe()

    # Exibir DataFrame atualizado
    st.header('Tabela Completa:')
    st.write(df2)

    # Selecionar a ação (Incluir, Editar, Excluir)
    action = st.selectbox('Selecione a ação:', ['Selecione...', 'Incluir', 'Editar', 'Excluir'])

    if action != 'Selecione...':
        if action == 'Incluir':
            st.header('Adicionar Nova Linha:')
            situacao = st.selectbox('SITUAÇÃO ECONSIG:', options=['', 'Arquivado pela PP1', 'Arquivado pela CPC', 'Análise CPC', 'Encaminhado para CPC', 'Encaminhado para PP1', 'Aguardando Documentações', 'Enviado para Homologação', 'Enviado para Publicação', 'Aguardando assinaturas CPC'], index=0)
            subprocesso = st.text_input('SUBPROCESSO:')
            categoria = st.selectbox('CATEGORIA:', options=['', 'I', 'II', 'III'], index=0)
            natureza_desconto = st.selectbox('NATUREZA DE DESCONTO:', options=['', 'MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA', 'CARTÃO DE CRÉDITO', 'Seguro de Vida'], index=0)
            consignataria = st.text_input('CONSIGNATÁRIA:')
            cnpj = st.text_input('CNPJ:')
            cnpj = ''.join(filter(str.isdigit, cnpj))  # Remover caracteres não numéricos
            if len(cnpj) == 14:
                cnpj = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'  # Adicionar máscara se CNPJ tiver 14 dígitos
            contrato = st.text_input('NRO CONTRATO (PORTARIA OU TERMO):')
            bca_dou = st.text_input('BCA OU DOU:')
            situacao_atual = st.text_input('SITUAÇÃO:')
            data_expiracao = st.date_input('DATA EXPIRAÇÃO CONTRATUAL:', format='DD/MM/YYYY')
            if data_expiracao <= datetime.today().date():
                dias_vigencia = 'Expirado'
            else:
                dias_vigencia = (data_expiracao - datetime.today().date()).days
            nup = st.text_input('NUP:')
            codigo = st.text_input('CÓDIGO:')
            status_credenciamento = st.text_input('STATUS CREDENCIAMENTO:')

            # Botão para adicionar nova linha
            if st.button('Adicionar'):
                if situacao == '' or subprocesso == '' or categoria == '' or natureza_desconto == '' or consignataria == '' or cnpj == '' or contrato == '' or bca_dou == '' or situacao_atual == '' or nup == '' or codigo == '' or status_credenciamento == '':
                    st.warning('Todos os campos devem ser preenchidos!')
                else:
                    new_row = pd.DataFrame({
                        'SITUAÇÃO ECONSIG': [situacao],
                        'SUBPROCESSO': [subprocesso],
                        'CATEGORIA': [categoria],
                        'NATUREZA DE DESCONTO': [natureza_desconto],
                        'CONSIGNATÁRIA': [consignataria],
                        'CNPJ': [cnpj],
                        'NRO CONTRATO (PORTARIA OU TERMO)': [contrato],
                        'BCA OU DOU': [bca_dou],
                        'SITUAÇÃO': [situacao_atual],
                        'DATA EXPIRAÇÃO CONTRATUAL': [data_expiracao.strftime('%d/%m/%Y')],
                        'Dias para Fim Vigência': [dias_vigencia],
                        'NUP': [nup],
                        'CÓDIGO': [codigo],
                        'STATUS CREDENCIAMENTO': [status_credenciamento]
                    })
                    df2 = pd.concat([df2, new_row], ignore_index=True)
                    df2.to_csv("data.csv", index=False)
                    st.success('Novo processo adicionado com sucesso!')

        elif action == 'Editar':
            st.header('Editar processo Existente:')
            row_index = st.selectbox('Selecione o número da linha do processo para edição:', options=list(range(len(df2))))
            situacao_edit = st.selectbox('SITUAÇÃO ECONSIG:', options=['', 'Arquivado pela PP1', 'Arquivado pela CPC', 'Análise CPC', 'Encaminhado para CPC', 'Encaminhado para PP1', 'Aguardando Documentações', 'Enviado para Homologação', 'Enviado para Publicação', 'Aguardando assinaturas CPC'], index=['Arquivado pela PP1', 'Arquivado pela CPC', 'Análise CPC', 'Encaminhado para CPC', 'Encaminhado para PP1', 'Aguardando Documentações', 'Enviado para Homologação', 'Enviado para Publicação', 'Aguardando assinaturas CPC'].index(df2.iloc[row_index]['SITUAÇÃO ECONSIG']))
            subprocesso_edit = st.text_input('SUBPROCESSO:', value=df2.iloc[row_index]['SUBPROCESSO'])
            categoria_edit = st.selectbox('CATEGORIA:', options=['', 'I', 'II', 'III'], index=['I', 'II', 'III'].index(df2.iloc[row_index]['CATEGORIA']))
            natureza_desconto_edit = st.selectbox('NATUREZA DE DESCONTO:', options=['', 'MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA', 'CARTÃO DE CRÉDITO', 'Seguro de Vida'], index=['MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA', 'CARTÃO DE CRÉDITO', 'Seguro de Vida'].index(df2.iloc[row_index]['NATUREZA DE DESCONTO']))
            consignataria_edit = st.text_input('CONSIGNATÁRIA:', value=df2.iloc[row_index]['CONSIGNATÁRIA'])
            cnpj_edit = st.text_input('CNPJ:', value=df2.iloc[row_index]['CNPJ'])
            contrato_edit = st.text_input('NRO CONTRATO (PORTARIA OU TERMO):', value=df2.iloc[row_index]['NRO CONTRATO (PORTARIA OU TERMO)'])
            bca_dou_edit = st.text_input('BCA OU DOU:', value=df2.iloc[row_index]['BCA OU DOU'])
            situacao_atual_edit = st.text_input('SITUAÇÃO:', value=df2.iloc[row_index]['SITUAÇÃO'])
            data_expiracao_edit = st.date_input('DATA EXPIRAÇÃO CONTRATUAL:', format='DD/MM/YYYY', value=datetime.strptime(df2.iloc[row_index]['DATA EXPIRAÇÃO CONTRATUAL'], '%d/%m/%Y'))
            if data_expiracao_edit <= datetime.today().date():
                dias_vigencia_edit = 'Expirado'
            else:
                dias_vigencia_edit = (data_expiracao_edit - datetime.today().date()).days
            nup_edit = st.text_input('NUP:', value=df2.iloc[row_index]['NUP'])
            codigo_edit = st.text_input('CÓDIGO:', value=df2.iloc[row_index]['CÓDIGO'])
            status_credenciamento_edit = st.text_input('STATUS CREDENCIAMENTO:', value=df2.iloc[row_index]['STATUS CREDENCIAMENTO'])

            # Botão para editar linha existente
            if st.button('Editar'):
                if situacao_edit == '' or subprocesso_edit == '' or categoria_edit == '' or natureza_desconto_edit == '' or consignataria_edit == '' or cnpj_edit == '' or contrato_edit == '' or bca_dou_edit == '' or situacao_atual_edit == '' or nup_edit == '' or codigo_edit == '' or status_credenciamento_edit == '':
                    st.warning('Todos os campos devem ser preenchidos!')
                else:
                    df2.loc[row_index] = {
                        'SITUAÇÃO ECONSIG': situacao_edit,
                        'SUBPROCESSO': subprocesso_edit,
                        'CATEGORIA': categoria_edit,
                        'NATUREZA DE DESCONTO': natureza_desconto_edit,
                        'CONSIGNATÁRIA': consignataria_edit,
                        'CNPJ': cnpj_edit,
                        'NRO CONTRATO (PORTARIA OU TERMO)': contrato_edit,
                        'BCA OU DOU': bca_dou_edit,
                        'SITUAÇÃO': situacao_atual_edit,
                        'DATA EXPIRAÇÃO CONTRATUAL': data_expiracao_edit.strftime('%d/%m/%Y'),
                        'Dias para Fim Vigência': dias_vigencia_edit,
                        'NUP': nup_edit,
                        'CÓDIGO': codigo_edit,
                        'STATUS CREDENCIAMENTO': status_credenciamento_edit
                    }
                    df2.to_csv("data.csv", index=False)
                    st.success('Linha editada com sucesso!')

        elif action == 'Excluir':
            st.header('Excluir Processo Existente:')
            row_index = st.selectbox('Selecione o número da linha para exclusão:', options=list(range(len(df2))))
            st.write(f'Linha selecionada para exclusão: {row_index}')
            if st.button('Excluir'):
                df2.drop(row_index, inplace=True)
                df2.to_csv("data.csv", index=False)
                st.success('Processo excluída com sucesso!')

if __name__ == "__main__":
    main()
