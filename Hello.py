import streamlit as st
import mysql.connector
import pandas as pd

def insert_data(data):
    # Estabelece a conexão com o banco de dados MySQL
    conn = mysql.connector.connect(
        host="monorail.proxy.rlwy.net",
        user="root",
        password="IavrTTLyCOohONgVOMWTdepOQrWuJHQO",
        database="railway",
        port=52280
    )

    # Verifica se a conexão foi bem-sucedida
    if conn.is_connected():
        # Cria um cursor para executar comandos SQL
        cursor = conn.cursor()

        # Define a consulta SQL para inserir os dados
        query = """
        INSERT INTO credenciamentocpc (
            SITUACAO_ECONSIG,
            SUBPROCESSO_SILOMS,
            CATEGORIA,
            NATUREZA_DE_DESCONTO,
            CONSIGNATARIA,
            CNPJ,
            NRO_CONTRATO,
            DOU,
            SITUACAO,
            DATA_EXPIRACAO_CONTRATUAL,
            Dias_para_Fim_Vigencia,
            CODIGO,
            STATUS_CREDENCIAMENTO,
            CPC_STATUS,
            CPC_ANUAL,
            DATA_DE_ENTRADA
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Executa a consulta SQL com os parâmetros
        cursor.execute(query, data)

        # Comita as mudanças no banco de dados
        conn.commit()

        # Fecha o cursor e a conexão
        cursor.close()
        conn.close()

        # Retorna True para indicar que a inserção foi bem-sucedida
        return True
    else:
        # Retorna False se não foi possível conectar ao banco de dados
        return False

def main():
    st.title('Banco de Dados CredenciamentoCPC')

    # Estabelece a conexão com o banco de dados MySQL
    conn = mysql.connector.connect(
        host="monorail.proxy.rlwy.net",
        user="root",
        password="IavrTTLyCOohONgVOMWTdepOQrWuJHQO",
        database="railway",
        port=52280
    )

    # Verifica se a conexão foi bem-sucedida
    if conn.is_connected():
        # Define a consulta SQL para recuperar todos os dados da tabela
        query = "SELECT * FROM credenciamentocpc"

        # Carrega os dados do banco de dados em um DataFrame pandas
        df = pd.read_sql(query, conn)

        # Fecha a conexão
        conn.close()

        # Mostra o DataFrame
        st.write("## Dados do Banco de Dados:")
        st.write(df)
    else:
        st.error("Erro ao conectar ao banco de dados MySQL.")

    # Botão para mostrar o formulário de inserção
    if st.button("Inserir"):
        # Coleta os dados do usuário através de inputs
        situacao_econsig = st.text_input("SITUACAO_ECONSIG:")
        subprocesso_siloms = st.text_input("SUBPROCESSO_SILOMS:")
        categoria = st.text_input("CATEGORIA:")
        natureza_de_desconto = st.text_input("NATUREZA_DE_DESCONTO:")
        consignataria = st.text_input("CONSIGNATARIA:")
        cnpj = st.text_input("CNPJ:")
        nro_contrato = st.text_input("NRO_CONTRATO:")
        dou = st.text_input("DOU:")
        situacao = st.text_input("SITUACAO:")
        data_expiracao_contratual = st.text_input("DATA_EXPIRACAO_CONTRATUAL:")
        dias_para_fim_vigencia = st.text_input("Dias_para_Fim_Vigencia:")
        codigo = st.text_input("CODIGO:")
        status_credenciamento = st.text_input("STATUS_CREDENCIAMENTO:")
        cpc_status = st.text_input("CPC_STATUS:")
        cpc_anual = st.text_input("CPC_ANUAL:")
        data_de_entrada = st.text_input("DATA_DE_ENTRADA:")

        # Botão para enviar os dados
        if st.button("Enviar"):
            # Verifica se todos os campos estão preenchidos
            if (
                situacao_econsig and subprocesso_siloms and categoria and
                natureza_de_desconto and consignataria and cnpj and
                nro_contrato and dou and situacao and data_expiracao_contratual and
                dias_para_fim_vigencia and codigo and status_credenciamento and
                cpc_status and cpc_anual and data_de_entrada
            ):
                # Tenta inserir os dados no banco de dados
                data = (
                    situacao_econsig, subprocesso_siloms, categoria,
                    natureza_de_desconto, consignataria, cnpj, nro_contrato,
                    dou, situacao, data_expiracao_contratual, dias_para_fim_vigencia,
                    codigo, status_credenciamento, cpc_status, cpc_anual,
                    data_de_entrada
                )
                if insert_data(data):
                    st.success("Dados inseridos com sucesso!")
                else:
                    st.error("Erro ao inserir os dados. Verifique a conexão com o banco de dados.")
            else:
                st.warning("Por favor, preencha todos os campos.")

if __name__ == "__main__":
    main()
