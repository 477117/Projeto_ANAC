import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import os
import base64
import time  # Para simular carregamento

# --- Configurações do Banco de Dados ---
DB_HOST = 'localhost'  # Substitua pelo seu host
DB_USER = 'root'  # Substitua pelo seu usuário
DB_PASSWORD = '477117'  # Substitua pela sua senha
DB_NAME = 'dw_projeto'  # Substitua pelo nome do seu banco de dados


# Dicionário de usuários e senhas (EM TEXTO PLANO - PARA DEMONSTRAÇÃO, NÃO USE EM PRODUÇÃO)
USUARIOS = {
    "Aluno": "Aluno123#",
    "Professor": "Profe123#",
    "Visitante": "Visit123#",
}

def obter_dados_fabricante_modelo(fabricante_selecionado=None, modelo_selecionado=None, ordenar_por='desc', top_n=12):
    """
    Obtém os dados de fabricante e modelo do MySQL com filtros e ordenação.

    Args:
        fabricante_selecionado (str, optional): Fabricante selecionado pelo usuário. Padrão é None.
        modelo_selecionado (str, optional): Modelo selecionado pelo usuário. Padrão é None.
        ordenar_por (str, optional): 'asc' para crescente, 'desc' para decrescente. Padrão é 'desc'.
        top_n (int, optional): Número máximo de resultados a retornar. Padrão é 12.

    Returns:
        pd.DataFrame: DataFrame com os dados filtrados e ordenados, ou DataFrame vazio em caso de erro.
    """
    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        mycursor = mydb.cursor()
        query = """
        SELECT a.nome_do_fabricante, a.modelo, COUNT(o.id_ocorrencia) AS total_ocorrencias
        FROM aeronaves a
        LEFT JOIN ocorrencias o ON a.id_aeronave = o.id_aeronave
        """
        filtros = []
        if fabricante_selecionado:
            filtros.append(f"a.nome_do_fabricante = '{fabricante_selecionado}'")
        if modelo_selecionado:
            filtros.append(f"a.modelo = '{modelo_selecionado}'")
        if filtros:
            query += " WHERE " + " AND ".join(filtros)
        query += " GROUP BY a.nome_do_fabricante, a.modelo"
        if ordenar_por == 'asc':
            query += " ORDER BY total_ocorrencias ASC"
        else:
            query += " ORDER BY total_ocorrencias DESC"
        query += f" LIMIT {top_n}"
        st.write(f"Executando consulta SQL: {query}")  # Para debug
        mycursor.execute(query)
        resultados = mycursor.fetchall()
        if not resultados:
            st.warning("A consulta não retornou resultados do banco de dados. Verifique os dados.")
            return pd.DataFrame()
        colunas = ['fabricante', 'modelo', 'total_ocorrencias']
        df = pd.DataFrame(resultados, columns=colunas)
        return df
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar ao MySQL: {err}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro durante a execução da consulta: {e}")
        return pd.DataFrame()
    finally:
        if mydb and mydb.is_connected():
            mycursor.close()
            mydb.close()



def gerar_grafico_fabricante_modelo(df_filtrado, top_n):
    """
    Gera o gráfico de barras para o Top N de Fabricante / Modelo por Total de Ocorrências.

    Args:
        df_filtrado (pd.DataFrame): DataFrame com os dados filtrados.
        top_n (int): Número de resultados a exibir no gráfico.

    Returns:
        matplotlib.figure.Figure: Objeto da figura do Matplotlib com o gráfico gerado.
    """
    try:
        plt.figure(figsize=(14, 8))
        ax = sns.barplot(x='total_ocorrencias', y=df_filtrado['fabricante'] + ' / ' + df_filtrado['modelo'], data=df_filtrado, dodge=False)
        plt.title(f'Top {top_n} Fabricante / Modelo (Total de Ocorrências)')
        plt.xlabel('Total de Ocorrências')
        plt.ylabel('Fabricante / Modelo')

        # Adicionando rótulos nas barras
        for p in ax.patches:
            largura = p.get_width()
            altura = p.get_y() + p.get_height() / 2.
            x = largura + 0.2
            ax.text(x, altura, f'{int(largura)}', ha='left', va='center')

        plt.tight_layout()
        return plt.gcf()  # Retorna a figura para ser exibida no Streamlit
    except Exception as e:
        st.error(f"Erro ao gerar o gráfico: {e}")
        return None

def mostrar_grafico_fabricante_modelo():
    """Exibe o gráfico de Top N Fabricante / Modelo por Total de Ocorrências."""
    # Inicializa o estado da sessão para os filtros, se ainda não estiverem definidos
    if 'fabricante_selecionado' not in st.session_state:
        st.session_state['fabricante_selecionado'] = 'Todos'
    if 'modelo_selecionado' not in st.session_state:
        st.session_state['modelo_selecionado'] = 'Todos'
    if 'ordenar_por' not in st.session_state:
        st.session_state['ordenar_por'] = 'Decrescente'
    if 'top_n' not in st.session_state:
        st.session_state['top_n'] = 12

    # Filtros interativos
    df_fabricante = obter_dados_fabricante_modelo()
    fabricantes = df_fabricante['fabricante'].unique()
    modelos = df_fabricante['modelo'].unique()

    st.sidebar.subheader("Filtros") # Move os filtros para a barra lateral
    fabricante_selecionado = st.sidebar.selectbox("Filtrar por Fabricante:", ['Todos'] + list(fabricantes), key='fabricante_selecionado')
    modelo_selecionado = st.sidebar.selectbox("Filtrar por Modelo:", ['Todos'] + list(modelos), key='modelo_selecionado')
    ordenar_por = st.sidebar.radio("Ordenar por:", ('Decrescente', 'Crescente'), key='ordenar_por')
    top_n = st.sidebar.slider("Número de Resultados:", min_value=1, max_value=50, value=12, key='top_n')

    ordenar_por = 'asc' if ordenar_por == 'Crescente' else 'desc'

    fabricante_selecionado = None if fabricante_selecionado == 'Todos' else fabricante_selecionado
    modelo_selecionado = None if modelo_selecionado == 'Todos' else modelo_selecionado

    with st.spinner("Carregando e gerando gráfico..."): # Adiciona um spinner
        df_filtrado = obter_dados_fabricante_modelo(fabricante_selecionado, modelo_selecionado, ordenar_por, top_n)

        if not df_filtrado.empty:
            st.write("Dados recuperados do banco de dados:")
            st.write(df_filtrado)  # Exibe os dados recuperados
            fig = gerar_grafico_fabricante_modelo(df_filtrado, top_n)
            if fig:
                st.pyplot(fig)
            else:
                st.error("Erro ao gerar o gráfico.")
        else:
            st.error("Não foi possível carregar os dados para o gráfico.")



def pagina_login():
    """Exibe a página de login."""
    st.subheader("Autenticação")
    usuario = st.sidebar.text_input("Usuário:")
    senha = st.sidebar.text_input("Senha:", type="password")
    mostrar_senha = st.sidebar.checkbox("Mostrar senha")
    if mostrar_senha:
        st.sidebar.text(senha)
    login_button = st.sidebar.button("Entrar")

    if login_button:
        if usuario in USUARIOS:
            if USUARIOS[usuario] == senha:
                st.success(f"Login realizado com sucesso, {usuario}!")
                st.session_state['login_sucesso'] = True
                st.session_state['pagina'] = 'grafico1'  # Alterado para ir direto ao gráfico
                st.session_state['usuario_logado'] = usuario
                st.rerun()
            else:
                st.error("Senha incorreta.")
        else:
            st.error("Usuário não encontrado.")


def barra_lateral():
    """Configura a barra lateral."""
    st.sidebar.subheader("Aplicativo de Visualização de Dados")
    st.sidebar.markdown("Selecione um gráfico para explorar os dados da ANAC.")
    st.sidebar.subheader("Autenticação")
    if st.session_state['login_sucesso']:
        if st.sidebar.button("Sair"):
            st.session_state['login_sucesso'] = False
            st.session_state['pagina'] = 'login'
            st.session_state.pop('usuario_logado', None)
            st.rerun()

def main():
    st.title("Visualizador de Gráficos ANAC")

    if 'login_sucesso' not in st.session_state:
        st.session_state['login_sucesso'] = False
        st.session_state['pagina'] = 'login'

    barra_lateral()

    # --- Conteúdo Principal ---
    if not st.session_state['login_sucesso']:
        pagina_login()
    elif st.session_state['pagina'] == 'grafico1':  # Alterado para ir direto ao gráfico
        mostrar_grafico_fabricante_modelo()

if __name__ == "__main__":
    main()
