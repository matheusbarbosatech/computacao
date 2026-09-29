// ==========================================================================
// CYBERDEFENSE 3D — FILA DE INCIDENTES DO SIEM & RESPOSTA TÉCNICA
// ==========================================================================

const INCIDENT_QUEUE = [
    {
        id: "INC-1042",
        horaDisparo: "08:30",
        horaSegundos: 8 * 3600 + 30 * 60,
        titulo: "Spearphishing com executável oculto: comprovante_pagamento.pdf.exe",
        severidade: "high",
        setor: "Financeiro",
        origem: "Defender for Office 365 + Usuário",
        descricao: "Juliana abriu chamado informando tentativa de cobrança com duplo executável. IP remetente ligado a rede Tor.",
        log: `[GATEWAY-MAIL-FILTER]
Date: 2026-09-29 08:28:14 UTC
From: cobranca@fornecedor-oficial.com.br (SPF: FAIL, DMARC: FAIL)
Sender IP: 185.220.101.45 (Tor Exit Node)
Subject: URGENTE: Notificação Extrajudicial de Débito
Attachment: comprovante_pagamento.pdf.exe
SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
Action: Mensagem retida na quarentena.`,
        mitre: "T1566.001 - Phishing: Spearphishing Attachment",
        status: "pendente",
        resolvido: false
    },
    {
        id: "INC-1043",
        horaDisparo: "10:15",
        horaSegundos: 10 * 3600 + 15 * 60,
        titulo: "Varredura Massiva de Portas (SYN Port Scan) no Firewall MikroTik",
        severidade: "med",
        setor: "Borda de Rede",
        origem: "MikroTik RouterOS v7 - Syslog",
        descricao: "Múltiplos pacotes TCP SYN em portas altas e sensíveis (22, 23, 445, 3389) vindos de IP suspeito.",
        log: `[FIREWALL-BORDER-RB4011]
Time: Oct 02 10:14:02
Rule: PORT_SCAN_DETECTED -> Action: Drop
Source: 194.26.29.112 -> Dest: 200.189.45.10 (Portas: 22, 23, 445, 3389)
Status: IP temporariamente bloqueado na address-list por 24h.`,
        mitre: "T1046 - Network Service Discovery",
        status: "pendente",
        resolvido: false
    },
    {
        id: "INC-1044",
        horaDisparo: "11:45",
        horaSegundos: 11 * 3600 + 45 * 60,
        titulo: "Ataque de Força Bruta contra RDP do Servidor de Arquivos (Event 4625)",
        severidade: "crit",
        setor: "Active Directory / Servidores",
        origem: "SIEM Wazuh - Regra 18152",
        descricao: "Mais de 450 tentativas falhas de login RDP contra o usuário 'Administrator' em menos de 2 minutos.",
        log: `[WAZUH-ALERT-ID 18152] - Level 12 (Critical)
Timestamp: 2026-09-29T11:43:21
Agent: SRV-DC01.corp.local (192.168.10.5)
Account Name: Administrator
Logon Type: 10 (RemoteInteractive - RDP)
Source Network Address: 10.0.5.88 (Túnel VPN Interno)
Action Required: Revogar sessão VPN imediatamente.`,
        mitre: "T1110.001 - Brute Force: Password Guessing",
        status: "pendente",
        resolvido: false
    },
    {
        id: "INC-1045",
        horaDisparo: "14:10",
        horaSegundos: 14 * 3600 + 10 * 60,
        titulo: "Auditoria GRC: Solicitação de Acesso Administrativo (Domain Admins)",
        severidade: "low",
        setor: "Governança / IAM",
        origem: "ServiceDesk TI - Chamado #8821",
        descricao: "Desenvolvedor Pedro pediu privilégio de Domain Admin para rodar instalador de homologação.",
        log: `[IAM-AUDIT-TICKET-8821]
Requisitante: Pedro Santos (Dev Backend)
Grupo Alvo: Domain Admins
Justificativa: "Preciso de permissão total para rodar script no servidor."
Regra ISO 27001 / Menor Privilégio: Acesso a Domain Admin deve ser NEGADO.`,
        mitre: "T1078 - Valid Accounts",
        status: "pendente",
        resolvido: false
    },
    {
        id: "INC-1046",
        horaDisparo: "15:40",
        horaSegundos: 15 * 3600 + 40 * 60,
        titulo: "Exfiltração de Dados / Comunicação C2 via DNS Tunneling",
        severidade: "crit",
        setor: "Estação Jurídico",
        origem: "Suricata IDS + Zeek",
        descricao: "Consultas DNS anômalas de 112 bytes em base64 direcionadas a domínio malicioso externo.",
        log: `[SURICATA-ALERT] [1:2024881:3] MALWARE High-Entropy Base64 DNS Queries (Cobalt Strike C2)
Timestamp: 2026-09-29 15:38:09
Host: 192.168.10.42 (Setor Jurídico)
Query: aW52ZW50YXJpby1jb25maWRlbmNpYWw==.c2-exfil.xyz
Action: Isolamento de porta no switch e sinkhole DNS.`,
        mitre: "T1071.004 - Application Protocol: DNS",
        status: "pendente",
        resolvido: false
    },
    {
        id: "INC-1047",
        horaDisparo: "16:45",
        horaSegundos: 16 * 3600 + 45 * 60,
        titulo: "Fechamento de Plantão & Relatório de Passagem de Turno (Handover)",
        severidade: "low",
        setor: "SOC Operacional",
        origem: "Procedimento Padrão N1 -> N2",
        descricao: "Consolidação dos chamados atendidos para repasse ao plantonista do turno noturno.",
        log: `[SHIFT-HANDOVER-CHECKLIST]
Expediente: 08:00 - 17:00
Incidentes Críticos Contidos: 2
IPs Bloqueados: 2
Status da Infra: Operacional e Protegida.`,
        mitre: "Procedimento Operacional Padrão",
        status: "pendente",
        resolvido: false
    }
];

// Linux Terminal Command Handler
function processarComandoTerminal(cmd) {
    const limpo = cmd.trim().toLowerCase();
    if (!limpo) return "";
    
    if (limpo === "help") {
        return `Comandos disponíveis:
  help              - Mostra esta lista de ajuda
  status            - Exibe status da segurança e expediente
  nmap <ip>         - Simula varredura de portas
  iptables -L       - Lista regras de firewall ativas
  wireshark         - Abre resumo do tráfego capturado
  mitre <tecnica>   - Consulta tática da matriz MITRE ATT&CK
  whoami            - Mostra informações do usuário atual
  clear             - Limpa o terminal`;
    }
    
    if (limpo === "status") {
        return `[CYBERDEFENSE SOC STATUS]
Turno: 08:00 - 17:00
DEFCON: 3 (Moderado)
Incidentes Pendentes: ${INCIDENT_QUEUE.filter(i => !i.resolvido).length}
Servidores Monitorados: 42 nós operacionais.`;
    }

    if (limpo === "whoami") {
        return "matheus (Analista de SOC N1 - Grupo: Security-Operations, Sudoer)";
    }

    if (limpo.startsWith("nmap")) {
        return `Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for host (alvo)
Host is up (0.0021s latency).
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
3389/tcp closed ms-wbt-server
Nmap done: 1 IP address scanned in 1.42 seconds`;
    }

    if (limpo.startsWith("iptables")) {
        return `Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
DROP       tcp  --  194.26.29.112        0.0.0.0/0            /* PortScan Blacklist */
DROP       tcp  --  185.220.101.45       0.0.0.0/0            /* Tor Exit Node Block */`;
    }

    if (limpo === "wireshark") {
        return `[WIRESHARK CAPTURE SUMMARY - eth0]
Total Packets: 148,290 | Dropped: 0
Protocols: TCP (72%), TLSv1.3 (21%), DNS (6%), ICMP (1%)
Top Talker: 192.168.10.42 (High volume of DNS TXT/A queries)`;
    }

    if (limpo.startsWith("mitre")) {
        return `[MITRE ATT&CK KNOWLEDGE BASE]
Technique ID consultada. Táticas defensivas mapeadas:
- Detecção via Sysmon Event ID 1 / 3 / 22
- Regra de correlação no SIEM Wazuh
- Mitigação recomendada: Bloqueio de IP no EDR e quarentena do host.`;
    }

    if (limpo === "clear") {
        return "__CLEAR__";
    }

    return `bash: comando não encontrado: '${cmd}'. Digite 'help' para comandos úteis.`;
}
