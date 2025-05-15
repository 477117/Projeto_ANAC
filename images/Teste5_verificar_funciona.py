import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import os
import base64
import time  # Para simular carregamento
import plotly.express as px  # Para gráficos interativos

# --- Configurações do Banco de Dados ---
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '477117'
DB_NAME = 'dw_projeto'

# Dicionário para armazenar informações adicionais sobre os gráficos
info_graficos = {
    "Gráfico 1": "Top 12 de Fabricante / Modelo por Total de Ocorrências.",
    "Gráfico 2": "Número de Ocorrências por Ano.",
    "Gráfico 3": "Distribuição de Ocorrências por Tipo de Aeronave.",
    "Gráfico 4": "Ocorrências por Fase de Operação.",
    "Gráfico 5": "Top 10 Causas de Ocorrências.",
    "Gráfico 6": "Ocorrências por Condição Meteorológica.",
    "Gráfico 7": "Evolução das Ocorrências ao Longo do Tempo",
}

# Dicionário de usuários e senhas (EM TEXTO PLANO - PARA DEMONSTRAÇÃO, NÃO USE EM PRODUÇÃO)
USUARIOS = {
    "Aluno": "Aluno123#",
    "Professor": "Profe123#",
    "Visitante": "Visit123#",
}

@st.cache_data
def obter_dados_fabricante_modelo(fabricante_selecionado=None, modelo_selecionado=None, ordenar_por='desc', top_n=12):
    """Obtém os dados de fabricante e modelo do MySQL."""
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
        st.write(f"Executando consulta SQL: {query}")
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



@st.cache_data
def obter_dados_ocorrencias_por_ano():
    """Obtém o número de ocorrências por ano."""
    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        mycursor = mydb.cursor()
        query = """
        SELECT YEAR(data_ocorrencia) AS ano, COUNT(id_ocorrencia) AS total_ocorrencias
        FROM ocorrencias
        GROUP BY ano
        ORDER BY ano
        """
        mycursor.execute(query)
        resultados = mycursor.fetchall()
        colunas = ['ano', 'total_ocorrencias']
        df = pd.DataFrame(resultados, columns=colunas)
        return df
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar ao MySQL: {err}")
        return pd.DataFrame()
    finally:
        if mydb and mydb.is_connected():
            mycursor.close()
            mydb.close()



@st.cache_data
def obter_dados_ocorrencias_por_tipo_aeronave():
    """Obtém a distribuição de ocorrências por tipo de aeronave."""
    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        mycursor = mydb.cursor()
        query = """
        SELECT a.tipo_aeronave, COUNT(o.id_ocorrencia) AS total_ocorrencias
        FROM aeronaves a
        JOIN ocorrencias o ON a.id_aeronave = o.id_aeronave
        GROUP BY a.tipo_aeronave
        ORDER BY total_ocorrencias DESC
        """
        mycursor.execute(query)
        resultados = mycursor.fetchall()
        colunas = ['tipo_aeronave', 'total_ocorrencias']
        df = pd.DataFrame(resultados, columns=colunas)
        return df
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar ao MySQL: {err}")
        return pd.DataFrame()
    finally:
        if mydb and mydb.is_connected():
            mycursor.close()
            mydb.close()

@st.cache_data
def obter_dados_ocorrencias_por_fase_operacao():
    """Obtém a distribuição de ocorrências por fase de operação."""
    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        mycursor = mydb.cursor()
        query = """
        SELECT f.nome_fase_operacao, COUNT(o.id_ocorrencia) AS total_ocorrencias
        FROM fases_operacao f
        JOIN ocorrencias o ON f.id_fase_operacao = o.id_fase_operacao
        GROUP BY f.nome_fase_operacao
        ORDER BY total_ocorrencias DESC
        """
        mycursor.execute(query)
        resultados = mycursor.fetchall()
        colunas = ['fase_operacao', 'total_ocorrencias']
        df = pd.DataFrame(resultados, columns=colunas)
        return df
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar ao MySQL: {err}")
        return pd.DataFrame()
    finally:
        if mydb and mydb.is_connected():
            mycursor.close()
            mydb.close()

@st.cache_data
def obter_dados_top_causas():
    """Obtém as 10 principais causas de ocorrências."""
    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        mycursor = mydb.cursor()
        query = """
        SELECT c.nome_causa, COUNT(o.id_ocorrencia) AS total_ocorrencias
        FROM causas c
        JOIN ocorrencias o ON c.id_causa = o.id_causa
        GROUP BY c.nome_causa
        ORDER BY total_ocorrencias DESC
        LIMIT 10
        """
        mycursor.execute(query)
        resultados = mycursor.fetchall()
        colunas = ['causa', 'total_ocorrencias']
        df = pd.DataFrame(resultados, columns=colunas)
        return df
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar ao MySQL: {err}")
        return pd.DataFrame()
    finally:
        if mydb and mydb.is_connected():
            mycursor.close()
            mydb.close()

@st.cache_data
def obter_dados_ocorrencias_por_condicao_meteorologica():
    """Obtém as ocorrências por condição meteorológica."""
    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        mycursor = mydb.cursor()
        query = """
        SELECT m.nome_condicao_meteorologica, COUNT(o.id_ocorrencia) AS total_ocorrencias
        FROM condicoes_meteorologicas m
        JOIN ocorrencias o ON m.id_condicao_meteorologica = o.id_condicao_meteorologica
        GROUP BY m.nome_condicao_meteorologica
        ORDER BY total_ocorrencias DESC
        """
        mycursor.execute(query)
        resultados = mycursor.fetchall()
        colunas = ['condicao_meteorologica', 'total_ocorrencias']
        df = pd.DataFrame(resultados, columns=colunas)
        return df
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar ao MySQL: {err}")
        return pd.DataFrame()
    finally:
        if mydb and mydb.is_connected():
            mycursor.close()
            mydb.close()

@st.cache_data
def obter_evolucao_ocorrencias():
    """Obtém a evolução das ocorrências ao longo do tempo."""
    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        mycursor = mydb.cursor()
        query = """
        SELECT DATE_FORMAT(data_ocorrencia, '%Y-%m') AS mes_ano, COUNT(id_ocorrencia) AS total_ocorrencias
        FROM ocorrencias
        GROUP BY mes_ano
        ORDER BY mes_ano
        """
        mycursor.execute(query)
        resultados = mycursor.fetchall()
        colunas = ['mes_ano', 'total_ocorrencias']
        df = pd.DataFrame(resultados, columns=colunas)
        return df
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar ao MySQL: {err}")
        return pd.DataFrame()
    finally:
        if mydb and mydb.is_connected():
            mycursor.close()
            mydb.close()



def mostrar_grafico_fabricante_modelo():
    """Exibe o gráfico de Top N Fabricante / Modelo por Total de Ocorrências."""
    # Inicializa o estado da sessão para os filtros
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

    st.sidebar.subheader("Filtros")
    fabricante_selecionado = st.sidebar.selectbox("Filtrar por Fabricante:", ['Todos'] + list(fabricantes), key='fabricante_selecionado')
    modelo_selecionado = st.sidebar.selectbox("Filtrar por Modelo:", ['Todos'] + list(modelos), key='modelo_selecionado')
    ordenar_por = st.sidebar.radio("Ordenar por:", ('Decrescente', 'Crescente'), key='ordenar_por')
    top_n = st.sidebar.slider("Número de Resultados:", min_value=1, max_value=50, value=12, key='top_n')

    ordenar_por = 'asc' if ordenar_por == 'Crescente' else 'desc'
    fabricante_selecionado = None if fabricante_selecionado == 'Todos' else fabricante_selecionado
    modelo_selecionado = None if modelo_selecionado == 'Todos' else modelo_selecionado

    with st.spinner("Carregando e gerando gráfico..."):
        df_filtrado = obter_dados_fabricante_modelo(fabricante_selecionado, modelo_selecionado, ordenar_por, top_n)
        if not df_filtrado.empty:
            st.write("Dados recuperados do banco de dados:")
            st.write(df_filtrado)
            try:
                # Use Plotly para criar o gráfico de barras com tooltips
                fig = px.bar(
                    df_filtrado,
                    x='total_ocorrencias',
                    y=df_filtrado['fabricante'] + ' / ' + df_filtrado['modelo'],
                    labels={'total_ocorrencias': 'Total de Ocorrências', 'y': 'Fabricante / Modelo'},
                    title=f'Top {top_n} Fabricante / Modelo (Total de Ocorrências)',
                    hover_data=['fabricante', 'modelo', 'total_ocorrencias']  # Adiciona dados ao tooltip
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico: {e}")
        else:
            st.error("Não foi possível carregar os dados para o gráfico.")



def mostrar_grafico_ocorrencias_por_ano():
    """Exibe o gráfico de ocorrências por ano."""
    df_ano = obter_dados_ocorrencias_por_ano()
    if not df_ano.empty:
        try:
            plt.figure(figsize=(10, 6))
            plt.plot(df_ano['ano'], df_ano['total_ocorrencias'], marker='o')
            plt.title('Número de Ocorrências por Ano')
            plt.xlabel('Ano')
            plt.ylabel('Total de Ocorrências')
            plt.grid(True)
            st.pyplot(plt)
        except Exception as e:
            st.error(f"Erro ao gerar gráfico: {e}")
    else:
        st.error("Não há dados suficientes para exibir o gráfico de ocorrências por ano.")



def mostrar_grafico_ocorrencias_por_tipo_aeronave():
    """Exibe o gráfico de distribuição de ocorrências por tipo de aeronave."""
    df_tipo_aeronave = obter_dados_ocorrencias_por_tipo_aeronave()
    if not df_tipo_aeronave.empty:
        try:
            plt.figure(figsize=(10, 6))
            plt.pie(df_tipo_aeronave['total_ocorrencias'], labels=df_tipo_aeronave['tipo_aeronave'], autopct='%1.1f%%')
            plt.title('Distribuição de Ocorrências por Tipo de Aeronave')
            st.pyplot(plt)
        except Exception as e:
            st.error(f"Erro ao gerar gráfico: {e}")
    else:
        st.error("Não há dados suficientes para exibir o gráfico de ocorrências por tipo de aeronave.")

def mostrar_grafico_ocorrencias_por_fase_operacao():
    """Exibe o gráfico de distribuição de ocorrências por fase de operação."""
    df_fase_operacao = obter_dados_ocorrencias_por_fase_operacao()
    if not df_fase_operacao.empty:
        try:
            plt.figure(figsize=(12, 6))
            sns.barplot(x='total_ocorrencias', y='fase_operacao', data=df_fase_operacao)
            plt.title('Ocorrências por Fase de Operação')
            plt.xlabel('Total de Ocorrências')
            plt.ylabel('Fase de Operação')
            st.pyplot(plt)
        except Exception as e:
            st.error(f"Erro ao gerar o gráfico: {e}")
    else:
        st.error("Não há dados suficientes para exibir o gráfico de ocorrências por fase de operação.")

def mostrar_grafico_top_causas():
    """Exibe o gráfico das 10 principais causas de ocorrências."""
    df_top_causas = obter_dados_top_causas()
    if not df_top_causas.empty:
        try:
            plt.figure(figsize=(12, 6))
            sns.barplot(x='total_ocorrencias', y='causa', data=df_top_causas)
            plt.title('Top 10 Causas de Ocorrências')
            plt.xlabel('Total de Ocorrências')
            plt.ylabel('Causa')
            st.pyplot(plt)
        except Exception as e:
            st.error(f"Erro ao gerar o gráfico: {e}")
    else:
        st.error("Não há dados suficientes para exibir o gráfico das 10 principais causas.")

def mostrar_grafico_ocorrencias_por_condicao_meteorologica():
    """Exibe o gráfico de ocorrências por condição meteorológica."""
    df_condicao_meteorologica = obter_dados_ocorrencias_por_condicao_meteorologica()
    if not df_condicao_meteorologica.empty:
        try:
            plt.figure(figsize=(12, 6))
            sns.barplot(x='total_ocorrencias', y='condicao_meteorologica', data=df_condicao_meteorologica)
            plt.title('Ocorrências por Condição Meteorológica')
            plt.xlabel('Total de Ocorrências')
            plt.ylabel('Condição Meteorológica')
            st.pyplot(plt)
        except Exception as e:
            st.error(f"Erro ao gerar o gráfico: {e}")
    else:
        st.error("Não há dados suficientes para exibir o gráfico de ocorrências por condição meteorológica.")

def mostrar_grafico_evolucao_ocorrencias():
    """Exibe o gráfico da evolução das ocorrências ao longo do tempo."""
    df_evolucao = obter_evolucao_ocorrencias()
    if not df_evolucao.empty:
        try:
            plt.figure(figsize=(12, 6))
            plt.plot(df_evolucao['mes_ano'], df_evolucao['total_ocorrencias'], marker='o')
            plt.title('Evolução das Ocorrências ao Longo do Tempo')
            plt.xlabel('Mês e Ano')
            plt.ylabel('Total de Ocorrências')
            plt.grid(True)
            plt.xticks(rotation=45)
            st.pyplot(plt)
        except Exception as e:
            st.error(f"Erro ao gerar o gráfico: {e}")
    else:
        st.error("Não há dados suficientes para exibir o gráfico de evolução das ocorrências.")



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
                st.session_state['pagina'] = 'grafico1'
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
    # Menu de navegação
    st.sidebar.subheader("Gráficos")
    grafico_selecionado = st.sidebar.radio("Selecione o Gráfico",
                                          ("Gráfico 1", "Gráfico 2", "Gráfico 3", "Gráfico 4", "Gráfico 5", "Gráfico 6", "Gráfico 7"))
    st.session_state['pagina'] = grafico_selecionado # Atualiza a página com o gráfico selecionado


def main():
    st.title("Visualizador de Gráficos ANAC")

    if 'login_sucesso' not in st.session_state:
        st.session_state['login_sucesso'] = False
        st.session_state['pagina'] = 'login'

    barra_lateral()

    # --- Conteúdo Principal ---
    if not st.session_state['login_sucesso']:
        pagina_login()
    else:
        # Exibe o gráfico selecionado
        if st.session_state['pagina'] == 'Gráfico 1':
            mostrar_grafico_fabricante_modelo()
        elif st.session_state['pagina'] == 'Gráfico 2':
            mostrar_grafico_ocorrencias_por_ano()
        elif st.session_state['pagina'] == 'Gráfico 3':
            mostrar_grafico_ocorrencias_por_tipo_aeronave()
        elif st.session_state['pagina'] == 'Gráfico 4':
            mostrar_grafico_ocorrencias_por_fase_operacao()
        elif st.session_state['pagina'] == 'Gráfico 5':
            mostrar_grafico_top_causas()
        elif st.session_state['pagina'] == 'Gráfico 6':
            mostrar_grafico_ocorrencias_por_condicao_meteorologica()
        elif st.session_state['pagina'] == 'Gráfico 7':
            mostrar_grafico_evolucao_ocorrencias()

if __name__ == "__main__":
    main()

