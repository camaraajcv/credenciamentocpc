import streamlit as st
import mysql.connector

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
        # Cria um cursor para executar comandos SQL
        cursor = conn.cursor()

        # Define a consulta SQL para recuperar os dados
        query = "SELECT * FROM credenciamentocpc"

        # Executa a consulta SQL
        cursor.execute(query)

        # Recupera os resultados da consulta
        results = cursor.fetchall()

        # Mostra os dados existentes
        st.write("## Dados Existente:")
        for row in results:
            st.write(f"Nome: {row[0]}, Idade: {row[1]}")

        # Fecha o cursor e a conexão
        cursor.close()
        conn.close()
    else:
        st.error("Erro ao conectar ao banco de dados MySQL.")

if __name__ == "__main__":
    main()
