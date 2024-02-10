import streamlit as st
from streamlit_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

# Função para criar dataframe de exemplo
def create_dataframe():
    data = {
        'Nome': ['João', 'Maria', 'Carlos'],
        'Idade': [25, 30, 35],
        'Cidade': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte']
    }
    df = pd.DataFrame(data)
    return df

# Função principal
def main():
    st.title('Edição de DataFrame')

    # Criando o dataframe
    df = create_dataframe()

    # Exibindo o dataframe com a tabela interativa
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=True)
    gridOptions = gb.build()
    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        height=500,
        width='100%',
        update_mode=GridUpdateMode.VALUE_CHANGED,
        data_return_mode=DataReturnMode.DATAFRAME,
        allow_unsafe_jscode=True,  # Permitindo a execução de código JavaScript não seguro
    )

    # Atualizando o dataframe com os dados editados
    if grid_response['event'] == 'gridUpdate':
        edited_df = grid_response['data']
        st.write(edited_df)

# Executando o aplicativo
if __name__ == '__main__':
    main()
