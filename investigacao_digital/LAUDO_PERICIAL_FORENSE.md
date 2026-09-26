# 🛡️ LAUDO DE PERÍCIA E INVESTIGAÇÃO FORENSE DIGITAL

**Identificador do Procedimento:** `CASO-2026-PF-001`  
**Perito Responsável:** `Matheus Barbosa (Perito Digital)`  
**Data e Hora da Coleta:** `2026-09-24 17:57:05`  
**Padrão de Conformidade:** ISO/IEC 27037 (Diretrizes para Gestão de Evidências Digitais)  

---

## 1. OBJETIVO DA PERÍCIA
Proceder à triagem técnica, preservação da cadeia de custódia e exame pericial em artefatos digitais suspeitos para identificar vetores de intrusão, conexões ativas e tentativas de fraude/engenharia social.

---

## 2. INTEGRIDADE DA CADEIA DE CUSTÓDIA (HASHES FORENSES)

| Arquivo de Evidência | Tamanho | Algoritmo SHA-256 (Hash Imutável) |
| :--- | :---: | :--- |
| `forensic_investigator.py` | 9270 bytes | `797accfdac2daaf1eca43a58505aa219216726b4e8ddfef1df79ae88a488a737` |
| `100_PROJETOS_PRATICOS_PBL_CYBER_HACKING.md` | 77473 bytes | `2b81ce54d2e65a29f046a4d3943216b3490f177612c0646c2693dc23d43103ca` |

> **Certificação de Integridade:** Os hashes acima atestam que nenhuma evidência sofreu modificação após a coleta.

---

## 3. EXAME PERICIAL DE E-MAIL FRAUDULENTO (SPOOFING / BEC)

* **Remetente Aparente (From):** `Notificacao Urgente <financeiro@bancodobrasil.com.br>`
* **Endereço de Resposta Real (Reply-To):** `capturador-dados@servidor-russo.com`
* **Endereço IP de Origem do Servidor:** `185.220.101.5`
* **Resultado da Validação SPF:** `FAIL (SPOOFING DETECTADO)`
* **Parecer Técnico:** **ALTA PROBABILIDADE DE FRAUDE / PHISHING**

---

## 4. TELEMETRIA VOLÁTIL DE CONEXÕES DE REDE (LIVE TRIAGE)

| Protocolo | Endereço Local | Endereço Remoto | Estado | PID |
| :---: | :--- | :--- | :---: | :---: |
| TCP | `0.0.0.0:135` | `0.0.0.0:0` | LISTENING | `1308` |
| TCP | `0.0.0.0:445` | `0.0.0.0:0` | LISTENING | `4` |
| TCP | `0.0.0.0:5040` | `0.0.0.0:0` | LISTENING | `3700` |
| TCP | `0.0.0.0:5357` | `0.0.0.0:0` | LISTENING | `4` |
| TCP | `0.0.0.0:7680` | `0.0.0.0:0` | LISTENING | `5644` |
| TCP | `0.0.0.0:49664` | `0.0.0.0:0` | LISTENING | `1068` |
| TCP | `0.0.0.0:49665` | `0.0.0.0:0` | LISTENING | `584` |
| TCP | `0.0.0.0:49666` | `0.0.0.0:0` | LISTENING | `1724` |
| TCP | `0.0.0.0:49667` | `0.0.0.0:0` | LISTENING | `2104` |
| TCP | `0.0.0.0:49669` | `0.0.0.0:0` | LISTENING | `3568` |

---

## 5. CONCLUSÃO PERICIAL
1. A evidência analisada confirma a utilização de servidores internacionais não autorizados para envio de comunicações forjadas com falso remetente institucional.
2. A cadeia de custódia foi preservada mediante geração de assinaturas criptográficas SHA-256 e MD5.
3. Recomenda-se o bloqueio preventivo do IP identificado no firewall de borda e abertura de inquérito competente.

**Local e Data:** Curitiba/PR — 2026-09-24 17:57:05  
**Assinatura Digital do Perito:** `[ASSINADO DIGITALMENTE - ICP-BRASIL / SHA256]`
