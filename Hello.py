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
def carregar_dataframe():
    try:
        # Carregar o arquivo Excel a partir da URL
        response = requests.get(excel_url)
        response.raise_for_status()  # Lança uma exceção se a solicitação não for bem-sucedida
        # Ler o DataFrame a partir do arquivo Excel
        df = pd.read_excel(response.content, engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio se houver algum erro

# Função para salvar o DataFrame em um arquivo Excel no GitHub
def salvar_dataframe(df):
    try:
        # Salvar DataFrame como um arquivo Excel temporário
        temp_file = "temp_dados_cpc.xlsx"
        df.to_excel(temp_file, index=False)
        
        # Remover o arquivo Excel original, se existir
        if os.path.exists("dados_cpc.xlsx"):
            os.remove("dados_cpc.xlsx")
        
        # Renomear o arquivo temporário para o nome original
        os.rename(temp_file, "dados_cpc.xlsx")
        
        st.success('Dados salvos com sucesso.')
    except Exception as e:
        st.error(f"Erro ao salvar os dados: {e}")
    
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
            subprocesso_siloms = st.text_input('Subprocesso Siloms*')
            subprocesso_siloms = subprocesso_siloms.replace(',', '')

            # Adicionar o valor convertido ao DataFrame
            df['SUBPROCESSO SILOMS'] = pd.to_numeric(subprocesso_siloms, errors='coerce')
            consignataria = st.text_input('Consignatária*')
            bca_ou_dou = st.text_input('BCA ou DOU')
            situacao = st.selectbox('Situação*', options=['', 'Encaminhado para Secretário(a) da CPC', 'Análise Equipe A', 'Análise Equipe B', 'Análise Equipe C', 'Análise Equipe D', 'Análise Equipe E' ,'Aguardando Assinaturas', 'encaminhado para a PP1 (conclusão/arquivamento)','encaminhado para a PP1 para análise'])
            
            categoria = st.selectbox('Categoria*', options=['', 'I', 'II', 'III'])
            natureza_desconto = st.selectbox('Natureza de Desconto*', options=['', 'MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA','CARTÃO DE CRÉDITO', 'SEGURO DE VIDA'])
            cnpj = st.text_input('CNPJ*', placeholder='XX.XXX.XXX/XXXX-XX')
           

        with col2:
            data_entrada = st.date_input('Data de Entrada*', format='DD/MM/YYYY', value=date.today())
            # Obtém a data atual
            data_atual = date.today()

            # Obtém a data de expiração do contrato do usuário
            data_expiracao_contratual = st.date_input('Data Expiração Contratual', None, format='DD/MM/YYYY', key='data_expiracao_contratual')

            # Calcula os dias para o fim da vigência apenas se data_expiracao_contratual não for None
            if data_expiracao_contratual is not None:
                dias_para_fim_vigencia = (data_expiracao_contratual - data_atual).days
                if dias_para_fim_vigencia < 0:
                    dias_para_fim_vigencia = 'Expirado'
                else:
                    dias_para_fim_vigencia = str(dias_para_fim_vigencia) + ' dias'
            else:
                dias_para_fim_vigencia = ''

            # Exibe os dias para o fim da vigência
            st.text_input('Dias para Fim Vigência', value=dias_para_fim_vigencia, disabled=True, key='dias_para_fim_vigencia')
            #nup = st.text_input('NUP')
            codigo = st.text_input('Código Caixa')
            status_credenciamento = st.text_input('Status Credenciamento -  Observações')
            cpc_status = st.selectbox('CPC Status', options=['','EM ANÁLISE', 'CONCLUÍDO', 'ENTREGUE', 'REJEITADO','EM ANÁLISE PP1'])
            cpc_anual = st.selectbox('CPC Anual', options=['', 'CPC 2021', 'CPC 2022', 'CPC 2023', 'CPC 2024', 'CPC 2025', 'CPC 2026'])
            numero_contrato = st.text_input('NRO CONTRATO')
        if st.button('Inserir'):
            if validar_cnpj(cnpj):
                if consignataria.strip() == '' or situacao.strip() == '' or situacao_econsig.strip() == '' :
                    st.error('Os campos marcados com * são obrigatórios.')
                else:
                    novo_dado = {
                        'SITUAÇÃO ECONSIG': situacao_econsig,
                        'SUBPROCESSO SILOMS': subprocesso_siloms,
                        'CATEGORIA': categoria,
                        'NATUREZA DE DESCONTO': natureza_desconto,
                        'CONSIGNATÁRIA': consignataria,
                        'CNPJ': cnpj,
                        'NRO CONTRATO': numero_contrato,
                        'BCA OU DOU': bca_ou_dou,
                        'SITUAÇÃO': situacao,
                        ##'DATA EXPIRAÇÃO CONTRATUAL': data_expiracao_contratual.strftime('%d/%m/%Y'),
                        'Dias para Fim Vigência': dias_para_fim_vigencia,
                        #'NUP': nup,
                        'CÓDIGO': codigo,
                        'STATUS CREDENCIAMENTO': status_credenciamento,
                        'CPC STATUS': cpc_status,
                        'CPC ANUAL': cpc_anual,
                        'DATA DE ENTRADA': data_entrada.strftime('%d/%m/%Y')
                    }

                    novo_df = pd.DataFrame([novo_dado])
                    df = pd.concat([df, novo_df], ignore_index=True)
                    salvar_dataframe(df) 
                    st.success('Dados inseridos com sucesso.')

    if opcao_selecionada == 'excluir':
        # Exibir formulário para exclusão de linha
        st.header('Excluir Dados')

        if not df.empty:
            indice_exclusao = st.number_input('Índice da Linha a ser Excluída', min_value=0, max_value=len(df)-1, step=1, value=0)

            if st.button('Excluir'):
                df = df.drop(index=indice_exclusao)
                st.success('Linha excluída com sucesso.')
                salvar_dataframe(df) 
    if opcao_selecionada == 'editar':
        # Exibir formulário para edição de dados
        st.header('Editar Dados')

        if not df.empty:
            indice_edicao = st.number_input('Índice da Linha a ser Editada', min_value=0, max_value=len(df)-1, step=1, value=0)

            situacoes_disponiveis = ['', 'Sem Cadastro', 'Recredenciado', 'Credenciado', 'Aguardando Publicação', 'Arquivado','Bloqueado','Credenciamento Vencido']
            indice_selecionado = situacoes_disponiveis.index(df.loc[indice_edicao, 'SITUAÇÃO ECONSIG']) if df.loc[indice_edicao, 'SITUAÇÃO ECONSIG'] in situacoes_disponiveis else 0

            situacao_econsig_edit = st.selectbox('Situação Econsig*', options=situacoes_disponiveis, index=indice_selecionado)
            subprocesso_siloms_edit = st.text_input('SUBPROCESSO SILOMS*', value=str(df.loc[indice_edicao, 'SUBPROCESSO SILOMS']), max_chars=6)

        # Remover vírgulas
        subprocesso_siloms_edit = subprocesso_siloms_edit.replace(',', '')

        # Verificar se é um número inteiro
        if subprocesso_siloms_edit.isdigit():
            # Convertendo para inteiro
            subprocesso_siloms_edit = int(subprocesso_siloms_edit)
        else:
            # Se não for um número válido, você pode tratar de acordo com sua lógica
            st.error("Por favor, insira um número inteiro válido.")
            consignataria_edit = st.text_input('Consignatária*', value=df.loc[indice_edicao, 'CONSIGNATÁRIA'])
            bca_ou_dou_edit = st.text_input('BCA ou DOU', value=df.loc[indice_edicao, 'BCA OU DOU'])
            situacao_edit = st.selectbox('Situação*', 
                            options=['', 'Encaminhado para Secretário(a) da CPC', 'Análise Equipe A', 'Análise Equipe B', 'Análise Equipe C', 'Análise Equipe D', 'Análise Equipe E', 'Aguardando Assinaturas', 'Encaminhado para a PP1'], 
                            index=0 if df.loc[indice_edicao, 'SITUAÇÃO'] == '' else ['Encaminhado para Secretário(a) da CPC', 'Análise Equipe A', 'Análise Equipe B', 'Análise Equipe C', 'Análise Equipe D', 'Análise Equipe E','Aguardando Assinaturas',  'encaminhado para a PP1 (conclusão/arquivamento)','encaminhado para a PP1 para análise'].index(df.loc[indice_edicao, 'SITUAÇÃO']) + 1)
            # Tratar a entrada de data com possibilidade de valor None ou NaN
            data_expiracao_contratual_str = str(df.loc[indice_edicao, 'DATA EXPIRAÇÃO CONTRATUAL'])
            if data_expiracao_contratual_str == 'nan' or data_expiracao_contratual_str == '':
                data_expiracao_contratual_edit = st.date_input('Data Expiração Contratual', value=None, format='DD/MM/YYYY')
            else:
                data_expiracao_contratual_edit = st.date_input('Data Expiração Contratual', 
                                                                value=datetime.strptime(data_expiracao_contratual_str, '%d/%m/%Y'), 
                                                                format='DD/MM/YYYY')
            categoria_edit = st.selectbox('Categoria*', 
                            options=['', 'I', 'II', 'III'], 
                            index=['', 'I', 'II', 'III'].index(df.loc[indice_edicao, 'CATEGORIA']))
            natureza_desconto_edit = st.selectbox('Natureza de Desconto*', 
                                    options=['', 'MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA','CARTÃO DE CRÉDITO', 'SEGURO DE VIDA'], 
                                    index=['', 'MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA','CARTÃO DE CRÉDITO', 'SEGURO DE VIDA'].index(df.loc[indice_edicao, 'NATUREZA DE DESCONTO']))
            cnpj_edit = st.text_input('CNPJ*', placeholder='XX.XXX.XXX/XXXX-XX', value=df.loc[indice_edicao, 'CNPJ'])
            data_atual = date.today()  # Obtém a data atual
            # Verificar se data_expiracao_contratual_edit é None antes de calcular dias_para_fim_vigencia
            if data_expiracao_contratual_edit is not None:
                dias_para_fim_vigencia = (data_expiracao_contratual_edit - data_atual).days
                if dias_para_fim_vigencia < 0:
                    dias_para_fim_vigencia = 'Expirado'
                else:
                    dias_para_fim_vigencia = str(dias_para_fim_vigencia) + ' dias'
            else:
                # Lidar com o caso em que data_expiracao_contratual_edit é None
                dias_para_fim_vigencia = ''  # ou qualquer valor que você queira atribuir nesse caso

           # Definir o valor para dias_para_fim_vigencia_edit
            dias_para_fim_vigencia_edit = st.text_input('Dias para Fim Vigência', value=dias_para_fim_vigencia, disabled=True, key='dias_para_fim_vigencia')

            # Verificar se dias_para_fim_vigencia é um número antes de fazer a comparação
            if isinstance(dias_para_fim_vigencia, int) and dias_para_fim_vigencia < 0:
                dias_para_fim_vigencia = 'Expirado'
            elif isinstance(dias_para_fim_vigencia, int):
                dias_para_fim_vigencia = str(dias_para_fim_vigencia) + ' dias'
            dias_para_fim_vigencia_edit = st.text_input('Dias para Fim Vigência', value=dias_para_fim_vigencia, disabled=True)
            #nup_edit = st.text_input('NUP', value=df.loc[indice_edicao, 'NUP'])
            codigo_edit = st.text_input('Código Caixa', value=df.loc[indice_edicao, 'CÓDIGO'])
            status_credenciamento_edit = st.text_input('Status Credenciamento -  Observações', value=df.loc[indice_edicao, 'STATUS CREDENCIAMENTO'])
            # Obtém o valor da coluna 'CPC STATUS' para o índice de edição
            cpc_status_value = df.loc[indice_edicao, 'CPC STATUS']

            # Verifica se o valor é NaN
            if pd.isnull(cpc_status_value):
                # Se for NaN, atribui um valor padrão ou vazio
                cpc_status_value = ''

            # Define as opções do selectbox
            opcoes_cpc_status = ['', 'EM ANÁLISE', 'CONCLUÍDO', 'ENTREGUE', 'REJEITADO', 'EM ANÁLISE PP1']

            # Obtém o índice do valor atual no selectbox
            if cpc_status_value in opcoes_cpc_status:
                indice_cpc_status = opcoes_cpc_status.index(cpc_status_value)
            else:
                # Se o valor atual não estiver na lista de opções, assume o índice 0
                indice_cpc_status = 0

            # Cria o selectbox com o valor atual selecionado
            cpc_status_edit = st.selectbox('CPC Status*', options=opcoes_cpc_status, index=indice_cpc_status)
            cpc_anual_options = ['', 'CPC 2021', 'CPC 2022', 'CPC 2023', 'CPC 2024', 'CPC 2025', 'CPC 2026']
            cpc_anual_initial_index = cpc_anual_options.index(df.loc[indice_edicao, 'CPC ANUAL']) if df.loc[indice_edicao, 'CPC ANUAL'] in cpc_anual_options else 0
            cpc_anual_edit = st.selectbox('CPC Anual', options=cpc_anual_options, index=cpc_anual_initial_index)
            # Assuming df is your DataFrame
            # Check if the value is NaN before conversion
            value_to_convert = df.loc[indice_edicao, 'NRO CONTRATO']
            if pd.isna(value_to_convert):
                value_to_display = ''  # or any other default value or message
            else:
                value_to_display = str(int(value_to_convert))

            numero_contrato_edit = st.text_input('NRO CONTRATO', value=value_to_display)
            data_entrada_edit = st.date_input('Data de Entrada*', value=datetime.strptime(df.loc[indice_edicao, 'DATA DE ENTRADA'], '%d/%m/%Y') if 'DATA DE ENTRADA' in df.columns else datetime.now(), format='DD/MM/YYYY')
            if st.button('Alterar'):
                if validar_cnpj(cnpj_edit):
                    if consignataria_edit.strip() == '' or situacao_edit.strip() == '' or situacao_econsig_edit.strip() == '':
                        st.error('Os campos marcados com * são obrigatórios.')
                    else:
                        df.loc[indice_edicao, 'SITUAÇÃO ECONSIG'] = situacao_econsig_edit
                        df.loc[indice_edicao, 'SUBPROCESSO SILOMS'] = subprocesso_siloms_edit
                        df.loc[indice_edicao, 'CATEGORIA'] = categoria_edit
                        df.loc[indice_edicao, 'NATUREZA DE DESCONTO'] = natureza_desconto_edit
                        df.loc[indice_edicao, 'CONSIGNATÁRIA'] = consignataria_edit
                        df.loc[indice_edicao, 'CNPJ'] = cnpj_edit
                        df.loc[indice_edicao, 'BCA OU DOU'] = bca_ou_dou_edit
                        df.loc[indice_edicao, 'SITUAÇÃO'] = situacao_edit
                        ##df.loc[indice_edicao, 'DATA EXPIRAÇÃO CONTRATUAL'] = data_expiracao_contratual_edit.strftime('%d/%m/%Y')
                        df.loc[indice_edicao, 'Dias para Fim Vigência'] = dias_para_fim_vigencia_edit
                        #df.loc[indice_edicao, 'NUP'] = nup_edit
                        df.loc[indice_edicao, 'CÓDIGO'] = codigo_edit
                        df.loc[indice_edicao, 'STATUS CREDENCIAMENTO'] = status_credenciamento_edit
                        #df.loc[indice_edicao, 'AÇÃO'] = acao_edit
                        #df.loc[indice_edicao, 'OFÍCIO PARA EC'] = oficio_para_ec_edit
                        df.loc[indice_edicao, 'CPC STATUS'] = cpc_status_edit
                        #df.loc[indice_edicao, 'Verificado ?'] = verificado_edit
                        df.loc[indice_edicao, 'CPC ANUAL'] = cpc_anual_edit
                        df.loc[indice_edicao, 'NRO CONTRATO'] = numero_contrato_edit
                        df.loc[indice_edicao, 'DATA DE ENTRADA'] = data_entrada_edit.strftime('%d/%m/%Y')
                        salvar_dataframe(df) 
                        st.success('Dados alterados com sucesso.')
    
    # Exibir DataFrame atualizado
    st.header('Processos Atualizados')
    st.write(df)

    # Salvar DataFrame em arquivo CSV
    salvar_dataframe(df)
    # Configuração para desativar o aviso PyplotGlobalUseWarning
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # Adicionar gráficos e indicadores
    st.header('Indicadores')
    st.subheader('Total de Processos por Situação')
    count_by_situation = df['SITUAÇÃO'].value_counts()
    st.bar_chart(count_by_situation)

    st.subheader('Distribuição das Categorias')
    count_by_category = df['CATEGORIA'].value_counts()
    st.bar_chart(count_by_category)

    st.subheader('Processos por Natureza de Desconto')
    count_by_natureza = df['NATUREZA DE DESCONTO'].value_counts()
    st.write(count_by_natureza)

    st.subheader('Tempo desde a entrada')
    
    # Copie as colunas necessárias do DataFrame original
    tempo_entrada = df[['SUBPROCESSO SILOMS','CNPJ','CONSIGNATÁRIA','DATA DE ENTRADA', 'SITUAÇÃO']].copy()

    # Converta a coluna 'DATA DE ENTRADA' para o tipo datetime
    tempo_entrada['DATA DE ENTRADA'] = pd.to_datetime(tempo_entrada['DATA DE ENTRADA'])

    # Obtenha a data atual como um objeto datetime
    data_atual = pd.to_datetime(date.today())

    # Calcule o número de dias decorridos desde a entrada até a data atual
    tempo_entrada['Dias Decorridos'] = (data_atual - tempo_entrada['DATA DE ENTRADA']).dt.days.abs()

    # Exiba o DataFrame atualizado
    st.write(tempo_entrada.sort_values(by='Dias Decorridos', ascending=False).drop(columns=['DATA DE ENTRADA']))
    


    

    plt.figure(figsize=(8, 6))
    plt.pie(count_by_natureza, labels=count_by_natureza.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot()

    
   
    
    # Adicionar botão para fazer o download do arquivo CSV
    if not df.empty:
        st.subheader('Baixar Arquivo CSV')
        st.download_button(label='Clique aqui para baixar os dados como CSV', data=df.to_csv(index=False), file_name='dados_cpc.xlsx', mime='text/csv')



if __name__ == "__main__":
        main()
