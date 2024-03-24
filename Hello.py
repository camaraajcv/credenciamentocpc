import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date
import re
import warnings

# URL da imagem
image_url = "https://www.fab.mil.br/om/logo/mini/dirad2.jpg"

#Código HTML e CSS para ajustar a largura da imagem para 20% da largura da coluna e centralizar
html_code = f'<div style="display: flex; justify-content: center;"><img src="{image_url}" alt="Imagem" style="width:8vw;"/></div>'
# Exibir a imagem usando HTML
st.markdown(html_code, unsafe_allow_html=True)

# Centralizar o texto abaixo da imagem
st.markdown("<h1 style='text-align: center; font-size: 1.5em;'>DIRETORIA DE ADMINISTRAÇÃO DA AERONÁUTICA</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-size: 1.2em;'>SUBDIRETORIA DE PAGAMENTO DE PESSOAL</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 1em; text-decoration: underline;'>PP1 - DIVISÃO DE DESCONTOS</h3>", unsafe_allow_html=True)

# Texto explicativo
st.write("CPC - Comissão Permanente de Credenciamento")
# Suprimindo o aviso específico
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable")
# Função para buscar um registro específico no banco de dados
def fetch_single_data(id_to_edit):
    try:
        conn = mysql.connector.connect(
            host="monorail.proxy.rlwy.net",
            user="root",
            password="IavrTTLyCOohONgVOMWTdepOQrWuJHQO",
            database="railway",
            port=52280
        )

        if conn.is_connected():
            cursor = conn.cursor()

            sql = "SELECT * FROM credenciamentocpc WHERE id = %s"

            cursor.execute(sql, (id_to_edit,))
            data = cursor.fetchone()

            cursor.close()
            conn.close()

            return data
    except mysql.connector.Error as err:
        print(f"Erro ao executar a consulta SQL: {err}")
    except Exception as e:
        print(f"Erro desconhecido: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
   

# Função para atualizar um registro específico no banco de dados
def update_data(id_to_edit, new_data):
    try:
        # Conexão com o banco de dados MySQL
        conn = mysql.connector.connect(
            host="monorail.proxy.rlwy.net",
            user="root",
            password="IavrTTLyCOohONgVOMWTdepOQrWuJHQO",
            database="railway",
            port=52280
        )

        # Verifica se a conexão foi bem-sucedida
        if conn.is_connected():
            cursor = conn.cursor()

            # Prepara a instrução SQL para atualizar os dados
            sql = "UPDATE credenciamentocpc SET situacao_econsig = %s, subprocesso_siloms = %s, categoria = %s, natureza_de_desconto = %s, consignataria = %s, cnpj = %s, nro_contrato = %s, dou = %s, situacao = %s, data_expiracao_contratual = %s, codigo = %s, status_credenciamento = %s, cpc_status = %s, cpc_anual = %s, data_de_entrada = %s WHERE id = %s"

            # Adiciona o ID à lista de dados a serem atualizados
            new_data.append(id_to_edit)

            # Executa a instrução SQL
            cursor.execute(sql, new_data)

            # Confirma a transação
            conn.commit()

            # Fecha o cursor e a conexão
            cursor.close()
            conn.close()

            return True

    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar os dados: {err}")
        return False
def fetch_all_data():
    try:
        # Conexão com o banco de dados MySQL
        conn = mysql.connector.connect(
            host="monorail.proxy.rlwy.net",
            user="root",
            password="IavrTTLyCOohONgVOMWTdepOQrWuJHQO",
            database="railway",
            port=52280
        )

        # Verifica se a conexão foi bem-sucedida
        if conn.is_connected():
            cursor = conn.cursor()

            # Prepara a instrução SQL para selecionar todos os dados
            sql = "SELECT * FROM credenciamentocpc"

            # Executa a instrução SQL
            cursor.execute(sql)

            # Obtém todos os dados
            data = cursor.fetchall()

            # Obtém os nomes das colunas
            columns = [i[0] for i in cursor.description]

            # Fecha o cursor e a conexão
            cursor.close()
            conn.close()

            return pd.DataFrame(data, columns=columns)

    except mysql.connector.Error as err:
        st.error(f"Erro ao recuperar os dados: {err}")
# Função para inserir dados no banco de dados
def insert_data(data):
    try:
        # Conexão com o banco de dados MySQL
        conn = mysql.connector.connect(
            host="monorail.proxy.rlwy.net",
            user="root",
            password="IavrTTLyCOohONgVOMWTdepOQrWuJHQO",
            database="railway",
            port=52280
        )

        # Verifica se a conexão foi bem-sucedida
        if conn.is_connected():
            cursor = conn.cursor()

            # Prepara a instrução SQL para inserir os dados
            sql = """
            INSERT INTO credenciamentocpc 
            (situacao_econsig, subprocesso_siloms, categoria, natureza_de_desconto, consignataria, cnpj, nro_contrato, dou, situacao, data_expiracao_contratual, codigo, status_credenciamento, cpc_status, cpc_anual, data_de_entrada, dias_para_fim_vigencia) 
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Executa a instrução SQL
            cursor.execute(sql, data)

            # Confirma a transação
            conn.commit()

            # Fecha o cursor e a conexão
            cursor.close()
            conn.close()

            return True, None  # Indica que a inserção foi bem-sucedida, sem erros

    except mysql.connector.Error as err:
        error_message = str(err)
        return False, error_message  # Indica que a inserção falhou e retorna a mensagem de erro
def insert_data(data):
    try:
        # Conexão com o banco de dados MySQL
        conn = mysql.connector.connect(
            host="monorail.proxy.rlwy.net",
            user="root",
            password="IavrTTLyCOohONgVOMWTdepOQrWuJHQO",
            database="railway",
            port=52280
        )

        # Verifica se a conexão foi bem-sucedida
        if conn.is_connected():
            cursor = conn.cursor()

            # Prepara a instrução SQL para inserir os dados
            sql = "INSERT INTO credenciamentocpc (situacao_econsig, subprocesso_siloms, categoria, natureza_de_desconto, consignataria, cnpj, nro_contrato, dou, situacao, data_expiracao_contratual, codigo, status_credenciamento, cpc_status, cpc_anual, data_entrada, dias_para_fim_vigencia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            # Executa a instrução SQL
            cursor.execute(sql, data)

            # Confirma a transação
            conn.commit()

            # Fecha o cursor e a conexão
            cursor.close()
            conn.close()

            return True, None  # Indica que a inserção foi bem-sucedida, sem erros

    except mysql.connector.Error as err:
        error_message = str(err)
        return False, error_message  # Indica que a inserção falhou e retorna a mensagem de erro
def excluir_dados(id_to_delete):
    try:
        # Conexão com o banco de dados MySQL
        conn = mysql.connector.connect(
            host="monorail.proxy.rlwy.net",
            user="root",
            password="IavrTTLyCOohONgVOMWTdepOQrWuJHQO",
            database="railway",
            port=52280
        )

        # Verifica se a conexão foi bem-sucedida
        if conn.is_connected():
            cursor = conn.cursor()

            # Prepara a instrução SQL para excluir os dados por ID
            sql = "DELETE FROM credenciamentocpc WHERE id = %s"

            # Executa a instrução SQL
            cursor.execute(sql, (id_to_delete,))

            # Confirma a transação
            conn.commit()

            # Fecha o cursor e a conexão
            cursor.close()
            conn.close()

            return True, None  # Indica que a exclusão foi bem-sucedida, sem erros

    except mysql.connector.Error as err:
        error_message = str(err)
        return False, error_message  # Indica que a exclusão falhou e retorna a mensagem de erro

# Função para validar o CNPJ
def validar_cnpj(cnpj):
    if not re.match(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', cnpj):
        st.error('O CNPJ deve ter o formato XX.XXX.XXX/XXXX-XX')
        return False
    return True
# Função para confirmar a exclusão
def confirmar_exclusao():
    return st.button("Confirmar Exclusão")
# Função principal
def main():
    opcao_selecionada = st.sidebar.radio("Opção", ['Incluir Processo', 'Excluir Processo', 'Visualizar Processos', 'editar'])

    if opcao_selecionada == 'Incluir Processo':
        # Divide o formulário em duas colunas
        col1, col2 = st.columns(2)

        # Coleta os dados do usuário através de inputs
        with col1:
            situacao_econsig = st.selectbox('Situação Econsig*', options=[''] + ['Sem Cadastro', 'Recredenciado', 'Credenciado', 'Aguardando Publicação', 'Arquivado', 'Bloqueado', 'Credenciamento Vencido'])
            subprocesso_siloms = st.text_input('Subprocesso Siloms*')
            categoria = st.selectbox('Categoria*', options=[''] + ['I', 'II', 'III'])
            natureza_de_desconto = st.selectbox('Natureza de Desconto*', options=[''] + ['MENSALIDADE ASSOCIATIVA', 'PREVIDÊNCIA COMPLEMENTAR', 'ASSISTÊNCIA FINANCEIRA', 'CARTÃO DE CRÉDITO', 'SEGURO DE VIDA'])
            consignataria = st.text_input('Consignatária*')
            cnpj = st.text_input('CNPJ*', placeholder='XX.XXX.XXX/XXXX-XX')
            nro_contrato = st.text_input('NRO CONTRATO*')
            dou = st.text_input('DOU')

        with col2:
            situacao = st.selectbox('Situação*', options=[''] + ['Encaminhado para Secretário(a) da CPC', 'Análise Equipe A', 'Análise Equipe B', 'Análise Equipe C', 'Análise Equipe D', 'Análise Equipe E' ,'Aguardando Assinaturas', 'Encaminhado para a PP1 (conclusão/arquivamento)', 'Encaminhado para a PP1 para análise'])
            data_expiracao_contratual = st.date_input('Data Expiração Contratual', None, format='DD/MM/YYYY', key='data_expiracao_contratual')
            # Calcula os dias para o fim da vigência apenas se data_expiracao_contratual não for None
            if data_expiracao_contratual is not None:
                data_atual = date.today()
                dias_para_fim_vigencia = (data_expiracao_contratual - data_atual).days
                if dias_para_fim_vigencia < 0:
                    dias_para_fim_vigencia = 'Expirado'
                else:
                    dias_para_fim_vigencia = str(dias_para_fim_vigencia) + ' dias'
            else:
                dias_para_fim_vigencia = ''

            # Exibe os dias para o fim da vigência
            st.text_input('Dias para Fim Vigência', value=dias_para_fim_vigencia, disabled=True, key='dias_para_fim_vigencia')
            codigo = st.text_input('Código Caixa')
            status_credenciamento = st.text_input('Status Credenciamento - Observações')
            cpc_status = st.selectbox('CPC Status', options=[''] + ['EM ANÁLISE', 'CONCLUÍDO', 'ENTREGUE', 'REJEITADO','EM ANÁLISE PP1'])
            cpc_anual = st.selectbox('CPC Anual', options=[''] + ['CPC 2021', 'CPC 2022', 'CPC 2023', 'CPC 2024', 'CPC 2025', 'CPC 2026'])
            data_entrada = st.date_input('Data de Entrada', None, format='DD/MM/YYYY')

        # Botão para enviar os dados
        if st.button("Inserir"):
            # Verifica se todos os campos obrigatórios foram preenchidos
            if (
                situacao_econsig and subprocesso_siloms and categoria and natureza_de_desconto and consignataria and cnpj and nro_contrato and
                situacao and data_entrada):

                # Tenta inserir os dados no banco de dados
                data = (
                    situacao_econsig, subprocesso_siloms, categoria,
                    natureza_de_desconto, consignataria, cnpj, nro_contrato,
                    dou, situacao, data_expiracao_contratual, codigo,
                    status_credenciamento, cpc_status, cpc_anual, data_entrada,
                    dias_para_fim_vigencia  # Adicionando o valor calculado aqui
                )
                success, error_message = insert_data(data)
                if success:
                    st.success("Dados inseridos com sucesso!")
                else:
                    st.error(f"Erro ao inserir os dados: {error_message}")
            else:
                st.warning("Por favor, preencha todos os campos obrigatórios.")

    elif opcao_selecionada == 'Excluir Processo':
        id_to_delete = st.number_input("Insira o ID a ser excluído:", min_value=1, step=1)
        if st.button("Excluir"):
            # Tenta excluir os dados do banco de dados
            success, error_message = excluir_dados(id_to_delete)
            if success:
                st.success("Dados excluídos com sucesso!")
            else:
                st.error(f"Erro ao excluir os dados: {error_message}")
    elif opcao_selecionada == 'Visualizar Processos':
        # Mostra os dados do banco de dados
        st.header("Visualizar Contratos")
        data = fetch_all_data()
        if data is not None:
            st.dataframe(data)
        else:
            st.warning("Nenhum dado encontrado.")

    elif opcao_selecionada == 'editar':
        st.header('Editar Dados')

        # Entrada para o ID do registro a ser editado
        id_to_edit = st.number_input('ID do Registro a ser Editado:', min_value=1, step=1)

        if st.button('Buscar Registro'):
            # Busca o registro no banco de dados
            data_to_edit = fetch_single_data(id_to_edit)
            if data_to_edit is not None:
                # Se o registro for encontrado, exibe o formulário para edição
                situacao_econsig_edit = st.text_input('Situação Econsig', value=data_to_edit[1])
                subprocesso_siloms_edit = st.text_input('Subprocesso Siloms', value=data_to_edit[2])
                categoria_edit = st.text_input('Categoria', value=data_to_edit[3])
                natureza_de_desconto_edit = st.text_input('Natureza de Desconto', value=data_to_edit[4])
                consignataria_edit = st.text_input('Consignatária', value=data_to_edit[5])
                cnpj_edit = st.text_input('CNPJ', value=data_to_edit[6])
                nro_contrato_edit = st.text_input('Nro. Contrato', value=data_to_edit[7])
                dou_edit = st.text_input('DOU', value=data_to_edit[8])
                situacao_edit = st.text_input('Situação', value=data_to_edit[9])
                
                # Corrigindo a entrada de data para data_expiracao_contratual_edit e data_entrada_edit
                data_expiracao_contratual_edit = st.date_input('Data de Expiração Contratual', value=pd.to_datetime(data_to_edit[10], errors='coerce'))
                if isinstance(data_expiracao_contratual_edit, pd.Timestamp):
                    data_expiracao_contratual_edit = data_expiracao_contratual_edit.date()
                
                codigo_edit = st.text_input('Código', value=data_to_edit[11])
                status_credenciamento_edit = st.text_input('Status de Credenciamento', value=data_to_edit[12])
                cpc_status_edit = st.text_input('CPC Status', value=data_to_edit[13])
                cpc_anual_edit = st.text_input('CPC Anual', value=data_to_edit[14])
                
                # Corrigindo a entrada de data para data_entrada_edit
                data_entrada_edit = st.date_input('Data de Entrada', None,  value=data_to_edit[15],format='DD/MM/YYYY')


                if st.button('Atualizar Registro'):
                    # Atualiza o registro no banco de dados
                    new_data = [
                        situacao_econsig_edit, subprocesso_siloms_edit, categoria_edit,
                        natureza_de_desconto_edit, consignataria_edit, cnpj_edit,
                        nro_contrato_edit, dou_edit, situacao_edit, data_expiracao_contratual_edit,
                        codigo_edit, status_credenciamento_edit, cpc_status_edit,
                        cpc_anual_edit, data_entrada_edit
                    ]

                    if update_data(id_to_edit, new_data):
                        st.success('Registro atualizado com sucesso!')
                    else:
                        st.error('Erro ao atualizar o registro.')

            else:
                st.warning('Nenhum registro encontrado para o ID fornecido.')


# Executa a função principal
if __name__ == "__main__":
    main()

