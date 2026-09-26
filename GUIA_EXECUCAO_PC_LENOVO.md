# 💻 GUIA PRÁTICO: COMO RODAR O SISTEMA NO SEU PC LENOVO

> Este guia explica o passo a passo exato para você rodar o seu **Segundo Cérebro no Obsidian**, o **Robô Minerador do Drive** e a **Ponte Telegram -> Drive 5TB** no seu computador secundário (PC Lenovo).

---

## 📥 Passo 1: Puxar o Código Atualizado no PC Lenovo

No seu PC Lenovo, abra o terminal (PowerShell ou Prompt de Comando) e navegue até a pasta onde você quer salvar o projeto:

```bash
# Se for a primeira vez no Lenovo:
git clone https://github.com/matheusbarbosatech/computacao.git
cd computacao

# Se você já clonou antes, basta atualizar:
cd computacao
git pull origin main
```

---

## 🧠 Passo 2: Como Abrir o Segundo Cérebro no OBSIDIAN

1. Baixe e instale o [Obsidian](https://obsidian.md/) no seu PC Lenovo (é 100% gratuito);
2. Ao abrir o Obsidian, clique em: **"Open folder as vault" (Abrir pasta como cofre)**;
3. Selecione a pasta:
   ```
   C:\Users\SEU_USUARIO\computacao\SEGUNDO_CEREBRO_VAULT
   ```
4. **Pronto!** Automaticamente você terá:
   * A nota central de boas-vindas: `00_CENTRAL_MESTRE_SEGUNDO_CEREBRO.md`;
   * Todas as pastas organizadas por área (*01_CIBERSEGURANCA*, *02_MICRO_SAAS*, *03_IA*, etc.);
   * O **Graph View (Visualizador de Grafos)** apertando `Ctrl + G`, mostrando as conexões visuais entre cursos, ideias de SaaS e códigos!

---

## 🚀 Passo 3: Executar a Central no PC Lenovo (1 Clique)

Na pasta do projeto, basta dar dois cliques no arquivo:
👉 **`RODAR_LENOVO_SEGUNDO_CEREBRO.bat`**

Ele abrirá um menu interativo com as opções:
* **[1] 🚀 Executar Robô Minerador:** Varre os cursos do Google Drive e cria as notas no Obsidian;
* **[2] 📁 Abrir a Pasta do Vault:** Abre os arquivos no Explorer;
* **[3] ☁️ Ponte Telegram -> Google Drive 5TB:** Dispara a fila de upload sem encher o disco;
* **[4] 🌐 Abrir Painel Visual HTML:** Abre o painel executivo com busca instantânea.

---

## ☁️ Passo 4: Como Funciona a Ponte Telegram -> Drive de 5TB (Zero Consumo de SSD)

Como o Lenovo tem um disco rígido finito, o script `scripts/ponte_telegram_para_drive.py` utiliza a estratégia **Move-on-Upload**:
1. Baixa 1 aula do canal do Telegram;
2. Envia imediatamente para a sua pasta `TELEGRAM_CURSOS_BACKUP_5TB` no Google Drive via `rclone`;
3. **Deleta imediatamente o arquivo temporário local** assim que o Drive confirma o recebimento;
4. Repete o ciclo para a próxima aula.

Dessa forma, você pode subir 500GB ou 2TB de cursos para a nuvem sem nunca estourar o armazenamento do seu PC Lenovo!
