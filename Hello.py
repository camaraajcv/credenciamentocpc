import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date
import re
import warnings

# Suprimindo o aviso específico
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable")
# Função para inserir dados no banco de dados
def insert_data(data):
    try:
        # Conexão com o banco de dados MySQL
        conn = mysql.connector.connect(
            host="monorail.proxy.rlwy.net",
            user="root",
            password="IavrTTLyCOohONgVOMWTdepOQrWuJHQO",
            database="railway",
            port=52280
        )

        # Verifica se a conexão foi bem-sucedida
        if conn.is_connected():
            cursor = conn.cursor()

            # Prepara a instrução SQL para inserir os dados
            sql = """
            INSERT INTO credenciamentocpc 
            (situacao_econsig, subprocesso_siloms, categoria, natureza_de_desconto, consignataria, cnpj, nro_contrato, dou, situacao, data_expiracao_contratual, codigo, status_credenciamento, cpc_status, cpc_anual, data_entrada) 
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Executa a instrução SQL
            cursor.execute(sql, data)

            # Confirma a transação
            conn.commit()

            # Fecha o cursor e a conexão
            cursor.close()
            conn.close()

            return True
        else:
            print("Erro ao conectar ao banco de dados MySQL.")
            return False

    except Exception as e:
        print("Erro durante a inserção de dados:", e)
        return False
# Função para validar o CNPJ
def validar_cnpj(cnpj):
    if not re.match(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', cnpj):
        st.error('O CNPJ deve ter o formato XX.XXX.XXX/XXXX-XX')
        return False
    return True

# Função principal
def main():
    st.title('Banco de Dados CredenciamentoCPC')

    # Opções de menu
    opcao_selecionada = st.radio('Selecione uma opção:', ['Visualizar', 'Inserir'])

    # Conexão com o banco de dados MySQL
    conn = mysql.connector.connect(
        host="monorail.proxy.rlwy.net",
        user="root",
        password="IavrTTLyCOohONgVOMWTdepOQrWuJHQO",
        database="railway",
        port=52280
    )

    # Verifica se a conexão foi bem-sucedida
    if conn.is_connected():
        # Consulta SQL para recuperar todos os dados da tabela
        query = "SELECT * FROM credenciamentocpc"

        # Carrega os dados do banco de dados em um DataFrame pandas
        df = pd.read_sql(query, conn)

        # Fecha a conexão
        conn.close()

        # Mostra o DataFrame apenas se a opção selecionada for 'Visualizar'
        if opcao_selecionada == 'Visualizar':
            st.write("## Dados do Banco de Dados:")
            st.write(df)

        # Se a opção selecionada for 'Inserir', mostra o formulário para inserir dados
        elif opcao_selecionada == 'Inserir':
            st.write("## Inserir Dados:")

            # Divide o formulário em duas colunas
            col1, col2 = st.columns(2)

            # Coleta os dados do usuário através de inputs
            with col1:
                situacao_econsig = st.selectbox('Situação Econsig*', options=[''] + ['Sem Cadastro', 'Recredenciado', 'Credenciado', 'Aguardando Publicação', 'Arquivado', 'Bloqueado', 'Credenciamento Vencido'])
                subprocesso_siloms = st.text_input('Subprocesso Siloms*')
                categoria = st.selectbox('Categoria*', options=[''] + ['I', 'II', 'III'])
                natureza_de_desconto = st.selectbox('Natureza de Desconto*', options=[''] + ['MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA', 'CARTÃO DE CRÉDITO', 'SEGURO DE VIDA'])
                consignataria = st.text_input('Consignatária*')
                cnpj = st.text_input('CNPJ*', placeholder='XX.XXX.XXX/XXXX-XX')
                nro_contrato = st.text_input('NRO CONTRATO*')
                dou = st.text_input('DOU')

            with col2:
                situacao = st.selectbox('Situação*', options=[''] + ['Encaminhado para Secretário(a) da CPC', 'Análise Equipe A', 'Análise Equipe B', 'Análise Equipe C', 'Análise Equipe D', 'Análise Equipe E' ,'Aguardando Assinaturas', 'Encaminhado para a PP1 (conclusão/arquivamento)', 'Encaminhado para a PP1 para análise'])
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
                codigo = st.text_input('Código Caixa')
                status_credenciamento = st.text_input('Status Credenciamento - Observações')
                cpc_status = st.selectbox('CPC Status', options=[''] + ['EM ANÁLISE', 'CONCLUÍDO', 'ENTREGUE', 'REJEITADO','EM ANÁLISE PP1'])
                cpc_anual = st.selectbox('CPC Anual', options=[''] + ['CPC 2021', 'CPC 2022', 'CPC 2023', 'CPC 2024', 'CPC 2025', 'CPC 2026'])
                data_entrada = st.date_input('Data de Entrada', None, format='DD/MM/YYYY')

            # Botão para enviar os dados
            if st.button("Enviar"):
                # Verifica se todos os campos obrigatórios foram preenchidos
                if (
                    situacao_econsig and subprocesso_siloms and categoria and
                    natureza_de_desconto and consignataria and cnpj and nro_contrato and
                    situacao and data_entrada
                ):
                    # Tenta inserir os dados no banco de dados
                    data = (
                        situacao_econsig, subprocesso_siloms, categoria,
                        natureza_de_desconto, consignataria, cnpj, nro_contrato,
                        dou, situacao, data_expiracao_contratual, codigo,
                        status_credenciamento, cpc_status, cpc_anual, data_entrada
                    )
                    if insert_data(data):
                        st.success("Dados inseridos com sucesso!")
                    else:
                        st.error("Erro ao inserir os dados. Verifique a conexão com o banco de dados.")
                else:
                    st.warning("Por favor, preencha todos os campos obrigatórios.")

# Executa a função principal
if __name__ == "__main__":
    main()

