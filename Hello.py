import streamlit as st
import pandas as pd

# Carrega os dados da planilha
@st.cache
def load_data(file_path):
    return pd.read_excel(file_path)

def main():
    st.title('Leitor de Planilha Excel')

    # Carrega os dados
    file_path = 'cpc.xls'
    df = load_data(file_path)

    # Exibe os dados na interface
    st.write(df)

if __name__ == '__main__':
    main()
