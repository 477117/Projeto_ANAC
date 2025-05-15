# Visualizador de Gráficos ANAC

Bem-vindo ao repositório do Visualizador de Gráficos ANAC! Este projeto consiste em um aplicativo web interativo construído com Streamlit, projetado para facilitar a exploração e análise de dados da Agência Nacional de Aviação Civil (ANAC) através de visualizações gráficas intuitivas.

Este README fornece um guia completo para entender, instalar e utilizar este aplicativo. Você encontrará informações sobre as funcionalidades oferecidas, as tecnologias empregadas, as etapas de instalação e execução, além de instruções detalhadas sobre como interagir com a interface do usuário.

Esperamos que esta ferramenta seja útil para estudantes, professores, pesquisadores e qualquer pessoa interessada em obter insights a partir dos dados da aviação civil no Brasil. Explore os gráficos, faça seus próprios downloads e aprofunde sua compreensão sobre este importante setor!

Para começar, siga as instruções detalhadas nas próximas seções deste arquivo.

## Funcionalidades Detalhadas

* **Autenticação de Usuário:**
    * Implementa um sistema de login simples diretamente na barra lateral do aplicativo.
    * Permite o acesso com três perfis de usuário distintos: "Aluno", "Professor" e "Visitante".
    * As credenciais para cada usuário são definidas diretamente no código (`USUARIOS`). **É crucial notar que este método de autenticação é apenas para demonstração e não é seguro para ambientes de produção.** Em aplicações reais, um sistema de autenticação mais robusto e seguro deve ser implementado.
    * Oferece uma opção de "Mostrar senha" através de um checkbox para facilitar a digitação e verificação das credenciais.
    * Após o login bem-sucedido, o nome do usuário logado é exibido na tela de seleção de gráficos.
    * Um botão "Sair" na barra lateral permite que o usuário encerre a sessão e retorne à tela de login.

* **Visualização de Gráficos:**
    * A tela principal apresenta uma grade de botões, cada um representando um dos gráficos de análise de dados da ANAC.
    * Ao clicar em um botão, o gráfico correspondente é carregado e exibido na tela.
    * Utiliza a biblioteca PIL (Pillow) para abrir e exibir as imagens dos gráficos.
    * Implementa uma mensagem de carregamento ("Carregando gráfico...") enquanto a imagem é processada, proporcionando um feedback visual ao usuário durante a espera.

* **Informações Adicionais sobre os Gráficos:**
    * Para cada gráfico, uma breve descrição textual é exibida abaixo da imagem.
    * Essas informações contextuais são armazenadas no dicionário `info_graficos` e visam fornecer insights sobre o conteúdo e a relevância de cada visualização de dados.
    * A formatação em uma "info-box" estilizada com CSS ajuda a destacar essas descrições.

* **Opção de Download de Gráficos:**
    * Abaixo de cada gráfico visualizado, um link "Baixar Gráfico" é disponibilizado.
    * Ao clicar neste link, o usuário pode salvar a imagem do gráfico no formato PNG em seu dispositivo local.
    * A funcionalidade de download é implementada convertendo a imagem para bytes e, em seguida, codificando-a em Base64 para criar um link de dados (`data:` URI).

* **Interface de Usuário Intuitiva:**
    * A tela de seleção de gráficos organiza os botões em um layout de grade de três colunas, otimizando o espaço e facilitando a navegação, especialmente em telas maiores.
    * Botões claros e identificáveis com os nomes dos gráficos permitem uma seleção fácil.
    * A funcionalidade de "Voltar para a Seleção" garante uma navegação fluida entre a visualização de um gráfico específico e a tela com todos os gráficos disponíveis.

* **Design Personalizado com CSS:**
    * O aplicativo incorpora um bloco de código Markdown com tags `<style>` para injetar CSS personalizado.
    * Este CSS personaliza a aparência geral do aplicativo, incluindo a cor de fundo, a cor de fundo da barra lateral, a cor dos títulos e a estilização dos botões.
    * A classe `.info-box` define o estilo das caixas de informação dos gráficos, e a classe `.caption` formata legendas ou textos descritivos menores.

* **Otimização com Cache de Imagens:**
    * A função `carregar_imagem` utiliza o decorador `@st.cache_data` do Streamlit.
    * Isso significa que, após a primeira vez que um gráfico é carregado, o Streamlit armazena a imagem em cache. Em visualizações subsequentes do mesmo gráfico, a imagem é carregada diretamente da memória cache, resultando em um carregamento mais rápido e eficiente.

* **Feedback Visual com Mensagem de Carregamento:**
    * Ao selecionar um gráfico para visualização, a função `mostrar_grafico` exibe um spinner com a mensagem "Carregando gráfico...".
    * Isso fornece um feedback visual imediato ao usuário, indicando que o aplicativo está processando a solicitação e carregando a imagem, melhorando a experiência do usuário.
    * Um pequeno delay (`time.sleep(0.2)`) é introduzido para garantir que o spinner seja visível, mesmo para carregamentos rápidos.

## Tecnologias Utilizadas

* **Python (versão 3.6+)**: A linguagem de programação principal para o desenvolvimento do aplicativo Streamlit. Sua sintaxe clara e vasta gama de bibliotecas a tornam ideal para tarefas de análise de dados e criação de interfaces web.
* **Streamlit (versão 1.0+)**: Um framework Python de código aberto que simplifica a criação de aplicativos web interativos para ciência de dados e aprendizado de máquina. Sua API intuitiva permite construir interfaces ricas com poucas linhas de código.
* **Pillow (PIL Fork) (versão 9.0+)**: Uma biblioteca essencial para manipulação de imagens em Python. Neste projeto, é utilizada para abrir e exibir os arquivos de imagem dos gráficos (`.png`).
* **base64 (módulo padrão do Python)**: Fornece funcionalidades para codificar dados binários (como arquivos de imagem) em strings ASCII Base64 e vice-versa. É utilizado aqui para criar URLs de dados que permitem o download das imagens diretamente do navegador.
* **time (módulo padrão do Python)**: Oferece funções relacionadas ao tempo. Neste script, `time.sleep()` é usado para simular um pequeno atraso no carregamento do gráfico, permitindo que a mensagem de carregamento seja exibida adequadamente.

## Pré-requisitos

Antes de executar o aplicativo, certifique-se de que os seguintes pré-requisitos estejam atendidos em seu ambiente de desenvolvimento:

1.  **Python:** É necessário ter o Python instalado em seu sistema operacional. Recomenda-se utilizar a versão 3.6 ou superior para garantir a compatibilidade com as bibliotecas utilizadas. Você pode verificar sua versão do Python abrindo o terminal ou prompt de comando e executando:
    ```bash
    python --version
    ```
    Se o Python não estiver instalado, você pode baixá-lo do site oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2.  **Gerenciador de Pacotes Pip:** O Pip (Package Installer for Python) é o gerenciador de pacotes padrão para Python e é utilizado para instalar e gerenciar as bibliotecas de terceiros necessárias para o projeto. Geralmente, o Pip é instalado automaticamente com o Python. Você pode verificar se o Pip está instalado executando:
    ```bash
    pip --version
    ```
    Se o Pip não estiver instalado ou precisar ser atualizado, consulte a documentação oficial do Python para obter instruções de instalação: [https://pip.pypa.io/en/stable/installation/](https://pip.pypa.io/en/stable/installation/)

3.  **Bibliotecas Python:** As seguintes bibliotecas Python são dependências do projeto e precisam ser instaladas utilizando o Pip:
    * `streamlit`
    * `Pillow`

    Para instalar essas bibliotecas, abra o seu terminal ou prompt de comando e execute o seguinte comando:
    ```bash
    pip install streamlit Pillow
    ```
    Este comando irá baixar e instalar as versões mais recentes dessas bibliotecas e quaisquer outras dependências necessárias. Certifique-se de executar este comando no ambiente Python onde você pretende executar o aplicativo.

Com o Python e as bibliotecas necessárias instaladas, você estará pronto para configurar e executar o Visualizador de Gráficos ANAC.

## Instalação

Para configurar o Visualizador de Gráficos ANAC em seu ambiente local, siga estas etapas:

1.  **Clone o Repositório (Opcional):** Se o código deste aplicativo estiver hospedado em um repositório Git (como o GitHub), você pode cloná-lo para o seu computador utilizando o seguinte comando no seu terminal ou prompt de comando:
    ```bash
    git clone [URL_DO_SEU_REPOSITÓRIO]
    cd [NOME_DO_REPOSITÓRIO]
    ```
    Substitua `[URL_DO_SEU_REPOSITÓRIO]` pelo endereço web do seu repositório e `[NOME_DO_REPOSITÓRIO]` pelo nome da pasta que será criada localmente.

2.  **Obtenha o Arquivo do Script:** Se você recebeu o código diretamente (por exemplo, como um arquivo `.py`), salve-o em um local de sua preferência em seu sistema. Certifique-se de lembrar o diretório onde o arquivo foi salvo. Por conveniência, você pode renomeá-lo para `app_anac.py`.

3.  **Organize as Imagens dos Gráficos:** O script espera encontrar os arquivos de imagem dos gráficos em um diretório específico, conforme definido no dicionário `graficos` dentro do código Python. Por padrão, os caminhos estão configurados para:
    ```
    C:\Users\usuario\Documents\Faculdade Senac_2025\Introducao Estatistica\Projeto_ANAC\images\
    ```
    **É fundamental que você ajuste esses caminhos no seu script `app_anac.py` para corresponder à localização real das suas imagens.** Se você preferir manter suas imagens em um diretório diferente, modifique os valores no dicionário `graficos` para os caminhos corretos. Uma estrutura de pastas comum seria criar uma pasta chamada `images` no mesmo diretório do seu script `app_anac.py` e colocar todos os arquivos `.png` dos gráficos dentro dela. Nesse caso, você ajustaria o dicionário `graficos` da seguinte forma:
    ```python
    graficos = {
        "Gráfico de Análise_Python 1": r"images/Grafico_1.png",
        "Gráfico de Análise_Python 2": r"images/Grafico_2.png",
        "Gráfico de Análise_Python 3": r"images/Grafico_3.png",
        "Gráfico de Análise_Python 4": r"images/Grafico_4.png",
        "Gráfico de Análise_Python 5": r"images/Grafico_5.png",
        "Gráfico de Análise_Python 6": r"images/Grafico_6.png",
        "Gráfico de Análise_Python 7": r"images/Grafico_7.png",
    }
    ```
    Certifique-se de que os nomes dos arquivos no dicionário `graficos` correspondam exatamente aos nomes dos seus arquivos de imagem.

Com o script salvo e as imagens organizadas no local correto (e os caminhos no script atualizados, se necessário), você estará pronto para executar o aplicativo.

## Como Executar o Aplicativo

Siga estas etapas para iniciar o Visualizador de Gráficos ANAC:

1.  **Abra o Terminal ou Prompt de Comando:** No seu sistema operacional, abra a interface de linha de comando.

2.  **Navegue até o Diretório do Projeto:** Utilize o comando `cd` (change directory) para navegar até a pasta onde você salvou o arquivo `app_anac.py`. Por exemplo, se você clonou o repositório para uma pasta chamada `visualizador_anac` na sua área de trabalho, o comando seria algo como:
    ```bash
    cd Desktop/visualizador_anac
    ```
    Se você simplesmente salvou o arquivo `app_anac.py` em um diretório específico, navegue até esse diretório.

3.  **Execute o Comando Streamlit:** Uma vez que você esteja no diretório correto, execute o seguinte comando para iniciar o aplicativo Streamlit:
    ```bash
    streamlit run app_anac.py
    ```
    Ao executar este comando, o Streamlit iniciará um servidor de desenvolvimento local e abrirá automaticamente o seu navegador web padrão com a interface do Visualizador de Gráficos ANAC. Geralmente, o aplicativo estará acessível no endereço `http://localhost:8501`.

4.  **Interaja com o Aplicativo:** No seu navegador web, você verá a interface do aplicativo. Siga as instruções na tela para fazer login e visualizar os gráficos disponíveis.

Enquanto o aplicativo estiver em execução, o terminal ou prompt de comando onde você executou o comando `streamlit run` exibirá logs e informações sobre a atividade do servidor Streamlit. Para parar o aplicativo, você pode geralmente pressionar `Ctrl + C` no terminal.

## Uso

Após executar o aplicativo com sucesso, você poderá interagir com a interface web no seu navegador:

1.  **Barra Lateral de Autenticação:** No lado esquerdo da tela, você encontrará a barra lateral com a seção de "Autenticação".
    * **Usuário:** Digite o nome de usuário desejado (Aluno, Professor ou Visitante).
    * **Senha:** Digite a senha correspondente (Aluno123#, Profe123# ou Visit123#).
    * **Mostrar senha (Checkbox):** Marque esta opção se desejar visualizar a senha enquanto a digita.
    * **Entrar (Botão):** Clique neste botão para tentar fazer login.
    * **Feedback de Login:** Se as credenciais estiverem corretas, uma mensagem de sucesso será exibida, e você será redirecionado para a tela de seleção de gráficos. Se as credenciais estiverem incorretas, uma mensagem de erro será mostrada.

2.  **Tela de Seleção de Gráficos:** Após o login bem-sucedido, a tela principal exibirá uma grade de botões. Cada botão representa um dos gráficos de análise de dados da ANAC disponíveis para visualização. Os nomes dos botões corresponderão aos nomes definidos no dicionário `graficos` no script.

3.  **Visualização de um Gráfico:**
    * Clique em um dos botões de gráfico na tela de seleção.
    * Uma mensagem "Carregando gráfico..." será brevemente exibida enquanto a imagem é processada.
    * O gráfico selecionado aparecerá na tela, juntamente com o seu nome como um subtítulo.
    * Abaixo do gráfico, uma caixa de informação (estilizada) exibirá a descrição textual correspondente, conforme definido no dicionário `info_graficos`.

4.  **Download do Gráfico:**
    * Próximo ao gráfico visualizado, você encontrará um link com o texto "Baixar Gráfico".
    * Clique neste link para iniciar o download da imagem do gráfico no formato PNG para o seu dispositivo. O nome do arquivo baixado será o mesmo nome do gráfico (por exemplo, `Gráfico de Análise_Python 1.png`).

5.  **Voltar para a Seleção:**
    * Na parte inferior da página de visualização de um gráfico, haverá um botão com o texto "Voltar para a Seleção".
    * Clique neste botão para retornar à tela principal com todos os botões de seleção de gráficos.

6.  **Sair (Barra Lateral):**
    * Se você já estiver logado, um botão "Sair" estará visível na barra lateral.
    * Clique neste botão para encerrar a sua sessão. Você será deslogado e redirecionado de volta para a tela de login na próxima vez que a página for carregada ou atualizada.

Através desta interface simples e intuitiva, você pode facilmente navegar entre os diferentes gráficos, visualizar as informações relevantes e baixar as imagens para suas próprias análises ou apresentações.