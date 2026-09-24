"""
MÓDULO DE ANÁLISE ACÚSTICA MULTIMODAL (ÁUDIO REAL)
IBPM CR Automation System - Fase 2 Multimodal

Analisa a curva de energia acústica (RMS) e silêncios naturais (VAD)
para garantir que o LLM só minere cortes onde o orador falou com autoridade
e onde os cortes comecem e terminem em pausas reais de respiração.
"""

import os
import time
import tempfile
import subprocess
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")

class StructlogCompatLogger:
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
    def info(self, msg: str, **kwargs):
        if kwargs:
            extra_str = " ".join(f"{k}={v}" for k, v in kwargs.items())
            self._logger.info(f"{msg} | {extra_str}")
        else:
            self._logger.info(msg)
    def error(self, msg: str, **kwargs):
        if kwargs:
            extra_str = " ".join(f"{k}={v}" for k, v in kwargs.items())
            self._logger.error(f"{msg} | {extra_str}")
        else:
            self._logger.error(msg)

logger = StructlogCompatLogger("AudioEnergyAnalyzer")


class AudioEnergyAnalyzer:
    """
    Extrai o envelope de energia acústica de vídeos/áudios e cruza com a transcrição.
    """

    def __init__(self, sample_rate: int = 16000, window_sec: float = 1.0):
        self.sample_rate = sample_rate
        self.window_sec = window_sec
        self.samples_per_window = int(sample_rate * window_sec)

    def extract_rms_profile(self, media_path: Path) -> np.ndarray:
        """
        Extrai o áudio como PCM 16-bit mono 16kHz via FFmpeg em pipe
        e calcula o RMS por segundo de todo o arquivo com altíssima performance.
        """
        if not media_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado para análise acústica: {media_path}")

        logger.info("Iniciando extração acústica PCM...", file=media_path.name)
        temp_raw = Path(tempfile.gettempdir()) / f"energy_pcm_{os.getpid()}_{time.time_ns()}.raw"
        cmd = [
            "ffmpeg", "-nostdin", "-y", "-loglevel", "error",
            "-i", str(media_path),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ac", "1",
            "-ar", str(self.sample_rate),
            "-f", "s16le",
            str(temp_raw)
        ]

        proc = subprocess.run(cmd, capture_output=True)

        if proc.returncode != 0 or not temp_raw.exists() or temp_raw.stat().st_size == 0:
            err = proc.stderr.decode('utf-8', errors='ignore') if proc.stderr else "Arquivo vazio ou não gerado"
            logger.error("Erro na extração de áudio via FFmpeg", error=err)
            if temp_raw.exists():
                try:
                    temp_raw.unlink()
                except Exception:
                    pass
            raise RuntimeError(f"Falha ao extrair áudio PCM de {media_path}: {err}")

        # Converte bytes brutos para array int16 direto do arquivo temporário
        audio_data = np.fromfile(temp_raw, dtype=np.int16).astype(np.float32)
        try:
            temp_raw.unlink()
        except Exception:
            pass

        total_samples = len(audio_data)
        duracao_total = total_samples / self.sample_rate

        logger.info(f"Áudio extraído: {duracao_total:.1f}s ({duracao_total/60:.1f} min)")

        # Divide em janelas e calcula RMS
        n_windows = int(np.ceil(total_samples / self.samples_per_window))
        rms_values = np.zeros(n_windows, dtype=np.float32)

        for i in range(n_windows):
            start_idx = i * self.samples_per_window
            end_idx = min(start_idx + self.samples_per_window, total_samples)
            chunk = audio_data[start_idx:end_idx]
            if len(chunk) > 0:
                rms_values[i] = np.sqrt(np.mean(chunk**2))

        # Evita log de zero
        rms_values = np.maximum(rms_values, 1.0)
        # Converte para dB relativo
        db_values = 20.0 * np.log10(rms_values / 32768.0)

        # Normaliza para escala 0 a 100 baseada nos percentis da própria pregação
        p_min = np.percentile(db_values, 5)
        p_max = np.percentile(db_values, 95)
        scale_range = max(1.0, p_max - p_min)

        norm_energy = np.clip((db_values - p_min) / scale_range * 100.0, 0.0, 100.0)
        return norm_energy

    def segmentar_transcricao_por_respiracao(
        self,
        words: List[Dict[str, Any]],
        min_block_sec: float = 20.0,
        max_block_sec: float = 85.0,
        min_silence_gap: float = 0.45
    ) -> List[Dict[str, Any]]:
        """
        Agrupa palavras em blocos sintáticos naturais delimitados por pausas reais de respiração.
        Garante que NUNCA haja corte de sílaba no início ou no fim do bloco.
        """
        if not words:
            return []

        # Ordena palavras por start
        sorted_words = sorted(words, key=lambda w: float(w.get("start", 0)))
        blocks = []
        curr_words = []

        for i, w in enumerate(sorted_words):
            curr_words.append(w)
            w_start = float(curr_words[0].get("start", 0))
            w_end = float(curr_words[-1].get("end", 0))
            dur = w_end - w_start

            # Verifica se há pausa de respiração para a próxima palavra
            is_gap = False
            if i + 1 < len(sorted_words):
                next_start = float(sorted_words[i + 1].get("start", 0))
                gap = next_start - w_end
                if gap >= min_silence_gap:
                    is_gap = True

            # Verifica pontuação forte
            text_word = str(w.get("word", "")).strip()
            has_strong_punct = text_word.endswith(('.', '!', '?'))

            # Critérios de fechamento de bloco:
            # 1. Se atingiu a duração mínima (>= 20s) e tem pausa de respiração (>0.45s) ou pontuação forte
            # 2. OU se estourou a duração máxima (>= 80s) e encontrou qualquer pausa (>0.25s)
            should_close = False
            if dur >= min_block_sec and (is_gap or has_strong_punct):
                should_close = True
            elif dur >= max_block_sec and (is_gap or (i + 1 < len(sorted_words) and (float(sorted_words[i+1].get("start", 0)) - w_end) > 0.25)):
                should_close = True

            if should_close:
                block_text = " ".join(str(x.get("word", "")).strip() for x in curr_words)
                blocks.append({
                    "start_sec": round(w_start, 2),
                    "end_sec": round(w_end, 2),
                    "duracao_sec": round(dur, 2),
                    "texto": block_text,
                    "first_word": str(curr_words[0].get("word", "")).strip(),
                    "last_word": str(curr_words[-1].get("word", "")).strip(),
                    "n_words": len(curr_words)
                })
                curr_words = []

        # Adiciona remanescente se tiver ao menos 10 segundos
        if curr_words:
            w_start = float(curr_words[0].get("start", 0))
            w_end = float(curr_words[-1].get("end", 0))
            dur = w_end - w_start
            if dur >= 10.0:
                blocks.append({
                    "start_sec": round(w_start, 2),
                    "end_sec": round(w_end, 2),
                    "duracao_sec": round(dur, 2),
                    "texto": " ".join(str(x.get("word", "")).strip() for x in curr_words),
                    "first_word": str(curr_words[0].get("word", "")).strip(),
                    "last_word": str(curr_words[-1].get("word", "")).strip(),
                    "n_words": len(curr_words)
                })

        return blocks

    def enriquecer_blocos_com_energia(
        self,
        blocks: List[Dict[str, Any]],
        energy_profile: np.ndarray
    ) -> List[Dict[str, Any]]:
        """
        Cruza cada bloco sintático com o envelope de energia acústica
        e atribui métricas de intensidade vocal real.
        """
        total_sec = len(energy_profile)
        p75 = float(np.percentile(energy_profile, 75))
        p50 = float(np.percentile(energy_profile, 50))

        enriched = []
        for idx, b in enumerate(blocks):
            st = int(max(0, b["start_sec"]))
            en = int(min(total_sec, np.ceil(b["end_sec"])))

            if en > st and st < total_sec:
                segment_energy = energy_profile[st:en]
                media_energia = float(np.mean(segment_energy))
                pico_energia = float(np.max(segment_energy))
            else:
                media_energia = 50.0
                pico_energia = 50.0

            # Classificação
            if media_energia >= p75 or pico_energia >= 85.0:
                nivel = "CLIMAX_ALTA"
            elif media_energia >= p50:
                nivel = "MEDIA_CONSTANTE"
            else:
                nivel = "BAIXA_CALMA"

            b_copy = dict(b)
            b_copy["bloco_id"] = idx + 1
            b_copy["energia_media"] = round(media_energia, 1)
            b_copy["energia_pico"] = round(pico_energia, 1)
            b_copy["nivel_energia"] = nivel
            enriched.append(b_copy)

        return enriched
