import streamlit as st
import mysql.connector
import pandas as pd

def main():
    st.title('Dados do Banco de Dados')

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

        # Mostra o DataFrame
        st.write("## Dados do Banco de Dados:")
        st.write(df)

        # Fecha a conexão
        conn.close()
    else:
        st.error("Erro ao conectar ao banco de dados MySQL.")

if __name__ == "__main__":
    main()