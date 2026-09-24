"""
Gerador de Legendas ASS Dinâmicas Estilo TikTok / Reels (Open Captions).
IBPM CR Automation System - Fase 3.
"""

import re
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class AssSubtitleGenerator:
    """
    Gera arquivos de legenda .ass com tipografia moderna (Impact / Arial Black)
    em branco sólido com contorno preto grosso, respeitando pausas e sem repetições.
    """
    HEADER_TEMPLATE = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Impact,78,&H00FFFFFF,&H00000000,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,2,40,40,260,1
Style: Headline,Impact,60,&H00FFFFFF,&H00000000,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,2,8,40,40,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    @staticmethod
    def format_timestamp(seconds: float) -> str:
        seconds = max(0.0, seconds)
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        cs = int((seconds - int(seconds)) * 100)
        return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"

    def generate_ass(
        self,
        word_events: Optional[List[Dict[str, Any]]],
        text_snippet: str,
        start_offset_sec: float,
        duration_sec: float,
        output_ass: Path,
        time_scale: float = 1.0,
        headline_topo: Optional[str] = None,
        palavras_enfase: Optional[List[str]] = None
    ) -> Path:
        """
        Gera o arquivo .ass formatado no disco com:
        1. Frases naturais e ritmo calmo (5 a 7 palavras por bloco).
        2. Respiração adequada (permanência de 2.0s a 3.5s por tela).
        3. Quebra balanceada em 2 linhas (\\N) para blocos médios.
        4. Karaokê suave iluminando a palavra ativa em Amarelo Ouro (&H00D7FF&).
        """
        output_ass.parent.mkdir(parents=True, exist_ok=True)
        lines = [self.HEADER_TEMPLATE.strip()]

        # Adiciona Headline Superior Fixa se fornecida explicitamente
        if headline_topo and headline_topo.strip():
            clean_head = headline_topo.strip()
            headline_event = f"Dialogue: 1,0:00:00.00,{self.format_timestamp(duration_sec)},Headline,,0,0,0,,{{\\fad(200,200)}}{clean_head}"
            lines.append(headline_event)

        enfase_set = set(p.strip().upper() for p in (palavras_enfase or []) if p.strip())

        if word_events and len(word_events) > 0:
            # 1. Deduplicação inteligente de palavras por timestamp e texto
            seen_words = {}
            for w in word_events:
                raw_s = float(w.get("start_sec", w.get("start", 0.0)))
                raw_e = float(w.get("end_sec", w.get("end", raw_s + 0.35)))
                
                t_s = round((raw_s - start_offset_sec) * time_scale, 2)
                t_e = round((raw_e - start_offset_sec) * time_scale, 2)
                t_e = max(t_s + 0.15, t_e)

                if t_s < 0.0 or t_s >= duration_sec:
                    continue
                t_e = min(duration_sec, t_e)
                
                w_text = str(w.get("word", w.get("raw_word", ""))).strip()
                if not w_text:
                    continue

                key = (round(t_s, 2), w_text.lower())
                if key not in seen_words:
                    seen_words[key] = {
                        "word": w_text,
                        "start": t_s,
                        "end": t_e
                    }

            clean_words = sorted(seen_words.values(), key=lambda x: x["start"])

            # 2. Agrupamento em frases completas e confortáveis (7 a 9 palavras, até 48 caracteres)
            chunks = []
            curr_chunk = []
            max_words_per_chunk = 8
            max_chars_per_chunk = 48

            for w in clean_words:
                if not curr_chunk:
                    curr_chunk.append(w)
                    continue

                prev_w = curr_chunk[-1]
                gap = w["start"] - prev_w["end"]
                has_strong_punct = prev_w["word"].endswith(('.', '?', '!'))
                curr_text = " ".join(x["word"] for x in curr_chunk)
                new_text = curr_text + " " + w["word"]

                # Quebra em pausa real (>0.85s) OU pontuação forte com ao menos 4 palavras OU estourou limites
                exceeded_limits = len(curr_chunk) >= max_words_per_chunk or len(new_text) > max_chars_per_chunk
                if gap > 0.85 or (has_strong_punct and len(curr_chunk) >= 4) or exceeded_limits:
                    chunks.append(curr_chunk)
                    curr_chunk = [w]
                else:
                    curr_chunk.append(w)

            if curr_chunk:
                chunks.append(curr_chunk)

            # Pós-processamento de fluidez: se bloco for muito curto (<2.2s) e o próximo começar rápido (<0.75s), funde
            merged_chunks = []
            ci = 0
            while ci < len(chunks):
                c = chunks[ci]
                dur_c = c[-1]["end"] - c[0]["start"]
                if dur_c < 2.2 and ci + 1 < len(chunks):
                    next_c = chunks[ci + 1]
                    gap_to_next = next_c[0]["start"] - c[-1]["end"]
                    combined_len = len(" ".join(x["word"] for x in (c + next_c)))
                    if gap_to_next < 0.75 and combined_len <= 52:
                        merged_chunks.append(c + next_c)
                        ci += 2
                        continue
                merged_chunks.append(c)
                ci += 1

            # 3. Montagem dos eventos ASS com Karaokê Ativo Suave e Sem Nenhuma Sobreposição
            raw_events = []
            for i, ch in enumerate(merged_chunks):
                t_chunk_start = ch[0]["start"]
                if i + 1 < len(merged_chunks):
                    next_start = merged_chunks[i + 1][0]["start"]
                    t_chunk_limit = min(ch[-1]["end"] + 0.35, next_start)
                else:
                    t_chunk_limit = min(duration_sec, ch[-1]["end"] + 0.35)

                n_words = len(ch)
                total_text_len = sum(len(x["word"]) for x in ch) + n_words - 1
                break_idx = n_words // 2 if (n_words >= 5 or total_text_len > 24) else -1

                for w_idx in range(n_words):
                    active_w = ch[w_idx]
                    w_start = active_w["start"]
                    if w_idx + 1 < n_words:
                        w_end = ch[w_idx + 1]["start"]
                    else:
                        w_end = t_chunk_limit

                    colored_tokens = []
                    for k, w_item in enumerate(ch):
                        raw_w_up = w_item["word"].upper()
                        if k == w_idx:
                            # Palavra falada no momento: Amarelo Ouro Vivo
                            colored_tokens.append(f"{{\\c&H00D7FF&}}{raw_w_up}{{\\c&HFFFFFF&}}")
                        elif enfase_set and any(enf in raw_w_up for enf in enfase_set):
                            # Palavra-chave de ênfase: Laranja Ouro
                            colored_tokens.append(f"{{\\c&H00A5FF&}}{raw_w_up}{{\\c&HFFFFFF&}}")
                        else:
                            # Palavra normal: Branco sólido
                            colored_tokens.append(raw_w_up)

                    if 0 < break_idx < len(colored_tokens):
                        line_str = " ".join(colored_tokens[:break_idx]) + "\\N" + " ".join(colored_tokens[break_idx:])
                    else:
                        line_str = " ".join(colored_tokens)

                    raw_events.append({"start": w_start, "end": w_end, "text": line_str})

            # Sanitização Monotônica Global: Garante que cur.end <= next.start
            # Elimina 100% de sobreposições que causavam o empilhamento vertical/solavanco no libass
            sanitized = []
            last_end = 0.0
            for ev in raw_events:
                s = max(last_end, ev["start"])
                e = max(s + 0.05, ev["end"])
                sanitized.append({"start": s, "end": e, "text": ev["text"]})
                last_end = s

            for idx in range(len(sanitized)):
                cur = sanitized[idx]
                if idx + 1 < len(sanitized):
                    nxt = sanitized[idx + 1]
                    if cur["end"] > nxt["start"]:
                        cur["end"] = nxt["start"]
                if cur["end"] > duration_sec:
                    cur["end"] = duration_sec

                if cur["end"] > cur["start"] + 0.03:
                    dialogue_line = f"Dialogue: 0,{self.format_timestamp(cur['start'])},{self.format_timestamp(cur['end'])},Default,,0,0,0,,{cur['text']}"
                    lines.append(dialogue_line)

        elif text_snippet:
            # Fallback por texto corrido com chunks curtos
            words = str(text_snippet).split()
            chunk_size = 4
            total_duration = max(1.0, duration_sec)
            time_per_word = total_duration / max(1, len(words))

            for i in range(0, len(words), chunk_size):
                chunk = words[i:i + chunk_size]
                t_start = i * time_per_word
                t_end = min(total_duration, (i + len(chunk)) * time_per_word)
                formatted_words = [w.upper() for w in chunk]
                line_str = " ".join(formatted_words)
                dialogue_line = f"Dialogue: 0,{self.format_timestamp(t_start)},{self.format_timestamp(t_end)},Default,,0,0,0,,{line_str}"
                lines.append(dialogue_line)

        output_ass.write_text("\n".join(lines), encoding="utf-8")
        n_falas = len(lines) - 1  # 1 elemento = bloco do header completo
        logger.info(f"✅ Arquivo de legendas ASS gerado com sucesso: {output_ass.name} ({n_falas} falas, scale={time_scale:.4f})")
        return output_ass
