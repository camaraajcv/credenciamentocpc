import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime, date
import matplotlib.pyplot as plt
import seaborn as sns
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
# Função para carregar ou criar o DataFrame
def carregar_dataframe():
    if os.path.exists("dados.csv"):
        return pd.read_csv("dados.csv")
    else:
        colunas = ['SITUAÇÃO ECONSIG', 'SUBPROCESSO SILOMS', 'CATEGORIA', 'NATUREZA DE DESCONTO', 
                   'CONSIGNATÁRIA', 'CNPJ', 'NRO CONTRATO (PORTARIA OU TERMO)', 
                   'BCA OU DOU', 'SITUAÇÃO', 'DATA EXPIRAÇÃO CONTRATUAL', 
                   'Dias para Fim Vigência', 'NUP', 'CÓDIGO', 'STATUS CREDENCIAMENTO', 
                   'AÇÃO', 'OFÍCIO PARA EC', 'CPC STATUS', 'Verificado ?', 'CPC ANUAL', 'DATA DE ENTRADA']
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
            situacao_econsig = st.selectbox('Situação Econsig*', options=['', 'Sem Cadastro','Recredenciado', 'Credenciado', 'Aguardando Publicação', 'Arquivado'])
            subprocesso_siloms = st.text_input('SUBPROCESSO SILOMS*',max_chars=6)
            consignataria = st.text_input('Consignatária*')
            bca_ou_dou = st.text_input('BCA ou DOU')
            situacao = st.selectbox('Situação*', options=['', 'Encaminhado para Secretária da CPC', 'Análise Equipe 1', 'Análise Equipe 2', 'Análise Equipe 3', 'Análise Equipe 4', 'Aguardando Assinaturas', 'encaminhado para a PP1 (conclusão/arquivamento)','encaminhado para a PP1 para análise'])
            data_expiracao_contratual = st.date_input('Data Expiração Contratual*', format='DD/MM/YYYY')
            categoria = st.selectbox('Categoria*', options=['', 'I', 'II', 'III'])
            natureza_desconto = st.selectbox('Natureza de Desconto*', options=['', 'MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA','CARTÃO DE CRÉDITO', 'SEGURO DE VIDA'])
            cnpj = st.text_input('CNPJ*', placeholder='XX.XXX.XXX/XXXX-XX')
            data_entrada = st.date_input('Data de Entrada*', format='DD/MM/YYYY', value=date.today())

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
            numero_contrato = st.text_input('NRO CONTRATO (PORTARIA OU TERMO)')
        if st.button('Inserir'):
            if validar_cnpj(cnpj):
                if consignataria.strip() == '' or situacao.strip() == '' or situacao_econsig.strip() == '' or verificado.strip() == '':
                    st.error('Os campos marcados com * são obrigatórios.')
                else:
                    novo_dado = {
                        'SITUAÇÃO ECONSIG': situacao_econsig,
                        'SUBPROCESSO SILOMS': subprocesso_siloms,
                        'CATEGORIA': categoria,
                        'NATUREZA DE DESCONTO': natureza_desconto,
                        'CONSIGNATÁRIA': consignataria,
                        'CNPJ': cnpj,
                        'NRO CONTRATO (PORTARIA OU TERMO)': numero_contrato,
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
                        'DATA DE ENTRADA': data_entrada.strftime('%d/%m/%Y')
                    }

                    novo_df = pd.DataFrame([novo_dado])
                    df = pd.concat([df, novo_df], ignore_index=True)

                    st.success('Dados inseridos com sucesso.')

    if opcao_selecionada == 'excluir':
        # Exibir formulário para exclusão de linha
        st.header('Excluir Dados')

        if not df.empty:
            indice_exclusao = st.number_input('Índice da Linha a ser Excluída', min_value=0, max_value=len(df)-1, step=1, value=0)

            if st.button('Excluir'):
                df = df.drop(index=indice_exclusao)
                st.success('Linha excluída com sucesso.')

    if opcao_selecionada == 'editar':
        # Exibir formulário para edição de dados
        st.header('Editar Dados')

        if not df.empty:
            indice_edicao = st.number_input('Índice da Linha a ser Editada', min_value=0, max_value=len(df)-1, step=1, value=0)

            situacao_econsig_edit = st.selectbox('Situação Econsig*', 
                                    options=['', 'Sem Cadastro', 'Recredenciado', 'Credenciado', 'Aguardando Publicação', 'Arquivado'], 
                                    index=['', 'Sem Cadastro', 'Recredenciado', 'Credenciado', 'Aguardando Publicação', 'Arquivado'].index(df.loc[indice_edicao, 'SITUAÇÃO ECONSIG']) if df.loc[indice_edicao, 'SITUAÇÃO ECONSIG'] in ['Sem Cadastro', 'Recredenciado', 'Credenciado', 'Aguardando Publicação', 'Arquivado'] else 0)
            subprocesso_siloms_edit = st.text_input('SUBPROCESSO SILOMS*', value=df.loc[indice_edicao, 'SUBPROCESSO SILOMS'])
            consignataria_edit = st.text_input('Consignatária*', value=df.loc[indice_edicao, 'CONSIGNATÁRIA'])
            bca_ou_dou_edit = st.text_input('BCA ou DOU', value=df.loc[indice_edicao, 'BCA OU DOU'])
            situacao_edit = st.selectbox('Situação*', 
                            options=['', 'Encaminhado para Secretária da CPC', 'Análise Equipe 1', 'Análise Equipe 2', 'Análise Equipe 3', 'Análise Equipe 4', 'Aguardando Assinaturas', 'Encaminhado para a PP1'], 
                            index=0 if df.loc[indice_edicao, 'SITUAÇÃO'] == '' else ['Encaminhado para Secretária da CPC', 'Análise Equipe 1', 'Análise Equipe 2', 'Análise Equipe 3', 'Análise Equipe 4', 'Aguardando Assinaturas',  'encaminhado para a PP1 (conclusão/arquivamento)','encaminhado para a PP1 para análise'].index(df.loc[indice_edicao, 'SITUAÇÃO']) + 1)
            data_expiracao_contratual_edit = st.date_input('Data Expiração Contratual*', value=datetime.strptime(df.loc[indice_edicao, 'DATA EXPIRAÇÃO CONTRATUAL'], '%d/%m/%Y'), format='DD/MM/YYYY')
            categoria_edit = st.selectbox('Categoria*', 
                            options=['', 'I', 'II', 'III'], 
                            index=['', 'I', 'II', 'III'].index(df.loc[indice_edicao, 'CATEGORIA']))
            natureza_desconto_edit = st.selectbox('Natureza de Desconto*', 
                                    options=['', 'MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA','CARTÃO DE CRÉDITO', 'SEGURO DE VIDA'], 
                                    index=['', 'MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA','CARTÃO DE CRÉDITO', 'SEGURO DE VIDA'].index(df.loc[indice_edicao, 'NATUREZA DE DESCONTO']))
            cnpj_edit = st.text_input('CNPJ*', placeholder='XX.XXX.XXX/XXXX-XX', value=df.loc[indice_edicao, 'CNPJ'])
            data_atual = date.today()  # Obtém a data atual
            dias_para_fim_vigencia = (data_expiracao_contratual_edit - data_atual).days
            if dias_para_fim_vigencia < 0:
                dias_para_fim_vigencia = 'Expirado'
            else:
                dias_para_fim_vigencia = str(dias_para_fim_vigencia) + ' dias'
            dias_para_fim_vigencia_edit = st.text_input('Dias para Fim Vigência', value=dias_para_fim_vigencia, disabled=True)
            nup_edit = st.text_input('NUP', value=df.loc[indice_edicao, 'NUP'])
            codigo_edit = st.text_input('Código Caixa', value=df.loc[indice_edicao, 'CÓDIGO'])
            status_credenciamento_edit = st.text_input('Status Credenciamento -  Observações', value=df.loc[indice_edicao, 'STATUS CREDENCIAMENTO'])
            acao_edit = st.text_input('Ação', value=df.loc[indice_edicao, 'AÇÃO'])
            oficio_para_ec_edit = st.text_input('Ofício para EC', value=df.loc[indice_edicao, 'OFÍCIO PARA EC'])
            cpc_status_edit = st.selectbox('CPC Status', 
                                options=['','EM ANÁLISE', 'CONCLUÍDO', 'ENTREGUE', 'REJEITADO'], 
                                index=['','EM ANÁLISE', 'CONCLUÍDO', 'ENTREGUE', 'REJEITADO'].index(df.loc[indice_edicao, 'CPC STATUS']))
            cpc_anual_options = ['', 'CPC 2021', 'CPC 2022', 'CPC 2023', 'CPC 2024', 'CPC 2025', 'CPC 2026']
            cpc_anual_initial_index = cpc_anual_options.index(df.loc[indice_edicao, 'CPC ANUAL']) if df.loc[indice_edicao, 'CPC ANUAL'] in cpc_anual_options else 0
            cpc_anual_edit = st.selectbox('CPC Anual', options=cpc_anual_options, index=cpc_anual_initial_index)
            verificado_options = ['', 'Sim', 'Não']
            verificado_initial_index = verificado_options.index(df.loc[indice_edicao, 'Verificado ?']) if df.loc[indice_edicao, 'Verificado ?'] in verificado_options else 0
            verificado_edit = st.selectbox('Verificado?*', options=verificado_options, index=verificado_initial_index)
            numero_contrato_edit = st.text_input('NRO CONTRATO (PORTARIA OU TERMO)', value=df.loc[indice_edicao, 'NRO CONTRATO (PORTARIA OU TERMO)'])
            data_entrada_edit = st.date_input('Data de Entrada*', value=datetime.strptime(df.loc[indice_edicao, 'DATA DE ENTRADA'], '%d/%m/%Y') if 'DATA DE ENTRADA' in df.columns else datetime.now(), format='DD/MM/YYYY')
            if st.button('Alterar'):
                if validar_cnpj(cnpj_edit):
                    if consignataria_edit.strip() == '' or situacao_edit.strip() == '' or situacao_econsig_edit.strip() == '' or verificado_edit.strip() == '':
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
                        df.loc[indice_edicao, 'DATA EXPIRAÇÃO CONTRATUAL'] = data_expiracao_contratual_edit.strftime('%d/%m/%Y')
                        df.loc[indice_edicao, 'Dias para Fim Vigência'] = dias_para_fim_vigencia_edit
                        df.loc[indice_edicao, 'NUP'] = nup_edit
                        df.loc[indice_edicao, 'CÓDIGO'] = codigo_edit
                        df.loc[indice_edicao, 'STATUS CREDENCIAMENTO'] = status_credenciamento_edit
                        df.loc[indice_edicao, 'AÇÃO'] = acao_edit
                        df.loc[indice_edicao, 'OFÍCIO PARA EC'] = oficio_para_ec_edit
                        df.loc[indice_edicao, 'CPC STATUS'] = cpc_status_edit
                        df.loc[indice_edicao, 'Verificado ?'] = verificado_edit
                        df.loc[indice_edicao, 'CPC ANUAL'] = cpc_anual_edit
                        df.loc[indice_edicao, 'NRO CONTRATO (PORTARIA OU TERMO)'] = numero_contrato_edit
                        df.loc[indice_edicao, 'DATA DE ENTRADA'] = data_entrada_edit.strftime('%d/%m/%Y')

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

    st.subheader('Percentual por Natureza de Desconto')
    count_by_natureza = df['NATUREZA DE DESCONTO'].value_counts()
    st.write(count_by_natureza)
    plt.figure(figsize=(8, 6))
    plt.pie(count_by_natureza, labels=count_by_natureza.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot()

    st.header('Gráficos')
   
    st.subheader('Correlação entre Dias para Fim Vigência e CPC Anual')

    # Converter a coluna 'Dias para Fim Vigência' para numérica
    df['Dias para Fim Vigência'] = pd.to_numeric(df['Dias para Fim Vigência'].str.split(' ').str[0])

    # Ordenar o DataFrame pela coluna 'Dias para Fim Vigência'
    df_sorted = df.sort_values(by='Dias para Fim Vigência')

    # Plotar o gráfico de dispersão com o DataFrame ordenado
    fig, ax = plt.subplots()
    sns.scatterplot(data=df_sorted, x='Dias para Fim Vigência', y='CPC ANUAL', ax=ax)
    st.pyplot(fig)



if __name__ == "__main__":
    main()