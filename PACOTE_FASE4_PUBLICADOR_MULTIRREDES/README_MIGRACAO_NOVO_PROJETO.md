# 🚀 MANUAL COMPLETO DE MIGRAÇÃO — FASE 4 (MOTOR DE PUBLICAÇÃO MULTIRREDES)

Este pacote contém **100% da esteira de publicação automática** desenvolvida, testada e desacoplada para ser utilizada em qualquer novo projeto de computação.

---

## 📁 Estrutura do Pacote

```
PACOTE_FASE4_PUBLICADOR_MULTIRREDES/
│
├── scripts/
│   ├── publicador_nuvem_github_actions.py  # Robô Mestre (executa nos 6 horários na nuvem)
│   ├── instagram_uploader.py               # Postagem no Instagram Reels (Meta Graph API)
│   ├── tiktok_uploader.py                  # Postagem no TikTok (Content Posting API v2)
│   ├── whatsapp_status_uploader.py         # Envio para WhatsApp Status (Evolution API)
│   ├── whatsapp_canal_e_status.py          # Envio para WhatsApp Canal & Status
│   ├── youtube_uploader.py                 # Envio para YouTube Shorts / Vídeos
│   ├── gerar_copies_postagem.py            # Gerador de copies, ganchos e hashtags
│   ├── gerador_capas.py                    # Gerador automático de thumbnails (16:9 e 9:16)
│   ├── exibir_chaves_github_secrets.py     # Utilitário para exportar variáveis para o GitHub
│   └── sincronizador_mestre_gdrive.py      # Watcher de pasta local / nuvem
│
├── workflows/
│   └── publicador_multirredes_6x_dia.yml   # Workflow do GitHub Actions (6x ao dia)
│
├── config/
│   ├── client_secret.example.json          # Template OAuth YouTube
│   ├── instagram_credentials.example.json   # Template Meta Graph API
│   ├── tiktok_credentials.example.json      # Template TikTok API
│   └── whatsapp_credentials.example.json    # Template Evolution API
│
├── templates/
│   └── 00_SINCRONIZACAO_TEMPLATE.json      # Banco JSON com a fila de vídeos e copies
│
├── requirements.txt                        # Dependências Python mínimas
├── PROMPT_PARA_O_OUTRO_CHAT.md             # Prompt pronto para copiar e colar na outra IA
└── README_MIGRACAO_NOVO_PROJETO.md         # Este guia
```

---

## 🛠️ Como Funciona o Motor de Publicação

1. **Repositório Central dos Vídeos (Google Drive ou S3):**
   * Os vídeos prontos ficam hospedados em uma pasta compartilhada no Google Drive.
2. **Execução Autônoma no GitHub Actions:**
   * O GitHub Actions acorda nos horários programados (`06h`, `09h`, `12h`, `15h`, `18h`, `21h`).
   * Ele consulta o arquivo de agendamento JSON (`00_SINCRONIZACAO_TEMPLATE.json`).
   * Localiza o vídeo do horário, faz o download do arquivo MP4 em 2 segundos.
   * Dispara as APIs simultâneas de publicação:
     - **Instagram Reels:** Upload de mídia via container e publicação na Meta Graph API.
     - **TikTok:** Inicialização de upload e publicação via TikTok Developer API.
     - **WhatsApp:** Envio de vídeo para Status e Canal via Evolution API hospedada no Render.
     - **YouTube:** Upload oficial via API v3 com título, tags e categoria.

---

## 🔑 Credenciais e Variáveis de Ambiente (GitHub Secrets)

No repositório do seu novo projeto no GitHub, vá em **Settings > Secrets and variables > Actions** e adicione:

* `INSTAGRAM_ACCESS_TOKEN`
* `INSTAGRAM_ACCOUNT_ID`
* `INSTAGRAM_USER_ID`
* `TIKTOK_CLIENT_KEY`
* `TIKTOK_CLIENT_SECRET`
* `TIKTOK_REFRESH_TOKEN`
* `EVOLUTION_API_URL` (ex: `https://evolution-api-latest-djvp.onrender.com`)
* `EVOLUTION_API_KEY` (ex: `ibpmcr_2026_seguro`)
* `EVOLUTION_INSTANCE` (ex: `matheus_barbosa`)
* `GDRIVE_FOLDER_ID` (ID da pasta no Google Drive onde estão os vídeos)

---

## 🚀 Como Integrar no Novo Projeto em 3 Passos

1. **Copie a pasta `scripts/` e `templates/`** para dentro do novo projeto.
2. **Copie o arquivo `workflows/publicador_multirredes_6x_dia.yml`** para `.github/workflows/` no novo projeto.
3. **Preencha o arquivo JSON de catálogo** (`00_SINCRONIZACAO_TEMPLATE.json`) com os nomes dos novos vídeos, títulos e legendas do novo projeto.
