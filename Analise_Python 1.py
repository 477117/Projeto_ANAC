# Bibliotecas usadas no processo

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    SELECT a.nome_do_fabricante, a.modelo, COUNT(o.id_ocorrencia) AS total_ocorrencias
    FROM aeronaves a
    LEFT JOIN ocorrencias o ON a.id_aeronave = o.id_aeronave
    GROUP BY a.nome_do_fabricante, a.modelo
    ORDER BY total_ocorrencias DESC;
    """
    
    mycursor.execute(query)
    resultados = mycursor.fetchall()
    colunas = ['fabricante', 'modelo', 'total_ocorrencias']
    df_fabricante = pd.DataFrame(resultados, columns=colunas)
    print(df_fabricante.head(12))

    # Geração do Gráfico
    n_top = 12 # Número de combinações (tipo, fabricante, modelo) a serem exibidas
    top_ocorrencias = df_fabricante.head(n_top)

    plt.figure(figsize=(14, 8))
    ax = sns.barplot(x='total_ocorrencias', y=top_ocorrencias['fabricante'] + ' / ' + top_ocorrencias['modelo'], data=top_ocorrencias, dodge=False)
    plt.title(f'Top {n_top} Fabricante / Modelo (Total de Ocorrências)')
    plt.xlabel('Total de Ocorrências')
    plt.ylabel('Fabricante / Modelo')

    # Adicionando rótulos nas barras
    for p in ax.patches:
        largura = p.get_width()
        altura = p.get_y() + p.get_height() / 2.
        x = largura + 0.2
        ax.text(x, altura, f'{int(largura)}', ha='left', va='center')

    plt.tight_layout()
    plt.show()

except mysql.connector.Error as err:
    print(f"Erro ao conectar ao MySQL: {err}")

finally:
    if mydb and mydb.is_connected():
        mycursor.close()
        mydb.close()
        print("Conexão com o MySQL fechada.")