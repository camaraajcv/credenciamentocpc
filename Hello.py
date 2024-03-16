import streamlit as st
import pandas as pd

def main():
    st.title('Aplicativo para Visualização de Dados Excel')

    # URL do arquivo Excel no GitHub
    excel_url = "dados_cpc.xlsx"

    # Lê o arquivo Excel diretamente da URL
    df = pd.read_excel(excel_url)

    # Mostrar os dados na tabela
    st.write("## Dados do Excel")
    st.write(df)

if __name__ == "__main__":
    main()