# Bibliotecas usadas no processo
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mode
import numpy as np  # Importe a biblioteca NumPy para usar NaN
from sklearn.linear_model import LinearRegression


# Gera o grafico preditivo para os anos seguinte a 2024

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
    SELECT
        YEAR(data_da_ocorrencia) AS ano,
        COUNT(id_ocorrencia) AS total_ocorrencias
    FROM
        ocorrencias
    GROUP BY
        ano
    HAVING
        ano >= 2014
    ORDER BY
        ano;
    """

    mycursor.execute(query)
    resultados = mycursor.fetchall()
    colunas = ['ano', 'total_ocorrencias']
    df_ocorrencias_ano = pd.DataFrame(resultados, columns=colunas)
    print(df_ocorrencias_ano.head())

    # Calcular as estatísticas POR ANO
    estatisticas_por_ano = df_ocorrencias_ano.groupby('ano')['total_ocorrencias'].agg(['mean', 'median', 'std'])
    estatisticas_por_ano = estatisticas_por_ano.rename(columns={'mean': 'média', 'median': 'mediana', 'std': 'desvio padrão'})
    estatisticas_por_ano = estatisticas_por_ano.reset_index()

    print("\nEstatísticas de Ocorrências por Ano:")
    print(estatisticas_por_ano)

    
    # Função para adicionar rótulos em gráficos de linha
    def add_value_labels_line(ax, spacing=5):
        for line in ax.lines:
            for x, y in zip(line.get_xdata(), line.get_ydata()):
                ax.annotate(f'{y:.0f}', (x, y), textcoords="offset points", xytext=(0, spacing), ha='center')

    # Função para adicionar rótulos em gráficos de barra
    def add_value_labels_bar(ax, spacing=5):
        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = spacing
            va = 'bottom'
            if y_value < 0:
                space *= -1
                va = 'top'
            label = f'{y_value:.2f}'
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center', va=va)

    # 1. Gráfico do Total de Ocorrências por Ano COM TENDÊNCIA E PREVISÃO
    plt.figure(figsize=(12, 6))
    ax1 = sns.scatterplot(x='ano', y='total_ocorrencias', data=df_ocorrencias_ano, label='Total de Ocorrências (Real)')

    # Preparar dados para regressão
    anos = df_ocorrencias_ano['ano'].values.reshape(-1, 1)
    ocorrencias = df_ocorrencias_ano['total_ocorrencias'].values

    # Ajustar modelo de regressão linear
    modelo = LinearRegression()
    modelo.fit(anos, ocorrencias)

    # Criar anos para a linha de tendência (incluindo a previsão)
    anos_tendencia = np.array(range(df_ocorrencias_ano['ano'].min(), 2027)).reshape(-1, 1)
    previsoes_tendencia = modelo.predict(anos_tendencia)

    # Plotar a linha de tendência
    plt.plot(anos_tendencia, previsoes_tendencia, color='red', linestyle='--', label='Tendência (com Previsão)')
    add_value_labels_line(ax1) # Adiciona rótulos aos dados reais

    plt.title('Tendência do Total de Ocorrências por Ano com Previsão até 2026')
    plt.xlabel('Ano')
    plt.ylabel('Total de Ocorrências')
    plt.xticks(range(df_ocorrencias_ano['ano'].min(), 2027))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 2. Gráfico do Total de Ocorrências por Ano (SEM PREVISÃO - apenas a linha original)
    plt.figure(figsize=(10, 5))
    ax2 = sns.lineplot(x='ano', y='total_ocorrencias', data=df_ocorrencias_ano, marker='o')
    add_value_labels_line(ax2) # Adiciona rótulos
    plt.title('Total de Ocorrências por Ano')
    plt.xlabel('Ano')
    plt.ylabel('Total de Ocorrências')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

 


except mysql.connector.Error as err:
    print(f"Erro ao conectar ao MySQL: {err}")

finally:
    if mydb.is_connected():
        mycursor.close()
        mydb.close()
        print("Conexão com o MySQL fechada.")