import streamlit as st
import pandas as pd
import time

# Função para ler o arquivo Excel sem cache
@st.cache(allow_output_mutation=True)
def load_excel_data(excel_url):
    return pd.read_excel(excel_url)

def main():
    st.title('Aplicativo para Visualização e Edição de Dados Excel')

    # URL do arquivo Excel no GitHub
    excel_url = "dados_cpc.xlsx"

    # Carrega o DataFrame a partir do Excel
    df = load_excel_data(excel_url)

    # Mostra os dados na tabela
    st.write("## Dados do Excel")
    st.write(df)

    # Opção para selecionar linhas para exclusão
    rows_to_delete = st.multiselect("Selecione as linhas para excluir", df.index)

    if st.button("Excluir Linhas"):
        # Exclui as linhas selecionadas do DataFrame
        df = df.drop(index=rows_to_delete)

        # Salva o DataFrame modificado localmente
        df.to_excel("dados_cpc_modificado.xlsx", index=False)

        # Mostra mensagem de confirmação
        st.success("Linhas excluídas com sucesso!")

        # Mostra os dados atualizados na tabela
        st.write("## Dados do Excel Atualizados")
        st.write(df)

if __name__ == "__main__":
    main()