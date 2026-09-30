# 🛡️ RELATÓRIO CONFIDENCIAL DE INTELIGÊNCIA PATRIMONIAL & OSINT
> **DOCUMENTO PERICIAL DE SUPORTE PROBATÓRIO JUDICIAL**  
> **Classificação:** ESTRITAMENTE CONFIDENCIAL — RESERVADO  
> **Finalidade:** Subsidiar Ação de Execução de Título Extrajudicial / Penhora de Bens  
> **Elaborado por:** Consultoria de Inteligência & Perícia Forense Digital  
> **Base Legal:** Lei Federal nº 13.432/2017 (Investigação Privada) & Art. 159/465 do CPC  
> **Cadeia de Custódia:** Evidências digitais preservadas com Hash SHA-256 (ISO 27037)

---

## 📋 1. IDENTIFICAÇÃO DO ALVO (INVESTIGADO)

| Campo | Dados Cadastrais Identificados |
| :--- | :--- |
| **Nome Completo:** | Roberto Mendonça da Silva (*Nome Fictício para Amostra*) |
| **CPF:** | `***.482.917-**` |
| **Status Processual:** | Devedor Executado nos autos do processo nº `0012345-67.2024.8.19.0205` (TJ-RJ) |
| **Valor Atualizado da Execução:** | **R$ 487.650,00** |
| **Alegação nos Autos:** | Insolvência civil / Ausência de bens penhoráveis (Sisbajud e Renajud infrutíferos) |

---

## ⚡ 2. RESUMO EXECUTIVO DOS ACHADOS DE INTELIGÊNCIA

Embora o devedor declare formalmente nos autos não possuir patrimônio nem saldo em contas bancárias, a investigação técnica em fontes abertas e bases cruzadas revelou:

* 🚗 **Patrimônio Oculto Identificado:** **R$ 685.000,00** em bens móveis e cotas empresariais ativas.
* 🏢 **Empresas Ativas Ocultadas:** 2 empresas operantes em nome de parentes de 1º grau (interpostas pessoas / "laranjas").
* 🚙 **Veículos em Uso Pessoal:** 1 Veículo Toyota Hilux SRX (Ano 2023) emplacado em nome de empresa de fachada, utilizado exclusivamente pelo executado.
* ✈️ **Padrão de Vida incompatível:** 3 viagens internacionais nos últimos 8 meses com fotos e registros geolocalizados por metadados.

---

## 🔍 3. MAPA DE VÍNCULOS SOCIETÁRIOS & CONFUSÃO PATRIMONIAL

```mermaid
graph TD
    Alvo["Roberto Mendonça (Devedor Executado)<br>Declara 'Zero Bens'"] 
    Filho["Lucas Mendonça (Filho - 21 anos)<br>Estudante sem renda declarada"]
    Irma["Cláudia Mendonça (Irmã)<br>Professora Estadual"]
    
    Empresa1["🏢 Silva & Mendonça Logística Eireli<br>Faturamento Anual: R$ 1.8M"]
    Empresa2["🏢 RMS Participações e Consultoria Ltda<br>Ativo: 1 Imóvel Comercial em Campo Grande"]
    Veiculo["🚙 Toyota Hilux 2023 (Placa RJ-***-4920)<br>Avaliação Tabela FIPE: R$ 285.000"]
    
    Alvo -.->|Sócio Oculto / Procuração Plenos Poderes| Empresa1
    Alvo -.->|Administrador de Fato| Empresa2
    Filho -->|Sócio Titular 90% (Laranja)| Empresa1
    Irma -->|Sócia Administradora| Empresa2
    Empresa1 -->|Proprietária Registrada| Veiculo
    Alvo ===>|Uso Pessoal Diário & Vaga de Garagem| Veiculo

    classDef devedor fill:#ff4d4d,stroke:#990000,stroke-width:2px,color:#fff;
    classDef laranja fill:#ffcc00,stroke:#cc9900,stroke-width:1px,color:#000;
    classDef ativo fill:#2ecc71,stroke:#27ae60,stroke-width:2px,color:#fff;
    class Alvo devedor;
    class Filho,Irma laranja;
    class Empresa1,Empresa2,Veiculo ativo;
```

### Detalhamento das Evidências Técnicas:
1. **Empresa Silva & Mendonça Logística (CNPJ `42.***.***/0001-**`):**
   * Aberta 4 meses após a distribuição do processo de execução.
   * O titular no QSA é o filho do executado (21 anos), sem histórico contributivo prévio no CAGED/INSS.
   * Constatado instrumento de procuração pública conferindo ao devedor **poderes irrestritos de movimentação bancária e assinatura de contratos**.
2. **Desconsideração Inversa da Personalidade Jurídica:**
   * Elementos probatórios robustos configurando **Confusão Patrimonial e Desvio de Finalidade** (Art. 50 do Código Civil).

---

## 📍 4. PADRÃO DE VIDA VS. INSOLVÊNCIA (ANÁLISE OSINT)

| Data | Registro Identificado | Evidência Técnica | Implicações Jurídicas |
| :---: | :--- | :--- | :--- |
| `14/04/2026` | Hospedagem em Resort de Luxo em Angra dos Reis | Imagem extraída de rede social pública com metadados EXIF contendo coordenadas GPS precisas (`-23.0065, -44.3188`). | Padrão incompatível com insolvência alegada em petição protocolada 10 dias antes. |
| `28/05/2026` | Embarque Internacional para Cancún | Registro de cartão de embarque em stories públicos em nome de *"Roberto Mendonça"*. | Capacidade financeira flagrante; subsídio para pedido de **Apreensão de Passaporte** (Art. 139, IV do CPC). |
| `12/08/2026` | Aquisição de Lancha Marina da Glória | Vínculo identificado em clube náutico sob nome fantasia de empresa de fachada. | Bem de alto valor passível de penhora cautelar imediata. |

---

## 🪙 5. RASTREAMENTO DE CRIPTOATIVOS (BLOCKCHAIN FORENSICS)

Através do cruzamento de e-mails secundários e identificadores de transações P2P vinculadas ao número de telefone do devedor:
* **Carteira Identificada (USDT - Rede TRON):** `TX7r9...q2pM`
* **Volume Transacionado nos últimos 90 dias:** Mais de **$ 32.400 USDT** (~R$ 178.000,00).
* **Exchange de Liquidação:** Identificados múltiplos envios para carteiras de depósito pertencentes à corretora **Binance**.
* **Medida Judicial Aplicável:** Expedição de ofício à *B Digital Brasil (Binance Brasil)* para bloqueio e penhora de saldo de criptoativos do CPF do executado.

---

## ⚖️ 6. CONCLUSÃO PERICIAL & SUGESTÃO DE MEDIDAS COERCITIVAS

Com base no arcabouço probatório anexado (Doc. 01 ao Doc. 08 deste relatório), resta cristalina a manobra fraudulenta de ocultação de bens para frustrar o pagamento da dívida.

Recomenda-se ao patrono da causa pleitear perante o juízo da execução:
1. **Desconsideração Inversa da Personalidade Jurídica** da empresa `Silva & Mendonça Logística`, incluindo-a no polo passivo da execução.
2. **Penhora e Bloqueio de Circulação do Veículo Toyota Hilux** (Placa `RJ-***-4920`).
3. **Ofício com ordem de bloqueio judicial às corretoras Binance Brasil e Mercado Bitcoin** para constrição de criptoativos.
4. **Aplicação de Medidas Coercitivas Atípicas (Art. 139, IV do CPC):** Apreensão de Passaporte e CNH, fundamentada na comprovada viagem internacional de lazer concomitante à alegação de insolvência.

---
*Relatório emitido sob estrita conformidade com a Lei Federal nº 13.432/2017 e normas técnicas de computação forense.*  
**Perito / Investigador Responsável:** Matheus Barbosa — Inteligência & Perícia Digital  
**Campo Grande, Rio de Janeiro — RJ**
