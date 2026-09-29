import os
import sys
import argparse
from downloader import process_batch
from cleaner import clean_vtt_file
import glob

def main():
    parser = argparse.ArgumentParser(
        description="Pipeline Automatizado de Extração de Legendas do Vimeo / Nutror (Eduzz)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de Uso:
  python main.py --download               # Baixa e higieniza as legendas de 'lista_aulas.txt'
  python main.py --crawl                  # Abre o Chrome para mapear os links das aulas na Nutror
  python main.py --full                   # Executa o crawler e, em seguida, baixa tudo automaticamente
  python main.py --clean                  # Apenas limpa arquivos .vtt locais já baixados
  python main.py --file minhas_aulas.txt  # Usa uma lista personalizada de links
        """
    )
    
    parser.add_argument("--download", action="store_true", help="Processa a lista de aulas e baixa as legendas")
    parser.add_argument("--crawl", action="store_true", help="Abre o navegador para capturar os links do Vimeo na Nutror")
    parser.add_argument("--full", action="store_true", help="Mapeia na Nutror e baixa tudo em sequência")
    parser.add_argument("--clean", action="store_true", help="Higieniza arquivos .vtt locais")
    parser.add_argument("--file", default="lista_aulas.txt", help="Caminho do arquivo com a lista de URLs (padrão: lista_aulas.txt)")
    parser.add_argument("--out", default="transcricoes_limpas", help="Diretório de saída para os arquivos .txt (padrão: transcricoes_limpas)")
    parser.add_argument("--url", default=None, help="URL direta da página do curso na Nutror para o crawler")

    args = parser.parse_args()

    # Se nenhum argumento foi passado, apresenta menu interativo rápido
    if not (args.download or args.crawl or args.full or args.clean):
        print("=" * 65)
        print("   PIPELINE DE EXTRAÇÃO DE AULAS - NUTROR / VIMEO")
        print("=" * 65)
        print(" 1. Baixar e limpar legendas a partir de 'lista_aulas.txt'")
        print(" 2. Abrir navegador para capturar links do Vimeo na Nutror (Crawler)")
        print(" 3. Modo Completo (Mapear na Nutror + Baixar Legendas)")
        print(" 4. Limpar arquivos .vtt existentes")
        print(" 0. Sair")
        print("-" * 65)
        
        escolha = input("Selecione uma opção [1-4]: ").strip()
        if escolha == "1":
            args.download = True
        elif escolha == "2":
            args.crawl = True
        elif escolha == "3":
            args.full = True
        elif escolha == "4":
            args.clean = True
        else:
            print("Operação cancelada.")
            sys.exit(0)

    # Executa Crawler se solicitado
    if args.crawl or args.full:
        try:
            from crawler import crawl_nutror_course
            crawl_nutror_course(course_url=args.url, output_list_file=args.file)
        except ImportError:
            print("[!] Playwright não encontrado. Para instalar: uv pip install playwright && playwright install chromium")
            sys.exit(1)

    # Executa Downloader se solicitado
    if args.download or args.full:
        process_batch(lista_aulas_path=args.file, output_dir=args.out)

    # Executa apenas limpeza se solicitado
    if args.clean:
        vtt_files = glob.glob(os.path.join(".temp_vtt", "*.vtt"))
        print(f"[*] Limpando {len(vtt_files)} arquivos .vtt locais...")
        for idx, vf in enumerate(vtt_files, 1):
            out_txt = os.path.join(args.out, f"aula_{idx:02d}.txt")
            clean_vtt_file(vf, out_txt)
            print(f"    [+] {vf} -> {out_txt}")
        print("[*] Limpeza concluída!")

if __name__ == "__main__":
    main()
