#!/bin/bash
# ==============================================================================
# SCRIPT DE PÓS-INSTALAÇÃO E OTIMIZAÇÃO - LINUX MINT XFCE
# Usuário: Matheus (Acer Aspire E1-571 / Intel i5 / Intel HD 4000 / 6GB RAM)
# Foco: Cibersegurança/Hacking + Antigravity + Jogos Clássicos/Retrô (Sem Steam)
# ==============================================================================

set -e

# Cores para o terminal
VERDE='\033[0;32m'
AZUL='\033[0;34m'
AMARELO='\033[1;33m'
RESET='\033[0m'

echo -e "${AZUL}================================================================${RESET}"
echo -e "${VERDE}  INICIANDO A CONFIGURAÇÃO MESTRE DO SEU LINUX MINT XFCE 🚀     ${RESET}"
echo -e "${AZUL}================================================================${RESET}"

# 1. Atualizar repositórios e pacotes do sistema
echo -e "\n${AMARELO}[1/9] Atualizando o sistema operacional...${RESET}"
sudo apt update && sudo apt upgrade -y

# 2. Utilitários essenciais do sistema e comunidade Linux
echo -e "\n${AMARELO}[2/9] Instalando utilitários essenciais (Flameshot, VLC, BleachBit, etc.)...${RESET}"
sudo apt install -y curl wget git build-essential software-properties-common \
    htop neofetch p7zip-full unrar unzip flameshot vlc bleachbit tldr \
    zsh default-jre

# 3. Ambiente de Desenvolvimento e IA (Python 3, Git)
echo -e "\n${AMARELO}[3/9] Configurando Python 3, ambientes virtuais e Git...${RESET}"
sudo apt install -y python3 python3-pip python3-venv python3-dev

# 4. Ferramentas Nativas de Cibersegurança / Pentest
echo -e "\n${AMARELO}[4/9] Instalando arsenal de Cibersegurança e Hacking...${RESET}"
sudo apt install -y nmap wireshark tshark tcpdump aircrack-ng john hydra \
    sqlmap whois netcat-openbsd traceroute nikto binwalk hashcat

# Permitir captura de pacotes pelo Wireshark sem precisar rodar como root
sudo usermod -aG wireshark $USER || true

# 5. Virtualização Leve (KVM / QEMU / Virt-Manager para o Kali Linux)
echo -e "\n${AMARELO}[5/9] Configurando KVM / QEMU (Virtualização direta no Kernel para o Kali)...${RESET}"
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager
sudo usermod -aG libvirt $USER
sudo usermod -aG kvm $USER

# 6. Navegadores (Brave Browser focado em privacidade + Google Chrome)
echo -e "\n${AMARELO}[6/9] Instalando Navegadores (Brave sem anúncios + Google Chrome)...${RESET}"
# Brave Browser
sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list
sudo apt update
sudo apt install -y brave-browser

# Google Chrome
if ! command -v google-chrome &> /dev/null; then
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/chrome.deb
    sudo apt install -y /tmp/chrome.deb
    rm /tmp/chrome.deb
fi

# 7. Produtividade (Telegram Desktop e Obsidian)
echo -e "\n${AMARELO}[7/9] Instalando Telegram Desktop e Obsidian...${RESET}"
sudo apt install -y telegram-desktop

# Configuração Flatpak para Obsidian
if ! command -v flatpak &> /dev/null; then
    sudo apt install -y flatpak
fi
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install -y flathub md.obsidian.Obsidian

# 8. Jogos Clássicos e Retrô (Sem Steam - Wine, Lutris, RetroArch, PPSSPP)
echo -e "\n${AMARELO}[8/9] Configurando Wine/Lutris (para GTA San Andreas e CS 1.6) e Emuladores...${RESET}"
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install -y wine wine32 wine64 winetricks lutris retroarch ppsspp

# 9. Limpeza final e otimização de Swap
echo -e "\n${AMARELO}[9/9] Otimizando uso de memória RAM (Swappiness = 10)...${RESET}"
# Reduz o uso do disco para troca, mantendo o máximo possível na RAM de 6GB
if ! grep -q "vm.swappiness=10" /etc/sysctl.conf; then
    echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
    sudo sysctl -p
fi

sudo apt autoremove -y

echo -e "\n${VERDE}================================================================${RESET}"
echo -e "${VERDE}  🎉 INSTALAÇÃO E OTIMIZAÇÃO CONCLUÍDAS COM SUCESSO!            ${RESET}"
echo -e "${VERDE}================================================================${RESET}"
echo -e "O que já está pronto para uso:"
echo -e " • ${AZUL}Hacking/Pentest:${RESET} Nmap, Wireshark, Aircrack, John, Hydra, Sqlmap, Virt-Manager (KVM)"
echo -e " • ${AZUL}Navegadores:${RESET} Brave (sem anúncios) e Google Chrome"
echo -e " • ${AZUL}Produtividade:${RESET} Telegram Desktop, Obsidian, Python 3, Git"
echo -e " • ${AZUL}Jogos:${RESET} RetroArch, PPSSPP, Wine e Lutris (GTA SA e CS 1.6 prontos para rodar)"
echo -e " • ${AZUL}Leitor PDF Nativo:${RESET} Xreader (já instalado e ultraleve)"
echo -e " • ${AZUL}Captura de Tela:${RESET} Flameshot"
echo -e ""
echo -e "${AMARELO}Próximo passo:${RESET}"
echo -e "1. Baixe o Antigravity IDE (pacote .deb ou AppImage) para seu editor de código e IA."
echo -e "2. Extraia seus arquivos do Telegram para suas pastas de trabalho."
