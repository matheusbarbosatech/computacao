import os
import json

DESKTOP = r"C:\Users\matheus\Desktop"

# 1. Gerar o Guia de Estudos e Resumo Executivo em Markdown
study_guide_md = """# 📘 Guia de Estudos Mestre & Resumo Executivo — Clube do Consultor de TI
> **Base de Conhecimento Oficial:** Extraído e condensado das 32 aulas práticas de Consultoria, Negócios e Monetização para TI / Devs / Hackers.

---

## 🧭 Visão Geral do Método

O **Clube do Consultor de TI** ensina a transição do profissional de TI da condição de *"Técnico Escravo / CLT / Apagador de Incêndios"* para a de **Consultor Estratégico de TI**, fechando contratos recorrentes de **R$ 5.000 a R$ 20.000/mês por cliente**.

```mermaid
graph TD
    A["Técnico Operacional / CLT<br>(Vende Horas / Apaga Incêndios)"] -->|Quebra da Matrix| B["Especialista com Posicionamento<br>(Foco na Dor do Negócio)"]
    B -->|Oferta Irresistível| C["Diagnóstico & Auditoria<br>(Segurança / Infra / Nuvem)"]
    C -->|Prospecção Ativa B2B| D["Reunião Estratégica 30min<br>(Descoberta & Valor)"]
    D -->|Fechamento de Alto Valor| E["Contrato Recorrente Retainer<br>(R$ 5.000 a R$ 20.000/mês)"]
```

---

## 🏛️ Os 4 Pilares Fundamentais

### Pilar 1: Mentalidade & Desprogramação do Técnico
- **A Matrix da TI:** Profissionais de TI são treinados para amar ferramentas (Linux, Firewalls, Docker, Python) e ignorar o dinheiro.
- **O Cliente não compra tecnologia:** Ele compra **redução de custos**, **aumento de lucro**, **continuidade do negócio** e **segurança jurídica**.
- **A Morte do Preço por Hora:** Vender hora é o caminho mais rápido para a exaustão. Consultores vendem **Impacto e Disponibilidade Estratégica**.

### Pilar 2: Construção da Oferta Irresistível (R$ 5k a R$ 20k)
- **O Tripé da Consultoria:**
  1. **Auditoria & Diagnóstico Inicial (Entrada):** R$ 1.500 a R$ 5.000 (Relatório de Vulnerabilidades, Gargalos de Nuvem ou Risco de Parada).
  2. **Contrato de Retenção Recorrente (MRR):** R$ 3.000 a R$ 15.000/mês para monitoramento, segurança proativa, infraestrutura e governança.
  3. **Projetos de Transformação / Migração:** R$ 10.000 a R$ 50.000 (Migração para Nuvem, Implantação de SOC/Wazuh, Hardening).

### Pilar 3: Prospecção B2B Ativa & Reunião de Fechamento
- **Onde estão os melhores clientes:** Empresas com 15 a 150 funcionários (Clínicas médicas, Escritórios de Advocacia, Contabilidades, Distribuidoras, Indústrias locais).
- **Abordagem pelo Risco Invisível:** Não fale de antivírus ou backup. Fale do custo de **3 dias de operação parada por ransomware** ou multas da LGPD.
- **Script da Reunião de 30 Minutos:**
  - *Primeiros 10 min:* Perguntas de Diagnóstico (Qual o custo de 1 hora da sua empresa parada?).
  - *Próximos 10 min:* Apresentação do Abismo (O que está em risco hoje no seu ambiente).
  - *Últimos 10 min:* A Solução Estratégica e Proposta Comercial no próprio call.

### Pilar 4: Entrega Estratégica, SLA & Retenção Infinita
- **Relatório Executivo Mensal:** Nunca envie logs técnicos. Envie um resumo em 1 página: *Quantos ataques bloqueados, quantos backups testados e quanto tempo de operação 100% no ar*.
- **O Poder da Proatividade:** O cliente deve ser avisado do problema **depois que você já o resolveu**, e não ligar para reclamar que o sistema caiu.

---

## 💬 Matriz de Quebra de Objeções Reais

| Objeção do Cliente | Resposta do Consultor Estratégico |
| :--- | :--- |
| *"Já tenho um rapaz que cuida do TI aqui."* | *"Perfeito! A maioria dos nossos clientes também tinha um suporte para formatar computadores. Nosso trabalho não concorre com ele: nós somos a governança estratégica de segurança e servidores que evita que a empresa seja paralisada por ataques cibernéticos."* |
| *"Está muito caro para o nosso momento."* | *"Entendo perfeitamente. Mas me permita perguntar: se o seu servidor parar amanhã e você perder o banco de dados do faturamento, qual seria o prejuízo financeiro e com clientes em apenas 48 horas? Nosso investimento anual é menor que 1 dia de crise."* |
| *"Manda uma proposta por e-mail que eu analiso."* | *"Com certeza! Mas como cada empresa tem riscos e infraestruturas muito particulares, uma proposta genérica por e-mail seria leviana. Vamos fazer um diagnóstico rápido de 15 minutos na quinta-feira às 14h para eu personalizar os pontos exatos?"* |

---

## 🎯 Checklist de Ação Imediata para Devs & Hackers
- [ ] Definir o Nicho Inicial (ex: Clínicas de Saúde, Escritórios Contábeis ou E-commerces locais).
- [ ] Criar o Pacote de Diagnóstico Inicial (Avaliação de Risco & Vulnerabilidade).
- [ ] Enviar 15 abordagens personalizadas por dia no LinkedIn e WhatsApp dos tomadores de decisão (Sócios, Diretores, CEOs).
- [ ] Conduzir a Reunião com Foco em Negócio (não abra o terminal na frente do CEO).
- [ ] Fechar o primeiro contrato de R$ 3.000 a R$ 5.000/mês com pagamento adiantado.
"""

with open(os.path.join(DESKTOP, "GUIA_DE_ESTUDOS_CLUBE_DO_CONSULTOR.md"), "w", encoding="utf-8") as f:
    f.write(study_guide_md)

print("Guia de Estudos em Markdown gerado no Desktop!")
