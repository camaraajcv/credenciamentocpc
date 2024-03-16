import streamlit as st
import pandas as pd
import os

def main():
    st.title('Aplicativo para Visualização e Edição de Dados Excel')

    # URL do arquivo Excel no GitHub
    excel_url = "dados_cpc.xlsx"

    # Carrega o DataFrame a partir do Excel
    df = pd.read_excel(excel_url)

    # Mostra os dados na tabela
    st.write("## Dados do Excel")
    st.write(df)

    # Opção para selecionar linhas para exclusão
    rows_to_delete = st.multiselect("Selecione as linhas para excluir", df.index)

    if st.button("Excluir Linhas"):
        # Exclui as linhas selecionadas do DataFrame
        df = df.drop(index=rows_to_delete)

        # Define o caminho absoluto para salvar o arquivo Excel
        new_excel_filepath = os.path.join(os.getcwd(), "dados_cpc_modificado.xlsx")

        # Salva um novo arquivo Excel com os dados atualizados
        df.to_excel(new_excel_filepath, index=False)

        # Mostra mensagem de confirmação
        st.success(f"As linhas selecionadas foram excluídas. Um novo arquivo Excel foi salvo como {new_excel_filepath}.")

        # Mostra os dados atualizados na tabela
        st.write("## Dados do Excel Atualizados")
        st.write(df)

if __name__ == "__main__":
    main()