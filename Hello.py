import streamlit as st
import mysql.connector

def insert_data(nome, idade):
    # Estabelece a conexão com o banco de dados MySQL
    conn = mysql.connector.connect(
        host="seu_host",
        user="seu_usuario",
        password="sua_senha",
        database="seu_banco_de_dados",
        port=52280  # Porta do MySQL alterada para 52280
    )

    # Verifica se a conexão foi bem-sucedida
    if conn.is_connected():
        # Cria um cursor para executar comandos SQL
        cursor = conn.cursor()

        # Define a consulta SQL para inserir os dados
        query = "INSERT INTO sua_tabela (nome, idade) VALUES (%s, %s)"

        # Executa a consulta SQL com os parâmetros
        cursor.execute(query, (nome, idade))

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
    st.title('Formulário de Inserção de Dados')

    # Botão para mostrar os dados existentes
    if st.button("Mostrar Dados"):
        # Estabelece a conexão com o banco de dados MySQL
        conn = mysql.connector.connect(
        host="monorail.proxy.rlwy.net",
        user="root",
        password="IavrTTLyCOohONgVOMWTdepOQrWuJHQO",
        database="railway",
        port = 52280
    )
   

        # Verifica se a conexão foi bem-sucedida
        if conn.is_connected():
            # Cria um cursor para executar comandos SQL
            cursor = conn.cursor()

            # Define a consulta SQL para recuperar os dados
            query = "SELECT * FROM sua_tabela"

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

    # Botão para mostrar o formulário de inserção
    if st.button("Mais"):
        # Coleta os dados do usuário através de inputs
        nome = st.text_input("Nome:")
        idade = st.number_input("Idade:")

        # Botão para enviar os dados
        if st.button("Enviar"):
            # Verifica se os campos estão preenchidos
            if nome and idade:
                # Tenta inserir os dados no banco de dados
                if insert_data(nome, idade):
                    st.success("Dados inseridos com sucesso!")
                else:
                    st.error("Erro ao inserir os dados. Verifique a conexão com o banco de dados.")
            else:
                st.warning("Por favor, preencha todos os campos.")

if __name__ == "__main__":
    main()
