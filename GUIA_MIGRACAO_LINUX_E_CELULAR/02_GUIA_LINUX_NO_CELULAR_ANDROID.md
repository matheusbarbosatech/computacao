# GUIA COMPLETO: LINUX E CIBERSEGURANÇA NO CELULAR ANDROID
> **Repositório:** Computação & Cibersegurança  
> **Autor:** Matheus Barbosa  
> **Objetivo:** Como rodar Linux puro ou ferramentas de cibersegurança/hacking direto no smartphone Android (com ou sem root).

---

## 📱 1. O Android já é Linux?
Sim! O Android utiliza o **Kernel Linux** como núcleo de sistema operacional. No entanto, o Google e as fabricantes (Samsung, Xiaomi, Motorola) colocam uma máquina virtual (ART) e camadas pesadas proprietárias por cima, escondendo o poder real do sistema.

Existem duas formas principais de usar Linux no celular:
1. **Nível 1 (Sem Root / Fácil e Seguro):** Rodar um ambiente Linux completo em espaço de usuário (Termux ou Andronix) sem alterar o sistema do celular.
2. **Nível 2 (Avançado / Modificação):** Instalar o **Kali NetHunter** ou substituir o Android por **Ubuntu Touch / postmarketOS**.

---

## 🚀 2. Opção 1: Termux (O Terminal Linux Completo no Celular - Sem Root)
O **Termux** é a ferramenta número 1 de qualquer estudante ou profissional de segurança no Android. Ele não precisa de root e oferece um terminal Linux completo com o gerenciador de pacotes `pkg` / `apt`.

### Como Instalar Corretamente:
> ⚠️ **Aviso:** Nunca baixe o Termux pela Google Play Store (a versão de lá foi abandonada e dá erro de repositório).

1. Baixe a versão atualizada pelo **[F-Droid](https://f-droid.org/packages/com.termux/)** ou direto pelo **GitHub oficial**: [termux/termux-app](https://github.com/termux/termux-app/releases).
2. Abra o Termux e digite os primeiros comandos de atualização:
```bash
pkg update && pkg upgrade -y
termux-setup-storage
```
*(Confirme a permissão de acesso aos arquivos para o Termux acessar seus downloads do celular).*

### O que você pode rodar no celular pelo Termux:
* **Python 3:** `pkg install python`
* **Git:** `pkg install git`
* **Nmap (Varredura de redes):** `pkg install nmap`
* **Metasploit Framework:** É possível instalar o Metasploit completo no Termux para testes de intrusão móveis.
* **Servidor Web / SSH:** Você pode subir um servidor local em Python ou Node.js que roda na bateria do seu celular!

---

## 🛡️ 3. Opção 2: Kali NetHunter (A Suíte de Ataque Oficial da Offensive Security)
O **Kali NetHunter** é a plataforma de teste de penetração oficial do Kali Linux feita para dispositivos Android.

### Níveis do NetHunter:
1. **NetHunter Rootless (Sem Root):**
   * Instala o Kali Linux dentro do Termux com suporte a interface gráfica via VNC (você abre a área de trabalho do Kali na tela do celular como um aplicativo!).
   * Comandos de instalação no Termux:
     ```bash
     pkg install wget
     wget -O install-nethunter-termux https://offs.ec/2MceZWr
     chmod +x install-nethunter-termux
     ./install-nethunter-termux
     ```
   * Para abrir a linha de comando do Kali: `nethunter`
   * Para abrir a interface visual: `nh kex &` e conecte pelo aplicativo **NetHunter Kex** na Play Store.

2. **NetHunter Completo (Com Root / Kernel Customizado):**
   * Exige desbloqueio de Bootloader e Root (Magisk).
   * **Superpoderes:**
     * **BadUSB Attack:** O celular finge ser um teclado USB conectado ao PC e digita comandos automáticos de invasão em 2 segundos.
     * **Injeção de Pacotes Wi-Fi:** Usando uma placa Wi-Fi externa com cabo OTG para capturar handshakes WPA2.
     * **HID Attacks e Evil AP:** Criação de pontos de acesso falsos.

---

## 🖥️ 4. Opção 3: Substituir o Android por Linux Puro (Ubuntu Touch / postmarketOS)
Se você tem um celular secundário parado e quer transformá-lo num computador Linux de verdade:

### A. [Ubuntu Touch (UBports)](https://ubuntu-touch.io/)
* O sistema operacional da Canonical adaptado pela comunidade para smartphones.
* **Destaque:** Tem suporte a **Convergência**. Se você plugar um hub USB-C com HDMI, monitor, teclado e mouse no celular, ele vira um desktop Ubuntu de verdade!
* **Aparelhos suportados:** Google Pixel 3a, OnePlus One/3/5, Xiaomi Redmi Note 7/8/9, PinePhone, Volla Phone.

### B. [postmarketOS](https://postmarketos.org/)
* Baseado em Alpine Linux (super leve).
* Feito para dar 10 anos de vida a celulares antigos que foram abandonados pelos fabricantes sem atualizações.
* Oferece interfaces gráficas como Phosh (baseada no GNOME) ou Plasma Mobile (KDE).

---

## 📌 5. Resumo e Próximos Passos
1. **Para o dia a dia:** Mantenha o seu Android normal e instale o **Termux** (pelo F-Droid) + **Kali NetHunter Rootless**. Você terá todo o poder do Linux e ferramentas de hacking no bolso sem perder a estabilidade, a câmera e os apps de banco do celular.
2. **Para um celular secundário de testes:** Instale o **Ubuntu Touch** ou **NetHunter Root** para transformar o aparelho num canivete suíço portátil de pentest!
