"""
=============================================================================
GRADE EXPANDIDA DAS 8 ESCOLAS DA COMPUTAÇÃO (MAPAS 201 A 700)
=============================================================================
Complementa os 200 mapas iniciais para totalizar 700 mapas mentais no padrão
Sketchnote, unindo os 3 pilares:
1. UNINTER: Base acadêmica, fundamentos teóricos e rigor científico
2. ALURA: Prática de mercado, ferramentas contemporâneas e trilhas de carreira
3. FEYNMAN / CS50: Analogias intuitivas de primeiros princípios para iniciantes
=============================================================================
"""

from typing import List, Dict

# =============================================================================
# ESCOLA 03: PYTHON ESPECIALISTA (IDs 201 ao 260 - 60 Mapas)
# =============================================================================
MAPAS_PYTHON: List[Dict] = [
    # Carreira 1: Sintaxe Moderna & Estruturas de Dados Pythonicas
    {"id": 201, "escola": "03_python_especialista", "modulo": "Python Básico", "tema": "Variáveis e F-Strings no Python 3", "foco": "Interpolação moderna de variáveis com f-strings sem concatenações confusas"},
    {"id": 202, "escola": "03_python_especialista", "modulo": "Python Básico", "tema": "Listas e Métodos: append, pop e slicing", "foco": "Manipulando gavetas sequenciais com fatiamento dinâmico [inicio:fim:passo]"},
    {"id": 203, "escola": "03_python_especialista", "modulo": "Python Básico", "tema": "Tuplas vs Listas: Por que Imutabilidade Importa?", "foco": "Dados protegidos contra alterações acidentais e ganho de performance"},
    {"id": 204, "escola": "03_python_especialista", "modulo": "Python Básico", "tema": "Dicionários Python: Chave e Valor", "foco": "Busca ultrarrápida via Hash Table sem varrer lista inteira"},
    {"id": 205, "escola": "03_python_especialista", "modulo": "Python Básico", "tema": "Conjuntos (Sets) e Operações Matemáticas", "foco": "Removendo duplicatas automaticamente com união, interseção e diferença"},
    {"id": 206, "escola": "03_python_especialista", "modulo": "Python Básico", "tema": "List Comprehensions: Loops Elegantes em 1 Linha", "foco": "Transformando e filtrando listas de forma concisa e legível"},
    {"id": 207, "escola": "03_python_especialista", "modulo": "Python Básico", "tema": "Dict Comprehensions e Set Comprehensions", "foco": "Criando tabelas e conjuntos dinâmicos com sintaxe funcional"},
    {"id": 208, "escola": "03_python_especialista", "modulo": "Python Básico", "tema": "Funções com *args e **kwargs Descomplicadas", "foco": "Recebendo quantidade flexível de argumentos posicionais e nomeados"},
    {"id": 209, "escola": "03_python_especialista", "modulo": "Python Básico", "tema": "Funções Lambda e Map/Filter no Python", "foco": "Pequenas funções anônimas para transformações imediatas"},
    {"id": 210, "escola": "03_python_especialista", "modulo": "Python Básico", "tema": "Geradores (yield) e Economia de Memória", "foco": "Processando milhões de registros sob demanda sem estourar a RAM"},
    {"id": 211, "escola": "03_python_especialista", "modulo": "Python Básico", "tema": "Tratamento de Exceções: try, except, else e finally", "foco": "Como blindar o script para nunca fechar inesperadamente na cara do usuário"},
    {"id": 212, "escola": "03_python_especialista", "modulo": "Python Básico", "tema": "Gerenciador de Contexto: O Comando with", "foco": "Fechamento automático e seguro de conexões e arquivos"},
    
    # Carreira 2: Automação de Tarefas & Manipulação de Arquivos
    {"id": 213, "escola": "03_python_especialista", "modulo": "Automação", "tema": "Manipulação de Arquivos de Texto (TXT e CSV)", "foco": "Lendo e escrevendo relatórios linha por linha com o módulo csv"},
    {"id": 214, "escola": "03_python_especialista", "modulo": "Automação", "tema": "Manipulando JSON no Python (json.loads e json.dumps)", "foco": "Convertendo dicionários em texto para APIs e vice-versa"},
    {"id": 215, "escola": "03_python_especialista", "modulo": "Automação", "tema": "O Módulo pathlib: Caminhos Modernos no Windows e Linux", "foco": "Criando pastas e encontrando arquivos sem conflito de barras"},
    {"id": 216, "escola": "03_python_especialista", "modulo": "Automação", "tema": "Automação de Planilhas com openpyxl", "foco": "Lendo células, criando fórmulas e formatando planilhas Excel em segundos"},
    {"id": 217, "escola": "03_python_especialista", "modulo": "Automação", "tema": "Manipulação de PDFs com pypdf e pdfplumber", "foco": "Juntando relatórios, extraindo texto e dividindo páginas"},
    {"id": 218, "escola": "03_python_especialista", "modulo": "Automação", "tema": "Automação de Mouse e Teclado com pyautogui", "foco": "O robô que clica e digita na tela simulando o humano"},
    {"id": 219, "escola": "03_python_especialista", "modulo": "Automação", "tema": "Envio Automatizado de E-mails com smtplib e email", "foco": "Disparando alertas com anexos em HTML automaticamente"},
    {"id": 220, "escola": "03_python_especialista", "modulo": "Automação", "tema": "Agendamento de Scripts com schedule e cron", "foco": "Fazendo seu script rodar todo dia às 8h da manhã sozinho"},
    
    # Carreira 3: Web Scraping & Coleta Automatizada
    {"id": 221, "escola": "03_python_especialista", "modulo": "Web Scraping", "tema": "Requisições HTTP com a Biblioteca requests", "foco": "GET, POST, Headers, status codes e timeout na prática"},
    {"id": 222, "escola": "03_python_especialista", "modulo": "Web Scraping", "tema": "Parseando HTML com BeautifulSoup4", "foco": "Encontrando tags, classes e IDs com find e find_all"},
    {"id": 223, "escola": "03_python_especialista", "modulo": "Web Scraping", "tema": "Navegação Automatizada com Selenium WebDriver", "foco": "Preenchendo formulários, lidando com JavaScript e aguardando elementos"},
    {"id": 224, "escola": "03_python_especialista", "modulo": "Web Scraping", "tema": "Scraping Moderno com Playwright Python", "foco": "Automação headless ultrarrápida com auto-wait e interceptação de rede"},
    {"id": 225, "escola": "03_python_especialista", "modulo": "Web Scraping", "tema": "Boas Práticas de Scraping: Rate Limit e User-Agents", "foco": "Como não derrubar o servidor e evitar bloqueios IP com rotação de headers"},
    {"id": 226, "escola": "03_python_especialista", "modulo": "Web Scraping", "tema": "Extração de Dados com Expressões Regulares (re)", "foco": "Capturando CPFs, telefones e e-mails com padrões de Regex"},

    # Carreira 4: POO Avançada & Boas Práticas Python
    {"id": 227, "escola": "03_python_especialista", "modulo": "POO Python", "tema": "Classes, Instâncias e o Método __init__", "foco": "O molde do bolo vs o bolo real na memória do computador"},
    {"id": 228, "escola": "03_python_especialista", "modulo": "POO Python", "tema": "O Parâmetro self Desmistificado", "foco": "Como cada objeto sabe quem ele é dentro da classe"},
    {"id": 229, "escola": "03_python_especialista", "modulo": "POO Python", "tema": "Métodos Especiais (Dunder Methods: __str__, __repr__, __len__)", "foco": "Ensinando o Python a tratar sua classe como tipo nativo"},
    {"id": 230, "escola": "03_python_especialista", "modulo": "POO Python", "tema": "Encapsulamento e Getters/Setters com @property", "foco": "Controlando acesso a atributos sem quebrar a sintaxe limpa"},
    {"id": 231, "escola": "03_python_especialista", "modulo": "POO Python", "tema": "Herança Simples e a Função super()", "foco": "Aproveitando a lógica da classe mãe e estendendo comportamentos"},
    {"id": 232, "escola": "03_python_especialista", "modulo": "POO Python", "tema": "Herança Múltipla e o MRO (Method Resolution Order)", "foco": "A ordem de busca dos métodos quando uma classe herda de várias"},
    {"id": 233, "escola": "03_python_especialista", "modulo": "POO Python", "tema": "Decorators no Python: Criando Funções que Envolvem Funções", "foco": "Medindo tempo de execução e checando login com @decorador"},
    {"id": 234, "escola": "03_python_especialista", "modulo": "POO Python", "tema": "Dataclasses: Classes Limpas sem Boilerplate", "foco": "O decorador @dataclass que gera construtor e comparações sozinho"},
    {"id": 235, "escola": "03_python_especialista", "modulo": "POO Python", "tema": "Tipagem Estática (Type Hints) e MyPy", "foco": "Prevenindo bugs antes da execução indicando tipos nas variáveis"},

    # Carreira 5: Desenvolvimento de APIs com FastAPI
    {"id": 236, "escola": "03_python_especialista", "modulo": "APIs Python", "tema": "Introdução ao FastAPI e Swagger UI Automático", "foco": "Criando seu primeiro endpoint / com documentação interativa grátis"},
    {"id": 237, "escola": "03_python_especialista", "modulo": "APIs Python", "tema": "Modelos Pydantic para Validação de Dados", "foco": "Garantindo que o JSON recebido tenha os campos e tipos corretos"},
    {"id": 238, "escola": "03_python_especialista", "modulo": "APIs Python", "tema": "Operações CRUD no FastAPI (GET, POST, PUT, DELETE)", "foco": "O ciclo completo de leitura, cadastro, atualização e exclusão"},
    {"id": 239, "escola": "03_python_especialista", "modulo": "APIs Python", "tema": "Injeção de Dependências (Depends) no FastAPI", "foco": "Compartilhando conexão com banco e autenticação de forma limpa"},
    {"id": 240, "escola": "03_python_especialista", "modulo": "APIs Python", "tema": "Autenticação JWT (JSON Web Token) no FastAPI", "foco": "Gerando tokens assinados para rotas protegidas de usuários"},
    {"id": 241, "escola": "03_python_especialista", "modulo": "APIs Python", "tema": "Conexão com Banco de Dados usando SQLAlchemy 2.0", "foco": "Mapeamento Objeto-Relacional moderno no Python"},
    {"id": 242, "escola": "03_python_especialista", "modulo": "APIs Python", "tema": "Migrações de Banco com Alembic", "foco": "Histórico de versão do esquema do banco de dados em código"},
    {"id": 243, "escola": "03_python_especialista", "modulo": "APIs Python", "tema": "Testes Automatizados de API com pytest e TestClient", "foco": "Garantindo que nenhum deploy quebre endpoints existentes"},

    # Carreira 6: Análise de Dados Rápida & Ferramentas
    {"id": 244, "escola": "03_python_especialista", "modulo": "Data Python", "tema": "Introdução ao Pandas: DataFrames e Séries", "foco": "A planilha de Excel turbinada na memória do Python"},
    {"id": 245, "escola": "03_python_especialista", "modulo": "Data Python", "tema": "Filtros e Seleções no Pandas (loc e iloc)", "foco": "Como fatiar linhas e colunas com critérios booleanos"},
    {"id": 246, "escola": "03_python_especialista", "modulo": "Data Python", "tema": "Limpeza de Dados: Tratando Valores Nulos (NaN)", "foco": "Identificando buracos na tabela com dropna e fillna"},
    {"id": 247, "escola": "03_python_especialista", "modulo": "Data Python", "tema": "Agrupamentos com groupby no Pandas", "foco": "Calculando médias, somas e métricas por categoria"},
    {"id": 248, "escola": "03_python_especialista", "modulo": "Data Python", "tema": "Gráficos Rápidos com Matplotlib e Seaborn", "foco": "Visualizando tendências com gráficos de linha, barra e dispersão"},
    {"id": 249, "escola": "03_python_especialista", "modulo": "Data Python", "tema": "Introdução ao NumPy: Arrays e Operações Vetoriais", "foco": "Cálculos matemáticos ultrarrápidos em lote sem usar loops"},
    {"id": 250, "escola": "03_python_especialista", "modulo": "Data Python", "tema": "Jupyter Notebooks: O Playground Científico", "foco": "Células interativas que misturam código, anotações e gráficos"},

    # Carreira 7: Empacotamento, Ambientes & Produção
    {"id": 251, "escola": "03_python_especialista", "modulo": "Deploy Python", "tema": "Ambientes Virtuais (venv): Isolando Dependências", "foco": "Evitando que pacotes de um projeto quebrem o outro no computador"},
    {"id": 252, "escola": "03_python_especialista", "modulo": "Deploy Python", "tema": "Gerenciamento de Pacotes com pip e requirements.txt", "foco": "Congelando e instalando versões exatas de bibliotecas"},
    {"id": 253, "escola": "03_python_especialista", "modulo": "Deploy Python", "tema": "Poetry e UV: Os Gerenciadores Modernos de Python", "foco": "Resolução veloz de dependências e empacotamento profissional"},
    {"id": 254, "escola": "03_python_especialista", "modulo": "Deploy Python", "tema": "Criando um Executável .EXE com PyInstaller", "foco": "Entregando seu script para o cliente final rodar com 2 cliques sem instalar Python"},
    {"id": 255, "escola": "03_python_especialista", "modulo": "Deploy Python", "tema": "Variáveis de Ambiente com python-dotenv", "foco": "Escondendo senhas e chaves de API fora do código fonte"},
    {"id": 256, "escola": "03_python_especialista", "modulo": "Deploy Python", "tema": "Logging Profissional no Python (logging module)", "foco": "Substituindo print por logs com timestamp e níveis de severidade"},
    {"id": 257, "escola": "03_python_especialista", "modulo": "Deploy Python", "tema": "Concorrência com Threading vs Multiprocessing", "foco": "Quando usar I/O bound com threads e quando usar CPU bound com processos"},
    {"id": 258, "escola": "03_python_especialista", "modulo": "Deploy Python", "tema": "Programação Assíncrona com asyncio e async/await", "foco": "Executando milhares de requisições de rede em um único thread"},
    {"id": 259, "escola": "03_python_especialista", "modulo": "Deploy Python", "tema": "Formatadores de Código: Black, Flake8 e Ruff", "foco": "Padronizando o estilo de código da equipe automaticamente"},
    {"id": 260, "escola": "03_python_especialista", "modulo": "Deploy Python", "tema": "Publicando seu Próprio Pacote no PyPI", "foco": "Como empacotar seu código para qualquer pessoa instalar com pip install"}
]

# =============================================================================
# ESCOLA 07: DEVOPS, LINUX & NUVEM (IDs 261 ao 340 - 80 Mapas)
# =============================================================================
MAPAS_DEVOPS: List[Dict] = [
    # Carreira 1: Linux Essencial & Shell Scripting
    {"id": 261, "escola": "07_devops_linux_e_nuvem", "modulo": "Linux", "tema": "A Árvore de Diretórios do Linux (/etc, /var, /home, /bin)", "foco": "A organização do sistema de arquivos onde tudo é um arquivo"},
    {"id": 262, "escola": "07_devops_linux_e_nuvem", "modulo": "Linux", "tema": "Navegação e Manipulação: cd, ls, mkdir, cp, mv, rm", "foco": "Comandos fundamentais do terminal sem medo de perder arquivos"},
    {"id": 263, "escola": "07_devops_linux_e_nuvem", "modulo": "Linux", "tema": "Visualizando Arquivos: cat, less, head, tail e tail -f", "foco": "Acompanhando logs de servidores em tempo real no console"},
    {"id": 264, "escola": "07_devops_linux_e_nuvem", "modulo": "Linux", "tema": "Permissões de Arquivos: chmod, chown e Octal (rwx)", "foco": "O segredo de 777, 755, leitura, escrita e execução para dono, grupo e outros"},
    {"id": 265, "escola": "07_devops_linux_e_nuvem", "modulo": "Linux", "tema": "O Poder do Pipe (|) e Redirecionamento (>, >>, 2>&1)", "foco": "Encadeando a saída de um comando direto na entrada do outro"},
    {"id": 266, "escola": "07_devops_linux_e_nuvem", "modulo": "Linux", "tema": "Filtros de Texto: grep, sed, awk e cut", "foco": "Minerando terabytes de dados no terminal com ferramentas clássicas"},
    {"id": 267, "escola": "07_devops_linux_e_nuvem", "modulo": "Linux", "tema": "Gerenciamento de Processos: ps, top, htop, kill e kill -9", "foco": "Identificando processos que travam a CPU e liberando memória"},
    {"id": 268, "escola": "07_devops_linux_e_nuvem", "modulo": "Linux", "tema": "Gerenciamento de Pacotes: apt, yum e dnf", "foco": "Instalando e atualizando softwares em distribuições Debian e RedHat"},
    {"id": 269, "escola": "07_devops_linux_e_nuvem", "modulo": "Linux", "tema": "SSH e Autenticação por Chaves Públicas e Privadas", "foco": "Acessando servidores remotos com segurança máxima sem usar senhas fracas"},
    {"id": 270, "escola": "07_devops_linux_e_nuvem", "modulo": "Linux", "tema": "Gerenciando Serviços com systemd e systemctl", "foco": "Iniciando, parando e habilitando servidores para ligar junto com o boot"},
    {"id": 271, "escola": "07_devops_linux_e_nuvem", "modulo": "Linux", "tema": "Agendamento com Crontab no Linux", "foco": "Sintaxe das 5 estrelas (* * * * *) para tarefas automáticas de manutenção"},
    {"id": 272, "escola": "07_devops_linux_e_nuvem", "modulo": "Linux", "tema": "Variáveis de Ambiente e Arquivos de Perfil (.bashrc, /etc/environment)", "foco": "Configurando o PATH e variáveis de sistema permanentes"},
    {"id": 273, "escola": "07_devops_linux_e_nuvem", "modulo": "Linux", "tema": "Shell Scripting: Variáveis, if/else e Laços no Bash", "foco": "Automatizando rotinas de backup e deploy com scripts .sh"},
    {"id": 274, "escola": "07_devops_linux_e_nuvem", "modulo": "Linux", "tema": "Compactação e Backup: tar, gzip, zip e rsync", "foco": "Sincronizando arquivos eficientemente pela rede com rsync"},

    # Carreira 2: Redes de Computadores para DevOps
    {"id": 275, "escola": "07_devops_linux_e_nuvem", "modulo": "Redes", "tema": "Modelo OSI vs Modelo TCP/IP", "foco": "As camadas de transporte, rede e aplicação explicadas de forma prática"},
    {"id": 276, "escola": "07_devops_linux_e_nuvem", "modulo": "Redes", "tema": "Endereçamento IP (IPv4 vs IPv6) e Máscaras de Sub-rede (CIDR)", "foco": "Entendendo /24, /16 e faixas de IP privadas (192.168, 10.0, 172.16)"},
    {"id": 277, "escola": "07_devops_linux_e_nuvem", "modulo": "Redes", "tema": "DNS (Domain Name System): A Lista Telefônica da Web", "foco": "Registros A, CNAME, MX, TXT e tempo de propagação TTL"},
    {"id": 278, "escola": "07_devops_linux_e_nuvem", "modulo": "Redes", "tema": "Portas de Rede e Protocolos Comuns (80, 443, 22, 5432, 3306)", "foco": "Os canais de comunicação onde cada serviço escuta conexões"},
    {"id": 279, "escola": "07_devops_linux_e_nuvem", "modulo": "Redes", "tema": "Diagnóstico de Rede: ping, traceroute, netstat, ss e curl", "foco": "Descobrindo exatamente onde um pacote de dados está travando"},
    {"id": 280, "escola": "07_devops_linux_e_nuvem", "modulo": "Redes", "tema": "Firewall no Linux: iptables, ufw e firewalld", "foco": "Bloqueando acessos externos e permitindo apenas portas necessárias"},
    {"id": 281, "escola": "07_devops_linux_e_nuvem", "modulo": "Redes", "tema": "Proxy Reverso e Balanceamento de Carga com Nginx", "foco": "Recebendo requisições e distribuindo entre servidores back-end"},
    {"id": 282, "escola": "07_devops_linux_e_nuvem", "modulo": "Redes", "tema": "Certificados SSL/TLS e Let's Encrypt com Certbot", "foco": "Habilitando HTTPS seguro com cadeado verde e renovação automática"},

    # Carreira 3: Containers com Docker & Docker Compose
    {"id": 283, "escola": "07_devops_linux_e_nuvem", "modulo": "Docker", "tema": "O que é um Container? (Container vs Máquina Virtual)", "foco": "Por que containers são leves compartilhando o kernel do sistema hospedeiro"},
    {"id": 284, "escola": "07_devops_linux_e_nuvem", "modulo": "Docker", "tema": "A Arquitetura Docker: Docker Daemon, CLI e Registries", "foco": "O cliente enviando comandos para o daemon que gerencia os containers"},
    {"id": 285, "escola": "07_devops_linux_e_nuvem", "modulo": "Docker", "tema": "Imagens Docker vs Containers em Execução", "foco": "A receita de bolo imutável vs o bolo pronto rodando na memória"},
    {"id": 286, "escola": "07_devops_linux_e_nuvem", "modulo": "Docker", "tema": "Comandos Básicos: docker run, ps, stop, start, rm e rmi", "foco": "O ciclo de vida completo de um container no dia a dia"},
    {"id": 287, "escola": "07_devops_linux_e_nuvem", "modulo": "Docker", "tema": "Criando seu Dockerfile: FROM, WORKDIR, COPY e RUN", "foco": "A receita passo a passo para empacotar sua aplicação com suas dependências"},
    {"id": 288, "escola": "07_devops_linux_e_nuvem", "modulo": "Docker", "tema": "CMD vs ENTRYPOINT no Dockerfile", "foco": "Definindo o comando padrão de execução e parâmetros customizáveis"},
    {"id": 289, "escola": "07_devops_linux_e_nuvem", "modulo": "Docker", "tema": "Port Mapping no Docker (-p 8080:80)", "foco": "Ligando a porta do seu computador à porta interna do container"},
    {"id": 290, "escola": "07_devops_linux_e_nuvem", "modulo": "Docker", "tema": "Persistência de Dados com Volumes Docker (-v)", "foco": "Garantindo que os dados do banco de dados não sumam ao reiniciar o container"},
    {"id": 291, "escola": "07_devops_linux_e_nuvem", "modulo": "Docker", "tema": "Redes no Docker (Bridge, Host, Overlay)", "foco": "Permitindo que a API converse com o banco pelo nome do container"},
    {"id": 292, "escola": "07_devops_linux_e_nuvem", "modulo": "Docker", "tema": "Multi-stage Builds: Criando Imagens Minúsculas", "foco": "Compilando código em um estágio e copiando só o binário para o container final"},
    {"id": 293, "escola": "07_devops_linux_e_nuvem", "modulo": "Docker", "tema": "O arquivo .dockerignore", "foco": "Evitando enviar node_modules ou arquivos temporários para dentro da imagem"},
    {"id": 294, "escola": "07_devops_linux_e_nuvem", "modulo": "Docker", "tema": "Docker Compose: Orquestrando Múltiplos Serviços", "foco": "Subindo API, Banco de Dados e Redis com um único comando docker compose up"},
    {"id": 295, "escola": "07_devops_linux_e_nuvem", "modulo": "Docker", "tema": "Variáveis de Ambiente no Docker Compose (env_file)", "foco": "Injetando credenciais de banco e chaves de forma padronizada"},
    {"id": 296, "escola": "07_devops_linux_e_nuvem", "modulo": "Docker", "tema": "Publicando Imagens no Docker Hub e GitHub Packages", "foco": "Compartilhando imagens prontas para servidores de produção baixarem"},

    # Carreira 4: Orquestração com Kubernetes (K8s)
    {"id": 297, "escola": "07_devops_linux_e_nuvem", "modulo": "Kubernetes", "tema": "Introdução ao Kubernetes: Por que Orquestração?", "foco": "Auto-cura, escalabilidade horizontal e balanceamento automático de carga"},
    {"id": 298, "escola": "07_devops_linux_e_nuvem", "modulo": "Kubernetes", "tema": "A Arquitetura do K8s: Control Plane e Worker Nodes", "foco": "O cérebro da orquestração e os nós trabalhadores que executam as cargas"},
    {"id": 299, "escola": "07_devops_linux_e_nuvem", "modulo": "Kubernetes", "tema": "Pods: A Menor Unidade de Execução do Kubernetes", "foco": "O casulo que abriga um ou mais containers compartilhando IP e volume"},
    {"id": 300, "escola": "07_devops_linux_e_nuvem", "modulo": "Kubernetes", "tema": "Deployments e ReplicaSets no K8s", "foco": "Garantindo que sempre existam N cópias da sua API ativas sem downtime"},
    {"id": 301, "escola": "07_devops_linux_e_nuvem", "modulo": "Kubernetes", "tema": "Services no K8s: ClusterIP, NodePort e LoadBalancer", "foco": "O endereço estável para conversar com pods que mudam de IP a todo momento"},
    {"id": 302, "escola": "07_devops_linux_e_nuvem", "modulo": "Kubernetes", "tema": "Ingress Controllers: Roteamento HTTP/HTTPS no Cluster", "foco": "O ponto de entrada único para direcionar api.empresa.com e app.empresa.com"},
    {"id": 303, "escola": "07_devops_linux_e_nuvem", "modulo": "Kubernetes", "tema": "ConfigMaps e Secrets: Configurações Desacopladas", "foco": "Injetando parâmetros e senhas criptografadas nos pods sem recriar imagens"},
    {"id": 304, "escola": "07_devops_linux_e_nuvem", "modulo": "Kubernetes", "tema": "Namespaces: Organizando Ambientes (Dev, Staging, Prod)", "foco": "Isolando times e projetos dentro do mesmo cluster físico"},
    {"id": 305, "escola": "07_devops_linux_e_nuvem", "modulo": "Kubernetes", "tema": "PersistentVolumes (PV) e Claims (PVC)", "foco": "Requisitando discos e storage permanente para pods do Kubernetes"},
    {"id": 306, "escola": "07_devops_linux_e_nuvem", "modulo": "Kubernetes", "tema": "HPA (Horizontal Pod Autoscaler)", "foco": "Multiplicando o número de pods automaticamente durante picos de acessos"},
    {"id": 307, "escola": "07_devops_linux_e_nuvem", "modulo": "Kubernetes", "tema": "Health Checks: Liveness e Readiness Probes", "foco": "Ensinando o K8s a saber se a aplicação travou para reiniciá-la na hora"},
    {"id": 308, "escola": "07_devops_linux_e_nuvem", "modulo": "Kubernetes", "tema": "Gerenciamento de Pacotes K8s com Helm", "foco": "Instalando pilhas inteiras (Prometheus, Postgres) com comandos helm install"},

    # Carreira 5: Computação em Nuvem (Cloud AWS)
    {"id": 309, "escola": "07_devops_linux_e_nuvem", "modulo": "Cloud", "tema": "O que é Computação em Nuvem? (IaaS, PaaS, SaaS)", "foco": "Alugando servidores e serviços sob demanda em datacenters globais"},
    {"id": 310, "escola": "07_devops_linux_e_nuvem", "modulo": "Cloud", "tema": "Regiões, Zonas de Disponibilidade (AZ) e Alta Disponibilidade", "foco": "Espalhando servidores para o sistema nunca cair se um prédio falhar"},
    {"id": 311, "escola": "07_devops_linux_e_nuvem", "modulo": "Cloud", "tema": "AWS IAM: Usuários, Grupos, Roles e Princípio do Menor Privilégio", "foco": "A segurança e controle de acesso a todos os recursos da nuvem"},
    {"id": 312, "escola": "07_devops_linux_e_nuvem", "modulo": "Cloud", "tema": "AWS EC2: Máquinas Virtuais Elásticas na Nuvem", "foco": "Escolhendo poder computacional, memória e sistemas operacionais"},
    {"id": 313, "escola": "07_devops_linux_e_nuvem", "modulo": "Cloud", "tema": "AWS S3: Armazenamento de Objetos Ilimitado", "foco": "Guardando fotos, vídeos e backups com 99.999999999% de durabilidade"},
    {"id": 314, "escola": "07_devops_linux_e_nuvem", "modulo": "Cloud", "tema": "AWS VPC: Sua Rede Privada Virtual na Nuvem", "foco": "Criando sub-redes públicas e privadas com tabelas de roteamento e NAT Gateway"},
    {"id": 315, "escola": "07_devops_linux_e_nuvem", "modulo": "Cloud", "tema": "AWS Security Groups e Network ACLs", "foco": "Os firewalls virtuais que controlam quem entra e sai das suas instâncias"},
    {"id": 316, "escola": "07_devops_linux_e_nuvem", "modulo": "Cloud", "tema": "AWS RDS: Banco de Dados Relacional Gerenciado", "foco": "Postgres e MySQL com backups automáticos, replicação e sem cuidar de SO"},
    {"id": 317, "escola": "07_devops_linux_e_nuvem", "modulo": "Cloud", "tema": "AWS Lambda e Serverless: Computação sem Servidor", "foco": "Executando código apenas quando acionado, pagando apenas por milissegundo"},
    {"id": 318, "escola": "07_devops_linux_e_nuvem", "modulo": "Cloud", "tema": "AWS CloudFront: CDN Global para Velocidade Máxima", "foco": "Entregando arquivos estáticos no servidor mais próximo do usuário no planeta"},
    {"id": 319, "escola": "07_devops_linux_e_nuvem", "modulo": "Cloud", "tema": "AWS Route 53: DNS Altamente Disponível", "foco": "Gerenciamento de domínios, health checks e roteamento geográfico"},
    {"id": 320, "escola": "07_devops_linux_e_nuvem", "modulo": "Cloud", "tema": "AWS CloudWatch: Métricas, Logs e Alarmes", "foco": "Monitorando uso de CPU e recebendo alertas no celular quando algo falhar"},

    # Carreira 6: Infraestrutura como Código (IaC) com Terraform
    {"id": 321, "escola": "07_devops_linux_e_nuvem", "modulo": "IaC", "tema": "O que é Infraestrutura como Código (IaC)?", "foco": "Criando servidores e redes através de código versionado no Git sem cliques manuais"},
    {"id": 322, "escola": "07_devops_linux_e_nuvem", "modulo": "IaC", "tema": "Fundamentos do Terraform: Providers, Resources e HCL", "foco": "A linguagem declarativa para descrever a infraestrutura desejada"},
    {"id": 323, "escola": "07_devops_linux_e_nuvem", "modulo": "IaC", "tema": "O Ciclo Terraform: init, plan, apply e destroy", "foco": "Verificando o que vai mudar antes de aplicar as alterações na nuvem"},
    {"id": 324, "escola": "07_devops_linux_e_nuvem", "modulo": "IaC", "tema": "O Arquivo de Estado (terraform.tfstate)", "foco": "A memória do Terraform que mapeia o código com a nuvem real"},
    {"id": 325, "escola": "07_devops_linux_e_nuvem", "modulo": "IaC", "tema": "State Remoto no S3 com Lock no DynamoDB", "foco": "Evitando que dois engenheiros apliquem mudanças concorrentes e quebrem o ambiente"},
    {"id": 326, "escola": "07_devops_linux_e_nuvem", "modulo": "IaC", "tema": "Módulos no Terraform: Reutilizando Código de Infra", "foco": "Empacotando arquiteturas inteiras de rede e banco para reutilizar em projetos"},

    # Carreira 7: CI/CD & Automação de Deploy
    {"id": 327, "escola": "07_devops_linux_e_nuvem", "modulo": "CI/CD", "tema": "O que é Integração Contínua (CI) e Entrega Contínua (CD)?", "foco": "Testando e publicando código automaticamente a cada git push"},
    {"id": 328, "escola": "07_devops_linux_e_nuvem", "modulo": "CI/CD", "tema": "GitHub Actions: Workflows, Jobs e Steps em YAML", "foco": "A estrutura de automação nativa do GitHub para desenvolvedores"},
    {"id": 329, "escola": "07_devops_linux_e_nuvem", "modulo": "CI/CD", "tema": "Gatilhos de Eventos no GitHub Actions (push, pull_request, schedule)", "foco": "Disparando pipelines quando alguém abre um Pull Request"},
    {"id": 330, "escola": "07_devops_linux_e_nuvem", "modulo": "CI/CD", "tema": "Segredos e Variáveis no GitHub Actions (Secrets)", "foco": "Protegendo chaves de deploy e tokens da nuvem com segurança"},
    {"id": 331, "escola": "07_devops_linux_e_nuvem", "modulo": "CI/CD", "tema": "Pipeline de Build e Testes Automatizados", "foco": "Bloqueando merges se os testes unitários falharem"},
    {"id": 332, "escola": "07_devops_linux_e_nuvem", "modulo": "CI/CD", "tema": "Pipeline de Build e Push de Imagem Docker", "foco": "Gerando imagens com tags semânticas e enviando ao Docker Hub automaticamente"},
    {"id": 333, "escola": "07_devops_linux_e_nuvem", "modulo": "CI/CD", "tema": "Estratégias de Deploy: Blue/Green vs Canary", "foco": "Atualizando produção sem derrubar usuários ativos com zero downtime"},
    {"id": 334, "escola": "07_devops_linux_e_nuvem", "modulo": "CI/CD", "tema": "GitOps com ArgoCD no Kubernetes", "foco": "Sincronizando o estado do cluster K8s diretamente com um repositório Git"},

    # Carreira 8: Observabilidade & Monitoramento
    {"id": 335, "escola": "07_devops_linux_e_nuvem", "modulo": "Observabilidade", "tema": "Os 3 Pilares da Observabilidade: Logs, Métricas e Traces", "foco": "Diferença crucial entre saber que falhou e saber onde e por que falhou"},
    {"id": 336, "escola": "07_devops_linux_e_nuvem", "modulo": "Observabilidade", "tema": "Coleta de Métricas com Prometheus", "foco": "Armazenamento de séries temporais e consultas em PromQL"},
    {"id": 337, "escola": "07_devops_linux_e_nuvem", "modulo": "Observabilidade", "tema": "Dashboards Incríveis com Grafana", "foco": "Montando telas visuais com gráficos de tráfego, erros e latência para o time"},
    {"id": 338, "escola": "07_devops_linux_e_nuvem", "modulo": "Observabilidade", "tema": "Centralização de Logs com Grafana Loki ou Elastic (ELK)", "foco": "Buscando em tempo real logs de 50 servidores em uma única barra de pesquisa"},
    {"id": 339, "escola": "07_devops_linux_e_nuvem", "modulo": "Observabilidade", "tema": "Rastreamento Distribuído com OpenTelemetry e Jaeger", "foco": "Acompanhando uma requisição passando por 5 microsserviços diferentes"},
    {"id": 340, "escola": "07_devops_linux_e_nuvem", "modulo": "Observabilidade", "tema": "Cultura SRE (Site Reliability Engineering): SLAs, SLOs e SLIs", "foco": "Definindo metas de confiabilidade e orçamentos de erro toleráveis"}
]

# =============================================================================
# ESCOLA 08: CIBERSEGURANÇA & ETHICAL HACKING (IDs 341 ao 410 - 70 Mapas)
# =============================================================================
MAPAS_CIBERSEGURANCA: List[Dict] = [
    # Carreira 1: Fundamentos de Cibersegurança & Criptografia
    {"id": 341, "escola": "08_ciberseguranca", "modulo": "Fundamentos", "tema": "A Tríade da Segurança: Confidencialidade, Integridade e Disponibilidade (CIA)", "foco": "Os 3 mandamentos essenciais da segurança da informação"},
    {"id": 342, "escola": "08_ciberseguranca", "modulo": "Fundamentos", "tema": "Ameaça, Vulnerabilidade, Exploit e Risco", "foco": "A diferença vital entre a brecha, a arma, o invasor e o impacto real"},
    {"id": 343, "escola": "08_ciberseguranca", "modulo": "Fundamentos", "tema": "Tipos de Hackers: White Hat, Black Hat e Gray Hat", "foco": "A ética do profissional de segurança vs a atividade cibercriminosa"},
    {"id": 344, "escola": "08_ciberseguranca", "modulo": "Criptografia", "tema": "Criptografia Simétrica (AES e ChaCha20)", "foco": "A mesma chave secreta tranca e destranca o cofre de dados"},
    {"id": 345, "escola": "08_ciberseguranca", "modulo": "Criptografia", "tema": "Criptografia Assimétrica (RSA e Curvas Elípticas ECC)", "foco": "A chave pública que qualquer um pode ver vs a chave privada que nunca sai da máquina"},
    {"id": 346, "escola": "08_ciberseguranca", "modulo": "Criptografia", "tema": "Funções de Hash Criptográfico (SHA-256, SHA-3)", "foco": "A impressão digital de mão única que comprova a integridade de arquivos"},
    {"id": 347, "escola": "08_ciberseguranca", "modulo": "Criptografia", "tema": "Armazenamento Seguro de Senhas: Sal (Salt), Pepper e BCrypt / Argon2", "foco": "Por que nunca salvar senhas em MD5 ou texto plano e como frustrar Rainbow Tables"},
    {"id": 348, "escola": "08_ciberseguranca", "modulo": "Criptografia", "tema": "Assinaturas Digitais e Infraestrutura de Chaves Públicas (PKI)", "foco": "Como provar com certeza matemática quem foi o autor de um documento ou código"},

    # Carreira 2: OWASP Top 10 & Segurança Web
    {"id": 349, "escola": "08_ciberseguranca", "modulo": "OWASP", "tema": "OWASP Top 10: O Padrão Ouro de Riscos em Aplicações Web", "foco": "O guia das dez vulnerabilidades mais críticas da internet"},
    {"id": 350, "escola": "08_ciberseguranca", "modulo": "OWASP", "tema": "SQL Injection (SQLi): Anatomia e Defesa com Prepared Statements", "foco": "Injeção de comandos SQL via campos de texto e como parametrizar consultas"},
    {"id": 351, "escola": "08_ciberseguranca", "modulo": "OWASP", "tema": "Cross-Site Scripting (XSS): Reflected, Stored e DOM", "foco": "Injeção de scripts maliciosos no navegador de terceiros e roubo de cookies"},
    {"id": 352, "escola": "08_ciberseguranca", "modulo": "OWASP", "tema": "Cross-Site Request Forgery (CSRF) e Tokens Anti-CSRF", "foco": "Forçando um usuário logado a executar transferências sem consentimento"},
    {"id": 353, "escola": "08_ciberseguranca", "modulo": "OWASP", "tema": "Quebra de Controle de Acesso (Broken Access Control & IDOR)", "foco": "Acessando dados de outro usuário apenas alterando o ID na barra de URL"},
    {"id": 354, "escola": "08_ciberseguranca", "modulo": "OWASP", "tema": "Falhas Criptográficas e Exposição de Dados Sensíveis", "foco": "Tráfego sem HTTPS, chaves hardcoded no código e algoritmos defasados"},
    {"id": 355, "escola": "08_ciberseguranca", "modulo": "OWASP", "tema": "Falhas de Identificação e Autenticação (Brute Force & Credential Stuffing)", "foco": "Ataques de dicionário e como implementar rate limiting e bloqueio progressivo"},
    {"id": 356, "escola": "08_ciberseguranca", "modulo": "OWASP", "tema": "Autenticação Multifator (MFA / 2FA) com TOTP", "foco": "Como funcionam os códigos temporários do Google Authenticator"},
    {"id": 357, "escola": "08_ciberseguranca", "modulo": "OWASP", "tema": "Insecure Deserialization: Execução Remota via Objetos", "foco": "Os perigos de desserializar dados de fontes não confiáveis em Python e Java"},
    {"id": 358, "escola": "08_ciberseguranca", "modulo": "OWASP", "tema": "SSRF (Server-Side Request Forgery)", "foco": "Manipulando o servidor web para atacar a rede interna e metadados da nuvem"},
    {"id": 359, "escola": "08_ciberseguranca", "modulo": "OWASP", "tema": "Componentes Vulneráveis e Desatualizados (SCA e CVEs)", "foco": "Monitorando dependências infectadas em bibliotecas open-source"},
    {"id": 360, "escola": "08_ciberseguranca", "modulo": "OWASP", "tema": "Headers de Segurança HTTP: CSP, HSTS, X-Frame-Options", "foco": "Configurando cabeçalhos no servidor para blindar navegadores contra ataques"},

    # Carreira 3: Metodologia de Pentest & Red Team
    {"id": 361, "escola": "08_ciberseguranca", "modulo": "Red Team", "tema": "Fases de um Pentest Profissional: PTES e Reconhecimento", "foco": "Do contrato de escopo ao relatório executivo final"},
    {"id": 362, "escola": "08_ciberseguranca", "modulo": "Red Team", "tema": "OSINT (Open Source Intelligence): Coleta de Informações Públicas", "foco": "Mapeando funcionários, e-mails vazados e tecnologias usando fontes abertas"},
    {"id": 363, "escola": "08_ciberseguranca", "modulo": "Red Team", "tema": "Varredura de Redes com Nmap: Port Scanning e Detecção de SO", "foco": "Identificando portas abertas, versões de serviços e scripts NSE"},
    {"id": 364, "escola": "08_ciberseguranca", "modulo": "Red Team", "tema": "Análise de Tráfego de Rede com Wireshark e tcpdump", "foco": "Capturando e dissecando pacotes de rede para investigar comunicações"},
    {"id": 365, "escola": "08_ciberseguranca", "modulo": "Red Team", "tema": "Intercepção de Requisições com Burp Suite", "foco": "O proxy interceptador que permite alterar requisições antes de chegarem ao servidor"},
    {"id": 366, "escola": "08_ciberseguranca", "modulo": "Red Team", "tema": "Fuzzing de Diretórios com Gobuster e ffuf", "foco": "Descobrindo páginas secretas, painéis administrativos e arquivos de backup esquecidos"},
    {"id": 367, "escola": "08_ciberseguranca", "modulo": "Red Team", "tema": "Introdução ao Metasploit Framework", "foco": "Exploits, payloads, listeners e sessões de Meterpreter"},
    {"id": 368, "escola": "08_ciberseguranca", "modulo": "Red Team", "tema": "Engenharia Social e Phishing Simulado", "foco": "O elo mais fraco da segurança: explorando a psicologia humana"},
    {"id": 369, "escola": "08_ciberseguranca", "modulo": "Red Team", "tema": "Movimentação Lateral e Escalação de Privilégios no Linux e Windows", "foco": "Como um invasor pula de um usuário comum para root ou Administrator"},
    {"id": 370, "escola": "08_ciberseguranca", "modulo": "Red Team", "tema": "Ataques de Negação de Serviço (DoS vs DDoS)", "foco": "Inundação volumétrica (SYN Flood, UDP Flood) e ataques em camada de aplicação"},

    # Carreira 4: Defesa, Monitoramento Blue Team & SOC
    {"id": 371, "escola": "08_ciberseguranca", "modulo": "Blue Team", "tema": "O que faz um SOC (Security Operations Center)?", "foco": "A torre de controle que vigia ameaças digitais 24 horas por dia"},
    {"id": 372, "escola": "08_ciberseguranca", "modulo": "Blue Team", "tema": "SIEM: Centralizando Eventos de Segurança com Splunk / Elastic", "foco": "Correlacionando alertas de firewalls, servidores e bancos para detectar invasões"},
    {"id": 373, "escola": "08_ciberseguranca", "modulo": "Blue Team", "tema": "EDR (Endpoint Detection and Response) vs Antivírus Tradicional", "foco": "Monitoramento comportamental de processos em computadores contra malware inédito"},
    {"id": 374, "escola": "08_ciberseguranca", "modulo": "Blue Team", "tema": "IDS e IPS (Snort, Suricata): Detecção e Prevenção de Intrusão", "foco": "O radar que avisa ou derruba conexões suspeitas na rede"},
    {"id": 375, "escola": "08_ciberseguranca", "modulo": "Blue Team", "tema": "WAF (Web Application Firewall): Cloudflare e AWS WAF", "foco": "A barreira inteligente que bloqueia SQLi, XSS e bots antes de tocar sua API"},
    {"id": 376, "escola": "08_ciberseguranca", "modulo": "Blue Team", "tema": "Honeypots: Armadilhas para Atrair e Estudar Invasores", "foco": "Servidores fictícios criados exclusivamente para coletar inteligência sobre cibercriminosos"},
    {"id": 377, "escola": "08_ciberseguranca", "modulo": "Blue Team", "tema": "Resposta a Incidentes (IR): As 6 Fases do NIST", "foco": "Preparação, Identificação, Contenção, Erradicação, Recuperação e Lições Aprendidas"},
    {"id": 378, "escola": "08_ciberseguranca", "modulo": "Blue Team", "tema": "Forense Digital e Cadeia de Custódia", "foco": "Preservando evidências digitais para terem validade jurídica em tribunais"},
    {"id": 379, "escola": "08_ciberseguranca", "modulo": "Blue Team", "tema": "Threat Intelligence e Framework MITRE ATT&CK", "foco": "O catálogo global que mapeia táticas, técnicas e procedimentos (TTPs) de hackers"},
    {"id": 380, "escola": "08_ciberseguranca", "modulo": "Blue Team", "tema": "Hardening de Servidores Linux e Windows", "foco": "Desativando serviços desnecessários e fechando portas para reduzir a superfície de ataque"},

    # Carreira 5: Privacidade, LGPD & DevSecOps
    {"id": 381, "escola": "08_ciberseguranca", "modulo": "DevSecOps", "tema": "O que é DevSecOps? (Shift Left Security)", "foco": "Integrando testes de segurança no pipeline de código desde o primeiro commit"},
    {"id": 382, "escola": "08_ciberseguranca", "modulo": "DevSecOps", "tema": "Análise Estática de Código (SAST) com SonarQube", "foco": "Encontrando falhas de segurança no código-fonte sem precisar executá-lo"},
    {"id": 383, "escola": "08_ciberseguranca", "modulo": "DevSecOps", "tema": "Análise Dinâmica de Segurança (DAST) com OWASP ZAP", "foco": "Atacando a aplicação em tempo de execução para encontrar vulnerabilidades ativas"},
    {"id": 384, "escola": "08_ciberseguranca", "modulo": "DevSecOps", "tema": "Secret Scanning: Evitando Vazamentos de Chaves no GitHub", "foco": "Ferramentas automáticas que impedem commit acidental de senhas e tokens"},
    {"id": 385, "escola": "08_ciberseguranca", "modulo": "Governança", "tema": "LGPD (Lei Geral de Proteção de Dados): Princípios e Direitos", "foco": "Consentimento, finalidade, descarte de dados e multas da ANPD"},
    {"id": 386, "escola": "08_ciberseguranca", "modulo": "Governança", "tema": "Privacy by Design e Privacy by Default", "foco": "Pensando na proteção de dados do usuário desde o desenho da arquitetura do software"},
    {"id": 387, "escola": "08_ciberseguranca", "modulo": "Governança", "tema": "Arquitetura Zero Trust: 'Nunca Confie, Sempre Verifique'", "foco": "Eliminando o conceito de rede interna segura e validando cada requisição"},
    {"id": 388, "escola": "08_ciberseguranca", "modulo": "Governança", "tema": "Segurança em Nuvem: Modelo de Responsabilidade Compartilhada", "foco": "O que é dever do provedor de nuvem (AWS/Azure) vs o que é dever da sua empresa"},
    {"id": 389, "escola": "08_ciberseguranca", "modulo": "Governança", "tema": "Gestão de Identidade e Acesso (IAM): RBAC vs ABAC", "foco": "Controle de permissões baseado em papéis ou em atributos contextuais"},
    {"id": 390, "escola": "08_ciberseguranca", "modulo": "Governança", "tema": "Plano de Continuidade de Negócios e Disaster Recovery (RPO e RTO)", "foco": "Quanto tempo sua empresa aguenta ficar fora do ar e quanto dado pode perder"},

    # Carreira 6: Ameaças Modernas & Ciberarmas
    {"id": 391, "escola": "08_ciberseguranca", "modulo": "Ameaças", "tema": "Ransomware: Anatomia, Disseminação e Como Prevenir", "foco": "O sequestro de dados criptografados e como backups imutáveis salvam empresas"},
    {"id": 392, "escola": "08_ciberseguranca", "modulo": "Ameaças", "tema": "Botnets e Dispositivos IoT Comprometidos", "foco": "Câmeras e roteadores zumbis usados para disparar ataques massivos"},
    {"id": 393, "escola": "08_ciberseguranca", "modulo": "Ameaças", "tema": "Ataques Man-in-the-Middle (MitM) e ARP Spoofing", "foco": "O invasor que se coloca no meio da conversa para escutar e modificar tráfego"},
    {"id": 394, "escola": "08_ciberseguranca", "modulo": "Ameaças", "tema": "Ataques de Supply Chain (Cadeia de Suprimentos)", "foco": "Infectando uma biblioteca open source popular para atingir milhares de empresas"},
    {"id": 395, "escola": "08_ciberseguranca", "modulo": "Ameaças", "tema": "Zero-Day Exploits e o Mercado de Vulnerabilidades", "foco": "Falhas que nem o próprio fabricante do software descobriu ainda"},
    {"id": 396, "escola": "08_ciberseguranca", "modulo": "Ameaças", "tema": "Engenharia Reversa de Binários com Ghidra", "foco": "Desmontando programas compilados para entender o que eles fazem internamente"},
    {"id": 397, "escola": "08_ciberseguranca", "modulo": "Ameaças", "tema": "Segurança em APIs: OWASP API Security Top 10", "foco": "Mass Assignment, Broken Object Level Authorization e excesso de dados expostos"},
    {"id": 398, "escola": "08_ciberseguranca", "modulo": "Ameaças", "tema": "Segurança de Redes Sem Fio (Wi-Fi): WPA2 vs WPA3", "foco": "Ataques de handshake, evil twin e desautenticação de clientes"},
    {"id": 399, "escola": "08_ciberseguranca", "modulo": "Ameaças", "tema": "Deepfakes, IA Maliciosa e Clonagem de Voz", "foco": "O novo patamar da engenharia social com inteligência artificial generativa"},
    {"id": 400, "escola": "08_ciberseguranca", "modulo": "Ameaças", "tema": "Bug Bounty: Como Faturar Reportando Falhas Legalmente", "foco": "Trabalhando em plataformas como HackerOne e Bugcrowd de forma ética e lucrativa"},

    # Carreira 7: Especialização Prática & Laboratório
    {"id": 401, "escola": "08_ciberseguranca", "modulo": "Laboratório", "tema": "Montando seu Lab de Estudos com Kali Linux e Metasploitable", "foco": "Ambiente seguro isolado em máquina virtual sem perigo de quebrar seu PC"},
    {"id": 402, "escola": "08_ciberseguranca", "modulo": "Laboratório", "tema": "Plataformas de Treinamento: Hack The Box e TryHackMe", "foco": "Gamificação de invasão de máquinas para acelerar a curva de aprendizado"},
    {"id": 403, "escola": "08_ciberseguranca", "modulo": "Laboratório", "tema": "Certificações de Cibersegurança: CompTIA Security+, CEH e OSCP", "foco": "O roadmap de validação profissional para entrar no mercado global"},
    {"id": 404, "escola": "08_ciberseguranca", "modulo": "Laboratório", "tema": "Segurança em Contêineres: Trivy e Docker Bench Security", "foco": "Escaneando imagens em busca de pacotes vulneráveis antes de ir para produção"},
    {"id": 405, "escola": "08_ciberseguranca", "modulo": "Laboratório", "tema": "Segurança em Kubernetes: Pod Security Standards e RBAC", "foco": "Impedindo que containers rodem como root e acessem o nó do host"},
    {"id": 406, "escola": "08_ciberseguranca", "modulo": "Laboratório", "tema": "Segurança em Servidores Windows: Active Directory e Kerberos", "foco": "Como funciona o login corporativo e como defender a floresta de domínios"},
    {"id": 407, "escola": "08_ciberseguranca", "modulo": "Laboratório", "tema": "Ataques Pass-the-Hash e Golden Ticket no Active Directory", "foco": "Como invasores usam hashes de senha em memória para dominar a rede"},
    {"id": 408, "escola": "08_ciberseguranca", "modulo": "Laboratório", "tema": "Automação de Tarefas de Segurança com Python (Scapy e Requests)", "foco": "Criando seus próprios scripts de teste e verificação de rede"},
    {"id": 409, "escola": "08_ciberseguranca", "modulo": "Laboratório", "tema": "Relatório de Pentest Profissional: Apresentando para a Diretoria", "foco": "Traduzindo termos técnicos em impacto financeiro e risco de reputação"},
    {"id": 410, "escola": "08_ciberseguranca", "modulo": "Laboratório", "tema": "O Futuro da Cibersegurança: Criptografia Pós-Quântica (PQC)", "foco": "Como os computadores quânticos ameaçam o RSA e quais os novos algoritmos"}
]

# =============================================================================
# ESCOLA 01: CIÊNCIA DA COMPUTAÇÃO UNINTER AVANÇADO (IDs 411 ao 460 - 50 Mapas)
# =============================================================================
MAPAS_UNINTER_AVANCADO: List[Dict] = [
    # Carreira 1: Arquitetura de Computadores & Hardware
    {"id": 411, "escola": "01_ciencia_computacao_uninter", "modulo": "Hardware", "tema": "A Arquitetura de Von Neumann: CPU, Memória e Barramentos", "foco": "O modelo que rege quase todos os computadores modernos desde 1945"},
    {"id": 412, "escola": "01_ciencia_computacao_uninter", "modulo": "Hardware", "tema": "A ULA (Unidade Lógica e Aritmética) e Registradores", "foco": "O coração que faz contas de somar e os bolsos ultrarrápidos dentro da CPU"},
    {"id": 413, "escola": "01_ciencia_computacao_uninter", "modulo": "Hardware", "tema": "O Ciclo de Busca, Decodificação e Execução (Fetch-Decode-Execute)", "foco": "A dança contínua que o processador repete bilhões de vezes por segundo"},
    {"id": 414, "escola": "01_ciencia_computacao_uninter", "modulo": "Hardware", "tema": "Hierarquia de Memória: Registradores, Cache L1/L2/L3, RAM e SSD", "foco": "O trade-off clássico entre velocidade extrema e capacidade de armazenamento"},
    {"id": 415, "escola": "01_ciencia_computacao_uninter", "modulo": "Hardware", "tema": "Pipelining na CPU: Linha de Montagem de Instruções", "foco": "Processando várias instruções simultaneamente em estágios diferentes sem esperar uma acabar"},
    {"id": 416, "escola": "01_ciencia_computacao_uninter", "modulo": "Hardware", "tema": "Arquiteturas RISC vs CISC (ARM vs x86-64)", "foco": "Instruções simples e eficientes para celulares vs instruções complexas de computadores"},
    {"id": 417, "escola": "01_ciencia_computacao_uninter", "modulo": "Hardware", "tema": "Álgebra Booleana e Portas Lógicas (AND, OR, NOT, XOR, NAND)", "foco": "A matemática dos transistores que transforma eletricidade em decisões lógicas"},
    {"id": 418, "escola": "01_ciencia_computacao_uninter", "modulo": "Hardware", "tema": "Circuitos Combinacionais: Somadores, Multiplexadores e Decodificadores", "foco": "Construindo blocos de cálculo unindo portas lógicas"},
    {"id": 419, "escola": "01_ciencia_computacao_uninter", "modulo": "Hardware", "tema": "Circuitos Sequenciais: Flip-Flops e Clocks", "foco": "Como o computador consegue 'lembrar' de um estado e sincronizar batimentos"},
    {"id": 420, "escola": "01_ciencia_computacao_uninter", "modulo": "Hardware", "tema": "Ponto Flutuante e o Padrão IEEE 754 (Por que 0.1 + 0.2 != 0.3)", "foco": "Como números reais são codificados em bits de sinal, expoente e mantissa"},

    # Carreira 2: Sistemas Operacionais & Concorrência
    {"id": 421, "escola": "01_ciencia_computacao_uninter", "modulo": "SO", "tema": "O Núcleo do Sistema Operacional (Kernel): Espaço de Usuário vs Kernel", "foco": "O árbitro que protege o hardware contra programas maliciosos ou defeituosos"},
    {"id": 422, "escola": "01_ciencia_computacao_uninter", "modulo": "SO", "tema": "Chamadas de Sistema (System Calls): A Ponte para o Kernel", "foco": "Como programas comuns pedem permissão para ler disco ou acessar a rede"},
    {"id": 423, "escola": "01_ciencia_computacao_uninter", "modulo": "SO", "tema": "Processos vs Threads: Isolamento de Memória vs Compartilhamento", "foco": "A diferença vital entre clonar um aplicativo inteiro e criar linhas de execução leves"},
    {"id": 424, "escola": "01_ciencia_computacao_uninter", "modulo": "SO", "tema": "Ciclo de Vida de um Processo (Novo, Pronto, Executando, Bloqueado, Terminado)", "foco": "Os estados em que um programa transita na fila do escalonador"},
    {"id": 425, "escola": "01_ciencia_computacao_uninter", "modulo": "SO", "tema": "Algoritmos de Escalonamento de CPU: FCFS, SJF e Round Robin", "foco": "Como o sistema decide quem ganha a CPU a seguir para evitar que tarefas morram de fome"},
    {"id": 426, "escola": "01_ciencia_computacao_uninter", "modulo": "SO", "tema": "Condições de Corrida (Race Conditions) e Regiões Críticas", "foco": "Quando dois threads tentam alterar a mesma variável ao mesmo tempo e geram caos"},
    {"id": 427, "escola": "01_ciencia_computacao_uninter", "modulo": "SO", "tema": "Mecanismos de Sincronização: Mutex, Semáforos e Locks", "foco": "A chave do banheiro público: só quem tem a chave pode entrar na seção crítica"},
    {"id": 428, "escola": "01_ciencia_computacao_uninter", "modulo": "SO", "tema": "O Problema do Deadlock (As 4 Condições de Coffman)", "foco": "O abraço mortal quando dois processos travam esperando um pelo recurso do outro"},
    {"id": 429, "escola": "01_ciencia_computacao_uninter", "modulo": "SO", "tema": "Memória Virtual e Paginação (Paging): O Espaço de Endereçamento", "foco": "A ilusão mágica que faz cada programa achar que tem a RAM inteira só para si"},
    {"id": 430, "escola": "01_ciencia_computacao_uninter", "modulo": "SO", "tema": "Page Fault e Algoritmos de Substituição de Página (LRU, FIFO)", "foco": "O que acontece quando o dado solicitado não está na RAM e precisa vir do disco"},
    {"id": 431, "escola": "01_ciencia_computacao_uninter", "modulo": "SO", "tema": "Comunicação Interprocessos (IPC): Pipes, Sockets e Memória Compartilhada", "foco": "Como processos independentes trocam mensagens de forma coordenada"},
    {"id": 432, "escola": "01_ciencia_computacao_uninter", "modulo": "SO", "tema": "Sistemas de Arquivos (Inodes, Journaling, NTFS, ext4)", "foco": "Como o disco organiza pastas, metadados e se recupera de quedas de energia"},

    # Carreira 3: Teoria da Computação, Autômatos & Compiladores
    {"id": 433, "escola": "01_ciencia_computacao_uninter", "modulo": "Teoria", "tema": "A Máquina de Turing: O Modelo Matemático da Computabilidade", "foco": "A fita infinita com leitor que define os limites do que qualquer computador pode calcular"},
    {"id": 434, "escola": "01_ciencia_computacao_uninter", "modulo": "Teoria", "tema": "O Problema da Parada (Halting Problem) e Indecidibilidade", "foco": "A prova matemática genial de que é impossível criar um programa que detecte todos os loops infinitos"},
    {"id": 435, "escola": "01_ciencia_computacao_uninter", "modulo": "Teoria", "tema": "A Hierarquia de Chomsky de Linguagens e Gramáticas", "foco": "Linguagens regulares, livres de contexto, sensíveis ao contexto e irrestritas"},
    {"id": 436, "escola": "01_ciencia_computacao_uninter", "modulo": "Teoria", "tema": "Autômatos Finitos Determinísticos (DFA) e Não-Determinísticos (NFA)", "foco": "Máquinas de estados finitos que reconhecem padrões e validam senhas e e-mails"},
    {"id": 437, "escola": "01_ciencia_computacao_uninter", "modulo": "Teoria", "tema": "Autômatos de Pilha e Linguagens Livres de Contexto", "foco": "Como validar abertura e fechamento de parênteses, chaves e tags HTML"},
    {"id": 438, "escola": "01_ciencia_computacao_uninter", "modulo": "Teoria", "tema": "Classes de Complexidade: P vs NP e o Problema do Milhão de Dólares", "foco": "Problemas fáceis de resolver vs problemas fáceis de verificar a resposta"},
    {"id": 439, "escola": "01_ciencia_computacao_uninter", "modulo": "Teoria", "tema": "NP-Completo e o Problema do Caixeiro Viajante (Traveling Salesperson)", "foco": "Por que achar a melhor rota para 50 cidades exigiria bilhões de anos"},
    {"id": 440, "escola": "01_ciencia_computacao_uninter", "modulo": "Compiladores", "tema": "Fases de um Compilador: Do Código Fonte ao Código de Máquina", "foco": "Léxico, Sintático, Semântico, Otimização e Geração de Código"},
    {"id": 441, "escola": "01_ciencia_computacao_uninter", "modulo": "Compiladores", "tema": "Análise Léxica (Lexing / Scanning) e Tokens", "foco": "Quebrando o texto do código em palavras-chave, identificadores e pontuações"},
    {"id": 442, "escola": "01_ciencia_computacao_uninter", "modulo": "Compiladores", "tema": "Árvore Sintática Abstrata (AST - Abstract Syntax Tree)", "foco": "A representação em árvore que dá sentido hierárquico às instruções"},
    {"id": 443, "escola": "01_ciencia_computacao_uninter", "modulo": "Compiladores", "tema": "Análise Semântica e Verificação de Tipos", "foco": "Garantindo que você não some um texto com uma data em linguagens estáticas"},
    {"id": 444, "escola": "01_ciencia_computacao_uninter", "modulo": "Compiladores", "tema": "Compilação Just-In-Time (JIT) na V8 e na JVM", "foco": "Como o interpretador monitora loops quentes e os compila para binário nativo no ar"},
    {"id": 445, "escola": "01_ciencia_computacao_uninter", "modulo": "Compiladores", "tema": "Garbage Collection (GC): Coleta de Lixo Mark-and-Sweep e Geracional", "foco": "Como Java, Python e JavaScript limpam a memória sem vazamentos"},

    # Carreira 4: Algoritmos Avançados & Estruturas Discretas
    {"id": 446, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "Grafos: Representação por Matriz de Adjacência vs Lista de Adjacência", "foco": "Modelando redes sociais, mapas de metrô e conexões de rede"},
    {"id": 447, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "Busca em Largura (BFS) vs Busca em Profundidade (DFS)", "foco": "Explorando em camadas concêntricas vs mergulhando fundo até o beco sem saída"},
    {"id": 448, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "O Algoritmo de Dijkstra para Menor Caminho", "foco": "Como o Google Maps calcula a rota mais rápida entre duas esquinas"},
    {"id": 449, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "O Algoritmo A* (A-Star) e Heurísticas para Jogos", "foco": "Encontrando caminhos inteligentes em labirintos direcionando a busca ao alvo"},
    {"id": 450, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "Árvores Geradoras Mínimas (MST): Algoritmos de Kruskal e Prim", "foco": "Conectando cidades com cabos de fibra ótica com o menor custo financeiro total"},
    {"id": 451, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "Programação Dinâmica: Memoização vs Tabulação", "foco": "Guardando resultados de subproblemas para nunca calcular a mesma coisa duas vezes"},
    {"id": 452, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "O Problema da Mochila (Knapsack Problem) com Programação Dinâmica", "foco": "Maximizando o valor dos itens sem estourar o limite de peso"},
    {"id": 453, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "Algoritmos Gulosos (Greedy Algorithms)", "foco": "Tomando a melhor decisão local a cada passo na esperança de achar o ótimo global"},
    {"id": 454, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "Árvores AVL e Red-Black Trees (Árvores Auto-Balanceáveis)", "foco": "Garantindo busca O(log n) constante mesmo após milhares de inserções"},
    {"id": 455, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "Tries (Árvores de Prefixos) e Algoritmos de Autocomplete", "foco": "Buscando sugestões de palavras conforme o usuário digita cada letra"},
    {"id": 456, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "Bloom Filters: Estrutura Probabilística de Pertencimento", "foco": "Respondendo com certeza se um elemento NÃO está no conjunto gastando 1% de memória"},
    {"id": 457, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "Algoritmo de Huffman: Compactação de Dados sem Perdas", "foco": "Atribuindo códigos curtos para letras frequentes (a base do ZIP e MP3)"},
    {"id": 458, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "Detecção de Ciclos em Grafos e Ordenação Topológica", "foco": "Descobrindo dependências circulares em pacotes e compilando na ordem certa"},
    {"id": 459, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "Teorema de Bellman-Ford para Grafos com Pesos Negativos", "foco": "Detectando ciclos de arbitragem cambial em finanças"},
    {"id": 460, "escola": "01_ciencia_computacao_uninter", "modulo": "Algoritmos", "tema": "Algoritmos Quânticos Básicos: Shor e Grover Desmistificados", "foco": "Como o paralelismo quântico ameaça a fatoração RSA e acelera buscas"}
]

# =============================================================================
# ESCOLA 04: BACK-END & MICROSSERVIÇOS AVANÇADO (IDs 461 ao 520 - 60 Mapas)
# =============================================================================
MAPAS_BACKEND_AVANCADO: List[Dict] = [
    # Carreira 1: Princípios SOLID & Clean Architecture
    {"id": 461, "escola": "04_backend_e_apis", "modulo": "Arquitetura", "tema": "Single Responsibility Principle (SRP): Responsabilidade Única", "foco": "Uma classe deve ter apenas um motivo para mudar"},
    {"id": 462, "escola": "04_backend_e_apis", "modulo": "Arquitetura", "tema": "Open/Closed Principle (OCP): Aberto para Extensão, Fechado para Modificação", "foco": "Adicionando novas funcionalidades sem alterar código já testado em produção"},
    {"id": 463, "escola": "04_backend_e_apis", "modulo": "Arquitetura", "tema": "Liskov Substitution Principle (LSP): Substituição de Liskov", "foco": "Classes filhas devem poder substituir a classe mãe sem quebrar o programa"},
    {"id": 464, "escola": "04_backend_e_apis", "modulo": "Arquitetura", "tema": "Interface Segregation Principle (ISP): Segregação de Interfaces", "foco": "Muitas interfaces específicas são melhores que uma interface gorda genérica"},
    {"id": 465, "escola": "04_backend_e_apis", "modulo": "Arquitetura", "tema": "Dependency Inversion Principle (DIP): Inversão de Dependência", "foco": "Módulos de alto nível não devem depender de módulos de baixo nível, ambos dependem de abstrações"},
    {"id": 466, "escola": "04_backend_e_apis", "modulo": "Arquitetura", "tema": "Clean Architecture (Arquitetura Limpa) do Uncle Bob", "foco": "Entidades, Casos de Uso, Controladores e Frameworks na camada externa"},
    {"id": 467, "escola": "04_backend_e_apis", "modulo": "Arquitetura", "tema": "Arquitetura Hexagonal (Ports & Adapters)", "foco": "Conectando bancos de dados e interfaces externas através de portas plugáveis"},
    {"id": 468, "escola": "04_backend_e_apis", "modulo": "Arquitetura", "tema": "Domain-Driven Design (DDD): Entidades, Value Objects e Agregados", "foco": "Modelando o software na linguagem do negócio (Ubiquitous Language)"},
    {"id": 469, "escola": "04_backend_e_apis", "modulo": "Arquitetura", "tema": "DDD Avançado: Bounded Contexts e Context Mapping", "foco": "Delimitando fronteiras conceituais entre sistemas diferentes na mesma empresa"},
    {"id": 470, "escola": "04_backend_e_apis", "modulo": "Arquitetura", "tema": "CQRS (Command Query Responsibility Segregation)", "foco": "Separando o modelo de gravação (comandos) do modelo de leitura (consultas)"},

    # Carreira 2: Design Patterns Clássicos (GoF)
    {"id": 471, "escola": "04_backend_e_apis", "modulo": "Patterns", "tema": "Pattern Factory Method vs Abstract Factory", "foco": "Criando famílias de objetos relacionados sem expor a lógica de instanciação"},
    {"id": 472, "escola": "04_backend_e_apis", "modulo": "Patterns", "tema": "Pattern Builder: Construindo Objetos Complexos Passo a Passo", "foco": "Evitando construtores gigantes com 15 parâmetros opcionais"},
    {"id": 473, "escola": "04_backend_e_apis", "modulo": "Patterns", "tema": "Pattern Singleton: Vantagens, Perigos e Testabilidade", "foco": "Garantindo uma única instância global e por que ele pode virar antipattern"},
    {"id": 474, "escola": "04_backend_e_apis", "modulo": "Patterns", "tema": "Pattern Adapter: Fazendo Interfaces Incompatíveis Conversarem", "foco": "O adaptador de tomada que conecta sua API ao sistema legado de terceiro"},
    {"id": 475, "escola": "04_backend_e_apis", "modulo": "Patterns", "tema": "Pattern Decorator: Adicionando Comportamentos Dinamicamente", "foco": "Envolvendo objetos para adicionar logs, compressão ou criptografia em tempo de execução"},
    {"id": 476, "escola": "04_backend_e_apis", "modulo": "Patterns", "tema": "Pattern Strategy: Trocando Algoritmos em Tempo de Execução", "foco": "Calculando frete por Sedex, PAC ou transportadora sem usar 10 if/elses"},
    {"id": 477, "escola": "04_backend_e_apis", "modulo": "Patterns", "tema": "Pattern Observer: O Padrão Publicador/Assinante (Pub/Sub)", "foco": "Notificando automaticamente dezenas de ouvintes quando um evento ocorre"},
    {"id": 478, "escola": "04_backend_e_apis", "modulo": "Patterns", "tema": "Pattern Repository: Desacoplando o Domínio do Banco de Dados", "foco": "A coleção em memória que esconde queries SQL ou chamadas ORM"},

    # Carreira 3: Ecossistema Java & Spring Boot
    {"id": 479, "escola": "04_backend_e_apis", "modulo": "Java/Spring", "tema": "Spring Boot: O que é Inversão de Controle e Injeção de Dependências", "foco": "O container Spring gerenciando o ciclo de vida dos Beans (@Component, @Service, @Autowired)"},
    {"id": 480, "escola": "04_backend_e_apis", "modulo": "Java/Spring", "tema": "Spring Data JPA e Hibernate: Mapeamento Objeto-Relacional", "foco": "Consultas automáticas a partir do nome do método (findByEmail)"},
    {"id": 481, "escola": "04_backend_e_apis", "modulo": "Java/Spring", "tema": "Spring Security & Autenticação Stateless com JWT", "foco": "Filtros de segurança que interceptam requisições e validam perfis de acesso"},
    {"id": 482, "escola": "04_backend_e_apis", "modulo": "Java/Spring", "tema": "Tratamento Global de Exceções com @ControllerAdvice", "foco": "Padronizando respostas de erro amigáveis para o cliente da API"},
    {"id": 483, "escola": "04_backend_e_apis", "modulo": "Java/Spring", "tema": "Validação de Beans com Jakarta Validation (@NotNull, @Size, @Email)", "foco": "Rejeitando requisições malformadas automaticamente antes de tocar no banco"},
    {"id": 484, "escola": "04_backend_e_apis", "modulo": "Java/Spring", "tema": "Testes de Integração com Spring Boot Test e Testcontainers", "foco": "Subindo um banco Postgres real em container Docker durante a suíte de testes"},

    # Carreira 4: Ecossistema .NET C# Moderno
    {"id": 485, "escola": "04_backend_e_apis", "modulo": ".NET", "tema": "ASP.NET Core Web API: Minimal APIs vs Controllers", "foco": "Criando rotas ultraleves com alto desempenho e poucas linhas de código"},
    {"id": 486, "escola": "04_backend_e_apis", "modulo": ".NET", "tema": "Entity Framework Core (EF Core): Code-First e Migrations", "foco": "Gerando o banco de dados a partir das classes C# com dotnet ef database update"},
    {"id": 487, "escola": "04_backend_e_apis", "modulo": ".NET", "tema": "LINQ (Language Integrated Query) no C#", "foco": "Consultando coleções e tabelas com sintaxe fluente e tipada"},
    {"id": 488, "escola": "04_backend_e_apis", "modulo": ".NET", "tema": "Middlewares no ASP.NET Core: O Pipeline de Requisições", "foco": "Adicionando logging, compressão e autenticação na esteira HTTP"},
    {"id": 489, "escola": "04_backend_e_apis", "modulo": ".NET", "tema": "Padrão MediatR e CQRS no C#", "foco": "Desacoplando comandos e consultas com mensageria interna no processo"},

    # Carreira 5: Node.js, TypeScript & NestJS
    {"id": 490, "escola": "04_backend_e_apis", "modulo": "Node/Nest", "tema": "O Event Loop do Node.js: Como o JavaScript Lida com I/O Assíncrono", "foco": "Call stack, libuv, microtasks e macrotasks sem travar a thread única"},
    {"id": 491, "escola": "04_backend_e_apis", "modulo": "Node/Nest", "tema": "TypeScript para Back-end: Interfaces, Types e Generics", "foco": "Blindando projetos Node com segurança de tipagem e autocompletion no editor"},
    {"id": 492, "escola": "04_backend_e_apis", "modulo": "Node/Nest", "tema": "NestJS: Arquitetura Modular com Decorators (Angular do Back-end)", "foco": "Controllers, Services, Modules e Injeção de Dependência enterprise em Node"},
    {"id": 493, "escola": "04_backend_e_apis", "modulo": "Node/Nest", "tema": "Prisma ORM: Tipagem Extrema de Banco de Dados", "foco": "O schema declarativo que gera cliente TypeScript 100% type-safe"},
    {"id": 494, "escola": "04_backend_e_apis", "modulo": "Node/Nest", "tema": "Streams e Buffers no Node.js", "foco": "Processando arquivos de 50GB em pedaços contínuos sem estourar a memória RAM"},

    # Carreira 6: Microsserviços, Mensageria & Eventos
    {"id": 495, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Monolito vs Microsserviços: Quando Decompor um Sistema?", "foco": "Vantagens de escala independente vs o pesadelo da complexidade operacional"},
    {"id": 496, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "API Gateway: O Ponto Único de Entrada dos Microsserviços", "foco": "Roteamento, rate limiting, autenticação e agregação de dados centralizados"},
    {"id": 497, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Comunicação Síncrona vs Assíncrona (REST/gRPC vs Filas)", "foco": "Quando esperar resposta imediata e quando disparar e esquecer"},
    {"id": 498, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Introdução a Filas de Mensagens com RabbitMQ (AMQP)", "foco": "Exchanges, Queues, Bindings e entrega garantida de tarefas em segundo plano"},
    {"id": 499, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Apache Kafka: Streaming de Eventos em Alta Escala", "foco": "Tópicos particionados, offsets e processamento distribuído de milhões de eventos por segundo"},
    {"id": 500, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Arquitetura Orientada a Eventos (Event-Driven Architecture)", "foco": "Sistemas que reagem a fatos passados (Ex: PedidoCriado, PagamentoAprovado)"},
    {"id": 501, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Padrão SAGA: Transações Distribuídas sem Two-Phase Commit", "foco": "Coreografia vs Orquestração para reverter transações em caso de falha"},
    {"id": 502, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Pattern Circuit Breaker (Disjuntor) com Resilience4j", "foco": "Cortando chamadas a serviços caídos para não contaminar o sistema inteiro"},
    {"id": 503, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Pattern Outbox: Garantindo Entrega de Eventos com Banco de Dados", "foco": "Gravando na mesma transação local o dado de negócio e a mensagem a ser enviada"},
    {"id": 504, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Idempotência em APIs e Webhooks", "foco": "Como garantir que passar o mesmo cartão duas vezes não cobre o cliente em dobro"},
    {"id": 505, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "gRPC e Protocol Buffers (Protobuf)", "foco": "Comunicação binária ultrarrápida entre microsserviços muito mais leve que JSON"},
    {"id": 506, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Service Mesh (Istio / Linkerd)", "foco": "A camada de infraestrutura que gerencia tráfego, mTLS e telemetria de microsserviços"},
    {"id": 507, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Distributed Tracing: Rastreando Requisições com Correlation IDs", "foco": "Passando o mesmo ID de rastreio em headers HTTP para encontrar o erro nos logs"},
    {"id": 508, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Cache Distribuído com Redis: Estratégias Cache-Aside e Write-Through", "foco": "Acelerando leituras de banco de 200ms para 1ms na memória RAM"},
    {"id": 509, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Rate Limiting com Algoritmo Token Bucket", "foco": "Impedindo abusos de requisições limitando a quantidade de chamadas por segundo"},
    {"id": 510, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Decomposição de Banco de Dados: Database per Service", "foco": "Por que cada microsserviço deve ser dono exclusivo do seu próprio banco"},
    {"id": 511, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Event Sourcing: Guardando o Histórico Completo em Vez do Estado Atual", "foco": "Recriando o saldo bancário somando todos os depósitos e saques históricos"},
    {"id": 512, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Webhooks: Notificando Clientes Externos em Tempo Real", "foco": "Como o gateway de pagamento avisa sua loja que o PIX foi pago"},
    {"id": 513, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "GraphQL vs REST: Resolvendo Over-fetching e Under-fetching", "foco": "O cliente requisita exatamente os campos de que precisa em uma única chamada"},
    {"id": 514, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "WebSockets: Comunicação Bidirecional em Tempo Real", "foco": "Mantendo uma conexão aberta para chats, jogos e cotações da bolsa"},
    {"id": 515, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Server-Sent Events (SSE): Streaming Unidirecional de Notificações", "foco": "Enviando dados contínuos para o navegador sem o peso de um WebSocket"},
    {"id": 516, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Testes de Contrato com Pact", "foco": "Garantindo que mudanças na API não quebrem as expectativas do front-end"},
    {"id": 517, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Chaos Engineering: Testando Resiliência com Chaos Monkey", "foco": "Derrubando servidores intencionalmente em produção para testar auto-cura"},
    {"id": 518, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Feature Flags (Alternância de Recursos) em Produção", "foco": "Ligando ou desligando funcionalidades para 5% dos usuários sem fazer novo deploy"},
    {"id": 519, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "Versionamento de APIs (URI vs Header vs Query String)", "foco": "Mantendo v1 e v2 ativas simultaneamente sem quebrar clientes legados"},
    {"id": 520, "escola": "04_backend_e_apis", "modulo": "Microsserviços", "tema": "O Teorema CAP (Consistência, Disponibilidade e Tolerância a Partição)", "foco": "Por que é matematicamente impossível ter os 3 em um sistema distribuído na rede"}
]

# =============================================================================
# ESCOLA 05: FRONT-END, MOBILE & UX/UI AVANÇADO (IDs 521 ao 580 - 60 Mapas)
# =============================================================================
MAPAS_FRONTEND_AVANCADO: List[Dict] = [
    # Carreira 1: React.js Profissional & Ecossistema Moderno
    {"id": 521, "escola": "05_frontend_e_mobile", "modulo": "React", "tema": "O Virtual DOM e o Algoritmo de Reconciliação do React", "foco": "Calculando a diferença mínima na árvore para atualizar apenas o que mudou na tela"},
    {"id": 522, "escola": "05_frontend_e_mobile", "modulo": "React", "tema": "React Hooks Essenciais: useState e useEffect na Prática", "foco": "Gerenciando estados locais e efeitos colaterais sem usar classes antigas"},
    {"id": 523, "escola": "05_frontend_e_mobile", "modulo": "React", "tema": "useRef: Acesso Direto a Elementos do DOM sem Re-renderizar", "foco": "Focando campos de formulário e guardando valores que não disparam render"},
    {"id": 524, "escola": "05_frontend_e_mobile", "modulo": "React", "tema": "useMemo e useCallback: Otimizando Desempenho e Re-renders", "foco": "Memorizando cálculos caros e referências de funções entre renderizações"},
    {"id": 525, "escola": "05_frontend_e_mobile", "modulo": "React", "tema": "Context API: Compartilhando Estado Global sem Prop Drilling", "foco": "Disponibilizando tema escuro e usuário autenticado para qualquer componente"},
    {"id": 526, "escola": "05_frontend_e_mobile", "modulo": "React", "tema": "Custom Hooks: Reutilizando Lógica de Componentes", "foco": "Criando funções useFetch, useDebounce e useLocalStorage reaproveitáveis"},
    {"id": 527, "escola": "05_frontend_e_mobile", "modulo": "React", "tema": "Gerenciamento de Estado de Servidor com TanStack Query (React Query)", "foco": "Cache automático, sincronização e refetch em segundo plano sem dores de cabeça"},
    {"id": 528, "escola": "05_frontend_e_mobile", "modulo": "React", "tema": "Gerenciamento de Estado Global Leve com Zustand", "foco": "A alternativa moderna e concisa ao Redux sem boilerplate"},
    {"id": 529, "escola": "05_frontend_e_mobile", "modulo": "React", "tema": "Formulários de Alta Performance com React Hook Form e Zod", "foco": "Validação ultrarrápida de dados com validação de esquema unificada"},

    # Carreira 2: Next.js & Server-Side Rendering (SSR)
    {"id": 530, "escola": "05_frontend_e_mobile", "modulo": "Next.js", "tema": "A Diferença entre SPA, SSR, SSG e ISR", "foco": "Renderização no cliente vs servidor vs páginas estáticas pré-compiladas"},
    {"id": 531, "escola": "05_frontend_e_mobile", "modulo": "Next.js", "tema": "Next.js App Router: Estrutura de Pastas e Roteamento", "foco": "Rotas baseadas em diretórios com layout.tsx, page.tsx e loading.tsx"},
    {"id": 532, "escola": "05_frontend_e_mobile", "modulo": "Next.js", "tema": "React Server Components (RSC): O que Roda no Servidor vs Cliente", "foco": "Executando buscas de banco direto no componente e enviando zero JavaScript de bundle"},
    {"id": 533, "escola": "05_frontend_e_mobile", "modulo": "Next.js", "tema": "Server Actions no Next.js: Mutando Dados sem Criar Rotas de API", "foco": "Enviando formulários diretamente para funções assíncronas do servidor"},
    {"id": 534, "escola": "05_frontend_e_mobile", "modulo": "Next.js", "tema": "Otimização de Imagens e Fontes com next/image e next/font", "foco": "Evitando Layout Shifts e gerando imagens WebP responsivas automaticamente"},
    {"id": 535, "escola": "05_frontend_e_mobile", "modulo": "Next.js", "tema": "SEO Dinâmico e Geração de Metatags com generateMetadata", "foco": "Configurando OpenGraph e Twitter Cards perfeitos para redes sociais compartilharem"},

    # Carreira 3: Desenvolvimento Mobile Multiplataforma com Flutter
    {"id": 536, "escola": "05_frontend_e_mobile", "modulo": "Flutter", "tema": "A Filosofia do Flutter: Tudo é um Widget", "foco": "O motor Skia/Impeller que desenha pixel por pixel na tela nativa"},
    {"id": 537, "escola": "05_frontend_e_mobile", "modulo": "Flutter", "tema": "StatelessWidget vs StatefulWidget no Flutter", "foco": "Elementos visuais estáticos vs telas que reagem a toques com setState"},
    {"id": 538, "escola": "05_frontend_e_mobile", "modulo": "Flutter", "tema": "Layouts Essenciais: Column, Row, Stack e Expanded", "foco": "Organizando interfaces verticais, horizontais e elementos sobrepostos"},
    {"id": 539, "escola": "05_frontend_e_mobile", "modulo": "Flutter", "tema": "Listas Dinâmicas de Alta Performance com ListView.builder", "foco": "Renderizando milhares de itens na tela sem engasgar o scroll"},
    {"id": 540, "escola": "05_frontend_e_mobile", "modulo": "Flutter", "tema": "Navegação e Rotas Nomeadas com GoRouter", "foco": "Passando parâmetros e gerenciando histórico de telas no app mobile"},
    {"id": 541, "escola": "05_frontend_e_mobile", "modulo": "Flutter", "tema": "Gerenciamento de Estado no Flutter com Bloc / Cubit", "foco": "Separando regras de negócio da interface com arquitetura baseada em eventos"},
    {"id": 542, "escola": "05_frontend_e_mobile", "modulo": "Flutter", "tema": "Consumindo APIs REST no Flutter com a Biblioteca Dio", "foco": "Interceptors, cancelamento de requisições e serialização de JSON"},
    {"id": 543, "escola": "05_frontend_e_mobile", "modulo": "Flutter", "tema": "Persistência Local no App com SharedPreferences e Hive/Isar", "foco": "Guardando o token do usuário e preferências offline em banco ultrarrápido"},
    {"id": 544, "escola": "05_frontend_e_mobile", "modulo": "Flutter", "tema": "Acessando Recursos Nativos: Câmera, GPS e Notificações Push", "foco": "Utilizando plugins para interagir com o hardware do Android e iOS"},
    {"id": 545, "escola": "05_frontend_e_mobile", "modulo": "Flutter", "tema": "Build e Publicação: Gerando APK, AAB e IPA para as Lojas", "foco": "Assinatura de certificados e regras da Google Play Store e Apple App Store"},

    # Carreira 4: CSS Avançado, Design Systems & Acessibilidade (a11y)
    {"id": 546, "escola": "05_frontend_e_mobile", "modulo": "CSS/Design", "tema": "CSS Grid Layout Avançado: Áreas Nomeadas (grid-template-areas)", "foco": "Desenhando layouts de dashboard inteiros como um mapa em texto"},
    {"id": 547, "escola": "05_frontend_e_mobile", "modulo": "CSS/Design", "tema": "Variáveis CSS Nativas (Custom Properties) e Temas Claro/Escuro", "foco": "Trocando as cores da interface inteira alterando uma única classe :root"},
    {"id": 548, "escola": "05_frontend_e_mobile", "modulo": "CSS/Design", "tema": "Animações Fluídas com CSS Transitions, Keyframes e transform", "foco": "Criando micro-interações sem degradar os 60 quadros por segundo da GPU"},
    {"id": 549, "escola": "05_frontend_e_mobile", "modulo": "CSS/Design", "tema": "Tailwind CSS: Utilitários em Primeiro Lugar e Configuração de Tema", "foco": "Estilizando interfaces rapidamente sem sair do arquivo JSX/HTML"},
    {"id": 550, "escola": "05_frontend_e_mobile", "modulo": "CSS/Design", "tema": "Componentes Estilizados com Tailwind e Shadcn/UI", "foco": "Componentes acessíveis, customizáveis e que você copia direto para o projeto"},
    {"id": 551, "escola": "05_frontend_e_mobile", "modulo": "CSS/Design", "tema": "Design Systems: Criando Design Tokens de Cor, Tipografia e Espaçamento", "foco": "A fonte única da verdade que alinha designers de produto e engenheiros de software"},
    {"id": 552, "escola": "05_frontend_e_mobile", "modulo": "CSS/Design", "tema": "Acessibilidade Web (a11y) e as Diretrizes WCAG", "foco": "Contrastes mínimos de cor, navegação por teclado e suporte a leitores de tela"},
    {"id": 553, "escola": "05_frontend_e_mobile", "modulo": "CSS/Design", "tema": "Papéis ARIA e Atributos de Acessibilidade (aria-label, aria-expanded)", "foco": "Ensinando leitores de tela a entender menus suspensos e modais dinâmicos"},
    {"id": 554, "escola": "05_frontend_e_mobile", "modulo": "CSS/Design", "tema": "Figma para Desenvolvedores: Tokens, Auto-Layout e Hand-off", "foco": "Lendo espaçamentos, tipografia e exportando assets do design para o código"},

    # Carreira 5: Performance Web & Testes de Front-end
    {"id": 555, "escola": "05_frontend_e_mobile", "modulo": "Performance", "tema": "Core Web Vitals do Google: LCP, INP e CLS", "foco": "As três métricas oficiais do Google que determinam a velocidade percebida e ranking de busca"},
    {"id": 556, "escola": "05_frontend_e_mobile", "modulo": "Performance", "tema": "Code Splitting e Lazy Loading com React.lazy e Suspense", "foco": "Baixando pedaços do JavaScript apenas quando o usuário visita a página da rota"},
    {"id": 557, "escola": "05_frontend_e_mobile", "modulo": "Performance", "tema": "Análise de Bundle com Webpack Bundle Analyzer e Vite Visualizer", "foco": "Descobrindo quais bibliotecas pesadas estão inflando o tempo de carregamento"},
    {"id": 558, "escola": "05_frontend_e_mobile", "modulo": "Performance", "tema": "Progressive Web Apps (PWA): Service Workers e Manifesto Web", "foco": "Transformando sites em aplicativos instaláveis com funcionamento offline"},
    {"id": 559, "escola": "05_frontend_e_mobile", "modulo": "Testes", "tema": "Testes Unitários e de Componentes com Vitest e React Testing Library", "foco": "Testando o comportamento da interface pelo ponto de vista do usuário real"},
    {"id": 560, "escola": "05_frontend_e_mobile", "modulo": "Testes", "tema": "Testes de Ponta a Ponta (E2E) com Playwright e Cypress", "foco": "Robôs que abrem o navegador, clicam em botões e compram produtos para testar fluxos inteiros"},
    {"id": 561, "escola": "05_frontend_e_mobile", "modulo": "UX/UI", "tema": "Leis da Psicologia em UX: Lei de Fitts e Lei de Hick", "foco": "Tamanho e distância de botões e por que ter opções demais paralisa o usuário"},
    {"id": 562, "escola": "05_frontend_e_mobile", "modulo": "UX/UI", "tema": "Hierarquia Visual e Tipografia na Construção de Interfaces", "foco": "Guiando o olho do leitor com pesos de fonte, contrastes e espaçamentos adequados"},
    {"id": 563, "escola": "05_frontend_e_mobile", "modulo": "UX/UI", "tema": "Estados de Interface: Ideal, Vazio, Carregando, Erro e Sucesso", "foco": "Os 5 estados obrigatórios que toda tela bem desenhada precisa contemplar"},
    {"id": 564, "escola": "05_frontend_e_mobile", "modulo": "UX/UI", "tema": "Design Responsivo Mobile-First vs Desktop-First", "foco": "Construindo para a tela menor e mais restritiva antes de expandir para telas grandes"},
    {"id": 565, "escola": "05_frontend_e_mobile", "modulo": "UX/UI", "tema": "Testes de Usabilidade e Arquitetura da Informação", "foco": "Card sorting, árvores de navegação e identificando onde usuários reais se perdem"},
    {"id": 566, "escola": "05_frontend_e_mobile", "modulo": "Mobile", "tema": "React Native vs Flutter: Comparativo de Arquitetura", "foco": "Ponte JavaScript vs compilação nativa para telas e motores gráficos"},
    {"id": 567, "escola": "05_frontend_e_mobile", "modulo": "Mobile", "tema": "Expo: O Ecossistema que Acelera Projetos React Native", "foco": "Desenvolvendo para iOS sem precisar de um Mac através do aplicativo Expo Go"},
    {"id": 568, "escola": "05_frontend_e_mobile", "modulo": "Mobile", "tema": "Gestão de Teclado e Telas Pequenas no Mobile (KeyboardAvoidingView)", "foco": "Evitando que o teclado virtual tampe o botão de confirmar ou os campos de formulário"},
    {"id": 569, "escola": "05_frontend_e_mobile", "modulo": "Mobile", "tema": "Deep Linking no Mobile: Abrindo Telas Específicas via Links da Web", "foco": "Levando o usuário direto para o produto da promoção ao tocar no link do Instagram"},
    {"id": 570, "escola": "05_frontend_e_mobile", "modulo": "Mobile", "tema": "Monetização e Compras no App (In-App Purchases)", "foco": "Integrando assinaturas de aplicativos com as APIs oficiais do Google e da Apple"},
    {"id": 571, "escola": "05_frontend_e_mobile", "modulo": "Front-end", "tema": "Web Components Nativos: Custom Elements e Shadow DOM", "foco": "Criando tags HTML próprias encapsuladas que funcionam em qualquer framework"},
    {"id": 572, "escola": "05_frontend_e_mobile", "modulo": "Front-end", "tema": "Micro Front-ends com Module Federation do Webpack", "foco": "Permitindo que equipes independentes façam deploy de partes da mesma página web"},
    {"id": 573, "escola": "05_frontend_e_mobile", "modulo": "Front-end", "tema": "WebAssembly (WASM): Rodando C++, Rust e Go no Navegador", "foco": "Executando softwares pesados de edição de vídeo e jogos na web com velocidade nativa"},
    {"id": 574, "escola": "05_frontend_e_mobile", "modulo": "Front-end", "tema": "Internacionalização (i18n): Suporte a Múltiplos Idiomas e Moedas", "foco": "Formatando datas, pluralização e textos em português, inglês e espanhol"},
    {"id": 575, "escola": "05_frontend_e_mobile", "modulo": "Front-end", "tema": "Trabalhando com Gráficos Interativos usando Chart.js e D3.js", "foco": "Renderizando gráficos de pizza, barras e visualizações de dados complexas em canvas/SVG"},
    {"id": 576, "escola": "05_frontend_e_mobile", "modulo": "Front-end", "tema": "Three.js e WebGL: Gráficos 3D Interativos na Web", "foco": "Cenas, câmeras, malhas, iluminação e renderização 3D no navegador"},
    {"id": 577, "escola": "05_frontend_e_mobile", "modulo": "Front-end", "tema": "Segurança no Front-end: Prevenção de Clickjacking e XSS", "foco": "Sanitizando dados inseridos por usuários com bibliotecas como DOMPurify"},
    {"id": 578, "escola": "05_frontend_e_mobile", "modulo": "Front-end", "tema": "Vite: A Ferramenta de Build Ultrarrápida baseada em ES Modules", "foco": "Hot Module Replacement (HMR) instantâneo que aposentou o Webpack tradicional"},
    {"id": 579, "escola": "05_frontend_e_mobile", "modulo": "Front-end", "tema": "Storybook: Desenvolvendo e Documentando Componentes Isolados", "foco": "O catálogo visual interativo para testar botões e cards fora da aplicação principal"},
    {"id": 580, "escola": "05_frontend_e_mobile", "modulo": "Front-end", "tema": "A Carreira de Front-end Specialist: Do Júnior ao Tech Lead", "foco": "As competências técnicas, visão de produto e liderança para evoluir na carreira"}
]

# =============================================================================
# ESCOLA 06: BANCO DE DADOS, BIG DATA & IA AVANÇADA (IDs 581 ao 640 - 60 Mapas)
# =============================================================================
MAPAS_DADOS_IA_AVANCADO: List[Dict] = [
    # Carreira 1: SQL Avançado & Tuning de Bancos Relacionais
    {"id": 581, "escola": "06_banco_dados_e_ia", "modulo": "SQL Avançado", "tema": "Window Functions no SQL: ROW_NUMBER, RANK e DENSE_RANK", "foco": "Calculando rankings e numerações de linhas sem precisar agrupar a consulta inteira"},
    {"id": 582, "escola": "06_banco_dados_e_ia", "modulo": "SQL Avançado", "tema": "Window Functions Analíticas: LEAD e LAG", "foco": "Comparando o valor da linha atual com a anterior para calcular variações de vendas"},
    {"id": 583, "escola": "06_banco_dados_e_ia", "modulo": "SQL Avançado", "tema": "Common Table Expressions (CTEs) e o Comando WITH", "foco": "Quebrando consultas SQL monstruosas em etapas legíveis e reutilizáveis"},
    {"id": 584, "escola": "06_banco_dados_e_ia", "modulo": "SQL Avançado", "tema": "CTEs Recursivas: Consultando Estruturas em Árvore e Hierarquias", "foco": "Mapeando chefes e subordinados ou categorias pai e filho em uma única query"},
    {"id": 585, "escola": "06_banco_dados_e_ia", "modulo": "SQL Avançado", "tema": "Operadores de Conjunto: UNION, UNION ALL, INTERSECT e EXCEPT", "foco": "Combinando resultados de tabelas diferentes respeitando a compatibilidade de colunas"},
    {"id": 586, "escola": "06_banco_dados_e_ia", "modulo": "SQL Avançado", "tema": "Subconsultas Correlacionadas vs Subconsultas Simples", "foco": "Subqueries que dependem da linha externa e os riscos de lentidão extrema"},
    {"id": 587, "escola": "06_banco_dados_e_ia", "modulo": "Tuning", "tema": "Como Funciona o Otimizador de Consultas (Query Planner)", "foco": "Como o banco lê seu SQL e escolhe o plano de execução mais eficiente"},
    {"id": 588, "escola": "06_banco_dados_e_ia", "modulo": "Tuning", "tema": "Lendo e Interpretando o Comando EXPLAIN ANALYZE", "foco": "Identificando se o banco está fazendo Sequential Scan (lento) ou Index Scan (rápido)"},
    {"id": 589, "escola": "06_banco_dados_e_ia", "modulo": "Tuning", "tema": "Tipos de Índices: B-Tree, Hash, GIN e GiST no PostgreSQL", "foco": "Escolhendo a estrutura de índice perfeita para números, textos ou buscas JSON"},
    {"id": 590, "escola": "06_banco_dados_e_ia", "modulo": "Tuning", "tema": "Índices Compostos e a Regra do Prefixo Mais à Esquerda", "foco": "A ordem correta das colunas ao criar um índice para multi-filtros"},
    {"id": 591, "escola": "06_banco_dados_e_ia", "modulo": "Tuning", "tema": "Índices Parciais e Índices em Expressões", "foco": "Indexando apenas linhas ativas (WHERE ativo = true) para economizar disco"},
    {"id": 592, "escola": "06_banco_dados_e_ia", "modulo": "Tuning", "tema": "Níveis de Isolamento de Transações: Read Committed vs Serializable", "foco": "Os 4 níveis do padrão SQL contra leituras sujas, não repetíveis e fantasmas"},
    {"id": 593, "escola": "06_banco_dados_e_ia", "modulo": "Tuning", "tema": "Locks no Banco de Dados: Pessimista vs Otimista", "foco": "Travando registros no SELECT FOR UPDATE vs checando versão do registro antes de salvar"},
    {"id": 594, "escola": "06_banco_dados_e_ia", "modulo": "Tuning", "tema": "Connection Pooling com PgBouncer e HikariCP", "foco": "Reutilizando conexões de banco para evitar o custo de abrir novas conexões a cada requisição"},
    {"id": 595, "escola": "06_banco_dados_e_ia", "modulo": "Tuning", "tema": "Particionamento de Tabelas (Table Partitioning)", "foco": "Dividindo tabelas com 1 bilhão de linhas por mês ou ano de forma transparente"},
    {"id": 596, "escola": "06_banco_dados_e_ia", "modulo": "Tuning", "tema": "Replicação de Banco: Primário/Réplica e Read Replicas", "foco": "Enviando todas as escritas para o servidor principal e leituras pesadas para as réplicas"},

    # Carreira 2: Bancos NoSQL & Modelagem Moderna
    {"id": 597, "escola": "06_banco_dados_e_ia", "modulo": "NoSQL", "tema": "Os 4 Tipos de Bancos NoSQL: Documento, Chave-Valor, Família de Colunas e Grafo", "foco": "Quando usar MongoDB, Redis, Cassandra ou Neo4j para cada tipo de problema"},
    {"id": 598, "escola": "06_banco_dados_e_ia", "modulo": "NoSQL", "tema": "Modelagem no MongoDB: Embutir (Embedding) vs Referenciar (Referencing)", "foco": "A decisão central de design no NoSQL orientada aos padrões de leitura da aplicação"},
    {"id": 599, "escola": "06_banco_dados_e_ia", "modulo": "NoSQL", "tema": "Aggregation Framework no MongoDB: Pipelines de Transformação ($match, $group)", "foco": "Processando relatórios e transformações analíticas diretamente no cluster de documentos"},
    {"id": 600, "escola": "06_banco_dados_e_ia", "modulo": "NoSQL", "tema": "Estruturas de Dados Avançadas no Redis (Hashes, Sorted Sets, Bitmaps)", "foco": "Criando placares de jogos e contadores de presença com velocidade de memória pura"},
    {"id": 601, "escola": "06_banco_dados_e_ia", "modulo": "NoSQL", "tema": "Cassandra e Bancos Wide-Column: Alta Disponibilidade e Escala Linear", "foco": "Gravando terabytes por segundo sem ponto único de falha"},
    {"id": 602, "escola": "06_banco_dados_e_ia", "modulo": "NoSQL", "tema": "Bancos de Dados em Grafo com Neo4j e Cypher", "foco": "Consultando relacionamentos complexos de redes sociais e detecção de fraudes"},
    {"id": 603, "escola": "06_banco_dados_e_ia", "modulo": "NoSQL", "tema": "Elasticsearch: Motor de Busca Textual e Inverted Index", "foco": "Buscando produtos com tolerância a erros de digitação (Fuzzy Search) em milissegundos"},

    # Carreira 3: Engenharia de Dados & Data Warehousing
    {"id": 604, "escola": "06_banco_dados_e_ia", "modulo": "Engenharia Dados", "tema": "O que é Engenharia de Dados? (OLTP vs OLAP)", "foco": "Bancos transacionais de dia a dia vs bancos analíticos para tomada de decisão"},
    {"id": 605, "escola": "06_banco_dados_e_ia", "modulo": "Engenharia Dados", "tema": "Pipelines de ETL (Extract, Transform, Load) vs ELT", "foco": "Como empresas movem dados de dezenas de fontes para um repositório central"},
    {"id": 606, "escola": "06_banco_dados_e_ia", "modulo": "Engenharia Dados", "tema": "Modelagem Dimensional: Esquema Estrela (Star Schema) e Floco de Neve", "foco": "Tabelas Fato com métricas e Tabelas Dimensão com contextos analíticos"},
    {"id": 607, "escola": "06_banco_dados_e_ia", "modulo": "Engenharia Dados", "tema": "Data Lakes vs Data Warehouses vs Data Lakehouses", "foco": "Armazenamento bruto de dados não estruturados vs dados limpos e tipados"},
    {"id": 608, "escola": "06_banco_dados_e_ia", "modulo": "Engenharia Dados", "tema": "Orquestração de Dados com Apache Airflow (DAGs)", "foco": "Agendando e monitorando pipelines de dados com código Python"},
    {"id": 609, "escola": "06_banco_dados_e_ia", "modulo": "Engenharia Dados", "tema": "Processamento Massivo com Apache Spark", "foco": "Computação distribuída em cluster para analisar petabytes de dados"},
    {"id": 610, "escola": "06_banco_dados_e_ia", "modulo": "Engenharia Dados", "tema": "Formatos de Arquivos Colunares: Parquet vs Avro vs CSV", "foco": "Por que o formato colunar Parquet reduz em 80% os custos de consulta na nuvem"},
    {"id": 611, "escola": "06_banco_dados_e_ia", "modulo": "Engenharia Dados", "tema": "Data Warehouses Modernos na Nuvem: BigQuery, Snowflake e Redshift", "foco": "Consultando petabytes com SQL padrão pagando apenas pelos bytes escaneados"},
    {"id": 612, "escola": "06_banco_dados_e_ia", "modulo": "Engenharia Dados", "tema": "Transformação de Dados com dbt (Data Build Tool)", "foco": "Aplicando boas práticas de software (versionamento e testes) em códigos SQL"},

    # Carreira 4: Machine Learning & Ciência de Dados
    {"id": 613, "escola": "06_banco_dados_e_ia", "modulo": "Machine Learning", "tema": "O Ciclo de Vida de um Projeto de Ciência de Dados (CRISP-DM)", "foco": "Do entendimento do problema de negócio até o modelo gerando valor em produção"},
    {"id": 614, "escola": "06_banco_dados_e_ia", "modulo": "Machine Learning", "tema": "Aprendizado Supervisionado vs Não Supervisionado vs Por Reforço", "foco": "Aprendendo com dados rotulados, descobrindo agrupamentos sozinhos ou tentativa e erro"},
    {"id": 615, "escola": "06_banco_dados_e_ia", "modulo": "Machine Learning", "tema": "Regressão Linear e Regressão Logística", "foco": "Prevendo um valor contínuo (preço) vs prevendo uma probabilidade (sim/não)"},
    {"id": 616, "escola": "06_banco_dados_e_ia", "modulo": "Machine Learning", "tema": "Árvores de Decisão e Random Forest", "foco": "Combinando centenas de árvores de decisão para criar previsões robustas"},
    {"id": 617, "escola": "06_banco_dados_e_ia", "modulo": "Machine Learning", "tema": "Algoritmos de Agrupamento: K-Means Desmistificado", "foco": "Segmentando clientes em grupos de compras similares pelo comportamento"},
    {"id": 618, "escola": "06_banco_dados_e_ia", "modulo": "Machine Learning", "tema": "Métricas de Avaliação: Acurácia, Precisão, Recall e F1-Score", "foco": "Por que a acurácia é enganosa em diagnósticos de doenças raras ou fraudes"},
    {"id": 619, "escola": "06_banco_dados_e_ia", "modulo": "Machine Learning", "tema": "A Matriz de Confusão: Falsos Positivos e Falsos Negativos", "foco": "O impacto no mundo real de classificar errado um cliente ou transação"},
    {"id": 620, "escola": "06_banco_dados_e_ia", "modulo": "Machine Learning", "tema": "Overfitting vs Underfitting: O Balanço do Viés e Variância", "foco": "O modelo que decora os dados de treino mas falha feio na vida real"},
    {"id": 621, "escola": "06_banco_dados_e_ia", "modulo": "Machine Learning", "tema": "Validação Cruzada (Cross-Validation K-Fold)", "foco": "Dividindo os dados em vários pedaços para testar a consistência do algoritmo"},
    {"id": 622, "escola": "06_banco_dados_e_ia", "modulo": "Machine Learning", "tema": "Engenharia de Features: Normalização, One-Hot Encoding e Imputação", "foco": "Preparando tabelas brutas para os algoritmos matemáticos conseguirem aprender"},
    {"id": 623, "escola": "06_banco_dados_e_ia", "modulo": "Machine Learning", "tema": "Redes Neurais Artificiais (ANN) e o Algoritmo Backpropagation", "foco": "Camadas de neurônios ajustando seus pesos através do gradiente descendente"},
    {"id": 624, "escola": "06_banco_dados_e_ia", "modulo": "Machine Learning", "tema": "Deep Learning: Redes Convolucionais (CNN) para Visão Computacional", "foco": "Como computadores identificam rostos e objetos em imagens com filtros de convolução"},
    {"id": 625, "escola": "06_banco_dados_e_ia", "modulo": "Machine Learning", "tema": "Redes Recorrentes (RNN) e LSTMs para Séries Temporais", "foco": "Modelos que possuem memória para prever cotações e próximas palavras de textos"},

    # Carreira 5: Engenharia de LLMs, Prompts, Embeddings & RAG
    {"id": 626, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "A Arquitetura Transformer e o Mecanismo de Atenção ('Attention is All You Need')", "foco": "A revolução que permitiu aos modelos de IA entender o contexto global de frases longas"},
    {"id": 627, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "O que são LLMs (Large Language Models) e como funcionam Tokens", "foco": "Previsão probabilística do próximo pedaço de palavra em escalas bilionárias"},
    {"id": 628, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "Engenharia de Prompts: Few-Shot, Chain-of-Thought e ReAct", "foco": "Instruindo o modelo a raciocinar passo a passo para não inventar respostas"},
    {"id": 629, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "Alucinações em LLMs: Por que Ocorrem e Como Mitigar", "foco": "Estratégias de temperatura, ancoragem em contexto real e validação de saídas"},
    {"id": 630, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "Embeddings Vetoriais: Transformando Texto e Imagens em Números", "foco": "Mapeando significado semântico em um espaço de centenas de dimensões"},
    {"id": 631, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "Similaridade de Cosseno para Busca Semântica", "foco": "Medindo o ângulo entre vetores para encontrar textos com ideias semelhantes"},
    {"id": 632, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "Bancos de Dados Vetoriais (Pinecone, ChromaDB, pgvector)", "foco": "Armazenando e consultando milhões de embeddings em frações de segundo"},
    {"id": 633, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "Arquitetura RAG (Retrieval-Augmented Generation)", "foco": "Alimentando a IA com os documentos privados da sua empresa antes de responder"},
    {"id": 634, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "Chunking de Documentos: Estratégias de Divisão de Texto para RAG", "foco": "Dividindo PDFs em pedaços com sobreposição (overlap) sem perder contexto"},
    {"id": 635, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "Frameworks de Orquestração de IA: LangChain e LlamaIndex", "foco": "Construindo pipelines com memória, ferramentas externas e conexões com bases de dados"},
    {"id": 636, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "Agentes Autônomos de IA e Chamada de Funções (Function Calling / Tool Calling)", "foco": "Permitindo que a IA execute código, consulte APIs e tome decisões dinâmicas"},
    {"id": 637, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "Fine-Tuning de Modelos com LoRA e QLoRA", "foco": "Ajustando os pesos de uma LLM para especializá-la em jargões médicos ou jurídicos"},
    {"id": 638, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "Modelos Open-Source vs APIs Proprietárias (Llama 3 vs GPT-4/Claude)", "foco": "Privacidade total rodando na sua máquina vs comodidade de APIs em nuvem"},
    {"id": 639, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "MLOps: Monitoramento e Versionamento de Modelos com MLflow", "foco": "Registrando experimentos de IA e fazendo deploy contínuo de modelos em produção"},
    {"id": 640, "escola": "06_banco_dados_e_ia", "modulo": "IA Generativa", "tema": "Ética em IA, Viés Algorítmico e Segurança (Prompt Injection)", "foco": "Defendendo sistemas de IA contra ataques de injeção e garantindo respostas justas"}
]

# =============================================================================
# ESCOLA 02: LÓGICA DE PROGRAMAÇÃO & DESAFIOS PRÁTICOS (IDs 641 ao 700 - 60 Mapas)
# =============================================================================
MAPAS_LOGICA_DESAFIOS: List[Dict] = [
    # Carreira 1: Estruturas de Dados Fundamentais na Prática
    {"id": 641, "escola": "02_logica_e_algoritmos", "modulo": "Algoritmos", "tema": "Pilhas (Stacks): Conceito LIFO e Casos de Uso Reais", "foco": "O botão Desfazer (Ctrl+Z) e o histórico de navegação do browser"},
    {"id": 642, "escola": "02_logica_e_algoritmos", "modulo": "Algoritmos", "tema": "Filas (Queues): Conceito FIFO e Fila de Impressão", "foco": "O primeiro que chega é o primeiro a ser atendido sem furar a ordem"},
    {"id": 643, "escola": "02_logica_e_algoritmos", "modulo": "Algoritmos", "tema": "Filas de Prioridade e Heaps Binários (Min-Heap e Max-Heap)", "foco": "Atendimento prioritário em emergências de hospital gerenciado em árvore"},
    {"id": 644, "escola": "02_logica_e_algoritmos", "modulo": "Algoritmos", "tema": "Listas Encadeadas Simples vs Duplamente Encadeadas", "foco": "Nós que apontam para o próximo elemento na memória sem alocação contígua"},
    {"id": 645, "escola": "02_logica_e_algoritmos", "modulo": "Algoritmos", "tema": "Tabelas Hash e Resolução de Colisões (Encadeamento vs Sondagem Aberta)", "foco": "Como a função hash transforma texto em índice e o que fazer se dois caírem na mesma gaveta"},
    {"id": 646, "escola": "02_logica_e_algoritmos", "modulo": "Algoritmos", "tema": "Árvores Binárias de Busca (BST): Inserção, Busca e Percursos", "foco": "Elementos menores à esquerda e maiores à direita com percurso em-ordem"},

    # Carreira 2: Algoritmos de Ordenação & Busca Comparados
    {"id": 647, "escola": "02_logica_e_algoritmos", "modulo": "Algoritmos", "tema": "Busca Linear vs Busca Binária: De O(n) para O(log n)", "foco": "Adivinhando o número secreto cortando a lista pela metade a cada tentativa"},
    {"id": 648, "escola": "02_logica_e_algoritmos", "modulo": "Algoritmos", "tema": "Bubble Sort e Selection Sort: Por que são Ineficientes?", "foco": "O custo quadrático O(n²) de comparar todos contra todos"},
    {"id": 649, "escola": "02_logica_e_algoritmos", "modulo": "Algoritmos", "tema": "Insertion Sort: O Algoritmo de Ordenar Cartas de Baralho na Mão", "foco": "Eficiente para listas pequenas ou dados que já chegam quase ordenados"},
    {"id": 650, "escola": "02_logica_e_algoritmos", "modulo": "Algoritmos", "tema": "Merge Sort: A Abordagem de Divisão e Conquista", "foco": "Dividindo a lista até o tamanho unitário e juntando os pedaços de forma ordenada"},
    {"id": 651, "escola": "02_logica_e_algoritmos", "modulo": "Algoritmos", "tema": "Quick Sort: A Escolha do Pivô e Particionamento", "foco": "O algoritmo padrão de sistemas operacionais e como evitar o pior caso"},
    {"id": 652, "escola": "02_logica_e_algoritmos", "modulo": "Algoritmos", "tema": "Counting Sort e Radix Sort: Ordenação em Tempo Linear O(n)", "foco": "Como ordenar sem fazer nenhuma comparação entre elementos"},

    # Carreira 3: Padrões de Resolução de Problemas em Entrevistas Técnicas
    {"id": 653, "escola": "02_logica_e_algoritmos", "modulo": "LeetCode", "tema": "Padrão Two Pointers (Dois Ponteiros)", "foco": "Dois índices andando em direções opostas para inverter strings ou achar somas"},
    {"id": 654, "escola": "02_logica_e_algoritmos", "modulo": "LeetCode", "tema": "Padrão Sliding Window (Janela Deslizante)", "foco": "Calculando a maior média ou menor subsequência sem reprocessar todos os elementos"},
    {"id": 655, "escola": "02_logica_e_algoritmos", "modulo": "LeetCode", "tema": "Padrão Fast and Slow Pointers (Tartaruga e Lebre de Floyd)", "foco": "Detectando ciclos em listas encadeadas sem gastar memória extra"},
    {"id": 656, "escola": "02_logica_e_algoritmos", "modulo": "LeetCode", "tema": "Padrão Monotonic Stack (Pilha Monotônica)", "foco": "Encontrando o próximo elemento maior à direita em tempo linear O(n)"},
    {"id": 657, "escola": "02_logica_e_algoritmos", "modulo": "LeetCode", "tema": "Manipulação de Bits (Bitwise): Operadores AND, OR, XOR e Shifts", "foco": "Truques de baixo nível para testar números ímpares e potência de 2 instantaneamente"},
    {"id": 658, "escola": "02_logica_e_algoritmos", "modulo": "LeetCode", "tema": "Algoritmo de Backtracking: O Problema das N-Rainhas e Sudoku", "foco": "Tentando um caminho e voltando atrás no primeiro erro até achar a solução"},
    {"id": 659, "escola": "02_logica_e_algoritmos", "modulo": "LeetCode", "tema": "Recursão vs Iteração: O Perigo do Stack Overflow", "foco": "Como cada chamada de função consome um pedaço da pilha de execução da memória"},
    {"id": 660, "escola": "02_logica_e_algoritmos", "modulo": "LeetCode", "tema": "Análise de Complexidade de Espaço (Space Complexity)", "foco": "Medindo quanta memória extra seu código consome além dos dados de entrada"},

    # Carreira 4: Engenharia de Software Prática & Resolução de Problemas
    {"id": 661, "escola": "02_logica_e_algoritmos", "modulo": "Prática Dev", "tema": "O Pensamento Computacional: Decomposição, Reconhecimento de Padrões, Abstração e Algoritmo", "foco": "Os 4 pilares mentais para resolver qualquer desafio do mundo real com tecnologia"},
    {"id": 662, "escola": "02_logica_e_algoritmos", "modulo": "Prática Dev", "tema": "Técnica de Depuração: Rubber Duck Debugging (O Pato de Borracha)", "foco": "Explicar o problema linha por linha em voz alta para ativar o raciocínio claro"},
    {"id": 663, "escola": "02_logica_e_algoritmos", "modulo": "Prática Dev", "tema": "Test-Driven Development (TDD): Red, Green, Refactor", "foco": "Escrevendo o teste que falha antes de escrever qualquer linha de implementação"},
    {"id": 664, "escola": "02_logica_e_algoritmos", "modulo": "Prática Dev", "tema": "Code Review: O que Avaliar no Código de Colegas de Equipe", "foco": "Legibilidade, segurança, casos de borda e empatia na comunicação técnica"},
    {"id": 665, "escola": "02_logica_e_algoritmos", "modulo": "Prática Dev", "tema": "Refatoração de Código: Identificando e Eliminando Code Smells", "foco": "Funções longas, classes com muitas responsabilidades e código duplicado"},
    {"id": 666, "escola": "02_logica_e_algoritmos", "modulo": "Prática Dev", "tema": "Git Avançado: git rebase vs git merge", "foco": "Mantendo um histórico linear limpo vs preservando o contexto exato de ramificações"},
    {"id": 667, "escola": "02_logica_e_algoritmos", "modulo": "Prática Dev", "tema": "Git Avançado: Desfazendo Coisas com reset, revert, stash e cherry-pick", "foco": "A caixa de ferramentas de emergência para quando você comete erros no repositório"},
    {"id": 668, "escola": "02_logica_e_algoritmos", "modulo": "Prática Dev", "tema": "Convenções de Commit: Conventional Commits e SemVer", "foco": "feat, fix, chore e versionamento semântico (MAJOR.MINOR.PATCH)"},
    {"id": 669, "escola": "02_logica_e_algoritmos", "modulo": "Prática Dev", "tema": "Documentação Técnica Eficaz: READMEs, Diagramas Mermaid e Wikis", "foco": "Como documentar para outro dev rodar o projeto em 5 minutos"},
    {"id": 670, "escola": "02_logica_e_algoritmos", "modulo": "Prática Dev", "tema": "Como Ler Códigos de Terceiros e Navegar em Bases Grandes (Codebase Navigation)", "foco": "Técnicas para entrar em uma empresa com 500 mil linhas de código sem pânico"},

    # Carreira 5: Lógica em Desafios do Mundo Real (Sistemas Famosos)
    {"id": 671, "escola": "02_logica_e_algoritmos", "modulo": "Mundo Real", "tema": "Como Funciona um Encurtador de URL (Bitly)", "foco": "Gerando IDs únicos em Base62 e redirecionamento HTTP 301/302"},
    {"id": 672, "escola": "02_logica_e_algoritmos", "modulo": "Mundo Real", "tema": "Como Funciona a Validação de CPF e Cartão de Crédito (Algoritmo de Luhn)", "foco": "Os dígitos verificadores matemáticos que detectam digitações incorretas"},
    {"id": 673, "escola": "02_logica_e_algoritmos", "modulo": "Mundo Real", "tema": "Como Funciona um Feed de Notícias (Instagram / Twitter)", "foco": "Fan-out on Write vs Fan-out on Read para celebridades com milhões de seguidores"},
    {"id": 674, "escola": "02_logica_e_algoritmos", "modulo": "Mundo Real", "tema": "Como Funciona o Sistema de Busca com Autocomplete do Google", "foco": "Árvores Trie em memória cache combinadas com frequência histórica de buscas"},
    {"id": 675, "escola": "02_logica_e_algoritmos", "modulo": "Mundo Real", "tema": "Como Funciona a Concorrência de Ingressos de Shows", "foco": "Filas virtuais com Redis, transações ACID e retenção temporária de assentos"},
    {"id": 676, "escola": "02_logica_e_algoritmos", "modulo": "Mundo Real", "tema": "Como Funciona o Cálculo de Rota do Uber", "foco": "Geohashing, células H3 e emparelhamento em tempo real entre motorista e passageiro"},
    {"id": 677, "escola": "02_logica_e_algoritmos", "modulo": "Mundo Real", "tema": "Como Funciona um Editor Colaborativo em Tempo Real (Google Docs / Figma)", "foco": "Operational Transformation (OT) vs CRDTs (Conflict-free Replicated Data Types)"},
    {"id": 678, "escola": "02_logica_e_algoritmos", "modulo": "Mundo Real", "tema": "Como Funciona a Detecção de Plágio e Diffs de Código", "foco": "O Algoritmo de Myers para encontrar a menor sequência de adições e remoções"},
    {"id": 679, "escola": "02_logica_e_algoritmos", "modulo": "Mundo Real", "tema": "Como Funciona o Mecanismo de Recomendação da Netflix", "foco": "Filtragem colaborativa e fatores latentes para sugerir filmes pelo seu gosto"},
    {"id": 680, "escola": "02_logica_e_algoritmos", "modulo": "Mundo Real", "tema": "Como Funciona o Gerenciamento de Memória de Jogos", "foco": "Object Pooling: Reutilizando projéteis e inimigos para evitar pausas do Garbage Collector"},

    # Carreira 6: Consolidação & Mentalidade do Engenheiro de Sucesso
    {"id": 681, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "A Navalha de Occam na Programação: A Solução Mais Simples", "foco": "Evitando engenharia excessiva (Overengineering) e complexidade desnecessária"},
    {"id": 682, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "A Falácia dos Custos Irrecuperáveis (Sunk Cost Fallacy) no Software", "foco": "A coragem de descartar código ruim antes que ele custe caro demais para manter"},
    {"id": 683, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "Débito Técnico: O que é, Como Gerenciar e Quando Pagar", "foco": "O atalho que você toma hoje pagando juros diários em manutenção amanhã"},
    {"id": 684, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "A Lei de Conway: O Software Reflete a Comunicação da Empresa", "foco": "Como a estrutura dos times molda diretamente a arquitetura dos sistemas"},
    {"id": 685, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "A Síndrome do Impostor no Desenvolvimento de Software", "foco": "Compreendendo que ninguém sabe tudo e que pesquisar faz parte do ofício"},
    {"id": 686, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "Aprender a Aprender: A Técnica Feynman Aplicada à Computação", "foco": "Explicando conceitos difíceis em linguagem simples para fixar o aprendizado"},
    {"id": 687, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "Como Fazer Perguntas Técnicas no Stack Overflow e aos Colegas", "foco": "Apresentando o contexto, o que você já tentou e exemplos mínimos reproduzíveis"},
    {"id": 688, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "Inglês para Programadores: O Vocabulário Essencial", "foco": "Desmistificando termos em inglês que destravam toda a documentação global"},
    {"id": 689, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "Construindo um Portfólio no GitHub que Encanta Recrutadores", "foco": "Projetos autorais com documentação impecável e código limpo em vez de cópias de cursos"},
    {"id": 690, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "Como se Preparar para Entrevistas de Emprego em Tecnologia", "foco": "Testes ao vivo (Live Coding), perguntas comportamentais e entrevistas de arquitetura"},
    {"id": 691, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "Open Source: Como Fazer sua Primeira Contribuição Pública", "foco": "Encontrando boas primeiras issues (Good First Issues) e abrindo Pull Requests"},
    {"id": 692, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "Trabalho Remoto Eficaz: Comunicação Assíncrona e Autonomia", "foco": "Produzindo com excelência sem precisar de reuniões intermináveis"},
    {"id": 693, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "Gestão de Tempo para Devs: Pomodoro e Blocos de Foco Profundo (Deep Work)", "foco": "Protegendo sua atenção contra interrupções para produzir em estado de flow"},
    {"id": 694, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "Ergonomia e Saúde do Programador: LER, DORT e Cuidados Visuais", "foco": "Postura, pausas ativas e ajustes de monitor para uma carreira longa e saudável"},
    {"id": 695, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "Carreira em Y: Especialista Técnico vs Gestor de Equipes", "foco": "Decidindo entre o caminho de Staff Engineer / Arquiteto ou Engineering Manager"},
    {"id": 696, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "Soft Skills que Dobram o Salário do Desenvolvedor", "foco": "Empatia, negociação de prazos, escuta ativa e clareza na transmissão de ideias"},
    {"id": 697, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "Networking Saudável em Tecnologia: Comunidades, Eventos e Meetups", "foco": "Criando conexões genuínas e ajudando outros para construir sua reputação"},
    {"id": 698, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "A Lei de Amdahl: Os Limites da Paralelização de Processos", "foco": "Por que adicionar mais processadores não acelera tarefas sequenciais obrigatórias"},
    {"id": 699, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "A Lei de Moore e o Futuro do Hardware de Computação", "foco": "A física dos transistores em escala nanométrica e os novos caminhos da computação"},
    {"id": 700, "escola": "02_logica_e_algoritmos", "modulo": "Mentalidade", "tema": "O Manifesto do Programador Vitalício (Lifelong Learner)", "foco": "A certeza de que na computação a curiosidade diária é o maior superpoder"}
]

def obter_todos_os_mapas_expansao() -> List[Dict]:
    """Retorna todos os 500 mapas da expansão consolidada (IDs 201 ao 700)."""
    return (
        MAPAS_PYTHON + 
        MAPAS_DEVOPS + 
        MAPAS_CIBERSEGURANCA + 
        MAPAS_UNINTER_AVANCADO + 
        MAPAS_BACKEND_AVANCADO + 
        MAPAS_FRONTEND_AVANCADO + 
        MAPAS_DADOS_IA_AVANCADO + 
        MAPAS_LOGICA_DESAFIOS
    )
