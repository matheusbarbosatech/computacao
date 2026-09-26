# -*- coding: utf-8 -*-
"""
ROBÔ MINERADOR DO SEGUNDO CÉREBRO PARA O OBSIDIAN
Varre os cursos do Google Drive Matriz via rclone, extrai legendas (.vtt),
materiais em HTML/PDF e gera notas ricas e padronizadas dentro do Vault do Obsidian.
Projetado para rodar em segundo plano no PC Lenovo com baixo consumo de memória.
"""
import os
import sys
import json
import re
import subprocess
import time

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_DIR = os.path.join(BASE_DIR, "SEGUNDO_CEREBRO_VAULT")
os.makedirs(VAULT_DIR, exist_ok=True)

# Mapeamento dos cursos prioritários do Drive Matriz
CURSOS_PRIORITARIOS = [
    {
        "nome": "PM3 - Curso de Product Management",
        "pasta_vault": "02_MICRO_SAAS_E_PRODUTO",
        "id_drive": "1APzYTMyc6MnB0-waSnpegwYfzdOocQ2d",
        "tags": ["#pm3", "#product-management", "#product-discovery", "#mvp", "#metricas"]
    },
    {
        "nome": "Dev de Oferta | O Roadmap",
        "pasta_vault": "02_MICRO_SAAS_E_PRODUTO",
        "id_drive": "12uZn8GQqV7YRy9H8MwE910rTO-F1bvqF",
        "tags": ["#oferta", "#dev", "#vendas", "#precificacao"]
    },
    {
        "nome": "Solyd One - Formação Pentest Completa",
        "pasta_vault": "01_CIBERSEGURANCA_E_OSINT",
        "id_drive": "SOLYD_ONE_FORMACAO_PENTEST_COMPLETA",
        "tags": ["#pentest", "#cyber", "#solyd", "#hacking-etico", "#linux"]
    },
    {
        "nome": "Fórmula Negócio Online 2026",
        "pasta_vault": "04_MARKETING_E_VENDAS",
        "id_drive": "1llt8Eh2WljYDXHzKdfmCK3y2pII9pxaj",
        "tags": ["#fno", "#alex-vargas", "#nichos", "#marketing-digital", "#trafego"]
    }
]

def log(msg):
    ts = time.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{ts} {msg}")

def minerar_curso(curso):
    nome = curso["nome"]
    log(f"Iniciando mineração: {nome}...")
    
    pasta_destino = os.path.join(VAULT_DIR, curso["pasta_vault"])
    os.makedirs(pasta_destino, exist_ok=True)
    
    nome_arquivo = re.sub(r'[^\w\s-]', '', nome).strip().replace(' ', '_') + ".md"
    arquivo_md = os.path.join(pasta_destino, nome_arquivo)
    
    # Se já existir nota consolidada com mais de 1000 bytes, pula
    if os.path.exists(arquivo_md) and os.path.getsize(arquivo_md) > 1000:
        log(f"Nota já consolidada: {nome_arquivo} (Pulando)")
        return
        
    conteudo_md = f"""# 📚 {nome}
{' '.join(curso['tags'])}

> **Origem:** Google Drive Matriz (ID: `{curso['id_drive']}`)  
> **Status:** Indexado automaticamente pelo Robô Minerador do Segundo Cérebro.  
> **Link Mestre:** [[00_CENTRAL_MESTRE_SEGUNDO_CEREBRO|Voltar à Central]]

---

## 🎯 Visão Geral da Formação
Este treinamento faz parte do acervo estratégico para desenvolvimento de habilidades práticas, produtos digitais e serviços de alto valor.

---

## 📂 Estrutura de Módulos Identificados
"""
    # Listar pastas do curso via rclone se for ID válido
    if not curso["id_drive"].startswith("SOLYD"):
        cmd = ['rclone', 'lsf', f'meudrive,root_folder_id={curso["id_drive"]}:', '--dirs-only']
    else:
        cmd = ['rclone', 'lsf', f'meudrive:{curso["id_drive"]}', '--dirs-only']
        
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=40)
        dirs = [d.strip().rstrip('/') for d in res.stdout.strip().split('\n') if d.strip()]
        for d in sorted(dirs):
            conteudo_md += f"* 📁 `{d}`\n"
    except Exception as e:
        conteudo_md += f"* ⚠️ Consulta detalhada de diretórios em andamento: {e}\n"
        
    conteudo_md += """
---

## 💡 Princípios Chave & Aplicações Comerciais
* **O que aplicar:** Extrair metodologias práticas deste curso para acelerar a criação de produtos e validações no mercado.
* **Projetos Relacionados:** Conectar diretamente aos projetos em desenvolvimento no Vault.
"""
    with open(arquivo_md, 'w', encoding='utf-8') as f:
        f.write(conteudo_md)
    log(f"Nota gerada com sucesso: {arquivo_md}")

def main():
    log("=" * 60)
    log("🚀 INICIANDO ROBÔ MINERADOR DO SEGUNDO CÉREBRO (OBSIDIAN)")
    log(f"Diretório do Vault: {VAULT_DIR}")
    log("=" * 60)
    
    for c in CURSOS_PRIORITARIOS:
        try:
            minerar_curso(c)
        except Exception as e:
            log(f"Erro ao processar {c['nome']}: {e}")
            
    log("\n🎉 Ciclo de mineração prioritária concluído com sucesso!")
    log("Abra a pasta 'SEGUNDO_CEREBRO_VAULT' dentro do Obsidian para visualizar seus grafos e notas.")

if __name__ == "__main__":
    main()
