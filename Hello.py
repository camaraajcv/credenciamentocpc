import streamlit as st
import pandas as pd

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
        
        # Atualiza o arquivo Excel com as linhas excluídas (opcional)
        df.to_excel(excel_url, index=False)  # Descomente esta linha se desejar atualizar o arquivo Excel no GitHub
        
        # Mostra os dados atualizados na tabela
        st.write("## Dados do Excel Atualizados")
        st.write(pd.read_excel(excel_url))

if __name__ == "__main__":
    main()