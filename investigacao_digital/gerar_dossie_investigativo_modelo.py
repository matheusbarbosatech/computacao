#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📁 GERADOR DE DOSSIÊ DE INTELIGÊNCIA PATRIMONIAL & OSINT (PORTFÓLIO MODELO)
Gera um Dossiê Pericial Profissional para Apresentação em Escritórios de Advocacia
"""

import os
import sys
import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DOSSIE = os.path.join(BASE_DIR, "DOSSIE_INTELIGENCIA_PATRIMONIAL_MODELO.md")

def gerar_dossie():
    ts = datetime.datetime.now().strftime("%d/%m/%Y")
    
    with open(OUTPUT_DOSSIE, "w", encoding="utf-8") as f:
        f.write(f"""# 📋 DOSSIÊ DE INTELIGÊNCIA PATRIMONIAL & RASTREAMENTO OSINT
> **RELATÓRIO CONFIDENCIAL DE SUPORTE PROBATÓRIO JUDICIAL**  
> **Procedimento de Investigação:** `OSINT-PATRIMONIAL-2026/089`  
> **Investigador / Perito:** `Matheus Barbosa — Especialista em Investigação Digital`  
> **Data de Emissão:** `{ts}`  
> **Finalidade:** Subsidiar Ação de Execução de Título Extrajudicial / Penhora de Bens

---

## 1. DADOS DO ALVO INVESTIGADO (MODELO ANOMIZADO)
* **Nome / Razão Social:** `INVESTIGADO EXEMPLO DA SILVA`
* **CPF:** `***.458.919-**`
* **Atividade Declarada:** Consultoria Empresarial e Gestão de Ativos
* **Situação Judicial:** Alegação de insolvência / ausência de bens penhoráveis via SISBAJUD.

---

## 2. MAPA DE VÍNCULOS EMPRESARIAIS (QSA & GRUPO ECONÔMICO)
Cruzando bases da Receita Federal e Juntas Comerciais, identificou-se que o investigado ocultava sua participação societária através de interpostas pessoas ("laranjas"):

```
[INVESTIGADO ALVO] 
       │
       ├── (Procurador / Administrador Oculto) ➔ [ALPHA HOLDINGS LTDA] (CNPJ: 45.***.***/0001-**)
       │                                              │
       │                                              └── Faturamento Estimado: R$ 4.2M/ano
       │
       └── (Sócio Majoritário 90%) ➔ [BETA LOGÍSTICA & TRANSPORTES] (CNPJ: 38.***.***/0001-**)
                                              │
                                              └── 4 Caminhões Scania e 2 Galpões Comerciais
```

---

## 3. RASTREAMENTO VEICULAR & IMOBILIÁRIO (FONTES ABERTAS)
Identificou-se padrão de vida de altíssimo padrão ostentado publicamente e incompatível com a declaração de pobreza:

| Tipo de Bem | Descrição / Modelo | Placa / Registro | Titular Registrado | Evidência OSINT |
| :--- | :--- | :---: | :--- | :--- |
| **Veículo de Luxo** | Porsche Macan GTS (2024) | `***-9E88` | Empresa do Filho (19 anos) | Multas e fotos com o Investigado ao volante |
| **Imóvel Urbano** | Mansão em Condomínio Fechado | `Matrícula 84.120` | Em nome da cunhada | Conta de consumo e internet no nome do Alvo |
| **Embarcação** | Lancha Real 365 (36 pés) | `Marinha: 441-***` | Alpha Holdings Ltda | Registros em Marina com o Alvo como comandante |

---

## 4. RASTREAMENTO DE CRIPTOMODAS & ATIVOS DIGITAIS
Identificou-se chave pública de carteira Ethereum vinculada ao e-mail institucional do investigado em fóruns públicos:
* **Endereço da Carteira:** `0x71C...88B9`
* **Saldo Atual Identificado na Blockchain:** `14.85 ETH + 45.000 USDT (Aprox. R$ 380.000,00)`
* **Hash da Última Transação:** `0x4a9f...e102` (Transferência realizada 48h antes da citação judicial).

---

## 5. CONCLUSÃO TÉCNICA PARA O ADVOGADO
1. **Confusão Patrimonial e Desconsideração da Personalidade Jurídica:** Há substrato probatório robusto (art. 50 do Código Civil) para pedir a penhora das contas e veículos da empresa `Alpha Holdings Ltda`.
2. **Penhora de Criptoativos:** Solicitação de ofício às corretoras nacionais (Mercado Bitcoin, Binance) e bloqueio judicial das carteiras identificadas.
3. **Cadeia de Custódia:** Todos os links, prints e transações de blockchain foram arquivados com hash criptográfico SHA-256 e ata notarial digital para validade irrefutável em juízo.

---
**Assinatura Digital:** `[MATHEUS BARBOSA — PERÍCIA FORENSE DIGITAL & OSINT]`
""")
    print(f"✅ Modelo de Dossiê Patrimonial criado em: {OUTPUT_DOSSIE}")

if __name__ == "__main__":
    gerar_dossie()
