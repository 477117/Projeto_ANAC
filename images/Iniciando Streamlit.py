import streamlit as st
from PIL import Image
import os
import base64
import time  # Para simular um carregamento mais longo

# Dicionário para armazenar os caminhos dos seus gráficos
graficos = {
    "Fabricante/Modelo - Total de Ocorrências": r"C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\Grafico_1.png",
    "Top 12 Tipos de Ococrrências": r"C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\Grafico_2.png",
    "Top 12 Municipios/UF - Total de Ocorrências": r"C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\Grafico_3.png",
    "Fabricante/Modelo - Tipos de Ocorrência": r"C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\Grafico_4.png",
    "Dados Estatísticos por Dia/Ano": r"C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\Grafico_5.png",
    "Tendência/Previsão - Total de Ocorrências": r"C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\Grafico_6.png",
    "Total de Ocorrências por Ano": r"C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\Grafico_7.png",
}

# Dicionário para armazenar informações adicionais sobre os gráficos
info_graficos = {
    "Fabricante/Modelo - Total de Ocorrências": "Este gráfico mostra o total de ocorrências que envolveram os fabricantes e seus modelos.",
    "Top 12 Tipos de Ococrrências": "Este gráfico mostra os 12 tipos de ocorrências com maior índice.",
    "Top 12 Municipios/UF - Total de Ocorrências": "Este gráfico mostra os 12 municípios/UF com maior incidência de ocorrências.",
    "Fabricante/Modelo - Tipos de Ocorrência": "Este gráfico mostra os fabricantes e seus modelos com maior índice por tipo de ocorrência.",
    "Dados Estatísticos por Dia/Ano": "Gráficos com dados estatísticos de ocorrências diárias ao longo dos anos (2014 até 2024)",
    "Tendência/Previsão - Total de Ocorrências": "Gráfico que representa uma tendência (previsão) de ocorrências até o ano de 2026",
    "Total de Ocorrências por Ano": "Este gráfico mostra o total de ocorrências por ano.",
}

# Dicionário de usuários e senhas (EM TEXTO PLANO - PARA DEMONSTRAÇÃO, NÃO USE EM PRODUÇÃO)
USUARIOS = {
    "Aluno": "Aluno123#",
    "Professor": "Profe123#",
    "Visitante": "Visit123#",
}

# Injeta CSS personalizado - tela com cor e formatação 
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6; /* Cor de fundo geral */
    }
    .st-sidebar {
        background-color: #e1e7ed; /* Cor de fundo da barra lateral */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #336699; /* Cor dos títulos */
    }
    .stButton > button {
        background-color: #4CAF50; /* Cor de fundo dos botões */
        color: white; /* Cor do texto dos botões */
        border-radius: 5px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .info-box {
        background-color: #d1ecf1;
        border-color: #bee5eb;
        color: #0c5460;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .caption {
        color: #777;
        font-size: 0.9em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def carregar_imagem(caminho_grafico):
    """Carrega a imagem do gráfico com cache."""
    try:
        img = Image.open(caminho_grafico)
        return img
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {caminho_grafico}")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar a imagem: {e}")
        return None

def img_to_bytes(img_path):
    """Converte um arquivo de imagem para bytes."""
    try:
        with open(img_path, "rb") as img_file:
            return img_file.read()
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {img_path}")
        return None
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None

def mostrar_grafico(nome_grafico, caminho_grafico, info_grafico=None):
    """Exibe o gráfico, suas informações e opções com mensagem de carregamento."""
    st.subheader(f"Gráfico: {nome_grafico}")
    with st.spinner("Carregando gráfico..."):
        imagem = carregar_imagem(caminho_grafico)
        time.sleep(0.2)  # Simula um pequeno delay de carregamento

    if imagem:
        st.image(imagem, caption=nome_grafico)
        if info_grafico:
            st.markdown(f'<div class="info-box">{info_grafico}</div>', unsafe_allow_html=True)

        # Opção de visualização ampliada
        #with st.expander("Visualizar em tamanho maior"):
           # st.image(imagem, caption=nome_grafico, use_column_width=True)

        # Opção de download dos gráficos
        img_bytes = img_to_bytes(caminho_grafico)
        if img_bytes:
            b64 = base64.b64encode(img_bytes).decode()
            href = f'<a href="data:image/png;base64,{b64}" download="{nome_grafico}.png">Baixar Gráfico</a>'
            st.markdown(href, unsafe_allow_html=True)

# Esta função cria a tela de login e autentica os usuários
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
                st.session_state['pagina'] = 'selecao'
                st.session_state['usuario_logado'] = usuario
                st.rerun()
            else:
                st.error("Senha incorreta.")
        else:
            st.error("Usuário não encontrado.")

# Esta função mostra os icones para a seleção dos gráficos
def pagina_selecao():
    """Exibe a página de seleção de gráficos."""
    st.subheader(f"Olá, {st.session_state.get('usuario_logado', 'Usuário')}! Selecione um gráfico para visualizar:")
    colunas_grid = st.columns(3)  # Cria 3 colunas para o grid de botões
    graficos_itens = list(graficos.items())

    for i, (nome_grafico, caminho) in enumerate(graficos_itens):
        with colunas_grid[i % 3]:
            if st.button(nome_grafico, key=f"botao_selecao_{nome_grafico}"):
                st.session_state['pagina'] = nome_grafico
                st.rerun()
            
            # Esta linhas de código mostram um texto sobre o gráfico
            #if nome_grafico in info_graficos:
             #   st.markdown(f'<p class="caption">{info_graficos[nome_grafico]}</p>', unsafe_allow_html=True)

# Esta função mostra o gráfico na tela
def pagina_grafico(nome_grafico):
    """Exibe a página de um gráfico específico."""
    caminho_grafico = graficos[nome_grafico]
    info_do_grafico = info_graficos.get(nome_grafico)
    mostrar_grafico(nome_grafico, caminho_grafico, info_do_grafico)

    if st.button("Voltar para a Seleção"):
        st.session_state['pagina'] = 'selecao'
        st.rerun()

# Esta função cria a tela de login
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

# Função de inicialização 
def main():
    st.title("Visualizador de Gráficos ANAC")

    if 'login_sucesso' not in st.session_state:
        st.session_state['login_sucesso'] = False
        st.session_state['pagina'] = 'login'

    barra_lateral()

    # --- Conteúdo Principal ---
    if not st.session_state['login_sucesso']:
        pagina_login()
    elif st.session_state['pagina'] == 'selecao':
        pagina_selecao()
    elif st.session_state['pagina'] in graficos:
        pagina_grafico(st.session_state['pagina'])

if __name__ == "__main__":
    main()

# Linha para ececutar o steamlit no prompt de comando
# streamlit run "c:/users/usuario/documents/faculdade senac_2025/introducao estatistica/projeto_anac/images/iniciando streamlit.py"