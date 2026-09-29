import re
import os

def clean_vtt_content(vtt_raw_text: str) -> str:
    """
    Remove cabeçalhos WebVTT, timestamps, tags HTML (<c>, <b>, etc.)
    e deduplica linhas repetidas geradas por legendas automáticas.
    """
    lines = vtt_raw_text.splitlines()
    cleaned_lines = []
    
    # Regex para timestamps: 00:00:01.000 --> 00:00:04.000 ou 00:01.000 --> 00:04.000
    timestamp_pattern = re.compile(r'^\d{2}:(?:\d{2}:)?\d{2}\.\d{3}\s+-->\s+\d{2}:(?:\d{2}:)?\d{2}\.\d{3}')
    # Regex para tags HTML e cue tags (<c>, </b>, <00:01:23.456>, etc.)
    tag_pattern = re.compile(r'<[^>]+>')
    
    prev_line = ""
    for line in lines:
        line = line.strip()
        
        # Ignora cabeçalhos WebVTT e metadados
        if not line:
            continue
        if line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if line.startswith("NOTE") or line.isdigit():
            continue
        
        # Ignora linhas de timestamp
        if timestamp_pattern.search(line):
            continue
            
        # Remove tags HTML
        line_clean = tag_pattern.sub('', line).strip()
        if not line_clean:
            continue
            
        # Deduplicação de linhas consecutivas idênticas (comum em legendas rolantes)
        if line_clean == prev_line:
            continue
            
        cleaned_lines.append(line_clean)
        prev_line = line_clean

    # Junta linhas em parágrafos coerentes
    text_content = " ".join(cleaned_lines)
    
    # Normaliza espaços múltiplos
    text_content = re.sub(r'\s+', ' ', text_content).strip()
    
    # Quebra em parágrafos lógicos após pontos finais seguidos de maiúsculas
    text_content = re.sub(r'(\.|\!|\?)\s+([A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ])', r'\1\n\n\2', text_content)
    
    return text_content


def clean_vtt_file(input_vtt_path: str, output_txt_path: str) -> bool:
    """
    Lê um arquivo .vtt, processa o texto e salva em .txt limpo.
    """
    try:
        with open(input_vtt_path, 'r', encoding='utf-8', errors='ignore') as f:
            raw_text = f.read()
            
        cleaned = clean_vtt_content(raw_text)
        
        os.makedirs(os.path.dirname(os.path.abspath(output_txt_path)), exist_ok=True)
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
            
        return True
    except Exception as e:
        print(f"[-] Erro ao limpar arquivo {input_vtt_path}: {e}")
        return False
