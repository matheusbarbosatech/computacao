/**
 * EXTRATOR INTELIGENTE NUTROR (VIMEO) - VERSÃO 2.0 (ANTI-MENU OCULTO)
 * Funciona mesmo com o menu espremido/fechado!
 * Ele clica automaticamente no botão "Próxima Aula" a cada 2.5 segundos
 * e captura todos os vídeos em sequência até o fim do curso.
 */
(async function extractNutrorAutoNext() {
    console.log("%c[+] INICIANDO EXTRATOR NUTROR V2.0...", "color: #22c55e; font-size: 16px; font-weight: bold;");

    const vimeoLinks = [];
    const seenIds = new Set();

    function grabVimeo() {
        const iframes = document.querySelectorAll('iframe');
        for (const f of iframes) {
            const src = f.src || f.getAttribute('data-src') || '';
            if (src.includes('vimeo.com')) {
                const clean = src.split('&')[0];
                const match = clean.match(/\/video\/(\d+)/);
                const vidId = match ? match[1] : clean;
                
                if (!seenIds.has(vidId)) {
                    seenIds.add(vidId);
                    vimeoLinks.push(clean);
                    console.log(`%c[+] AULA CAPTURADA (${vimeoLinks.length}): ${clean}`, "color: #38bdf8; font-size: 13px; font-weight: bold;");
                }
            }
        }
    }

    // 1. Captura o vídeo atual na tela
    grabVimeo();

    // 2. Se o menu estiver fechado (hambúrguer ≡), tenta abrir
    const menuBtn = document.querySelector('button[aria-label*="menu"], header button, .v-app-bar__nav-icon');
    if (menuBtn && !document.querySelector('.v-navigation-drawer--open, .sidebar-open')) {
        try { menuBtn.click(); await new Promise(r => setTimeout(r, 800)); } catch(e){}
    }

    // 3. Procura o botão "Próxima Aula"
    function getNextButton() {
        const allClickables = Array.from(document.querySelectorAll('button, a, div[role="button"]'));
        return allClickables.find(el => {
            const txt = (el.innerText || el.getAttribute('aria-label') || '').toLowerCase().trim();
            const isNext = (txt.includes('próxim') || txt.includes('proxim') || txt.includes('avançar') || txt === '>') && !txt.includes('anterior');
            return isNext && el.offsetParent !== null && !el.disabled;
        });
    }

    console.log("%c[*] Avançando automaticamente pelas aulas através do botão 'Próxima Aula'...", "color: #a855f7; font-size: 13px;");

    let maxAulas = 45; // limite de segurança para 40 aulas
    let rodadasSemMudar = 0;

    for (let i = 0; i < maxAulas; i++) {
        const nextBtn = getNextButton();
        if (!nextBtn) {
            console.log("%c[*] Botão 'Próxima Aula' não encontrado ou chegamos na última aula!", "color: #fbbf24; font-weight: bold;");
            break;
        }

        const qtdAntes = vimeoLinks.length;
        nextBtn.click();
        console.log(`[>>] Clicou em Próxima Aula... aguardando 2.5s para carregar o vídeo...`);
        
        await new Promise(r => setTimeout(r, 2500));
        grabVimeo();

        if (vimeoLinks.length === qtdAntes) {
            rodadasSemMudar++;
            if (rodadasSemMudar >= 3) {
                console.log("[i] Chegamos ao fim das aulas ou o próximo conteúdo é texto/quiz.");
                break;
            }
        } else {
            rodadasSemMudar = 0;
        }
    }

    // 4. Exportação final dos links capturados
    if (vimeoLinks.length === 0) {
        alert("Nenhum vídeo foi detectado. Certifique-se de estar com o vídeo da aula aberto.");
        return;
    }

    const textContent = vimeoLinks.join('\n');
    
    // Baixa o arquivo lista_aulas.txt
    const blob = new Blob([textContent], { type: 'text/plain;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'lista_aulas.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    console.log(`%c=====================================================`, "color: #22c55e;");
    console.log(`%c[SUCESSO TOTAL] ${vimeoLinks.length} AULAS CAPTURADAS!`, "color: #22c55e; font-size: 16px; font-weight: bold;");
    console.log(`%cArquivo 'lista_aulas.txt' baixado para sua pasta de Downloads.`, "color: #22c55e;");
    console.log(`%c=====================================================`, "color: #22c55e;");
})();
