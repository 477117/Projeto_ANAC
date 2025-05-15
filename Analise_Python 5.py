import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Gera os gráficos acertados mas falta o preditivo

# Detalhes da sua conexão com o MySQL
db_host = 'localhost'
db_user = 'root'
db_password = '477117'
db_name = 'dw_projeto'

mydb = None
mycursor = None

try:

    mydb = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    mycursor = mydb.cursor()
    query = """
    SELECT YEAR(data_da_ocorrencia) AS ano, DATE(data_da_ocorrencia) AS dia, COUNT(*) AS ocorrencias_dia
    FROM dw_projeto.ocorrencias
    WHERE YEAR(data_da_ocorrencia) >= 2014
    GROUP BY YEAR(data_da_ocorrencia), DATE(data_da_ocorrencia)
    """
    mycursor.execute(query)
    resultados = mycursor.fetchall()
    colunas = ['ano', 'dia', 'ocorrencias_dia']
    df_ocorrencias_dia = pd.DataFrame(resultados, columns=colunas)
    print(df_ocorrencias_dia.head())

    # Calcular as estatísticas POR ANO (média, mediana, desvio padrão e moda das ocorrências diárias)
    estatisticas_por_ano = df_ocorrencias_dia.groupby('ano')['ocorrencias_dia'].agg(
        ['mean', 'median', 'std', lambda x: x.mode().iloc[0] if not x.mode().empty else None]
    )
    estatisticas_por_ano = estatisticas_por_ano.rename(columns={'mean': 'Média', 'median': 'Mediana', 'std': 'Desvio Padrão', '<lambda_0>': 'Moda'})
    estatisticas_por_ano = estatisticas_por_ano.reset_index()
    estatisticas_por_ano_filtrado = estatisticas_por_ano[estatisticas_por_ano['ano'] >= 2014].dropna(subset=['Moda']) # Remove anos sem moda
    print (estatisticas_por_ano_filtrado)

    # Criar a figura e os subplots
    fig, axs = plt.subplots(4, 1, figsize=(12, 10), sharex=True)  # Agora 4 subplots

    # Plotar a Média
    axs[0].plot(estatisticas_por_ano_filtrado['ano'], estatisticas_por_ano_filtrado['Média'], marker='o', linestyle='-', color='skyblue')
    axs[0].set_ylabel('Média')
    axs[0].set_title('Média de Ocorrências por Dia por Ano (a partir de 2014)')
    axs[0].grid(True)
    for x, y in zip(estatisticas_por_ano_filtrado['ano'], estatisticas_por_ano_filtrado['Média']):
        axs[0].annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(5, 5), ha='left')

    # Plotar a Mediana
    axs[1].plot(estatisticas_por_ano_filtrado['ano'], estatisticas_por_ano_filtrado['Mediana'], marker='s', linestyle='--', color='salmon')
    axs[1].set_ylabel('Mediana')
    axs[1].set_title('Mediana de Ocorrências por Dia por Ano (a partir de 2014)')
    axs[1].grid(True)
    for x, y in zip(estatisticas_por_ano_filtrado['ano'], estatisticas_por_ano_filtrado['Mediana']):
        axs[1].annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(5, 5), ha='left')

    # Plotar o Desvio Padrão
    axs[2].plot(estatisticas_por_ano_filtrado['ano'], estatisticas_por_ano_filtrado['Desvio Padrão'], marker='^', linestyle=':', color='lightgreen')
    axs[2].set_ylabel('Desvio Padrão')
    axs[2].set_title('Desvio Padrão de Ocorrências por Dia por Ano (a partir de 2014)')
    axs[2].grid(True)
    for x, y in zip(estatisticas_por_ano_filtrado['ano'], estatisticas_por_ano_filtrado['Desvio Padrão']):
        axs[2].annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(5, 5), ha='left')

    # Plotar a Moda
    axs[3].plot(estatisticas_por_ano_filtrado['ano'], estatisticas_por_ano_filtrado['Moda'], marker='D', linestyle='-.', color='orange')
    axs[3].set_ylabel('Moda')
    axs[3].set_xlabel('Ano')
    axs[3].set_title('Moda de Ocorrências por Dia por Ano (a partir de 2014)')
    axs[3].grid(True)
    for x, y in zip(estatisticas_por_ano_filtrado['ano'], estatisticas_por_ano_filtrado['Moda']):
        axs[3].annotate(f'{int(y)}', (x, y), textcoords="offset points", xytext=(5, 5), ha='left') # Moda geralmente é um valor inteiro

    plt.tight_layout()
    plt.show()

    # Histograma do número de ocorrências por dia (todos os anos juntos)
    plt.figure(figsize=(10, 6))
    plt.hist(df_ocorrencias_dia['ocorrencias_dia'], bins=20, edgecolor='black', color='lightcoral')  # Ajuste o número de bins conforme necessário
    plt.xlabel('Número de Ocorrências por Dia')
    plt.ylabel('Frequência')
    plt.title('Distribuição do Número de Ocorrências por Dia (a partir de 2014)')
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    plt.show()

except mysql.connector.Error as err:
    print(f"Erro ao conectar ao MySQL: {err}")
finally:
    if 'mydb' in locals() and mydb.is_connected():
        mycursor.close()
        mydb.close()