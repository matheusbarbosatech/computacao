# 🚀 Pipeline de Extração em Lote - Nutror / Vimeo

Pipeline em Python para baixar e higienizar legendas de videoaulas do Vimeo embutidas na plataforma Nutror (Eduzz).

---

## 📁 Estrutura do Projeto

```
nutror_extractor/
├── main.py              # CLI principal de comando
├── downloader.py        # Motor de download em lote (yt-dlp + evasão + jitter)
├── cleaner.py           # Higienizador de legendas VTT para texto puro
├── crawler.py           # Capturador automatizado de links via Playwright
├── lista_aulas.txt      # Arquivo de entrada com as URLs dos iframes do Vimeo
└── transcricoes_limpas/ # Diretório de saída com aula_01.txt, aula_02.txt...
```

---

## ⚙️ Regras de Evasão Implementadas

1. **Injeção de Cabeçalho:** Adiciona `Referer: https://app.nutror.com/` em cada requisição para liberar vídeos privados configurados com restrição de domínio.
2. **Cookies Automáticos:** Usa `--cookies-from-browser chrome` para autenticação de sessão, com fallback suave caso o Chrome esteja aberto.
3. **Resfriamento / Jitter:** Atraso aleatório entre 3 e 7 segundos (`random.uniform(3.0, 7.0)`) entre as requisições para evitar rate limit ou bloqueio de IP.
4. **Tolerância a Falhas:** Bloco `try/except` robusto. Se uma aula não tiver legenda ou der erro, ela é registrada em `relatorio_extracao.json` e o loop continua ininterrupto para as próximas.
5. **Higienização de Texto:** Remove metadados WebVTT, timestamps e tags HTML (`<c>`, `<b>`), deduplica frases rolantes e organiza o texto em parágrafos legíveis.

---

## 🛠️ Como Usar

### Opção 1: Já tenho a lista de links
1. Cole os links no arquivo `lista_aulas.txt` (um por linha).
2. Execute no terminal:
```bash
uv run --with yt-dlp python main.py --download
```

---

### Opção 2: Capturar os links automaticamente da Nutror (Playwright)
O robô abre o Chrome, permite que você faça login na sua conta da Nutror e intercepta os links do Vimeo em tempo real conforme você navega ou pelo menu lateral:
```bash
uv run --with yt-dlp --with playwright python main.py --crawl
```
*Após capturar os links, eles já serão gravados automaticamente no `lista_aulas.txt`.*

---

### Opção 3: Modo Completo (Mapear + Baixar tudo)
```bash
uv run --with yt-dlp --with playwright python main.py --full
```

---

## 📊 Resultado
Os textos limpos e prontos para modelagem estarão em:
`transcricoes_limpas/aula_01.txt`, `aula_02.txt`, etc.
