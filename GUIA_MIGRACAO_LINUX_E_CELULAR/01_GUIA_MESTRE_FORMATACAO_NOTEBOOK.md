# GUIA MESTRE DE MIGRAÇÃO: WINDOWS PARA LINUX MINT XFCE
> **Repositório:** Computação & Cibersegurança  
> **Autor:** Matheus Barbosa  
> **Objetivo:** Guia definitivo para formatar, instalar do zero e configurar notebooks antigos/fracos (ex: Acer Aspire E1-571 / i5 / 6GB RAM) com foco em Cibersegurança, Antigravity IDE e Jogos Retrô/Clássicos sem Steam.

---

## 🖥️ 1. Contexto e Especificações do Hardware de Referência
* **Modelo:** Notebook Acer Aspire E1-571
* **Processador:** Intel Core i5-3230M @ 2.60 GHz (2 núcleos / 4 threads)
* **Placa de Vídeo:** Intel HD Graphics 4000 (integrada)
* **Placa Wi-Fi:** Qualcomm Atheros AR5B97 (driver `ath9k` nativo, suporte a monitor mode e injeção de pacotes)
* **Memória RAM:** 6 GB DDR3
* **Armazenamento:** Disco rígido de 500 GB (partição limpa em ext4)
* **Sistema Escolhido:** Linux Mint 22 (Edição XFCE de 64 bits)

---

## 💾 2. Passo a Passo: Criação do Pen Drive Bootável (Rufus)
1. Conecte um Pen Drive de no mínimo 4 GB ou 8 GB.
2. Baixe a ISO oficial do **Linux Mint XFCE** pelo site oficial (espelhos do Brasil como C3SL/UFPR).
3. Abra o **Rufus**:
   * **Dispositivo:** Escolha o Pen Drive.
   * **Seleção de boot:** Selecione a ISO baixada.
   * **Esquema de partição:** Selecione **MBR** (compatibilidade total com BIOS Legacy e UEFI).
   * **Sistema de destino:** BIOS (ou UEFI-CSM).
   * Clique em **INICIAR** em modo ISO. Aguarde a mensagem "Pronto".

---

## ⚙️ 3. O Truque da BIOS do Notebook Acer (Habilitar Tecla F12)
1. Ligue o notebook apertando **F2** repetidamente para entrar na BIOS.
2. Com as setas do teclado, vá até a aba **Main**.
3. Localize **F12 Boot Menu** e mude de `Disabled` para `Enabled`.
4. Pressione **F10**, confirme com *Yes* e aperte Enter para reiniciar.

---

## 🚀 4. Instalação Limpa ("Padrão de Fábrica")
1. Com o notebook reiniciando e o pen drive plugado, aperte **F12** repetidamente.
2. Escolha o **Pen Drive USB** na lista de inicialização.
3. Clique em **Start Linux Mint** (o sistema abrirá em modo Live para testes).
4. Na área de trabalho, clique duas vezes no ícone **"Install Linux Mint"**:
   * Idioma: *Português do Brasil*.
   * Teclado: *Português (Brasil)*.
   * Codecs: Marque *"Instalar codecs multimídia"*.
   * **Tipo de Instalação:** Escolha **"Apagar o disco e instalar o Linux Mint"** *(Zera o HD, remove o Windows por completo e deixa zerado de fábrica)*.
   * Crie seu usuário, nome da máquina e senha.
5. Ao concluir, clique em **Reiniciar Agora**, retire o pen drive e pressione Enter.

---

## 🛠️ 5. Pós-Instalação: O Script `instalar_tudo.sh`
Abra o terminal no Linux Mint e execute:
```bash
bash instalar_tudo.sh
```
O script instala e configura automaticamente:
* **Navegador:** Brave Browser (bloqueio nativo de anúncios) + Chrome.
* **Produtividade:** Telegram Desktop, Obsidian (segundo cérebro), Python 3, Git, venv.
* **Cibersegurança / Pentest:** Nmap, Wireshark, Metasploit, Aircrack-ng, John, Hydra, Sqlmap, Hashcat, Binwalk.
* **Virtualização:** KVM / QEMU / Virt-Manager (para rodar Kali Linux leve consumindo metade da RAM do VMware).
* **Jogos (Sem Steam):** Wine (32 bits), Lutris, RetroArch, PPSSPP (GTA San Andreas e CS 1.6 a 100 FPS).
* **Utilitários:** Flameshot (captura de tela), VLC, BleachBit (limpeza), `tldr` (manual rápido de comandos).
* **Otimização:** Ajuste de kernel `vm.swappiness=10` para priorizar a RAM de 6 GB e não forçar o disco.

---

## 📱 6. Prompt Mestre para o Gemini (No Celular)
Copie o prompt abaixo e cole no Gemini do celular para ter um guia passo a passo em tempo real durante a instalação:

```markdown
Olá, Gemini! Você será meu arquiteto de sistemas e guia pessoal durante a configuração do meu novo sistema operacional Linux Mint XFCE, que acabei de formatar e instalar do zero (padrão de fábrica).

Contexto da Máquina:
- Modelo: Notebook Acer Aspire E1-571 (Intel Core i5-3230M, Intel HD Graphics 4000, 6 GB de RAM, 500 GB de disco).
- Placa Wi-Fi: Qualcomm Atheros AR5B97 (driver ath9k nativo).
- Sistema: Linux Mint 22 (Edição XFCE de 64 bits).

Meus Objetivos:
1. Cibersegurança e Hacking: Ferramentas nativas no sistema e uma máquina virtual isolada do Kali Linux configurada no Virt-Manager / KVM (economizando RAM).
2. Desenvolvimento: Trabalho com Python 3 e agentes de IA usando o Antigravity IDE (não uso VS Code).
3. Navegador: Exclusivamente Brave Browser.
4. Jogos (Sem Steam): GTA San Andreas e CS 1.6 via Wine a 100 FPS, RetroArch, PPSSPP e PokeMMO.
5. Backup no Telegram: Tenho meus códigos em Python, repositórios e livros salvos em 4 zips no Telegram, além do script instalar_tudo.sh.

Regras de Resposta:
- Conduza estritamente PASSO A PASSO.
- Envie apenas UM comando por vez para colar no terminal.
- Aguarde minha confirmação de sucesso antes de enviar a etapa seguinte.

Estou na área de trabalho recém-instalada do Linux Mint XFCE. Qual é o primeiro passo que devemos fazer?
```
