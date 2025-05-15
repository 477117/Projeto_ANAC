import mysql.connector
import pandas as pd
import numpy as np
import mysql.connector

def carga_descricao_tipo(df):
    cnx = mysql.connector.connect(user='root',password='477117',host='localhost',database='dw_projeto' )
    cursor = cnx.cursor()
    for i,df_descricao_tipo_coluna in df[['Descricao_do_Tipo']].drop_duplicates().iterrows(): # Carrega apenas descrições únicas
        cursor.execute('''select id_descricao_tipo from dw_projeto.descricao_tipo where descricao_do_tipo = %s''',( df_descricao_tipo_coluna['Descricao_do_Tipo'],))
        result=cursor.fetchone()
        if not result :
            cursor.execute('''insert into dw_projeto.descricao_tipo(descricao_do_tipo) values (%s)''',(df_descricao_tipo_coluna['Descricao_do_Tipo'],))
    cnx.commit()
    cursor.close()
    cnx.close()

def carga_locais(df):
    cnx = mysql.connector.connect(user='root',password='477117',host='localhost',database='dw_projeto' )
    cursor = cnx.cursor()
    for i,df_locais_coluna in df[['Municipio', 'UF']].drop_duplicates().iterrows(): # Carrega apenas locais únicos
        cursor.execute('''select id_local from dw_projeto.locais where uf = %s and municipio = %s''',( df_locais_coluna['UF'], df_locais_coluna['Municipio']))
        result=cursor.fetchone()
        if not result :
            cursor.execute('''insert into dw_projeto.locais(municipio, uf) values (%s,%s)''',(df_locais_coluna['Municipio'], df_locais_coluna['UF']))
    cnx.commit()
    cursor.close()
    cnx.close()

def carga_aeronaves(df):
    cnx = mysql.connector.connect(user='root',password='477117',host='localhost',database='dw_projeto' )
    cursor = cnx.cursor()
    for i,df_aeronaves_coluna in df[['Modelo', 'Nome_do_Fabricante']].drop_duplicates().iterrows(): # Carrega apenas aeronaves únicas
        cursor.execute('''select id_aeronave from dw_projeto.aeronaves where modelo = %s and nome_do_fabricante = %s''',( df_aeronaves_coluna['Modelo'], df_aeronaves_coluna['Nome_do_Fabricante']))
        result=cursor.fetchone()
        if not result :
            cursor.execute('''insert into dw_projeto.aeronaves(modelo, nome_do_fabricante) values (%s,%s)''',(df_aeronaves_coluna['Modelo'], df_aeronaves_coluna['Nome_do_Fabricante']))
    cnx.commit()
    cursor.close()
    cnx.close()

def carga_ocorrencias(df):
    cnx = mysql.connector.connect(user='root', password='477117', host='localhost', database='dw_projeto')
    cursor = cnx.cursor()

    for i, df_ocorrencias_coluna in df.iterrows():
        numero_ocorrencia = df_ocorrencias_coluna['Numero_da_Ocorrencia']
        data_ocorrencia = df_ocorrencias_coluna['Data_da_Ocorrencia']

        modelo_aeronave = df_ocorrencias_coluna.get('Modelo')
        uf_local = df_ocorrencias_coluna.get('UF')
        descricao_tipo = df_ocorrencias_coluna.get('Descricao_do_Tipo')
        municipio_local = df_ocorrencias_coluna.get('Municipio')
        nome_fabricante = df_ocorrencias_coluna.get('Nome_do_Fabricante')

        cursor.execute('''select Numero_da_Ocorrencia from dw_projeto.ocorrencias where numero_da_ocorrencia = %s''', (numero_ocorrencia,))
        result = cursor.fetchone()

        if not result:
            id_aeronave = None
            id_local = None
            id_descricao_tipo = None

            if modelo_aeronave and nome_fabricante:
                cursor.execute('''select id_aeronave from dw_projeto.aeronaves where modelo = %s and nome_do_fabricante = %s''', (modelo_aeronave, nome_fabricante))
                aeronave_result = cursor.fetchone()
                if aeronave_result:
                    id_aeronave = aeronave_result[0]

            if uf_local and municipio_local:
                cursor.execute('''select id_local from dw_projeto.locais where uf = %s and municipio = %s''', (uf_local, municipio_local))
                local_result = cursor.fetchone()
                if local_result:
                    id_local = local_result[0]

            if descricao_tipo:
                cursor.execute('''select id_descricao_tipo from dw_projeto.descricao_tipo where descricao_do_tipo = %s''', (descricao_tipo,))
                descricao_result = cursor.fetchone()
                if descricao_result:
                    id_descricao_tipo = descricao_result[0]

            cursor.execute('''
                insert into dw_projeto.ocorrencias (
                    numero_da_ocorrencia,
                    data_da_ocorrencia,
                    id_aeronave,
                    id_local,
                    id_descricao_tipo
                )
                values (%s, %s, %s, %s, %s)
            ''', (numero_ocorrencia, data_ocorrencia, id_aeronave, id_local, id_descricao_tipo))
            cnx.commit()

    cursor.close()
    cnx.close()

# Caminho para o arquivo CSV
arquivo_csv = r'c:\Users\usuario\Documents\Faculdade Senac_2025_Atividades\Introducao Estatistica\Projeto_ANAC\V_OCORRENCIA_AMPLA.csv'
df_original = pd.read_csv(arquivo_csv, sep=';')
colunas = ["Numero_da_Ocorrencia", "Descricao_do_Tipo", "Data_da_Ocorrencia", "Municipio", "UF", "Nome_do_Fabricante", "Modelo"]
df = df_original[colunas].copy() # Use .copy() para evitar SettingWithCopyWarning

# Limpeza e tratamento de dados (manter como está)
df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
df.replace('', np.nan, inplace=True)
df.dropna(subset=['Descricao_do_Tipo'], inplace=True)
df = df[df['Descricao_do_Tipo'].str.strip() != ''].copy()
df = df[df['Descricao_do_Tipo'].str.split().apply(len) > 2].copy()
df['Descricao_do_Tipo'] = df['Descricao_do_Tipo'].str.lower().str.strip()
df['Descricao_do_Tipo'] = df['Descricao_do_Tipo'].apply(lambda x: ' '.join(x.split()))
df['Data_da_Ocorrencia'] = pd.to_datetime(df['Data_da_Ocorrencia'], format='%d/%m/%Y', errors='coerce').dt.strftime('%Y-%m-%d')
df.dropna(subset=['Data_da_Ocorrencia'], inplace=True)
df['Municipio'] = df['Municipio'].fillna('Desconhecido').str.upper().str.strip()
df['UF'] = df['UF'].fillna('Desconhecido').str.upper().str.strip()
df['Modelo'] = df['Modelo'].fillna('Desconhecido').str.strip()
df['Nome_do_Fabricante'] = df['Nome_do_Fabricante'].fillna('Desconhecido').str.strip()

# Executa carga de Dados (ordem corrigida e carregando dados únicos nas dimensões)
carga_descricao_tipo(df)
carga_locais(df)
carga_aeronaves(df)
carga_ocorrencias(df)