// ==========================================================================
// CYBERDEFENSE 3D — SISTEMA DE INTELIGÊNCIA DE NPCS & CORPMESSENGER
// ==========================================================================

const NPCS = {
    ciso: {
        id: "ciso",
        nome: "Marcos",
        cargo: "CISO / Gestor Geral de Segurança",
        avatar: "👔",
        setor: "Diretoria de Segurança",
        vozPitch: 0.9,
        dialogo3d: {
            inicial: {
                fala: "Matheus! Bom dia. Como estão as métricas de resposta a incidentes hoje? O conselho de administração me pediu o relatório preliminar do mês até as 17h. Preciso de tolerância zero com tempo de parada!",
                opcoes: [
                    { texto: "Fica tranquilo, Marcos. A fila de triagem tá 100% monitorada e sob controle.", rep: +5, resposta: "Excelente postura. É dessa proatividade que a diretoria precisa." },
                    { texto: "Tô com muita demanda acumulada, chefe... Talvez atrase um pouco.", rep: -5, resposta: "Atrasar não é opção quando temos SLA contratual com clientes, Matheus. Priorize os críticos!" },
                    { texto: "O que o conselho tá mais preocupado hoje?", rep: +2, resposta: "Ransomware e vazamento de dados de clientes (LGPD). Qualquer tráfego anômalo deve ser isolado imediatamente." }
                ]
            }
        }
    },
    senior: {
        id: "senior",
        nome: "Ricardo",
        cargo: "Analista N3 / Especialista em Forense",
        avatar: "☕",
        setor: "SOC Avançado & Threat Hunting",
        vozPitch: 0.8,
        dialogo3d: {
            inicial: {
                fala: "E aí, novato. Pegou seu café já? Olha, se pintar pacote malformado de DNS ou porta esquisita no firewall, não vai direto reiniciando serviço. Extrai o PCAP no Wireshark primeiro pra gente ver o payload.",
                opcoes: [
                    { texto: "Com certeza, Ricardo. Evidência forense em primeiro lugar antes de mitigar.", rep: +5, resposta: "Aí sim. Tá aprendendo rápido. Qualquer dúvida com comando esotérico de Linux me dá um toque." },
                    { texto: "Pode deixar que eu já bloqueio o IP direto no MikroTik pra cortar o mal pela raiz!", rep: 0, resposta: "Bloquear é bom, mas se não mapear o C2, eles mudam de IP em 30 segundos. Fica a dica." }
                ]
            }
        }
    },
    intern: {
        id: "intern",
        nome: "Lucas",
        cargo: "Estagiário de Cibersegurança",
        avatar: "🎒",
        setor: "SOC N1 (Seu companheiro de baia)",
        vozPitch: 1.1,
        dialogo3d: {
            inicial: {
                fala: "Cara, Matheus... ainda bem que você chegou! Eu tava olhando os logs de madrugada e vi centenas de conexões rejeitadas na porta 22. Achei que o servidor tinha caído! Você me ensina a filtrar isso?",
                opcoes: [
                    { texto: "Calma, Lucas! Isso é só port scan automatizado da internet. Vou te mostrar a regra de blacklist.", rep: +5, resposta: "Ufa, que alívio! Valeu demais cara, você é fera." },
                    { texto: "Depois eu vejo isso, agora tô focado nos meus chamados.", rep: -3, resposta: "Tranquilo... vou tentar ler a documentação do Wazuh aqui sozinho..." }
                ]
            }
        }
    },
    finance: {
        id: "finance",
        nome: "Juliana",
        cargo: "Analista Financeira",
        avatar: "💼",
        setor: "Financeiro & Contas a Pagar",
        vozPitch: 1.2,
        dialogo3d: {
            inicial: {
                fala: "Matheus! Eu recebi um e-mail de um fornecedor dizendo que uma fatura tá vencendo hoje. Tem um anexo 'fatura.pdf.exe'... Posso abrir pra pagar?",
                opcoes: [
                    { texto: "NÃO ABRA DE JEITO NENHUM! Isso é extensão dupla maliciosa. Vou isolar seu e-mail agora.", rep: +10, resposta: "Meu Deus! Quase que eu cliquei! Muito obrigada pelo aviso rápido!" },
                    { texto: "Se o remetente for de confiança, dá uma olhada rápida...", rep: -20, resposta: "Ai meu Deus, cliquei e a tela travou! Socorro!" }
                ]
            }
        }
    }
};

// Histórico e Mensagens Iniciais do CorpChat
const CHAT_DATABASE = {
    "soc-geral": [
        { autor: "Marcos (CISO)", role: "Gestor", avatar: "👔", hora: "08:02", texto: "Bom dia equipe SOC! Plantão iniciado. Atenção especial às tentativas de invasão externa registradas no final de semana." },
        { autor: "Ricardo (Senior)", role: "N3", avatar: "☕", hora: "08:05", texto: "Bom dia. Servidores atualizados com o último patch do kernel. Se alguém precisar de auxílio com análise de malware, me chamem no privado." },
        { autor: "Lucas (Estagiário)", role: "N1", avatar: "🎒", hora: "08:10", texto: "Bom dia pessoal! Café tá fresco na copa ☕" }
    ],
    "geral-empresa": [
        { autor: "RH Corporativo", role: "RH", avatar: "📢", hora: "08:00", texto: "Lembrete: O treinamento obrigatório de conscientização sobre Phishing vence nesta sexta-feira!" },
        { autor: "Pedro (Dev)", role: "Engenharia", avatar: "💻", hora: "08:12", texto: "Alguém do SOC pode liberar a porta 8080 pra gente testar a nova API de pagamentos?" }
    ],
    "ciso": [
        { autor: "Marcos (CISO)", role: "Gestor", avatar: "👔", hora: "08:05", texto: "Matheus, quando tiver 5 minutos, me dê o parecer sobre aquele falso positivo de sexta-feira. Bom plantão!" }
    ],
    "senior": [
        { autor: "Ricardo (Senior)", role: "N3", avatar: "☕", hora: "08:15", texto: "Dica do dia pro seu turno: sempre confira o cabeçalho SPF/DKIM antes de liberar qualquer e-mail da quarentena." }
    ],
    "intern": [
        { autor: "Lucas (Estagiário)", role: "N1", avatar: "🎒", hora: "08:20", texto: "Matheus, você usa o comando 'grep' ou 'jq' pra parsear JSON de logs do Suricata? Tô apanhando aqui kkk" }
    ],
    "finance": [
        { autor: "Juliana (Financeiro)", role: "Financeiro", avatar: "💼", hora: "08:28", texto: "Oi Matheus! Tudo bem? Tô com uma dúvida sobre uma nota fiscal estranha que chegou aqui..." }
    ]
};

// Voice Speech Synthesizer (Nativo do navegador)
function falarVozNpc(texto, pitch = 1.0) {
    try {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(texto);
            utterance.lang = 'pt-BR';
            utterance.rate = 1.05;
            utterance.pitch = pitch;
            window.speechSynthesis.speak(utterance);
        }
    } catch (e) {
        console.warn("TTS não disponível ou bloqueado pelo navegador", e);
    }
}
