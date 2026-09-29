// CYBERDEFENSE CORP — MESA DE OPERAÇÕES DE SOC N1
// Motor Interativo de Simulação de Expediente e Atendimento de Incidentes

// Sound Synthesizer via Web Audio API (Zero external dependencies)
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playTone(freq, type, duration, delay = 0) {
    setTimeout(() => {
        try {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = type;
            osc.frequency.value = freq;
            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        } catch (e) {}
    }, delay * 1000);
}

function soundAlertCritical() {
    playTone(880, 'sawtooth', 0.15, 0);
    playTone(440, 'sawtooth', 0.25, 0.15);
    playTone(880, 'sawtooth', 0.2, 0.4);
}

function soundChimeSuccess() {
    playTone(523.25, 'sine', 0.2, 0);
    playTone(659.25, 'sine', 0.2, 0.1);
    playTone(783.99, 'sine', 0.35, 0.2);
}

function soundClick() {
    playTone(400, 'triangle', 0.05);
}

// 6 INCIDENTES HIPER-REALISTAS DE UM DIA DE EXPEDIENTE (08:00 ÀS 17:00)
const INCIDENTES = [
    {
        id: "INC-1042",
        horaChegada: "08:30",
        horaTimestamp: 8 * 3600 + 30 * 60,
        titulo: "Alerta de Phishing: Setor Financeiro recebeu anexo 'comprovante_pagamento.pdf.exe'",
        severidade: "high",
        setor: "Financeiro / RH",
        origem: "Microsoft Defender for Office 365 + Alerta de Usuário",
        descricao: "A colaboradora Juliana (Analista Financeira) abriu um chamado urgente informando que recebeu um e-mail com remetente falso 'cobranca@fornecedor-oficial.com' solicitando a liquidação urgente de uma fatura com anexo duplo.",
        evidenciaLog: `[MAIL-GATEWAY-INSPECTION]
Date: 2026-09-29 08:28:14 UTC
From: cobranca@fornecedor-oficial.com.br (SPF: FAIL, DMARC: FAIL)
Sender IP: 185.220.101.45 (Tor Exit Node / Bulletproof Hosting)
Subject: URGENTE: Notificacao Extrajudicial de Debito e Fatura em Aberto
Attachment: comprovante_pagamento.pdf.exe
SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
Status: Email retido em quarentena. Terminal de Juliana isolado temporariamente para varredura.`,
        mitreSugerido: "T1566.001 - Phishing: Spearphishing Attachment",
        youtubeTake: "🎬 TAKE 1: 'Fala galera! Acabei de sentar na minha cadeira no SOC às 08:30 e já apitou o primeiro alerta do dia! O setor financeiro quase executou um malware com extensão dupla .pdf.exe. Vou mostrar na tela como analisar o cabeçalho SPF/DMARC e verificar o hash do arquivo no VirusTotal!'",
        parecerPadrao: "Incidente confirmado como tentativa de Spearphishing com anexo malicioso. O e-mail falhou nas verificações de SPF e DMARC. Hash e IP bloqueados no Gateway de E-mail e Firewall de borda. Terminal da colaboradora examinado sem persistência ativa.",
        status: "pendente"
    },
    {
        id: "INC-1043",
        horaChegada: "10:15",
        horaTimestamp: 10 * 3600 + 15 * 60,
        titulo: "Varredura Massiva de Portas (Port Scan) no Firewall de Borda MikroTik",
        severidade: "med",
        setor: "Infraestrutura de Rede",
        origem: "MikroTik RouterOS v7 - Syslog / Regra Filter",
        descricao: "O firewall de borda registrou múltiplos pacotes SYN em portas não abertas (21, 22, 23, 445, 3389, 8080) vindos de um único IP externo, caracterizando reconhecimento ativo de superfície de ataque.",
        evidenciaLog: `[MIKROTIK-FIREWALL-LOG]
Oct 02 10:14:02 BORDER-RB4011 firewall,info [PORT_SCAN_DROP] forward: in:ether1-WAN out:(unknown), src-mac 00:1a:2b:3c:4d:5e
proto=TCP, 194.26.29.112:48392 -> 200.189.45.10:22, len 60, SYN
proto=TCP, 194.26.29.112:48393 -> 200.189.45.10:23, len 60, SYN
proto=TCP, 194.26.29.112:48394 -> 200.189.45.10:445, len 60, SYN
proto=TCP, 194.26.29.112:48395 -> 200.189.45.10:3389, len 60, SYN
ACTION: Drop automatizado e adicionado a Address List 'Blacklist_Atacantes' por 24 horas.`,
        mitreSugerido: "T1046 - Network Service Discovery",
        youtubeTake: "🎬 TAKE 2: 'São 10:15 da manhã. O nosso firewall MikroTik acabou de barrar um Port Scan agressivo tentando achar portas SSH e RDP abertas na nossa WAN. Vou explicar como funciona o SYN scan do Nmap e como criamos a regra de tarpit e blacklist no RouterOS!'",
        parecerPadrao: "Varredura de reconhecimento externo mitigada com sucesso pelas regras de firewall de borda. IP de origem 194.26.29.112 incluído na blacklist temporária. Nenhuma porta sensível encontrava-se exposta.",
        status: "pendente"
    },
    {
        id: "INC-1044",
        horaChegada: "11:45",
        horaTimestamp: 11 * 3600 + 45 * 60,
        titulo: "Ataque de Força Bruta contra RDP / Servidor de Arquivos (Event ID 4625)",
        severidade: "crit",
        setor: "Servidores Windows / Active Directory",
        origem: "SIEM Wazuh - Regra 18152 (Windows Logon Failure)",
        descricao: "O agente Wazuh instalado no controlador de domínio disparou alerta crítico: mais de 450 tentativas falhas de login (Evento 4625) registradas em menos de 2 minutos contra a conta 'Administrator' e 'suporte'.",
        evidenciaLog: `[WAZUH-ALERT-ID 18152] - Level 12 (Critical)
Timestamp: 2026-09-29T11:43:21.104-0300
Agent: (002) - SRV-DC01.corp.local (192.168.10.5)
Rule: 18152 - Multiple Windows logon failures (Event ID 4625)
Log Data:
  Account Name: Administrator
  Failure Reason: Unknown user name or bad password
  Workstation Name: KALI-ATTACKER
  Source Network Address: 10.0.5.88 (Rede interna de VPN)
  Logon Type: 10 (RemoteInteractive - RDP)
Status: Conta alvo temporariamente bloqueada por política de Account Lockout.`,
        mitreSugerido: "T1110.001 - Brute Force: Password Guessing",
        youtubeTake: "🎬 TAKE 3: 'Galera, quase na hora do almoço (11:45) e apitou sirene vermelha no SIEM Wazuh! Um ataque de força bruta contra o nosso Servidor RDP com mais de 400 tentativas de senha. O mais alarmante: o IP de origem veio de dentro da VPN! Vamos isolar a sessão desse usuário agora!'",
        parecerPadrao: "Tentativa de Password Guessing detectada pelo SIEM Wazuh contra o SRV-DC01. Túnel VPN do IP 10.0.5.88 revogado preventivamente. Conta de rede submetida a troca forçada de credencial e habilitação mandatória de MFA.",
        status: "pendente"
    },
    {
        id: "INC-1045",
        horaChegada: "14:10",
        horaTimestamp: 14 * 3600 + 10 * 60,
        titulo: "Auditoria GRC: Solicitação de Acesso Administrativo (Domain Admins)",
        severidade: "low",
        setor: "Governança & Acessos (IAM)",
        origem: "ServiceDesk TI - Chamado #8821",
        descricao: "O desenvolvedor Pedro solicitou entrada no grupo 'Domain Admins' para instalar uma biblioteca no servidor de homologação.",
        evidenciaLog: `[IAM-REQUEST-TICKET-8821]
Requisitante: Pedro Santos (Dev Backend Júnior)
Grupo Requisitado: CN=Domain Admins,CN=Users,DC=corp,DC=local
Justificativa: "Preciso de permissão total para rodar um instalador de banco de dados no servidor."
Parecer de Compliance (ISO 27001 / Princípio do Menor Privilégio):
Acesso de Domain Admin viola a política de segregação de funções. Instalação em homologação deve ser feita via credencial local de máquina ou esteira de automação.`,
        mitreSugerido: "T1078 - Valid Accounts",
        youtubeTake: "🎬 TAKE 4: 'Voltando do almoço às 14h! Nem só de hacker vive o SOC: agora estamos analisando um chamado de Governança e Controle de Acessos. Um dev pediu acesso de Administrador de Domínio para instalar um programa. Vou mostrar como negar com educação e aplicar o Princípio do Menor Privilégio (ISO 27001)!'",
        parecerPadrao: "Solicitação de Domain Admin indeferida com base no Princípio do Menor Privilégio e ISO 27001. Concedido acesso de Administrador Local estritamente na VM de homologação com log de auditoria ativo.",
        status: "pendente"
    },
    {
        id: "INC-1046",
        horaChegada: "15:40",
        horaTimestamp: 15 * 3600 + 40 * 60,
        titulo: "Comunicação C2 / Tráfego Anômalo de DNS Tunneling",
        severidade: "crit",
        setor: "Rede Corporativa / Endpoint",
        origem: "Suricata IDS + Zeek Network Monitor",
        descricao: "O sensor de rede detectou centenas de consultas DNS para subdomínios gigantescos no formato 'data.a8f7c9e.attacker-c2.net', caracterizando exfiltração oculta de dados ou comando e controle via protocolo DNS.",
        evidenciaLog: `[SURICATA-ALERT] [1:2024881:3] ET MALWARE Suspicious High-Volume Base64 DNS Queries (DNS Tunneling / Cobalt Strike C2)
Timestamp: 2026-09-29 15:38:09.442
SrcIP: 192.168.10.42 (Estação de Trabalho - Setor Jurídico)
DstIP: 8.8.8.8:53 (Google DNS)
Query: aW52ZW50YXJpby1jb25maWRlbmNpYWwtMjAyNg==.c2-exfil.xyz
Query Length: 112 bytes (Extremamente anômalo para requisição DNS A)
Volume: 1.400 requisições por minuto com entropia elevada.`,
        mitreSugerido: "T1071.004 - Application Layer Protocol: DNS",
        youtubeTake: "🎬 TAKE 5: 'São 15:40 e pegamos o caso mais avançado do dia: DNS Tunneling! Um malware no setor jurídico está fatiando arquivos confidenciais em base64 e enviando disfarçados dentro de perguntas DNS para um servidor hacker. Vou mostrar a análise de tráfego no Wireshark e como conter esse host!'",
        parecerPadrao: "Confirmada atividade de C2 via DNS Tunneling no host 192.168.10.42. Host isolado na VLAN de quarentena. Domínio malicioso inserido no sinkhole do DNS interno. Coleta de memória RAM iniciada para análise forense.",
        status: "pendente"
    },
    {
        id: "INC-1047",
        horaChegada: "16:45",
        horaTimestamp: 16 * 3600 + 45 * 60,
        titulo: "Fechamento de Plantão & Relatório de Passagem de Turno (Shift Handover)",
        severidade: "low",
        setor: "SOC Operacional",
        origem: "Procedimento Padrão N1 -> N2",
        descricao: "Consolidação de todos os chamados atendidos, alertas contidos, endereços IP bloqueados e status dos ativos para o time do turno noturno.",
        evidenciaLog: `[SOC-SHIFT-CLOSING-CHECKLIST]
Expediente: 08:00 - 17:00
Incidentes Processados: 5
Incidentes Críticos Contidos: 2 (Brute Force RDP + DNS Tunneling C2)
Bloqueios Realizados: 2 IPs em Firewall, 1 Domínio em Sinkhole, 1 Quarentena de Host.
Status da Infraestrutura: Estável. Sem alertas pendentes de resolução imediata.`,
        mitreSugerido: "Procedimento Operacional Padronizado (SOP)",
        youtubeTake: "🎬 TAKE 6: '16:45 da tarde, final de expediente! Agora é hora de bater o ponto e gerar o Relatório de Passagem de Turno para o time da noite. Um dia intenso com 5 incidentes reais resolvidos. Esse relatório vai direto para o meu portfólio no LinkedIn!'",
        parecerPadrao: "Turno diurno encerrado com 100% dos incidentes triados e contidos. Relatório oficial exportado e repassado para o plantonista do turno noturno.",
        status: "pendente"
    }
];

// STATE
let currentSeconds = 8 * 3600; // 08:00:00
let speedMultiplier = 1; // 1x or 10x
let activeTicketId = null;
let resolvedCount = 0;

// ELEMENTS
const clockEl = document.getElementById("shiftClock");
const btnSpeed = document.getElementById("btnSpeed");
const ticketListEl = document.getElementById("ticketList");
const ticketDetailEl = document.getElementById("ticketDetail");
const shiftProgressFill = document.getElementById("shiftProgressFill");
const shiftPercentEl = document.getElementById("shiftPercent");
const creatorTipEl = document.getElementById("creatorTip");
const critCountEl = document.getElementById("critCount");
const highCountEl = document.getElementById("highCount");
const medCountEl = document.getElementById("medCount");
const doneCountEl = document.getElementById("doneCount");
const btnExportReport = document.getElementById("btnExportReport");
const reportModal = document.getElementById("reportModal");
const reportText = document.getElementById("reportText");
const btnCloseModal = document.getElementById("btnCloseModal");
const btnCopyReport = document.getElementById("btnCopyReport");

// FORMAT TIME
function formatTime(totalSec) {
    const h = String(Math.floor(totalSec / 3600)).padStart(2, '0');
    const m = String(Math.floor((totalSec % 3600) / 60)).padStart(2, '0');
    const s = String(totalSec % 60).padStart(2, '0');
    return `${h}:${m}:${s}`;
}

// UPDATE CLOCK & SHIFT PROGRESS
function tick() {
    currentSeconds += 1;
    if (currentSeconds > 17 * 3600) {
        currentSeconds = 17 * 3600;
    }
    
    clockEl.innerText = formatTime(currentSeconds);
    
    // Progress calculation (08:00 is 0%, 17:00 is 100%)
    const elapsed = Math.max(0, currentSeconds - 8 * 3600);
    const total = 9 * 3600;
    const pct = Math.min(100, Math.floor((elapsed / total) * 100));
    
    shiftProgressFill.style.width = `${pct}%`;
    shiftPercentEl.innerText = `${pct}%`;
    
    // Check if new tickets arrived
    INCIDENTES.forEach(inc => {
        if (!inc.notificado && currentSeconds >= inc.horaTimestamp) {
            inc.notificado = true;
            if (inc.severidade === 'crit' || inc.severidade === 'high') {
                soundAlertCritical();
            } else {
                playTone(600, 'sine', 0.1);
            }
            renderTicketList();
        }
    });
}

setInterval(() => {
    for (let i = 0; i < speedMultiplier; i++) {
        tick();
    }
}, 1000);

// SPEED TOGGLE
btnSpeed.addEventListener("click", () => {
    if (speedMultiplier === 1) {
        speedMultiplier = 10;
        btnSpeed.innerText = "⏩ 10x Ativado";
        btnSpeed.style.background = "rgba(0, 210, 255, 0.2)";
    } else {
        speedMultiplier = 1;
        btnSpeed.innerText = "⏩ 1x Normal";
        btnSpeed.style.background = "";
    }
});

// RENDER TICKET LIST
function renderTicketList() {
    ticketListEl.innerHTML = "";
    
    let crit = 0, high = 0, med = 0, done = 0;
    
    INCIDENTES.forEach(inc => {
        const disponivel = currentSeconds >= inc.horaTimestamp;
        if (!disponivel) return; // Só exibe se a hora já chegou no relógio
        
        if (inc.status === "resolvido") done++;
        else if (inc.severidade === "crit") crit++;
        else if (inc.severidade === "high") high++;
        else if (inc.severidade === "med") med++;
        
        const card = document.createElement("div");
        card.className = `ticket-card ${activeTicketId === inc.id ? 'active' : ''} ${inc.status === 'resolvido' ? 'status-done' : ''}`;
        card.innerHTML = `
            <div class="ticket-top">
                <span class="ticket-id">${inc.id}</span>
                <span class="ticket-severity sev-${inc.severidade}">${inc.severidade.toUpperCase()}</span>
            </div>
            <div class="ticket-title">${inc.titulo}</div>
            <div class="ticket-meta">
                <span>🕒 ${inc.horaChegada} • ${inc.setor}</span>
                <span>${inc.status === 'resolvido' ? '✅ Resolvido' : '⚠️ Pendente'}</span>
            </div>
        `;
        
        card.addEventListener("click", () => {
            selectTicket(inc.id);
        });
        
        ticketListEl.appendChild(card);
    });
    
    critCountEl.innerText = `${crit} Críticos`;
    highCountEl.innerText = `${high} Altos`;
    medCountEl.innerText = `${med} Médio`;
    doneCountEl.innerText = `${done} Resolvidos`;
}

// SELECT TICKET
function selectTicket(id) {
    activeTicketId = id;
    soundClick();
    renderTicketList();
    
    const inc = INCIDENTES.find(i => i.id === id);
    if (!inc) return;
    
    // Update YouTube Tip box
    creatorTipEl.innerHTML = `<p>${inc.youtubeTake}</p>`;
    
    // Render Detail
    ticketDetailEl.innerHTML = `
        <div class="detail-header">
            <div class="detail-badges">
                <span class="ticket-id">${inc.id}</span>
                <span class="ticket-severity sev-${inc.severidade}">${inc.severidade.toUpperCase()}</span>
                <span class="counter-badge med">Setor: ${inc.setor}</span>
                <span class="counter-badge high">Origem: ${inc.origem}</span>
            </div>
            <h3 style="margin-top: 10px;">${inc.titulo}</h3>
        </div>

        <div class="detail-section">
            <h4>📋 Descrição do Chamado</h4>
            <p>${inc.descricao}</p>
        </div>

        <div class="detail-section">
            <h4>🔍 Evidência Técnica & Raw Logs (SIEM / Firewall)</h4>
            <div class="log-terminal">${inc.evidenciaLog}</div>
        </div>

        <div class="detail-section">
            <h4>🏷️ Mapeamento de Táticas & Técnicas (MITRE ATT&CK)</h4>
            <select class="mitre-select" id="selectMitre">
                <option value="${inc.mitreSugerido}">Sugerido: ${inc.mitreSugerido}</option>
                <option value="T1566 - Phishing">T1566 - Phishing</option>
                <option value="T1046 - Network Service Discovery">T1046 - Network Service Discovery</option>
                <option value="T1110 - Brute Force">T1110 - Brute Force</option>
                <option value="T1078 - Valid Accounts">T1078 - Valid Accounts</option>
                <option value="T1071 - Application Layer Protocol">T1071 - Application Layer Protocol</option>
                <option value="T1059 - Command and Scripting Interpreter">T1059 - Command and Scripting Interpreter</option>
            </select>
        </div>

        <div class="detail-section">
            <h4>✍️ Seu Parecer Técnico de Resolução (Como Analista SOC N1)</h4>
            <textarea class="parecer-input" id="inputParecer" placeholder="Descreva as medidas tomadas (ex: bloqueio de IP, contenção de host, quarentena de arquivo)...">${inc.meuParecer || inc.parecerPadrao}</textarea>
        </div>

        <div style="display: flex; gap: 12px; margin-top: 10px;">
            <button class="btn-resolve" id="btnResolve">
                ${inc.status === 'resolvido' ? '✅ Chamado Já Concluído (Atualizar)' : '🎯 Concluir & Mitigar Incidente'}
            </button>
        </div>
    `;
    
    document.getElementById("btnResolve").addEventListener("click", () => {
        inc.status = "resolvido";
        inc.meuParecer = document.getElementById("inputParecer").value;
        inc.mitreEscolhido = document.getElementById("selectMitre").value;
        soundChimeSuccess();
        renderTicketList();
        selectTicket(inc.id);
    });
}

// GENERATE OFFICIAL SHIFT REPORT (LINKEDIN / PORTFOLIO)
btnExportReport.addEventListener("click", () => {
    soundClick();
    
    let text = `# 🛡️ RELATÓRIO DE PASSAGEM DE TURNO — SOC N1 (SHIFT HANDOVER)\n`;
    text += `Empresa: CYBERDEFENSE CORP • Global Operations\n`;
    text += `Operador: Matheus (Analista de Segurança Júnior / SOC N1)\n`;
    text += `Data: 29/09/2026 | Horário: 08:00 às 17:00\n\n`;
    text += `=================================================================\n`;
    text += `RESUMO OPERACIONAL DO PLANTÃO:\n`;
    text += `Total de Incidentes Triados: ${INCIDENTES.filter(i => i.status === 'resolvido').length} de ${INCIDENTES.length}\n`;
    text += `Status Geral da Infraestrutura: Protegida e Monitorada\n`;
    text += `=================================================================\n\n`;
    
    INCIDENTES.forEach((inc, idx) => {
        text += `[CASO #${idx+1}] ${inc.id} — ${inc.titulo}\n`;
        text += `• Horário: ${inc.horaChegada} | Severidade: ${inc.severidade.toUpperCase()}\n`;
        text += `• Setor Acometido: ${inc.setor}\n`;
        text += `• MITRE ATT&CK: ${inc.mitreEscolhido || inc.mitreSugerido}\n`;
        text += `• Parecer Técnico do Analista: ${inc.meuParecer || inc.parecerPadrao}\n`;
        text += `• Status: ${inc.status === 'resolvido' ? 'RESOLVIDO E MITIGADO' : 'EM ANÁLISE'}\n\n`;
    });
    
    text += `Relatório gerado automaticamente pela Mesa de Operações de SOC N1.\n`;
    text += `Portfólio Prático de Cibersegurança & Resposta a Incidentes.`;
    
    reportText.value = text;
    reportModal.classList.add("open");
});

btnCloseModal.addEventListener("click", () => {
    reportModal.classList.remove("open");
});

btnCopyReport.addEventListener("click", () => {
    reportText.select();
    document.execCommand("copy");
    btnCopyReport.innerText = "✅ Copiado com Sucesso!";
    setTimeout(() => {
        btnCopyReport.innerText = "📋 Copiar Relatório Completo";
    }, 2000);
});

// START
renderTicketList();
// Auto select first ticket
selectTicket("INC-1042");
