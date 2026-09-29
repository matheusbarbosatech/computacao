import os
import subprocess
import json

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>{{TITLE}}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;700&family=Orbitron:wght@700;900&family=Inter:wght@400;500;600;700&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }

        @page {
            size: 210mm 297mm;
            margin: 0;
        }

        body {
            background-color: #070312;
            color: #e2e8f0;
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            line-height: 1.6;
        }

        .page {
            width: 210mm;
            height: 297mm;
            page-break-after: always;
            position: relative;
            background: #070312 radial-gradient(circle at 50% 20%, rgba(147, 51, 234, 0.18) 0%, transparent 70%);
            background-image: 
                radial-gradient(rgba(168, 85, 247, 0.15) 1px, transparent 1px),
                radial-gradient(circle at 50% 20%, rgba(147, 51, 234, 0.18) 0%, transparent 70%);
            background-size: 24px 24px, 100% 100%;
            padding: 24mm 20mm;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* Scanline effect */
        .page::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(rgba(18, 16, 38, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
            background-size: 100% 4px;
            pointer-events: none;
            z-index: 10;
        }

        /* Corner Cyber Accents */
        .corner-tl, .corner-tr, .corner-bl, .corner-br {
            position: absolute;
            width: 16px;
            height: 16px;
            border-color: #a855f7;
            pointer-events: none;
        }
        .corner-tl { top: 12mm; left: 12mm; border-top: 2px solid; border-left: 2px solid; }
        .corner-tr { top: 12mm; right: 12mm; border-top: 2px solid; border-right: 2px solid; }
        .corner-bl { bottom: 12mm; left: 12mm; border-bottom: 2px solid; border-left: 2px solid; }
        .corner-br { bottom: 12mm; right: 12mm; border-bottom: 2px solid; border-right: 2px solid; }

        /* Header / Footer */
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(168, 85, 247, 0.3);
            padding-bottom: 8px;
            margin-bottom: 20px;
            font-family: 'Fira Code', monospace;
            font-size: 10px;
            color: #a855f7;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .page-footer {
            margin-top: auto;
            border-top: 1px solid rgba(168, 85, 247, 0.3);
            padding-top: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: 'Fira Code', monospace;
            font-size: 10px;
            color: #94a3b8;
        }

        /* Badges */
        .cyber-badge {
            display: inline-block;
            padding: 3px 8px;
            font-family: 'Fira Code', monospace;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            border-radius: 2px;
            letter-spacing: 0.5px;
        }
        .badge-green {
            background: rgba(34, 197, 94, 0.15);
            border: 1px solid #22c55e;
            color: #4ade80;
        }
        .badge-purple {
            background: rgba(168, 85, 247, 0.2);
            border: 1px solid #a855f7;
            color: #c084fc;
        }
        .badge-amber {
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid #f59e0b;
            color: #fbbf24;
        }

        /* Typography */
        h1.cyber-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 26px;
            color: #ffffff;
            letter-spacing: 1px;
            margin-bottom: 8px;
            text-shadow: 0 0 10px rgba(168, 85, 247, 0.5);
        }
        h2.cyber-subtitle {
            font-family: 'Fira Code', monospace;
            font-size: 13px;
            color: #a3e635;
            margin-bottom: 20px;
        }
        h3.section-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 15px;
            color: #c084fc;
            margin: 16px 0 8px 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Terminal Component */
        .terminal-box {
            background: #05020c;
            border: 1px solid rgba(168, 85, 247, 0.5);
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.15);
            border-radius: 4px;
            margin: 14px 0;
            overflow: hidden;
            font-family: 'Fira Code', monospace;
        }
        .terminal-header {
            background: #110726;
            border-bottom: 1px solid rgba(168, 85, 247, 0.3);
            padding: 6px 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 10px;
            color: #94a3b8;
        }
        .terminal-buttons {
            display: flex;
            gap: 6px;
        }
        .terminal-btn {
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }
        .btn-red { background: #ef4444; }
        .btn-yellow { background: #f59e0b; }
        .btn-green { background: #10b981; }

        .terminal-content {
            padding: 12px 14px;
            font-size: 11.5px;
            color: #38bdf8;
            line-height: 1.5;
        }
        .prompt { color: #a3e635; }
        .cmd { color: #ffffff; font-weight: bold; }
        .comment { color: #64748b; }
        .output { color: #e2e8f0; }

        /* Card Component */
        .cyber-card {
            background: rgba(15, 7, 36, 0.7);
            border: 1px solid rgba(168, 85, 247, 0.3);
            border-left: 3px solid #a855f7;
            border-radius: 3px;
            padding: 14px 16px;
            margin: 12px 0;
        }
        .cyber-card.alert {
            border-left-color: #ef4444;
            background: rgba(30, 10, 20, 0.7);
            border-color: rgba(239, 68, 68, 0.4);
        }
        .cyber-card.success {
            border-left-color: #22c55e;
            background: rgba(10, 30, 20, 0.7);
            border-color: rgba(34, 197, 94, 0.4);
        }

        /* Grid */
        .cyber-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 14px;
            margin: 14px 0;
        }

        /* COVER PAGE STYLES */
        .cover-page {
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 30mm 20mm;
        }
        .cover-meta {
            font-family: 'Fira Code', monospace;
            font-size: 10px;
            color: #a855f7;
            letter-spacing: 2px;
            margin-bottom: 25px;
        }
        .cover-main-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 38px;
            font-weight: 900;
            color: #ffffff;
            line-height: 1.1;
            margin-bottom: 14px;
            text-shadow: 0 0 20px rgba(168, 85, 247, 0.8);
        }
        .cover-highlight {
            background: #9333ea;
            color: #ccff00;
            padding: 2px 10px;
            border-radius: 4px;
            display: inline-block;
        }
        .cover-subtitle {
            font-family: 'Fira Code', monospace;
            font-size: 14px;
            color: #cbd5e1;
            margin-bottom: 40px;
            letter-spacing: 0.5px;
        }
        .cover-logo-badge {
            margin-top: auto;
            font-family: 'Orbitron', sans-serif;
            font-size: 16px;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: 2px;
        }
        .cover-logo-badge span {
            background: #ccff00;
            color: #05020c;
            padding: 2px 8px;
            border-radius: 3px;
            margin-left: 4px;
        }
    </style>
</head>
<body>
{{BODY}}
</body>
</html>
"""

def build_html(title, body):
    return HTML_TEMPLATE.replace("{{TITLE}}", title).replace("{{BODY}}", body)


def generate_pdf_from_html(html_content, output_pdf_path):
    temp_html = output_pdf_path.replace(".pdf", ".temp.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={output_pdf_path}",
        "--no-pdf-header-footer",
        temp_html
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print(f"Generated PDF successfully: {output_pdf_path}")


print("E-book Generator Engine loaded!")
