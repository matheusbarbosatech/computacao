"""
Motor de Visão Computacional e Reframe Inteligente 9:16 - IBPM CR Automation System.
FASE 4 - CINEMATOGRAFIA DE ALTA PRECISÃO (CVXPY + OSQP + FFmpeg sendcmd).

Implementa o algoritmo de reframe cinematográfico global baseado em Programação Quadrática:
1. Rastreamento Anatômico Estável (YOLOv8-Pose / MediaPipe Pose) imune a gesticulações.
2. Lead Room Lookahead (Espaço de Olhar antecipatório via Savitzky-Golay / EMA).
3. Otimização Convexa Global (CVXPY + OSQP):
   - Deadband / Huber Loss para absorver micro-movimentos sem reatividade.
   - Filtragem de Tendência L1 (L1-trend filtering): velocidade nula (v=0) durante pausas, eliminando drift.
   - Amortecimento L2 sobre aceleração e jerk (emulação de tripé hidráulico fluido Sachtler/ARRI).
4. Renderização Assíncrona Nativa com FFmpeg sendcmd (Zero memory piping).
"""

import os
import sys
import json
import subprocess
import tempfile
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Dict, Any, List

from src.core.logger import get_logger
from src.infrastructure.smart_reframe.pipeline import SmartAutoReframePipeline
from src.infrastructure.smart_reframe.optimizer import SmartAutoReframeOptimizer, OptimizerConfig
from src.infrastructure.smart_reframe.speaker_tracker import SpeakerPoseTracker, TrackerConfig
from src.infrastructure.smart_reframe.ffmpeg_orchestrator import FFmpegSendcmdOrchestrator, RenderConfig

logger = get_logger("SmoothAutoReframe")


class SmoothAutoReframe:
    """
    Fachada (Facade) para o Pipeline Smart Auto-Reframe 9:16 Cinematográfico.
    Garante retrocompatibilidade completa com os serviços existentes (ex: tratamento_audiovisual.py).
    """

    def __init__(
        self,
        target_width: int = 1080,
        target_height: int = 1920,
        optimizer_config: Optional[OptimizerConfig] = None,
        tracker_config: Optional[TrackerConfig] = None,
        render_config: Optional[RenderConfig] = None
    ):
        self.target_w = target_width
        self.target_h = target_height
        self.optimizer_config = optimizer_config or OptimizerConfig()
        self.tracker_config = tracker_config or TrackerConfig()
        self.render_config = render_config or RenderConfig(target_width=target_width, target_height=target_height)

        self.smart_pipeline = SmartAutoReframePipeline(
            target_width=self.target_w,
            target_height=self.target_h,
            optimizer_config=self.optimizer_config,
            tracker_config=self.tracker_config,
            render_config=self.render_config
        )
        logger.info("🎬 Motor SmoothAutoReframe inicializado com arquitetura de Otimização Convexa Global (CVXPY/OSQP).")

    def _probe_video_dimensions(self, video_path: str) -> Tuple[int, int]:
        """Obtém dimensões reais do vídeo via ffprobe."""
        vid_w, vid_h, _ = self.smart_pipeline.probe_video_dimensions_and_fps(video_path)
        return vid_w, vid_h

    def analyze_video_smart_crop(
        self,
        video_path: str,
        start_sec: float,
        duration_sec: float,
        sample_fps: int = 8,
        sendcmd_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Analisa o vídeo com rastreamento anatômico de pose, isola o pregador,
        aplica regras cinematográficas de Lead Room / Headroom, resolve a Programação
        Quadrática Global via CVXPY/OSQP e gera o arquivo sendcmd.txt.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Vídeo original não encontrado para rastreamento: {video_path}")

        # Atualiza taxa de amostragem no tracker se fornecido
        self.smart_pipeline.tracker_config.sample_fps = sample_fps
        self.smart_pipeline.tracker.config.sample_fps = sample_fps

        logger.info(
            f"🔍 Iniciando Smart Auto-Reframe (CVXPY + OSQP + sendcmd) | "
            f"Arquivo: {Path(video_path).name} | Trecho: {start_sec:.2f}s -> {start_sec + duration_sec:.2f}s"
        )

        return self.smart_pipeline.analyze_trajectory(
            video_path=video_path,
            start_sec=start_sec,
            duration_sec=duration_sec,
            sendcmd_dir=sendcmd_dir
        )