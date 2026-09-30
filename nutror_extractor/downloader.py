import os
import sys
import time
import random
import glob
import json
import subprocess
from cleaner import clean_vtt_file

def download_subtitles_for_url(
    url: str,
    output_prefix: str,
    temp_dir: str,
    referer: str = "https://app.nutror.com/",
    use_cookies: bool = False
) -> dict:

    """
    Executa o yt-dlp para baixar apenas a legenda do vídeo do Vimeo/Nutror.
    """
    os.makedirs(temp_dir, exist_ok=True)
    out_template = os.path.join(temp_dir, f"{output_prefix}_%(id)s.%(ext)s")
    
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-auto-sub",
        "--write-sub",
        "--all-subs",
        "--sub-format", "vtt/best",
        "--referer", referer,
        "--no-playlist",
        "--no-warnings",
        "-o", out_template,
        url
    ]
    
    if use_cookies:
        cmd.extend(["--cookies-from-browser", "chrome"])

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        
        # Se falhou por causa de cookies bloqueados pelo Chrome aberto, tenta sem cookies
        if res.returncode != 0 and "cookies" in res.stderr.lower() and use_cookies:
            print("    [!] Chrome parece aberto/bloqueado. Retentando sem cookies...")
            return download_subtitles_for_url(url, output_prefix, temp_dir, referer, use_cookies=False)
            
        # Procura arquivos .vtt gerados para este prefixo
        vtt_matches = glob.glob(os.path.join(temp_dir, f"{output_prefix}_*.vtt"))
        
        if vtt_matches:
            return {"success": True, "vtt_files": vtt_matches, "output": res.stdout}
        else:
            return {
                "success": False, 
                "error": "Nenhuma legenda encontrada/gerada para este vídeo.", 
                "stderr": res.stderr[:300] if res.stderr else res.stdout[:300]
            }
            
    except Exception as e:
        return {"success": False, "error": str(e)}


def process_batch(
    lista_aulas_path: str = None,
    output_dir: str = None,
    temp_dir: str = None,
    min_sleep: float = 3.0,
    max_sleep: float = 7.0
):
    """
    Processa o lote de aulas contidas no arquivo de texto sequencialmente.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if lista_aulas_path is None:
        lista_aulas_path = os.path.join(base_dir, "lista_aulas.txt")
    elif not os.path.isabs(lista_aulas_path):
        lista_aulas_path = os.path.join(base_dir, lista_aulas_path)

    if output_dir is None:
        output_dir = os.path.join(base_dir, "transcricoes_limpas")
    elif not os.path.isabs(output_dir):
        output_dir = os.path.join(base_dir, output_dir)

    if temp_dir is None:
        temp_dir = os.path.join(base_dir, ".temp_vtt")
    elif not os.path.isabs(temp_dir):
        temp_dir = os.path.join(base_dir, temp_dir)

    if not os.path.exists(lista_aulas_path):
        print(f"[!] Arquivo de lista não encontrado: {lista_aulas_path}")
        print(f"[i] Crie o arquivo '{lista_aulas_path}' com 1 link por linha.")
        return

    with open(lista_aulas_path, "r", encoding="utf-8", errors="ignore") as f:
        urls = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    total = len(urls)
    print("=" * 65)
    print(f"[*] INICIANDO PIPELINE DE EXTRAÇÃO: {total} AULAS IDENTIFICADAS")
    print(f"[*] Destino: {os.path.abspath(output_dir)}")
    print("=" * 65)

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    relatorio = {
        "total": total,
        "sucessos": 0,
        "falhas": 0,
        "detalhes": []
    }

    for idx, url in enumerate(urls, 1):
        nome_aula = f"aula_{idx:02d}"
        dest_txt = os.path.join(output_dir, f"{nome_aula}.txt")

        print(f"\n[{idx:02d}/{total:02d}] Processando: {url}")

        # Se já foi processada anteriormente, não baixa de novo (cache idempotente)
        if os.path.exists(dest_txt) and os.path.getsize(dest_txt) > 50:
            print(f"    [OK] Já processado anteriormente -> {dest_txt}")
            relatorio["sucessos"] += 1
            relatorio["detalhes"].append({"aula": nome_aula, "url": url, "status": "cached", "file": dest_txt})
            continue

        prefixo = f"vtt_{idx:02d}"
        result = download_subtitles_for_url(url, output_prefix=prefixo, temp_dir=temp_dir)

        if result.get("success"):
            vtt_file = result["vtt_files"][0]
            clean_ok = clean_vtt_file(vtt_file, dest_txt)
            if clean_ok:
                tamanho = os.path.getsize(dest_txt)
                print(f"    [+] Sucesso! Legenda limpa salva: {dest_txt} ({tamanho} bytes)")
                relatorio["sucessos"] += 1
                relatorio["detalhes"].append({"aula": nome_aula, "url": url, "status": "success", "file": dest_txt})
            else:
                print(f"    [-] Falha na higienização do VTT.")
                relatorio["falhas"] += 1
                relatorio["detalhes"].append({"aula": nome_aula, "url": url, "status": "cleaner_error"})
        else:
            erro_msg = result.get("error", "Erro desconhecido")
            print(f"    [-] AVISO: Não foi possível obter legenda ({erro_msg})")
            relatorio["falhas"] += 1
            relatorio["detalhes"].append({"aula": nome_aula, "url": url, "status": "failed", "error": erro_msg})

        # Jitter de evasão para evitar bloqueio por IP
        if idx < total:
            tempo_espera = round(random.uniform(min_sleep, max_sleep), 2)
            print(f"    [~] Resfriamento anti-bloqueio: aguardando {tempo_espera}s...")
            time.sleep(tempo_espera)

    # Salva relatório de execução
    relatorio_path = "relatorio_extracao.json"
    with open(relatorio_path, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 65)
    print(f"[*] PROCESSO CONCLUÍDO!")
    print(f"    Total: {total} | Sucesso: {relatorio['sucessos']} | Falhas/Sem Legenda: {relatorio['falhas']}")
    print(f"    Relatório salvo em: {os.path.abspath(relatorio_path)}")
    print("=" * 65)
