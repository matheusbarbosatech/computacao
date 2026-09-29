import os
import sys
import time
import re
from playwright.sync_api import sync_playwright

def crawl_nutror_course(
    course_url: str = None,
    output_list_file: str = None,
    session_dir: str = None
):
    """
    Inicia o navegador Playwright com perfil persistente, permitindo que o usuário
    faça login na Nutror e navegue pelas aulas, extraindo automaticamente os iframes do Vimeo.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if output_list_file is None:
        output_list_file = os.path.join(base_dir, "lista_aulas.txt")
    elif not os.path.isabs(output_list_file):
        output_list_file = os.path.join(base_dir, output_list_file)

    if session_dir is None:
        session_dir = os.path.join(base_dir, ".nutror_session")
    elif not os.path.isabs(session_dir):
        session_dir = os.path.join(base_dir, session_dir)

    os.makedirs(session_dir, exist_ok=True)
    vimeo_links = []
    seen_vimeo_ids = set()

    print("=" * 65)
    print("[*] INICIANDO CRAWLER INTELIGENTE NUTROR -> VIMEO")
    print("[*] O navegador será aberto. Faça login se necessário.")
    print("=" * 65)

    with sync_playwright() as p:
        # Tenta conectar em uma instância do Chrome já aberta com depuração (--remote-debugging-port=9222)
        connected_cdp = False
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222", timeout=3000)
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else context.new_page()
            connected_cdp = True
            print("[+] Conectado com sucesso ao seu Google Chrome já aberto via porta 9222!")
        except Exception:
            # Fallback para abrir nova janela com perfil dedicado
            context = p.chromium.launch_persistent_context(
                user_data_dir=os.path.abspath(session_dir),
                headless=False,
                channel="chrome",
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = context.new_page()


        # Interceptador de rede: captura URLs do Vimeo mesmo que estejam ocultas ou em Shadow DOM
        def handle_request(request):
            url = request.url
            if "player.vimeo.com/video/" in url:
                # Extrai o link base do player com o hash ?h= se existir
                clean_url = url.split("?")[0]
                hash_match = re.search(r'h=([a-zA-Z0-9]+)', url)
                if hash_match:
                    clean_url += f"?h={hash_match.group(1)}"
                
                vid_id_match = re.search(r'/video/(\d+)', clean_url)
                if vid_id_match:
                    vid_id = vid_id_match.group(1)
                    if vid_id not in seen_vimeo_ids:
                        seen_vimeo_ids.add(vid_id)
                        vimeo_links.append(clean_url)
                        print(f"\n[+] VIMEO DETECTADO NA REDE: {clean_url}")
                        # Salva imediatamente no arquivo para não perder nada
                        with open(output_list_file, "a", encoding="utf-8") as f:
                            f.write(clean_url + "\n")

        page.on("request", handle_request)

        # Navega para a URL fornecida ou para a home da Nutror
        target_url = course_url if course_url else "https://app.nutror.com/"
        print(f"[*] Navegando para: {target_url}")
        page.goto(target_url)

        print("\n" + "#" * 65)
        print("[i] INSTRUÇÕES:")
        print(" 1. Faça seu login na Nutror na janela aberta do Chrome.")
        print(" 2. Acesse o curso 'Clube do Consultor'.")
        print(" 3. Você pode clicar nas aulas pelo menu lateral OU deixar o bot varrer.")
        print(" 4. Conforme os vídeos carregam, os links do Vimeo são salvos automaticamente.")
        print(" 5. Quando terminar de mapear as 40 aulas, volte aqui e pressione ENTER.")
        print("#" * 65 + "\n")

        # Modo automático opcional: tentar varrer links da sidebar
        resposta = input("Deseja tentar extração automática pelo menu lateral das aulas? (s/n): ").strip().lower()
        
        if resposta == 's':
            print("\n[*] Procurando links de aulas na página atual...")
            time.sleep(3)
            # Localiza seletores comuns de aulas na Nutror
            links_aulas = page.query_selector_all("a[href*='/aula/'], a[href*='/lesson/'], div[data-lesson-id], div[class*='lesson']")
            print(f"[*] Elementos de aula encontrados: {len(links_aulas)}")
            
            hrefs = []
            for el in links_aulas:
                href = el.get_attribute("href")
                if href and href not in hrefs:
                    if href.startswith("/"):
                        href = "https://app.nutror.com" + href
                    hrefs.append(href)

            print(f"[*] Total de {len(hrefs)} URLs de aulas mapeadas no menu. Acessando sequencialmente...")
            for idx, h in enumerate(hrefs, 1):
                print(f"[{idx}/{len(hrefs)}] Acessando aula: {h}")
                try:
                    page.goto(h, timeout=20000)
                    time.sleep(3)  # Aguarda carregamento do iframe do Vimeo
                    
                    # Procura iframe diretamente no DOM
                    frames = page.frames
                    for frame in frames:
                        if "vimeo.com" in frame.url:
                            if frame.url not in vimeo_links:
                                vimeo_links.append(frame.url)
                                with open(output_list_file, "a", encoding="utf-8") as f:
                                    f.write(frame.url + "\n")
                                print(f"    [+] Iframe localizado: {frame.url}")
                except Exception as e:
                    print(f"    [-] Falha ao carregar aula {h}: {e}")
                    continue
        else:
            print("\n[*] Modo Manual Assistido ativo: Apenas clique nas aulas na tela do Chrome.")
            print("[*] Cada aula clicada terá o link do Vimeo capturado instantaneamente.")
            input("\n[Pressione ENTER quando tiver navegado por todas as aulas para finalizar]...")

        context.close()

    print("\n" + "=" * 65)
    print(f"[*] MAPEAMENTO FINALIZADO!")
    print(f"[*] Total de links do Vimeo capturados: {len(vimeo_links)}")
    print(f"[*] Salvo em: {os.path.abspath(output_list_file)}")
    print("=" * 65)
    return vimeo_links
