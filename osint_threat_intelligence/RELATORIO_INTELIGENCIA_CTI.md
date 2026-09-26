# 🕵️ RELATÓRIO DE INTELIGÊNCIA DE AMEAÇAS CIBERNÉTICAS (CTI BRIEFING)

**Alvo Analisado:** `globo.com`  
**Analista de Inteligência (CTI):** `Matheus Barbosa (CTI Analyst)`  
**Data de Produção do Relatório:** `2026-09-24 17:59:00`  
**Classificação da Informação:** TLP:AMBER (Uso Interno e Parceiros Confiáveis)  
**Metodologia:** Diamond Model of Intrusion Analysis & MITRE ATT&CK Framework  

---

## 1. SUMÁRIO EXECUTIVO (NÍVEL ESTRATÉGICO)
A presente análise de Cyber Threat Intelligence mapeou a superfície de exposição externa da organização `globo.com`, correlacionando ativos identificados via fontes abertas (OSINT) com as principais Táticas, Técnicas e Procedimentos (TTPs) utilizadas por grupos criminosos ativos no cenário global.

---

## 2. RECONHECIMENTO DE SUPERFÍCIE DE ATAQUE (OSINT / CERTIFICATE TRANSPARENCY)

Foram identificados **6 ativos públicos** associados à infraestrutura do domínio:

* 🌐 `admin.globo.com`
* 🌐 `api-internal.globo.com`
* 🌐 `auth.globo.com`
* 🌐 `mail.globo.com`
* 🌐 `portal.globo.com`
* 🌐 `vpn.globo.com`

### ⚠️ Vetores de Acesso Críticos Mapeados:

| Subdomínio Identificado | Nível de Criticidade | Hipótese de Vetor de Intrusão |
| :--- | :---: | :--- |
| `admin.globo.com` | **ALTA** | Ponto de Acesso Externo (Alvo prioritário de Credential Stuffing & Força Bruta) |
| `api-internal.globo.com` | **MÉDIA** | Ambiente de Desenvolvimento / API (Possível exposição de chaves e dados sensíveis) |
| `auth.globo.com` | **ALTA** | Ponto de Acesso Externo (Alvo prioritário de Credential Stuffing & Força Bruta) |
| `portal.globo.com` | **ALTA** | Ponto de Acesso Externo (Alvo prioritário de Credential Stuffing & Força Bruta) |
| `vpn.globo.com` | **ALTA** | Ponto de Acesso Externo (Alvo prioritário de Credential Stuffing & Força Bruta) |

---

## 3. PERFILAMENTO TÁTICO DE ATORES DE AMEAÇA (THREAT ACTOR PROFILING)

### 🎯 Grupo: `LockBit 3.0` (Ransomware-as-a-Service (RaaS))
* **Origem Provável:** Leste Europeu / Clandestino
* **Nível de Severidade:** `CRÍTICO (Nível 5/5)`
* **Alvos Típicos:** Grandes Corporações, Setor Financeiro, Saúde e Logística
* **Vetor Inicial:** Phishing com anexos maliciosos, Credenciais comprometidas e Brechas em RDP
* **TTPs Principais (MITRE ATT&CK):**
  * 📌 `T1190 - Exploit Public-Facing Application (VPNs/Firewalls vulneráveis)`
  * 📌 `T1059 - Command and Scripting Interpreter (PowerShell / Cobalt Strike)`
  * 📌 `T1078 - Valid Accounts (Uso de credenciais vazadas na Dark Web)`
  * 📌 `T1486 - Data Encrypted for Impact (Criptografia de arquivos com dupla extorsão)`

### 🎯 Grupo: `Lazarus Group (APT38)` (Grupo de Espionagem e Roubo Cibernético Patrocinado por Estado)
* **Origem Provável:** Coreia do Norte
* **Nível de Severidade:** `CRÍTICO (Nível 5/5)`
* **Alvos Típicos:** Bancos Centrais, Exchanges de Criptomoedas, Defesa e Aeroespacial
* **Vetor Inicial:** Engenharia social direcionada via redes sociais e trojanização de softwares abertos
* **TTPs Principais (MITRE ATT&CK):**
  * 📌 `T1566.002 - Spearphishing Link (Abordagens falsas no LinkedIn com ofertas de emprego)`
  * 📌 `T1055 - Process Injection (Injeção em processos legítimos do Windows)`
  * 📌 `T1573 - Encrypted Channel (Comunicação C2 criptografada customizada)`

### 🎯 Grupo: `APT29 (Cozy Bear)` (Ciberespionagem Governamental Avançada)
* **Origem Provável:** Rússia (SVR)
* **Nível de Severidade:** `EXTREMO (Nível 5/5)`
* **Alvos Típicos:** Governos, Embaixadas, Think Tanks e Empresas de Tecnologia (Supply Chain)
* **Vetor Inicial:** Comprometimento de cadeias de suprimentos de TI e campanhas sofisticadas de e-mail
* **TTPs Principais (MITRE ATT&CK):**
  * 📌 `T1195.002 - Supply Chain Compromise (Ataques a fornecedores de software)`
  * 📌 `T1071.001 - Web Protocols (Tráfego de C2 mascarado em Graph API da Microsoft)`
  * 📌 `T1550.001 - Application Access Token (Uso indevido de tokens de nuvem / Azure AD)`

### 🎯 Grupo: `Lapsus$` (Grupo Hacktivista / Extorsão Financeira Juvenil)
* **Origem Provável:** Internacional (Brasil / Reino Unido)
* **Nível de Severidade:** `ALTO (Nível 4/5)`
* **Alvos Típicos:** Gigantes de Tecnologia (Nvidia, Microsoft, Samsung, Okta, Ministério da Saúde)
* **Vetor Inicial:** Suborno de funcionários internos, SIM Swapping e compra de credenciais infostealer
* **TTPs Principais (MITRE ATT&CK):**
  * 📌 `T1539 - Steal Web Session Cookie (Roubo de cookies de sessão via infostealers)`
  * 📌 `T1621 - Multi-Factor Authentication Request Generation (MFA Fatigue / Bombing)`
  * 📌 `T1484 - Group Policy Modification (Escalação de privilégios em nuvem)`

---

## 4. RECOMENDAÇÕES DE MITIGAÇÃO & DEFESA ATIVA (SOC & BLUE TEAM)

1. **Implementação de MFA Resistente a Phishing:** Exigir chaves FIDO2/WebAuthn em todos os portais de acesso remoto (`vpn.*`, `auth.*`).
2. **Monitoramento de Infostealers na Dark Web:** Rastrear vazamentos de logs de navegadores (RedLine/Vidar) contendo credenciais de colaboradores.
3. **Alinhamento com a Matriz MITRE ATT&CK:** Implementar regras de detecção específicas para comandos PowerShell ofuscados e dumps de memória do processo `lsass.exe`.

**Relatório Homologado:** CTI Task Force — `2026-09-24 17:59:00`
