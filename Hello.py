import streamlit as st
import mysql.connector
import pandas as pd

def main():
    st.title('Aplicativo para Visualização de Dados MySQL')

    # Conexão ao banco de dados MySQL
    conn = mysql.connector.connect(
        host="monorail.proxy.rlwy.net",
        user="root",
        password="IavrTTLyCOohONgVOMWTdepOQrWuJHQO",
        database="railway",
        port = 52280
    )

    # Verifica se a conexão foi bem-sucedida
    if conn.is_connected():
        st.write("Conexão ao banco de dados MySQL bem-sucedida.")

        # Executa uma consulta SQL
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM railway")

        # Recupera os resultados da consulta
        results = cursor.fetchall()

        # Cria um DataFrame pandas com os resultados
        df = pd.DataFrame(results, columns=cursor.column_names)

        # Mostra os dados na tabela
        st.write("## Dados do Banco de Dados")
        st.write(df)

        # Fecha a conexão
        cursor.close()
        conn.close()
    else:
        st.error("Erro ao conectar ao banco de dados MySQL.")

if __name__ == "__main__":
    main()