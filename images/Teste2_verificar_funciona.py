import streamlit as st
from PIL import Image
import os

# Dicionário para armazenar os caminhos dos seus gráficos
graficos = {
    "Gráfico de Análise_Python 1": r"C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\Grafico_1.png",
    "Gráfico de Análise_Python 2": r"C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\Grafico_2.png",
    "Gráfico de Análise_Python 3": r"C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\Grafico_3.png",
    "Gráfico de Análise_Python 4": r"C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\Grafico_4.png",
    "Gráfico de Análise_Python 5": r"C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\Grafico_5.png",
    "Gráfico de Análise_Python 6": r"C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\Grafico_6.png",
    "Gráfico de Análise_Python 7": r"C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\Grafico_7.png",
}

# Dicionário para armazenar informações adicionais sobre os gráficos
info_graficos = {
    "Gráfico de Análise_Python 1": "Este gráfico mostra a distribuição de passageiros ao longo do tempo, destacando tendências sazonais e crescimento anual.",
    "Gráfico de Análise_Python 2": "Aqui podemos observar a comparação entre diferentes tipos de voos (domésticos vs. internacionais) em termos de volume e frequência.",
    "Gráfico de Análise_Python 3": "Este gráfico detalha a taxa de ocupação das aeronaves por região do Brasil, indicando a demanda em diferentes mercados.",
    "Gráfico de Análise_Python 4": "Informações sobre o volume de bagagem despachada por voo, com insights sobre possíveis variações por rota ou época do ano.",
    "Gráfico de Análise_Python 5": "Análise da satisfação dos clientes em relação aos serviços de bordo, com métricas e categorias de avaliação.",
    "Gráfico de Análise_Python 6": "Este gráfico apresenta a frequência de atrasos em diferentes aeroportos, identificando possíveis gargalos na operação.",
    "Gráfico de Análise_Python 7": "Visão geral do crescimento do número de voos nos últimos anos, ilustrando a expansão do setor aéreo.",
}

# Dicionário de usuários e senhas (EM TEXTO PLANO - PARA DEMONSTRAÇÃO, NÃO USE EM PRODUÇÃO)
USUARIOS = {
    "Aluno": "Aluno123#",
    "Professor": "Profe123#",
    "Visitante": "Visit123#",
}

def mostrar_grafico(nome_grafico, caminho_grafico, info_grafico=None):
    """Exibe o gráfico e suas informações adicionais."""
    st.subheader(f"Gráfico: {nome_grafico}")
    try:
        if os.path.exists(caminho_grafico):
            imagem = Image.open(caminho_grafico)
            st.image(imagem, caption=nome_grafico)
            if info_grafico:
                st.info(info_grafico)
        else:
            st.error(f"Arquivo não encontrado: {caminho_grafico}")
    except Exception as e:
        st.error(f"Erro ao carregar a imagem: {e}")

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
            if nome_grafico in info_graficos:
                st.caption(info_graficos[nome_grafico][:60] + "...") # Exibe uma breve descrição

def pagina_grafico(nome_grafico):
    """Exibe a página de um gráfico específico."""
    caminho_grafico = graficos[nome_grafico]
    info_do_grafico = info_graficos.get(nome_grafico)
    mostrar_grafico(nome_grafico, caminho_grafico, info_do_grafico)

    if st.button("Voltar para a Seleção"):
        st.session_state['pagina'] = 'selecao'
        st.rerun()

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
    elif st.session_state['pagina'] == 'selecao':
        pagina_selecao()
    elif st.session_state['pagina'] in graficos:
        pagina_grafico(st.session_state['pagina'])

if __name__ == "__main__":
    main()