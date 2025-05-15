# Bibliotecas usadas no processo

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Detalhes da sua conexão com o MySQL
db_host = 'localhost'  # Geralmente 'localhost' ou o IP do servidor MySQL
db_user = 'root'
db_password = '477117'
db_name = 'dw_projeto'

mydb = None
mycursor = None

try:
    mydb = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    mycursor = mydb.cursor()
    query = """
    SELECT 	t.descricao_do_tipo,
    COUNT(o.id_ocorrencia) AS frequencia
    FROM    descricao_tipo t
    JOIN    ocorrencias o ON t.id_descricao_tipo = o.id_descricao_tipo
    GROUP BY   t.descricao_do_tipo
    ORDER BY   frequencia DESC;

    """
    mycursor.execute(query)
    resultados = mycursor.fetchall()
    colunas = ['descricao_tipo', 'frequencia']
    df_tipo_ocorrencia_frequencia = pd.DataFrame(resultados, columns=colunas)
    print(df_tipo_ocorrencia_frequencia.head())
    
    # Geração do Gráfico
    n_top = 12 # com mais ocorrências
    top_tipo_ocorrencia_frequencia = df_tipo_ocorrencia_frequencia.head(n_top)

    plt.figure(figsize=(14, 6))
    ax = sns.barplot(x='descricao_tipo', y='frequencia', data=top_tipo_ocorrencia_frequencia)
    plt.title(f'Top {n_top} Tipos de Ocorrências com mais Frequencia')
    plt.xlabel('Tipos de Ocorrências')
    plt.ylabel('Frequencia')
    plt.xticks(rotation=45, ha='right') # Adicionando a rotação dos rótulos do eixo x

    # Adicionando rótulos nas barras de forma mais simples
    for p in ax.patches:
        altura = p.get_height()
        ax.text(p.get_x() + p.get_width() / 2., altura + 0.2,
        f'{int(altura)}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

except mysql.connector.Error as err:
    print(f"Erro ao conectar ao MySQL: {err}")

finally:
    if mydb and mydb.is_connected():
        mycursor.close()
        mydb.close()
        print("Conexão com o MySQL fechada.")